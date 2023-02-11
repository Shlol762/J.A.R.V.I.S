from DiscordClasses import *
import discord
import logging
from discord import *
from discord.abc import *
from discord.ext import commands
from discord.ext.commands import *
from discord.ext.tasks import *
from pytz import timezone as tz
from random import choice, randint
from asyncio import sleep, TimeoutError


_log = logging.getLogger(__name__)

# discord.utils.setup_logging(level=logging.INFO, handler=logging.StreamHandler(
# ), formatter=discord.utils._ColourFormatter(), root=True)


IST = tz('Asia/Kolkata')
