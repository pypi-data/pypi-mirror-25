class GuildWars2Format:
    def __init__(self, author='', timestamp='', url='', text='', type='', is_offical=False):
        self.author = author
        self.timestamp = timestamp
        self.url = url
        self.text = text
        self._is_offical = is_offical
        self._type = type

        self._request = None

    @property
    def is_forum(self):
        return self._type == 'forum'

    @property
    def is_blog(self):
        return self._type == 'blog'

    @property
    def arenanet_tag(self):
        if self._is_offical:
            return '[ARENA NET] '
        return ''

    @property
    def result(self):
        if self.is_blog:
            return f'[BLOG] [{self.author} posted on {self.timestamp}]({self.url}):\n {self.text} '
        elif self.is_forum:
            return f'{self.arenanet_tag}[{self.author} posted on {self.timestamp}]({self.url}):\n {self.text}'\
                .replace('\n', '\n>')
        return ''
