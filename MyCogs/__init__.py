from DiscordClasses import *
import nextcord
from nextcord import *
from nextcord.abc import *
from nextcord.ext import commands
from nextcord.ext.commands import *
from nextcord.ext.tasks import *
from pytz import timezone
from random import choice, randint
from asyncio import sleep, TimeoutError

with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/captains.json", "r") as f:
    caplist: dict = json.load(f)