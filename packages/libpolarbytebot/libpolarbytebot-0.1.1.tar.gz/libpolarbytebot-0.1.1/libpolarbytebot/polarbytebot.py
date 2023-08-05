import re
import logging
import praw
from sqlalchemy import desc

try:
    from .models import bot_comments, bot_submissions, bot_comments_anetpool, anet_member, create_session
except ImportError:
    from libpolarbytebot.models import bot_comments, bot_submissions, bot_comments_anetpool, anet_member, create_session

__all__ = ['Polarbytebot']


class Polarbytebot:

    def __init__(self, signature, microservice_id, oauth_client_secret, oauth_username, oauth_client_id,
                 oauth_redirect_uri, praw_useragent, database_system, database_username, database_password,
                 database_host, database_dbname):
        self.microservice_id = microservice_id
        self.signature = signature

        self.reddit = praw.Reddit(client_id=oauth_client_id, client_secret=oauth_client_secret,
                                  redirect_uri=oauth_redirect_uri, user_agent=praw_useragent, username=oauth_username)

        self.session = create_session(database_system, database_username, database_password, database_host,
                                      database_dbname)

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
                    obj = self.reddit.submission(id=tbcm.pure_thing_id)
                    reply_obj = obj.add_comment(tbcm.content)
                except (praw.errors.InvalidSubmission):
                    tbcm.set_failed_submitted()
                    logging.warning('submitComment: failed (parentDeleted): {0}'.format(tbcm.id))
                else:
                    tbcm.set_successful_submitted(reply_obj.name)
                    logging.info('submitComment: submit: {0}'.format(tbcm.id))
            elif tbcm.is_response_to_comment:
                try:
                    obj = self.reddit.comment(id=tbcm.pure_thing_id)
                    reply_obj = obj.reply(tbcm.content)
                except (praw.errors.InvalidComment):
                    tbcm.set_failed_submitted()
                    logging.warning('submitComment: failed (parentDeleted): {0}'.format(tbcm.id))
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
                    sub_obj = self.reddit.submit(tbsm.subreddit, tbsm.title, url=tbsm.content)
                elif tbsm.is_selfpost:
                    sub_obj = self.reddit.submit(tbsm.subreddit, tbsm.title, text=tbsm.content)
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
                obj = self.reddit.get_info(thing_id=tbe.thread_id)
                try:
                    reply_obj = obj.add_comment(tbe.content)
                except (praw.errors.InvalidSubmission):
                    self.update_edited(bot_comments_anetpool, tbe.edit_id, 'del-1')
                    logging.warning('submitEdit: failed (parentDeleted): {0}'.format(tbe.edit_id))
                else:
                    self.update_edited(bot_comments_anetpool, tbe.edit_id, reply_obj.name)
                    logging.info('submitEdit: submit to none submitted id: {0}'.format(tbe.edit_id))
            elif tbe.submitted_id[:1] == 'e':
                new_id = self.search_edited(bot_comments_anetpool, tbe.submitted_id[1:])
                if new_id is not None and new_id[:1] != 'e':
                    obj = self.reddit.get_info(thing_id=new_id)
                    try:
                        reply_obj = obj.reply(tbe.content)
                    except (praw.errors.InvalidComment):
                        self.update_edited(bot_comments_anetpool, tbe.edit_id, 'del-1')
                        logging.warning('submitEdit: failed (parentDeleted): {0}'.format(tbe.edit_id))
                    else:
                        self.update_edited(bot_comments_anetpool, tbe.edit_id, reply_obj.name)
                        logging.info('submitEdit: submit based on e: {0}'.format(tbe.edit_id))
            else:
                obj = self.reddit.get_info(thing_id=tbe.submitted_id)
                try:
                    reply_obj = obj.edit(tbe.content)
                except (praw.errors.InvalidComment):
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

        css = self.reddit.subreddit('GuildWars2').stylesheet
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
