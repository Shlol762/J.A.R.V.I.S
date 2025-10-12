import discord
import logging
from datetime import datetime as dt
from discord.ext import commands

from core.utils import get_prefix, prefixExists
from core.database import *
from core.decorators import funclog


log = logging.getLogger(__name__)

class Jarvis(commands.Bot):

    def __init__(self,  modes, *args, **kwargs):

        self.initialised_at = dt.now()
        
        self.modes = modes
        super().__init__(*args, **kwargs, intents=discord.Intents.all(),
                         activity=discord.Activity(type=discord.ActivityType.watching,
                                                   name=f'people talk...    V2.0.0'),
                         status=discord.Status.dnd, command_prefix=get_prefix, case_insensitive=True,
                         allowed_mentions=discord.AllowedMentions(),
                         strip_after_prefix=True
                         )
        

    async def close(self):
        """
        Gracefully close the bot while syncing/cleaning resources.
        """
        log.info("Shutting down...")
        log.debug(self.prefixes)
        if hasattr(self, "guildsettings") and hasattr(self, "prefixes"):
            await self.guildsettings.executemany(
                """
                INSERT INTO guild_settings (guild_id, prefix)
                VALUES (?, ?)
                ON CONFLICT(guild_id) DO UPDATE SET prefix=excluded.prefix
                """,
                [(int(gid), prefix) for gid, prefix in self.prefixes.items()]
            )
            log.info("Prefixes synced.")

            

        # You can add other cleanup tasks here:
        # e.g., closing aiohttp sessions, flushing caches, etc.
        await super().close()
        log.info("Shut down clean up complete. Have a good day sir!")

        

    async def setup_hook(self):
        log.debug("Loading cogs...")
        initial_cogs = ["cogs.tasks","cogs.events"] # "cogs.moderation", "cogs.music"]

        if self.modes.safe_mode:
            initial_cogs = ["cogs.events", "cogs.tasks"]

        if self.modes.cogs:
            initial_cogs = self.modes.cogs

        for cog in initial_cogs:
            try:
                log.debug(f"Loading cog: {cog}...")
                await self.load_extension(cog)
                log.debug(f"Loaded cog: {cog}")
            except commands.NoEntryPointError:
                log.exception(f"Extension 'cogs.{cog}' does not contain a setup function")
            except commands.ExtensionNotFound:
                log.exception(f"Extension Not Found: '{cog}' not found")
            except commands.ExtensionFailed as _exc:
                log.exception(_exc.args[0])


        log.debug("Loading Databases...")
        self.guildsettings = Database('databases/GuildSettings.db')

        self.prefixes = {row['guild_id']:row['prefix'] for row in await self.guildsettings.fetchall("SELECT guild_id, prefix FROM guild_settings")}
        log.debug(self.prefixes)


    async def on_message(self, message: discord.Message, /):
        if message.guild and not prefixExists(self, message):
            self.prefixes[str(message.guild.id)] = '$'

        log.debug(self.prefixes)

        return await super().on_message(message)
