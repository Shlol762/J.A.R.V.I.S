import asyncio
import json
import os
import random

import discord
from discord.ext import commands
from DiscordClasses import bot_token, WorldoMeter, get_prefix, time_set
import datetime
from typing import Union, Mapping

intents = discord.Intents.all()
client = commands.Bot(command_prefix=get_prefix, case_insensitive=True, intents=intents,
                      allowed_mentions=discord.AllowedMentions(everyone=False),
                      strip_after_prefix=True)
client.remove_command('help')


class Counter(discord.ui.View):
    @discord.ui.button(label='0', style=discord.ButtonStyle.red)
    async def counter(self, button: discord.ui.Button, interaction: discord.Interaction):
        number = int(button.label)
        button.label = str(number + 1)
        if number + 1 >= 5:
            button.style = discord.ButtonStyle.green

        await interaction.message.edit(view=self)

    @discord.ui.button(label="Henlo there!", style=discord.ButtonStyle.danger)
    async def hey(self, button: discord.ui.Button, interaction: discord.Interaction):
        button.label = random.choice([
            'Greetings my fran!',
            'Sup?', "AYOOO", "How you doin'?",
            'Hi'])
        button.style = random.choice([discord.ButtonStyle.green, discord.ButtonStyle.danger])
        await interaction.message.edit(view=self)

    async def on_timeout(self):
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True


for cog in os.listdir("C:/Users/Shlok/J.A.R.V.I.SV2021/MyCogs"):
    if cog.endswith(".py") and cog != '__init__.py':
        client.load_extension(f'MyCogs.{cog[:-3]}')


@client.command(hidden=True)
async def del_message(ctx: commands.Context, message: discord.Message):
    await ctx.reply(f"Deleted message with content: `{message.content}`")
    await message.delete()

sec_lvl = """
`1|The bots integrated interface Role on this Server    ` - <@&819518757617664021>
`2|Access to Admin. Use wisely. More than 9 months req. ` - <@&839069357581139998>
`3|Access to bot code snips. More than 6 months req.    ` - <@&839427298075476019>
`4|Access to VCs. More than 3 months required.          ` - <@&839427084219842561>
`5|Access to Core Logs. More than 14 days required.     ` - <@&839069487113699358>
`6|Access to Cross connect. More than 10 mins required. ` - <@&839068777521479691>
`7|Anyone who volunteers for Tests.                     ` - <@&839079368910438421>
"""

@client.command(hidden=True)
async def test(ctx: commands.Context):
    for comm in client.commands:
        if comm.extras:
            await ctx.send(comm.extras['emoji'])


@client.command(hidden=True)
async def refseclvl(ctx: commands.Context):
    with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/mainframe_members.json", "r") as f:
        mem_list: dict = json.load(f)
    now = datetime.datetime.now().date()
    lvl0: discord.Role = ctx.guild.get_role(839068777521479691)
    lvl1: discord.Role = ctx.guild.get_role(839069487113699358)
    lvl2: discord.Role = ctx.guild.get_role(839427084219842561)
    lvl3: discord.Role = ctx.guild.get_role(839427298075476019)
    admin: discord.Role = ctx.guild.get_role(839069357581139998)
    for member, join_time in mem_list.items():
        diff = (now - datetime.datetime.strptime(join_time, "%d %b %Y at %I:%M %p").date())
        try:
            member: discord.Member = await ctx.guild.fetch_member(int(member))
            if diff.seconds > 600:
                await member.add_roles(lvl0)
            elif diff.days > 14:
                await member.add_roles(lvl1, lvl0)
            elif diff.days > 90:
                await member.add_roles(lvl2, lvl1, lvl0)
            elif diff.days > 180:
                await member.add_roles(lvl3, lvl2, lvl1, lvl0)
            elif diff.days > 270:
                await member.add_roles(admin, lvl3, lvl2, lvl1, lvl0)
            await ctx.send(f"Clerance updates for {member.mention}")
        except (commands.MemberNotFound, discord.NotFound):
            try: user: discord.User = await client.fetch_user(int(member))
            except (commands.UserNotFound, discord.NotFound): await ctx.reply(f"{member} not found.")
            else: await ctx.reply(user.mention)
    await ctx.send("Refresh complete.")


@client.command(hidden=True)
async def update(ctx: commands.Context):
    channels: list[discord.abc.GuildChannel] = client.get_all_channels()
    link = 'https://discord.gg/zt6j4h7ep3'
    embed = discord.Embed(title='`Update!` - New command: `Timeout`',
    description=
f"""
**Timeout**

Keeps an annoying person in a timeout channel 
with no contact except those who have access
to that channel.

`  Name :     timeout    `
`Aliases: to|isl|isolate `

You can banish the annoying person by doing:
`$timeout <member>`

If you want to join my home server, click [`J.A.R.V.I.S`]({link})
""", colour=discord.Colour.random())
    for channel in channels:
        if 'general' in channel.name and isinstance(channel, discord.TextChannel):
            message: discord.Message = await channel.send(embed=embed)
            await ctx.reply(f'`Message link`: https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}')


class Fran(discord.ui.View):
    pass


@client.command(hidden=True)
async def test1(ctx: commands.Context):

    await ctx.send("Context", view=Fran().add_item(
        discord.ui.Button(style=discord.ButtonStyle.blurple, label="Test")))  # Blue button with button label of "Test"
    res = await client.wait_for("button_click")  # Wait for button to be clicked
    await res.respond(type=discord.InteractionType.ChannelMessageWithSource, content=f'Button Clicked')


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
                await ctx.reply(
                    f'`Message link`: https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}')


@client.command(hidden=True)
async def msg_dts(ctx: commands.Context, message: discord.Message):
    await ctx.send(f"Content: {message.content}")
    print(f"Content: {message.content}")


@client.command(hidden=True)
async def create_webhooks(ctx: commands.Context):
    webhook: discord.Webhook = await ctx.channel.create_webhook(name="cross-connect", avatar=None)
    await ctx.reply(webhook.id)


client.run(bot_token)
