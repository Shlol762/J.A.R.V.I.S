from DiscordClasses import *
import discord
from discord import *
from discord.abc import *
from discord.ext import commands
from discord.ext.commands import *
from discord.ext.tasks import *
from pytz import timezone
from random import choice, randint
from asyncio import sleep, TimeoutError

with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/captains.json", "r") as f:
    caplist: dict = json.load(f)