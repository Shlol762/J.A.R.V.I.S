from discord.errors import *
from discord.ext.commands import *

class ThreadNotSpecified(BadArgument):
    pass


class MissingArgument(Exception):
    pass
