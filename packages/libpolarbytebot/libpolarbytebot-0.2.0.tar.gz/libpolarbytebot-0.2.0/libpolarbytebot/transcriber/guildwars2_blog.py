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

__all__ = ['blog_parse', 'findall_blog_urls']


def findall_blog_urls(content):
    blog_findings = []
    temporary_blog_findings = re.findall('http.*?://[w\.]{4}?guildwars2\.com/[^ \])\s]*', content)
    # filter out false positives
    for finding in temporary_blog_findings:
        if re.match('http.*?://.{0,4}guildwars2\.com/.*?/the-game/', finding) is None:
            blog_findings.append(finding)

    blog_findings = set(blog_findings)
    return blog_findings


def blog_parse(url):
    post = guildwars2_format.GuildWars2Format(type='blog')
    article = content_selection(requests_get(url).text, '<div class="article">', '<div', '</div>')
    attribution = content_selection(article, '<p class="blog-attribution">', '<p', '</p>')
    post.author = blog_name(attribution)
    post.timestamp = blog_datetime(attribution)
    post.url = url
    post.text = html_to_markdown(content_selection(article, '<div class="text">', '<div', '</div>'),
                                 parse_host_from_url(url))
    return post.result


def requests_get(url):
    counter = 0
    while (True):
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


def content_selection(content, start_str, nst, net):
    content_start = content.find(start_str)
    if content_start != -1:
        content = content[content_start + len(start_str):]
        level = 1
        pointer = 0
        ned = 0
        while True:
            ned_old = ned
            nsd = content.find(nst, pointer)
            ned = content.find(net, pointer)
            if level == 0:
                break
            elif nsd > ned and ned != -1:
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


def blog_name(content):
    c_split = content.split()
    name = ''
    for i in range(1, len(c_split) - 4):
        name += c_split[i] + ' '
    return name.strip()


def blog_datetime(content):
    c_split = content.split()
    datetime = ''
    for i in range(len(c_split) - 3, len(c_split)):
        datetime += c_split[i] + ' '
    return datetime.strip()


def parse_host_from_url(url):
    return re.search('\/\/.*?guildwars2.com', url).group(0)[2:]


def html_to_markdown(content, host):
    # with open('debug/out', 'w') as f:
    #    f.write(content)
    parser = guildwars2_html2markdown.Htmlparser()
    parser.convert_charrefs = True
    parser.host = 'https://' + host
    content = content.replace('\n', '\n>')
    parser.feed(content)
    return parser.result


if __name__ == '__main__':
    print(findall_blog_urls('https://www.guildwars2.com/en/news/countdown-to-launch/ fwecwe'))

    t1 = 'rthtr [test1](https://en-forum.guildwars2.com/discussion/342/forum-moderation-and-infraction-system) fwefwef\n\n' \
         'erjfhero https://wiki.guildwars2.com/wiki/Feedback_(trait_skill) fwefwefwe\n\n' \
         'fwefwefwe https://en-forum.guildwars2.com/discussion/342/forum-moderation-and-infraction-system wefwefw\n\n' \
         'gregerg https://www.guildwars2.com/en/news/countdown-to-launch/ wefewfwefef\n\n' \
         '[test2](https://www.guildwars2.com/en/news/countdown-to-launch/) wefwefwef\n\n'
    print(findall_blog_urls(t1))
