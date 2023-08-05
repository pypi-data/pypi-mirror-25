import re
import requests

# Imports
try:
    from .markdown import overwatch_html2markdown
    from .markdown import markdown_dictionary as m
    from .formats import overwatch_format
except ImportError:
    import libpolarbytebot.transcriber.markdown.overwatch_html2markdown as overwatch_html2markdown
    import libpolarbytebot.transcriber.markdown.markdown_dictionary as m
    import libpolarbytebot.transcriber.formats.overwatch_format as overwatch_format

__all__ = ['overwatch_findall_forum_urls', 'overwatch_findall_forum_urls_mentions', 'overwatch_forum_parse']

__forum_url_regex = 'https?://.{2,3}?\.battle\.net/forums/[^ \]<")\s]*'


def overwatch_findall_forum_urls(content):
    forum_findings = re.findall(__forum_url_regex, content)
    forum_findings = set(forum_findings)
    return forum_findings


def overwatch_findall_forum_urls_mentions(content, mention_regex):
    forum_mention_findings = []
    temp_forum_mention_findings = re.findall(mention_regex + __forum_url_regex, content)

    for temp_mention in temp_forum_mention_findings:
        forum_mention_findings.extend(overwatch_findall_forum_urls(temp_mention))

    forum_mention_findings = set(forum_mention_findings)
    return forum_mention_findings


def overwatch_forum_parse(url, parse_refs=True):
    post = overwatch_format.OverwatchFormat(url=url)
    message = content_selection(requests_get(url).text, ' id="' + forum_id(url), '<div', '</div>')
    post.timestamp = forum_datetime(message)
    post.author, post._is_offical = forum_name(message)
    content = content_selection(message, '<div class="TopicPost-bodyContent" data-topic-post-body-content="true"',
                                '<div', '</div>')[1:] + '</div>'
    post.text = html_to_markdown(content, parse_host_from_url(url))

    # Search referenced posts
    all_links = overwatch_findall_forum_urls(content)
    if parse_refs and all_links != []:
        all_links = set(all_links)
        for link in all_links:
            post.referenced_posts.append(overwatch_forum_parse(link, parse_refs=False))

    return post.result


def forum_id(url):
    urlInformation = re.search(
        'https?://(?P<region>.{2,3}?)\.battle.net(?P<forum>\/forums)(?P<language>\/[^\/]*)(?P<subforum>\/[^\/]*)(?P<title>\/[^\/#]*)((?P<identifier1>\/[^\/#\s?]*)|)((?P<identifier2>(#?|\/)[^\/#\s]*)|)((?P<identifier3>([#/])[^\/#\s]*)|)',
        url)
    identifier1 = urlInformation.group('identifier1')
    identifier2 = urlInformation.group('identifier2')
    identifier3 = urlInformation.group('identifier3')
    # http://us.battle.net/forums/en/overwatch/topic/123456789
    # http://us.battle.net/forums/en/overwatch/topic/123456789/
    if identifier1[1:].isdigit and (identifier2 == '/' or identifier2 is None) and identifier3 is None:
        return 'post-1'
    # http://us.battle.net/forums/en/overwatch/topic/20745604460#post-4
    elif identifier1[1:].isdigit and identifier2[:6] == '#post-' and identifier3 is None:
        return identifier2[1:]
    # http://us.battle.net/forums/en/overwatch/topic/20745604460?page=3
    elif identifier1[1:].isdigit and identifier2[:6] == '?page=' and identifier3 is None:
        return 'post-' + str((int(identifier2[6:]) - 1) * 20 + 1)
    # http://us.battle.net/forums/en/overwatch/topic/20745604460?page=3#post-41
    elif identifier1[1:].isdigit and identifier2[:6] == '?page=' and identifier3[:6] == '#post-':
        return identifier3[1:]

    else:
        return forum_getFirstId(url)


def forum_getFirstId(url):
    req = requests_get(url)
    id = re.search(' id="post-[0123456789]*"', req.text)
    if id is not None:
        id = id.group(0)
        id = id[5:-1]
    else:
        id = '0'
    return id


def requests_get(url):
    counter = 0
    while True:
        try:
            req = requests.get(url)
        except:
            pass
        else:
            return req

        finally:
            counter += 1
            if counter > 100:
                return


def content_selection(content, start_str, nst, net):
    content_start = content.find(start_str)
    if content_start != -1:
        content = content[content_start + len(start_str):]
        level = 1
        pointer = 0
        ned = 0
        while (True):
            ned_old = ned
            nsd = content.find(nst, pointer)
            ned = content.find(net, pointer)
            if level == 0:
                break
            elif nsd > ned != -1:
                pointer = ned + 1
                level -= 1
            elif nsd < ned and nsd != -1:
                pointer = nsd + 1
                level += 1
            elif nsd < ned and nsd == -1:
                pointer = ned + 1
                level -= 1
        return content[:ned_old]
    else:
        return ''


def forum_name(content):
    posted_by_class = re.search('<aside class="TopicPost-author">.*?</aside>', content, re.DOTALL).group(0)
    posted_by_name = re.search('<span class="Author-name">(?P<name>.*?)</span>', posted_by_class, re.DOTALL).group(
        'name')
    # posted_by_name = posted_by_name.replace('-', ' ', posted_by_name.count('-') - 1).replace('-', '.')
    if 'Author-name--profileLink' in posted_by_name:
        posted_by_playoverwatch_name = re.search('<a class="Author-name--profileLink" href=".*?">(?P<pown>.*?)</a>',
                                                 posted_by_name, re.DOTALL).group('pown')
        posted_by_name = posted_by_playoverwatch_name
    return posted_by_name.strip(), forum_blizz(posted_by_class)


def forum_blizz(posted_by_class):
    posted_by_blizz = re.findall('class="Author[^"]*', posted_by_class)
    for found in posted_by_blizz:
        if "blizzard" in found:
            return True
    return False


def forum_datetime(content):
    # <a class="TopicPost-timestamp" .*? data-tooltip-content="06/23/2016 05:35 AM">.*?</a>
    posted_datetime_class = re.search('<a class="TopicPost-timestamp".*?data-tooltip-content=".*?">\s*.*?\s*</a>',
                                      content).group(0)
    return re.search('data-tooltip-content="[^"]*', posted_datetime_class).group(0)[len("data-tooltip-content=\""):]


def parse_host_from_url(url):
    return re.search('\/\/.*?battle.net', url).group(0)[2:]


def html_to_markdown(content, host):
    parser = overwatch_html2markdown.Htmlparser()
    parser.convert_charrefs = True
    parser.host = 'https://' + host
    content = content.replace('\n', '\n>')
    parser.feed(content)
    return parser.result


if __name__ == '__main__':
    overwatch_forum_parse('https://us.battle.net/forums/en/overwatch/topic/20759376545#post-1')
