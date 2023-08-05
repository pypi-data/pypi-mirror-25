import re
import logging
import praw
import datetime
from sqlalchemy import desc

import praw.exceptions
import prawcore.exceptions

try:
    from .models import bot_comments, bot_submissions, bot_comments_anetpool, anet_member, bot_errors, create_session
except ImportError:
    from libpolarbytebot.models import bot_comments, bot_submissions, bot_comments_anetpool, anet_member, bot_errors, \
        create_session

__all__ = ['Polarbytebot']


class Polarbytebot:
    def __init__(self, signature, microservice_id, oauth_client_secret, oauth_username, oauth_client_id,
                 oauth_redirect_uri, oauth_refresh_token, praw_useragent, database_system, database_username,
                 database_password, database_host, database_dbname):
        self.microservice_id = microservice_id
        self.signature = signature

        if oauth_refresh_token is not None:
            self.reddit = praw.Reddit(client_id=oauth_client_id, client_secret=oauth_client_secret,
                                      refresh_token=oauth_refresh_token, redirect_uri=oauth_redirect_uri,
                                      user_agent=praw_useragent, username=oauth_username)
        else:
            self.reddit = praw.Reddit(client_id=oauth_client_id, client_secret=oauth_client_secret,
                                      redirect_uri=oauth_redirect_uri, user_agent=praw_useragent,
                                      username=oauth_username)

        self.session = create_session(database_system, database_username, database_password, database_host,
                                      database_dbname)

        self.mention_regex = '\+/u/{botname} {1,3}'.replace('{botname}', oauth_username)
        self.username = oauth_username

    def create_comment(self, _thing_id, _content, _submitted=False):
        """
        Create a comment in response to another comment or submission. If the content surpasses the maximum amount of
        characters per comment, it'll be split into multiple comments, which are submitted in response of each other.
        :param _thing_id: id of the comment or submission which should be replied to
        :param _content: pure content of the reply (no signature, etc)
        :param _submitted: if the comment is already submitted
        """
        last_id = _thing_id
        for part in self.split_text(_content, 10000, self.signature):
            row = bot_comments()
            row.thing_id = last_id
            row.source_thing_id = _thing_id
            row.source_microservice_id = self.microservice_id
            row.submitted = _submitted
            row.content = part
            if not self.db_check_duplicate(row):
                self.session.add(row)
            self.session.commit()
            try:
                last_id = 'i{}'.format(
                    self.session.query(bot_comments).filter_by(source_thing_id=_thing_id,
                                                               source_microservice_id=self.microservice_id)
                        .order_by(desc(bot_comments.id)).first().id
                )
            except AttributeError:
                # the handled part is the first part of the series and therefor there is no related comment.
                pass

    def create_submission(self, _subreddit, _title, _content, _type, _submitted=False):
        row = bot_submissions()
        row.source_microservice_id = self.microservice_id
        row.title = _title
        row.type = _type
        row.subreddit = _subreddit
        row.content = _content
        row.submitted = _submitted
        if not self.db_check_duplicate(row):
            self.session.add(row)
        self.session.commit()

    def guildwars2_create_edit(self, _thread_id, _content, anetpool_template, _submitted=False,
                               max_comment_length=10000, split_seq='&#009;'):

        existingList = self.session.query(bot_comments_anetpool).filter_by(thread_id=_thread_id).order_by(
            desc(bot_comments_anetpool.edit_id)).first()

        if existingList is None:
            row = bot_comments_anetpool()
            row.thread_id = _thread_id
            _from_template = anetpool_template.split(split_seq, 1)
            row.content = _from_template[0] + _content + split_seq + _from_template[1]
            row.submitted = _submitted
            row.source_microservice_id = self.microservice_id
            if not self.db_check_duplicate(row):
                self.session.add(row)
        else:
            if _content in existingList.content:
                return
            if len(existingList.content) + len(_content) >= max_comment_length:
                row = bot_comments_anetpool()
                row.thread_id = _thread_id
                _from_template = anetpool_template.split(split_seq, 1)
                row.content = _from_template[0] + _content + split_seq + _from_template[1]
                row.submitted_id = 'e' + str(existingList.edit_id)
                row.submitted = _submitted
                row.source_microservice_id = self.microservice_id
                self.session.add(row)
            else:
                _from_save = existingList.content.split(split_seq, 1)
                self.session.query(bot_comments_anetpool).filter_by(edit_id=existingList.edit_id).update(
                    {'content': _from_save[0] + _content + split_seq + _from_save[1], 'submitted': False})
        self.session.commit()

    def guildwars2_list_developer(self):
        anet_query = list(self.session.query(anet_member))
        anet_members = []
        for member in anet_query:
            anet_members.append(member.username)
        return anet_members

    def db_check_duplicate(self, obj):
        for cmpobj in self.session.query(obj.__class__):
            if cmpobj == obj:
                return True
        return False

    def submit_comments(self):
        to_be_commented = self.session.query(bot_comments).filter_by(submitted=False).all()
        for tbcm in to_be_commented:
            if tbcm.is_response_to_submission:
                try:
                    reply_obj = self.reddit.submission(id=tbcm.pure_thing_id).reply(tbcm.content)
                except (praw.exceptions.PRAWException, prawcore.exceptions.PrawcoreException):
                    tbcm.set_failed_submitted()
                    logging.warning('submitComment: failed (maybe parentDeleted?): {0}'.format(tbcm.id))
                else:
                    tbcm.set_successful_submitted(reply_obj.name)
                    logging.info('submitComment: submit: {0}'.format(tbcm.id))
            elif tbcm.is_response_to_comment:
                try:
                    reply_obj = self.reddit.comment(id=tbcm.pure_thing_id).reply(tbcm.content)
                except (praw.exceptions.PRAWException, prawcore.exceptions.PrawcoreException):
                    tbcm.set_failed_submitted()
                    logging.warning('submitComment: failed (maybe parentDeleted?): {0}'.format(tbcm.id))
                else:
                    tbcm.set_successful_submitted(reply_obj.name)
                    logging.info('submitComment: submit: {0}'.format(tbcm.id))
            elif tbcm.is_chained_response:
                new_obj = self.search_submitted(bot_comments, tbcm.pure_chained_id)
                if new_obj.is_failed_chain:
                    tbcm.set_failed_submitted()
                if new_obj.submitted_id is not None:
                    self.update_thing_id(bot_comments, tbcm.id, new_obj.submitted_id)
            self.session.commit()

    def submit_submissions(self):
        to_be_submitted = self.session.query(bot_submissions).filter_by(submitted=False).all()
        for tbsm in to_be_submitted:
            try:
                if tbsm.is_link:
                    sub_obj = self.reddit.subreddit(tbsm.subreddit).submit(tbsm.title, url=tbsm.content)
                elif tbsm.is_selfpost:
                    sub_obj = self.reddit.subreddit(tbsm.subreddit).submit(tbsm.title, selftext=tbsm.content)
                tbsm.set_successful_submitted()
                logging.info('SubmitSubmission: submit: {0}'.format(tbsm.id))
                self.session.commit()
            except Exception as e:
                if tbsm.is_link:
                    logging.error('SubmitSubmissions: {0} on-id {1} on-url {2}'.format(e, tbsm.id, tbsm.content))
                else:
                    logging.error('SubmitSubmissions: {0} on-id {1}'.format(e, tbsm.id))
                tbsm.set_failed_submitted()
                logging.info('SubmitSubmission: failed-submit: {0}'.format(tbsm.id))
                self.session.commit()

    def submit_anetpool_edits(self):
        to_be_edited = self.session.query(bot_comments_anetpool).filter_by(submitted=False).all()
        for tbe in to_be_edited:
            if tbe.submitted_id is None:
                try:
                    reply_obj = self.reddit.submission(id=tbe.thread_id[3:]).reply(tbe.content)
                except (praw.exceptions.PRAWException, prawcore.exceptions.PrawcoreException):
                    self.update_edited(bot_comments_anetpool, tbe.edit_id, 'del-1')
                    logging.warning('submitEdit: failed (parentDeleted): {0}'.format(tbe.edit_id))
                else:
                    self.update_edited(bot_comments_anetpool, tbe.edit_id, reply_obj.name)
                    logging.info('submitEdit: submit to none submitted id: {0}'.format(tbe.edit_id))
            elif tbe.submitted_id[:1] == 'e':
                new_id = self.search_edited(bot_comments_anetpool, tbe.submitted_id[1:])
                if new_id is not None and new_id[:1] != 'e':
                    try:
                        reply_obj = self.reddit.comment(id=new_id[3:]).reply(tbe.content)
                    except (praw.exceptions.PRAWException, prawcore.exceptions.PrawcoreException):
                        self.update_edited(bot_comments_anetpool, tbe.edit_id, 'del-1')
                        logging.warning('submitEdit: failed (parentDeleted): {0}'.format(tbe.edit_id))
                    else:
                        self.update_edited(bot_comments_anetpool, tbe.edit_id, reply_obj.name)
                        logging.info('submitEdit: submit based on e: {0}'.format(tbe.edit_id))
            else:
                try:
                    self.reddit.comment(id=tbe.submitted_id[3:]).reply(tbe.content)
                except (praw.exceptions.PRAWException, prawcore.exceptions.PrawcoreException):
                    self.update_edited(bot_comments_anetpool, tbe.edit_id, 'del-1')
                    logging.warning('submitEdit: failed (commentDeleted): {0}'.format(tbe.edit_id))
                else:
                    self.update_edited(bot_comments_anetpool, tbe.edit_id)
                    logging.info('submitEdit: submit to existing: {0}'.format(tbe.edit_id))
            self.session.commit()

    def update_submitted(self, _table, _search_id, _submit_id=None):
        if _submit_id is not None:
            self.session.query(_table).filter_by(id=_search_id).update({'submitted': True, 'submitted_id': _submit_id})
        else:
            self.session.query(_table).filter_by(id=_search_id).update({'submitted': True})

    def update_edited(self, _table, _search_id, _submit_id=None):
        if _submit_id is not None:
            self.session.query(_table).filter_by(edit_id=_search_id).update(
                {'submitted': True, 'submitted_id': _submit_id})
        else:
            self.session.query(_table).filter_by(edit_id=_search_id).update({'submitted': True})

    def search_submitted(self, _table, _search_id):
        return self.session.query(_table).filter_by(id=_search_id).first()

    def update_thing_id(self, _table, _search_id, _new_id):
        self.session.query(_table).filter_by(id=_search_id).update({'thing_id': _new_id})

    def search_edited(self, _table, _search_id):
        return self.session.query(_table).filter_by(edit_id=_search_id).first().submitted_id

    def guildwars2_update_developer_names(self):
        FLAIR_IMAGE_URL = '%%arenanet-half'  # 'pYI5WAF5Gh8P-FLejPwHGztyIXKCmrGqtYRwv__sDiM.png'  # '%%arenanet-half6%%'

        css = self.reddit.subreddit('GuildWars2').stylesheet().stylesheet
        int_flairimg = css.find(FLAIR_IMAGE_URL)
        int_start_anet_section = css.rfind('ArenaNetTeam', 0, int_flairimg)

        t_str_names = re.findall('.author\[href\$="\/[^"]*"\]:before',
                                 css[int_start_anet_section - len('.author[href$="/ArenaNetTeam'):int_flairimg])
        self.session.query(anet_member).delete()

        for line in t_str_names:
            if line != '':
                row = anet_member()
                row.username = line.replace('"]:before', '') \
                    .replace('.author[href$="/', '')
                self.session.add(row)

        self.session.commit()

    def add_error(self, exception_text, url=''):
        row = bot_errors()
        row.url = url
        row.exception = exception_text
        row.timestamp = datetime.datetime.now()
        row.source_microservice_id = self.microservice_id
        self.session.add(row)

    @staticmethod
    def fix_permalink(slug):
        return f'https://reddit.com{slug}'

    @staticmethod
    def split_text(text, part_length, signature, continue_text='\n\n--- continued below ---', split_char='\n'):
        """
        Split a text into several parts. Attach signature to every message and an info regarding the split to every
        message except the last.
        :param text: text which should be splitted
        :param part_length: maximum amount of characters per part
        :param signature: signature which should be present on every part
        :param continue_text: info regarding the split, present on every part except the last
        :param split_char: character on which the split should be determined on
        :return: list of parts
        """
        extra_length = len(signature) + len(continue_text)
        parts = []
        while True:
            if len(text) <= 0:
                return parts
            content_parts = text.split(split_char)
            stitched_content = ''
            for part in content_parts:
                if len(stitched_content) + len(part + split_char) + extra_length <= part_length:
                    stitched_content += part + split_char
                else:
                    break
            if text[len(stitched_content):] == '':
                parts.append(stitched_content + signature)
            else:
                parts.append(stitched_content + continue_text + signature)
            text = text[len(stitched_content):]
