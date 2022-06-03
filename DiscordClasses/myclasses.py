from disnake.ext import commands
import disnake, re
from .errors import BadArgument
from .version import Version
from typing import Union, Optional


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

        super().__init__(*args, **kwargs, intents=disnake.Intents.all(),
                         activity=disnake.Activity(type=disnake.ActivityType.watching,
                                                   name=f'people talk...    V{self.VERSION}'),
                         status=disnake.Status.dnd
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
