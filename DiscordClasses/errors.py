from discord.errors import *
from discord.ext.commands.errors import *

class ThreadNotSpecified(BadArgument):
    pass


class MissingArgument(Exception):
    pass
