import discord
from datetime import datetime as dt
import logging
from discord.ext.commands import Cog, Context
from discord.ext.tasks import Loop, loop
from typing import List

from core import Jarvis, funclog


log = logging.getLogger(__name__)


class Tasks(Cog):

    def __init__(self, bot: Jarvis):
        self.bot = bot
        self.name = 'tasks'
        self.tasks: List[Loop] = [self.sync_databases]

    @Cog.listener()
    async def on_ready(self):

        # Starting tasks.
        if len(self.tasks) > 0:
            log.info("Starting tasks...")
        
        for task in self.tasks:
            try:
                task.start()
                log.debug(f"Started task: {task._name}.")
            except RuntimeError:
                log.warning(f"Failed to start task: {task._name}.")
                try:
                    task.restart()
                    log.debug(f"Re-Started task: {task._name}.")

                except RuntimeError:
                    log.exception(f"Failed to restart task: {task._name}.")

    @loop(minutes=5)
    async def sync_databases(self):

        await self.bot.guildsettings.executemany(
            """
            INSERT INTO guild_settings (guild_id, prefix)
            VALUES (?, ?)
            ON CONFLICT(guild_id) DO UPDATE SET prefix=excluded.prefix
            """,
            [(int(gid), prefix) for gid, prefix in self.bot.prefixes.items()]
        )

   


@funclog
async def setup(bot: Jarvis):
    await bot.add_cog(Tasks(bot))
