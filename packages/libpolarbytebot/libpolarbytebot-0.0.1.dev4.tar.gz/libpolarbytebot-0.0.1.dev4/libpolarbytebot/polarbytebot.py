import configparser
from sqlalchemy import desc

try:
    from .models import bot_comments, bot_submissions, create_session
except ImportError:
    from libpolarbytebot.models import bot_comments, bot_submissions, create_session

__all__ = ['Polarbytebot']


class Polarbytebot:
    def __init__(self, cfg_path, signature, microservice_id):
        self.microservice_id = microservice_id
        self.signature = signature

        self.cfg = configparser.ConfigParser()
        self.cfg.read(cfg_path)

        self.session = create_session(self.cfg.get('database', 'system'), self.cfg.get('database', 'username'),
                                      self.cfg.get('database', 'password'), self.cfg.get('database', 'host'),
                                      self.cfg.get('database', 'database'))

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
