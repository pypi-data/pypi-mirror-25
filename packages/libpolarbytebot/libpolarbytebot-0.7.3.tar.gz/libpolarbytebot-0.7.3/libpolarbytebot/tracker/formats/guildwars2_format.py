class GuildWars2TrackerFormat:
    def __init__(self, author='', permalink_slug='', content='', thread_title='', context=1000, website='https://reddit.com'):
        self.author = author
        self.permalink_slug = permalink_slug
        self.content = content
        self.thread_title = thread_title
        self.website = website

        self._context = 1000

    @property
    def title(self):
        if len(self.thread_title) + len(self.author) + len(' []') > 300:
            return '{0}... [{1}]'.format(self.thread_title[:300 - len(self.author) - len('... []')], self.author)
        else:
            return '{0} [{1}]'.format(self.thread_title, self.author)

    @property
    def selfpost(self):
        return '{cnt}\n\n---\n{permalink}'.format(cnt=self.content.replace("\n", "\n>"), permalink=self.contextlink)

    @property
    def contextlink(self):
        return f'{self.permalink}?context={self._context}'

    @property
    def permalink(self):
        return f'{self.website}{self.permalink_slug}'