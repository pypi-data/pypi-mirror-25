# Imports
try:
    from .formats import guildwars2_format
except ImportError:
    import libpolarbytebot.tracker.formats.guildwars2_format as guildwars2_format

__all__ = ['gen']


def gen(author, thread_title, permalink_slug, content):
    return guildwars2_format.GuildWars2TrackerFormat(author=author, permalink_slug=permalink_slug,
                                                     thread_title=thread_title, content=content)
