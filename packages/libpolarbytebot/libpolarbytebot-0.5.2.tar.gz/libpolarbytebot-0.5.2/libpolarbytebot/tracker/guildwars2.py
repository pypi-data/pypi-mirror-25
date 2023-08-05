# Imports
try:
    from .formats import guildwars2_format
except ImportError:
    import libpolarbytebot.tracker.formats.guildwars2_format as guildwars2_format

__all__ = ['gen']


def gen(author, thread_title, permalink, content):
    return guildwars2_format.GuildWars2TrackerFormat(author=author, permalink=permalink, thread_title=thread_title,
                                                     content=content)
