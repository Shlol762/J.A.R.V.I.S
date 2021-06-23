import asyncio
import json
import os
import discord
from discord.ext import commands
from DiscordClasses import bot_token, WorldoMeter, get_prefix
import datetime
from typing import Union, Mapping

intents = discord.Intents.all()
client = commands.Bot(command_prefix=get_prefix, case_insensitive=True, intents=intents,
                      allowed_mentions=discord.AllowedMentions(everyone=False),
                      strip_after_prefix=True)
client.remove_command('help')


for cog in os.listdir("C:/Users/Shlok/J.A.R.V.I.SV2021/MyCogs"):
    if cog.endswith(".py") and cog != '__init__.py':
        client.load_extension(f'MyCogs.{cog[:-3]}')


@client.command(hidden=True)
async def del_message(ctx: commands.Context, message: discord.Message):
    await ctx.send(f"Deleted message with content: `{message.content}`")
    await message.delete()


@client.command(hidden=True)
async def test(ctx: commands.Context):
    message: discord.Message = await ctx.send("Hellooo")
    await ctx.send(f'`Message link`: https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}')


@client.command(hidden=True)
async def update(ctx: commands.Context):
    channels: list[discord.abc.GuildChannel] = client.get_all_channels()
    link = 'https://discord.gg/zt6j4h7ep3'
    embed = discord.Embed(title='`Update!` - New command: `Settings`',
    description=
f"""
**Settings**

View all the settings the bot has for the server.

`  Name : settings `
`Aliases:    sts   `

You can view all settings by doing:
`$settings`

If you want to join my home server, click [`J.A.R.V.I.S`]({link})
""", colour=discord.Colour.random())
    for channel in channels:
        if 'general' in channel.name and isinstance(channel, discord.TextChannel):
            message: discord.Message = await channel.send(embed=embed)
            await ctx.send(f'`Message link`: https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}')


@client.command(hidden=True)
async def test1(ctx: commands.Context):
    prefixes: dict = {}
    for guild in ctx.bot.guilds:
        guild: discord.Guild = guild
        prefixes[str(guild.id)] = '$'
        await ctx.send(f"Def `prefix` set for `{guild.name}`")
    with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=3)


@client.command(hidden=True)
async def load_help_data(ctx: commands.Context):
    bot: commands.Bot = ctx.bot
    cogs: Mapping[str, commands.Cog] = bot.cogs
    d_cogs = {}
    for _cog in cogs.values():
        d_cog = {}
        d_commands = []
        comms: list[commands.Command] = _cog.get_commands()
        if _cog.get_commands() is None: continue
        for comm in comms:
            command_details = {
                "name": comm.name,
                "aliases": comm.aliases,
                "number": comm.brief,
                "usage": comm.usage,
                "help": comm.help
            }
            d_commands.append(command_details) if not comm.hidden else None
        d_cogs[_cog.qualified_name] = d_cog[_cog.name] = d_commands
    with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/help.json", "w") as f:
        json.dump(d_cogs, f, indent=3)


@client.command(hidden=True)
async def devan(ctx: commands.Context, *, text: str):
    if text:
        embed = discord.Embed(title="Announcement from `central mainframe`", description=text, colour=discord.Colour.random())
        for channel in ctx.bot.get_all_channels():
            if 'general' in channel.name and isinstance(channel, discord.TextChannel):
                message: discord.Message = await channel.send(embed=embed)
                await ctx.send(
                    f'`Message link`: https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}')


client.run(bot_token)
