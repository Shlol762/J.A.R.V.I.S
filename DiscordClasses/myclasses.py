from discord.ext import commands
import discord, re
from typing import Optional
from .version import Version
from .custom_funcs import get_prefix


class Jarvis(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        self._mainframe_members: dict[str, str] = {}
        self._settings: dict[str, dict[str, bool]] = {}

        with open("C:/Users/Shlok/bot_stuff/version.txt", 'r+') as f:
            ver = Version(f.read())
            match = re.search("(no?(ah)?|deny)", input("Version increment? "))
            self.VERSION = ver.version
            if not match:
                self.VERSION = ver.increment().version
                f.write(self.VERSION)

        super().__init__(*args, **kwargs, intents=discord.Intents.all(),
                         activity=discord.Activity(type=discord.ActivityType.watching,
                                                   name=f'people talk...    V{self.VERSION}'),
                         status=discord.Status.dnd, command_prefix=get_prefix, case_insensitive=True,
                         allowed_mentions=discord.AllowedMentions(),
                         strip_after_prefix=True
                         )

        self.remove_command('help')


    @property
    def MAINFRAME_MEMBERS(self):
        return self._mainframe_members

    @MAINFRAME_MEMBERS.setter
    def MAINFRAME_MEMBERS(self, value):
        self._mainframe_members = value

    @property
    def SETTINGS(self):
        return self._settings

    @SETTINGS.setter
    def SETTINGS(self, value):
        self._settings = value
