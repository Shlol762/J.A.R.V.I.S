from disnake.errors import *
from disnake.ext.commands import *

class ThreadNotSpecified(BadArgument):
    pass


class MissingArgument(Exception):
    pass


class ChannelArgMissing(BadArgument):
    pass
