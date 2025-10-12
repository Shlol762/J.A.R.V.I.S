import discord
from datetime import datetime as dt
import logging
from discord.ext.commands import Cog, Context
from discord.ext.tasks import Loop, loop
from typing import List

from core import Jarvis, funclog



log = logging.getLogger(__name__)


class Events(Cog):

    def __init__(self, bot: Jarvis):
        self.bot = bot
        self.name = 'events'

    @Cog.listener()
    async def on_ready(self):


        startup_delta = (dt.now() - self.bot.initialised_at).total_seconds()

        log.info("Connection to Discord successful.")
        log.info(f"Start up completed in {startup_delta:.3f} seconds.")

    @Cog.listener()
    async def on_message(self, message: discord.Message):
        
        guild = message.guild
        author = message.author
        channel = message.channel
        ctx = await self.bot.get_context(message)

        if not guild:
            return

    
        


@funclog
async def setup(bot: Jarvis):
    await bot.add_cog(Events(bot))
