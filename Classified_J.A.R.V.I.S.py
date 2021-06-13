import asyncio
import json
import os
import discord
from discord.ext import commands
from DiscordClasses import bot_token, WorldoMeter, CustomHelpCommand, get_prefix
import datetime
from typing import Union, Mapping

intents = discord.Intents.all()
client = commands.Bot(command_prefix=get_prefix, case_insensitive=True, intents=intents,
                      allowed_mentions=discord.AllowedMentions(everyone=False), help_command=CustomHelpCommand(),
                      strip_after_prefix=True)
# client.remove_command('help')


for cog in os.listdir("C:/Users/Shlok/J.A.R.V.I.SV2021/MyCogs"):
    if cog.endswith(".py") and cog != '__init__.py':
        client.load_extension(f'MyCogs.{cog[:-3]}')


@client.command(hidden=True)
async def del_message(ctx: commands.Context, channel_id: int, message_id: int):
    channel: discord.TextChannel = await client.fetch_channel(channel_id)
    message: discord.Message = await channel.fetch_message(message_id)
    await message.delete()


@client.command(hidden=True)
async def test(ctx: commands.Context):
    await ctx.send(embed=discord.Embed(description="[Hover for info](https://www.youtube.com/watch?v=dQw4w9WgXcQ/ \"hello there\")"))


@client.command(hidden=True)
async def update(ctx: commands.Context):
    channels: list[discord.abc.GuildChannel] = client.get_all_channels()
    url = 'https://pypi.org/'
    link = 'https://discord.gg/zt6j4h7ep3'
    embed = discord.Embed(title='`Update!` - New command: `Set Prefix`',
    description=
f"""
**Set Prefix**

Sets a custom prefix for the server.

`  Name :      SetPrefix     `
`Aliases:    setprefix, spf  `

You can set prefixes by doing:
`$spf|setprefix <prefix>`

If you want to join my home server, click [`J.A.R.V.I.S`]({link})
""", colour=discord.Colour.random())
    for channel in channels:
        if 'general' in channel.name and isinstance(channel, discord.TextChannel):
            message: discord.Message = await channel.send(embed=embed)
            await ctx.send(f'Message: `{message.id}`\nServer: `{channel.guild.name}`\nChannel: `{channel.id}`')


@client.command(hidden=True)
async def test1(ctx: commands.Context):
    prefixes: dict = {}
    for guild in ctx.bot.guilds:
        guild: discord.Guild = guild
        prefixes[str(guild.id)] = '$'
        await ctx.send(f"Def `prefix` set for `{guild.name}`")
    with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=3)


client.run(bot_token)
