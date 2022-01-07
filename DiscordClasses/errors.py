from nextcord.errors import *
from nextcord.ext.commands import *

class ThreadNotSpecified(BadArgument):
    pass


class MissingArgument(Exception):
    pass


class ChannelArgMissing(BadArgument):
    pass
