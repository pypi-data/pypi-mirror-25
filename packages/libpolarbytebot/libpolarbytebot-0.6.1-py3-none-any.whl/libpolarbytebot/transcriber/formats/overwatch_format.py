class OverwatchFormat:
    def __init__(self, author='', timestamp='', url='', text='', is_offical=False):
        self.author = author
        self.timestamp = timestamp
        self.url = url
        self.text = text
        self.referenced_posts = []
        self._is_offical = is_offical

        self._request = None

    @property
    def blizzard_tag(self):
        if self._is_offical:
            return '[BLIZZARD] '
        return ''

    @property
    def has_referenced_posts(self):
        return len(self.referenced_posts) > 0

    @property
    def result(self):
        if self.has_referenced_posts:
            return f'{self.no_referenced_results}\n\n---\n\nReferenced Postings:\n\n{self.all_referenced_results}'
        else:
            return self.no_referenced_results

    @property
    def no_referenced_results(self):
        return f'{self.blizzard_tag}[{self.author} posted on {self.timestamp}]({self.url}):\n {self.text}'

    @property
    def all_referenced_results(self):
        collab = ''
        for ref in self.referenced_posts:
            collab += '\n\n' + ref
        return collab
