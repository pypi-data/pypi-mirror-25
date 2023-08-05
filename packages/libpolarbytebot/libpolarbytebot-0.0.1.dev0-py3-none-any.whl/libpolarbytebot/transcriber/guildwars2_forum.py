import requests
import re
import time

# Imports
try:
    from .markdown import guildwars2_html2markdown
    from .formats import guildwars2_format
except ImportError:
    import libpolarbytebot.transcriber.markdown.guildwars2_html2markdown as guildwars2_html2markdown
    import libpolarbytebot.transcriber.formats.guildwars2_format as guildwars2_format

__all__ = ['forum_parse', 'findall_forum_urls']


class ForumUrl:
    def __init__(self, url):
        self.url = str(url).strip()

    @property
    def is_comment(self):
        return re.match('http.*?://..-forum\.guildwars2\.com/discussion/comment/\d*(/#Comment_\d*|/|)',
                        self.url) is not None

    @property
    def is_thread(self):
        return re.match('http.*?://..-forum\.guildwars2\.com/discussion/\d*?/.*', self.url) is not None

    @property
    def comment_id(self):
        result = None
        try:
            result = re.match('http.*?://..-forum\.guildwars2\.com/discussion/comment/(?P<id>\d*)(/#Comment_\d*|/|)',
                              self.url).group('id')
        except AttributeError:
            pass
        return result

    @property
    def json_url(self):
        return self.url.rsplit('#', maxsplit=1)[0] + '.json'


def findall_forum_urls(content):
    forum_findings = re.findall('http.*?://..-forum\.guildwars2\.com/discussion/[^ \])\s]*', content)
    forum_findings = set(forum_findings)
    return forum_findings


def forum_parse(url):
    """
    Fetch and transform a forums post into a markdown formatted string, usable in the polarbytebot post text body. 
    No signatures included.
    :param url: the url of the discussion or comment to transcribe.
    :return: formatted text which can be used in the textbody.
    """
    furl = ForumUrl(url)
    json_response = requests.get(furl.json_url).json()
    post = guildwars2_format.GuildWars2Format(type='forum', url=furl.url)
    if furl.is_comment:
        ref_comment = list(filter(lambda item: str(item['CommentID']) == furl.comment_id, json_response['Comments']))[0]
        post.author = ref_comment['InsertName']
        post.timestamp = ref_comment['DateInserted']
        if 'ArenaNet' in ref_comment['Roles'].values():
            post._is_offical = True
        post.text = ref_comment['Body']

    elif furl.is_thread:
        ref_discussion = json_response['Discussion']
        post.author = ref_discussion['InsertName']
        post.timestamp = ref_discussion['DateInserted']
        if 'ArenaNet' in ref_discussion['Roles'].values():
            post._is_offical = True
        post.text = ref_discussion['Body']




def requests_get(url):
    counter = 0
    while True:
        try:
            req = requests.get(url)
            time.sleep(0.5)
        except:
            pass
        else:
            return req
        finally:
            counter += 1
            if counter > 100:
                return


if __name__ == '__main__':
    t1 = 'rthtr [https://en-forum.guildwars2.com/discussion/342/forum-moderation-and-infraction-system](https://en-forum.guildwars2.com/discussion/342/forum-moderation-and-infraction-system) fwefwef\n\n' \
         'erjfhero https://wiki.guildwars2.com/wiki/Feedback_(trait_skill) fwefwefwe\n\n' \
         'fwefwefwe https://en-forum.guildwars2.com/discussion/342/forum-moderation-and-infraction-system wefwefw\n\n' \
         'gregerg https://www.guildwars2.com/en/news/countdown-to-launch/ wefewfwefef\n\n' \
         '[test2](https://www.guildwars2.com/en/news/countdown-to-launch/) wefwefwef\n\n'
    print(findall_forum_urls(t1))
    forum_parse('https://en-forum.guildwars2.com/discussion/comment/125824/#Comment_125824')
    forum_parse('https://en-forum.guildwars2.com/discussion/1831/shattered-observatory-doom-bombs-more-than-just-random')

