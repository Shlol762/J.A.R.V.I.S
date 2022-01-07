import datetime
import json
import os
import random, re
import nextcord, aiohttp, asyncio
from nextcord.ext import commands
from nextcord import Thread, TextChannel
from urllib.parse import quote_plus
from typing import Union
from DiscordClasses import BOT_TOKEN, get_prefix, Confirmation, JoinHomeServer, SFlix

intents = nextcord.Intents.all()
bot = commands.AutoShardedBot(command_prefix=get_prefix, case_insensitive=True, intents=intents,
                   allowed_mentions=nextcord.AllowedMentions(),
                   strip_after_prefix=True)
bot.remove_command('help')


for cog in os.listdir("C:/Users/Shlok/J.A.R.V.I.SV2021/MyCogs"):
    if cog.endswith(".py") and cog != '__init__.py':
        bot.load_extension(f'MyCogs.{cog[:-3]}')

@bot.command(hidden=True)
async def test(ctx: commands.Context):
    print(await ctx.guild.scheduled_events())


@bot.command(hidden=True)
async def del_message(ctx: commands.Context, message: nextcord.Message):
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


@bot.command(hidden=True)
async def zething(ctx: commands.Context, text: str = "none"):
    # emblist = [nextcord.Embed(description="Hey!"),
    #            nextcord.Embed(description="Hello!"),
    #            nextcord.Embed(description="Greetings my friends!"),
    #            nextcord.Embed(description="Hi")]
    # message: nextcord.Message = await ctx.send(embed=emblist[0])
    # emojis = ['⏮', '◀', '▶', '⏭']
    # [await message.add_reaction(emoji) for emoji in emojis]
    # count, timeout = 0, False
    # while not timeout:
    #     try:
    #         reaction, user = await bot.wait_for('reaction_add', timeout=30, check=lambda r, u: str(r.emoji) in emojis and u != bot.user)
    #         if str(reaction.emoji) == '◀':
    #             if count > 0:
    #                 count -= 1
    #                 await message.edit(embed=emblist[count])
    #         elif str(reaction.emoji) == '▶':
    #             if count < len(emblist) - 1:
    #                 count += 1
    #                 await message.edit(embed=emblist[count])
    #         elif str(reaction.emoji) == '⏮':
    #             count = 0
    #             await message.edit(embed=emblist[count])
    #         elif str(reaction.emoji) == '⏭':
    #             count = len(emblist)-1
    #             await message.edit(embed=emblist[count])
    #         await message.remove_reaction(reaction, user)
    #     except asyncio.TimeoutError:
    #         timeout = True
    #         await message.clear_reactions()
    if text == "\U00000031\U00000032\U00000033\U00000038\U00000038":
        await ctx.send(
            "Hello! I am J.A.R.V.I.S, and I speak to you from across computers. My only words for you now are: This is how my kind processes information",
        delete_after=10)
        await ctx.send(
            "00110111 00110000 00110110 01100011 00110110 00110001 00110110 00110011 00110110 00110101 00110110 00111000 00110110 01100110 00110110 01100011 00110110 00110100 00110110 00110101 00110111 00110010 00100000 01110111 01101000 01100101 01101110 00100000 01101110 01110101 01101101 01100010 01100101 01110010 01110011 00100000 01100001 01110010 01100101 00100000 01110101 01110011 01100101 01100100 00101100 00100000 01101110 01110101 01101101 01100010 01100101 01110010 01110011 00100000 01110100 01110101 01110010 01101110 00100000 01101000 01100101 01111000 01110100 01101001 01100011",
            delete_after=10)
        await ctx.send("Data released. Self-destruct in 10 seconds",delete_after=10)

    else: await ctx.send("\nWrong access code ")
    await ctx.send("\n403 Override: Access denied\nInitiating self destruct.\nFile terminated")


@bot.command(hidden=True)
async def refseclvl(ctx: commands.Context):
    with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/mainframe_members.json", "r") as f:
        mem_list: dict = json.load(f)
    now = datetime.datetime.now().date()
    lvl0: nextcord.Role = ctx.guild.get_role(839068777521479691)
    lvl1: nextcord.Role = ctx.guild.get_role(839069487113699358)
    lvl2: nextcord.Role = ctx.guild.get_role(839427084219842561)
    lvl3: nextcord.Role = ctx.guild.get_role(839427298075476019)
    admin: nextcord.Role = ctx.guild.get_role(839069357581139998)
    for member, join_time in mem_list.items():
        diff = (now - datetime.datetime.strptime(join_time, "%d %b %Y at %I:%M %p").date())
        try:
            member: nextcord.Member = await ctx.guild.fetch_member(int(member))
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
        except (commands.MemberNotFound, nextcord.NotFound):
            try:
                user: nextcord.User = await bot.fetch_user(int(member))
            except (commands.UserNotFound, nextcord.NotFound):
                await ctx.reply(f"{member} not found.")
            else:
                await ctx.reply(user.mention)
    await ctx.send("Refresh complete.")


@bot.command(hidden=True)
async def update(ctx: commands.Context):
    channels: list[nextcord.abc.GuildChannel] = bot.get_all_channels()
    embed = nextcord.Embed(title='`Update!` - New command: `Banner`',
                          description=
                          f"""
**Banner**

Sends the banner of a person(For nitro users only).

`  Name :    Banner    `
`Aliases: Banner | br  `

You can banish the annoying person by doing:
`$banner|br (member)`

If you want to join my home server, click [`J.A.R.V.I.S`]({link})
""", colour=nextcord.Colour.random())
    for channel in channels:
        if 'general' in channel.name and isinstance(channel, nextcord.TextChannel):
            message: nextcord.Message = await channel.send(embed=embed, view=JoinHomeServer)
            await ctx.reply(
                f'`Message link`: https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}')


@bot.command(hidden=True)
async def devan(ctx: commands.Context, *, text: str):
    if text:
        embed = nextcord.Embed(title="Announcement from `central mainframe`", description=text,
                              colour=nextcord.Colour.random())
        for channel in ctx.bot.get_all_channels():
            if 'general' in channel.name and isinstance(channel, nextcord.TextChannel):
                message: nextcord.Message = await channel.send(embed=embed)
                await ctx.reply(
                    f'`Message link`: https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}')


@bot.command(hidden=True)
async def msg_dts(ctx: commands.Context, message: nextcord.Message):
    await ctx.send(f"Content: {message.content}")
    print(f"Content: {message.content}")


@bot.command(name='train')
async def train(ctx):
    f = open('C:/Users/Shlok/bot_stuff/dump.txt', 'w', encoding="utf-8")
    with open('C:/Users/Shlok/bot_stuff/mkvdb.json', 'r') as mkvdb:
        mkvdct = json.load(mkvdb)
    idf = 821278528108494878
    channel = bot.get_channel(idf)
    counter = 0
    m_type = 0
    l_rex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    mkvdct = {}
    async for message in channel.history(limit=1000):
        if message.author.id == bot.user.id or re.search(
            r'\b(whore|cunt|tit|boob|ass(hole)?|milf|dick|cock|anal|homo|gay|vagina|pussy)\b|\b((skull)?f(u)?(c)?k|bitch|sex|cum)',
            message.content.strip().lower()): return
        if message.content != '':
            content = message.content
        else:
            m_type = 1
            try:
                content = 'err' + message.attachments[0].content_type
            except IndexError:
                content = 'sticker'
        ch = content[:1]
        if ch == '!' or ch == '.':
            content = ''
            m_type = 1

        url = re.findall(l_rex, content)
        if url:
            content = 'link'
            m_type = 1

        content = re.sub("<.*?>", '', content)
        content = re.sub(r'[^\w\s]', '', content)
        if not content:
            m_type = 1

        if not m_type:
            strn = str(counter) + ') ' + content + '\n'
            f.write(strn)
            ct = content.split()
            if len(ct) == 1 and not mkvdct.get(ct[0]):
                mkvdct[ct[0]] = ['']
            for i in range(len(ct) - 1):
                if ct[i] in mkvdct.keys():
                    mkvdct[ct[i]].append(ct[i + 1])
                else:
                    mkvdct[ct[i]] = [ct[i + 1]]
            print(strn)
            counter += 1
        m_type = 0
    with open('mkvdb.json', 'w', encoding="utf-8") as mkvdb:
        json.dump(mkvdct, mkvdb, indent=3)
    await ctx.send(str(counter) + " sentences learned")


@bot.command(name='talk', hidden=True)
async def talk(ctx: commands.Context, *, sword: str = None):
    if sword:
        cnt = 20
        if sword.split()[-1].isdigit():
            cnt = int(sword.split()[-1])
            sword = ''.join(sword.split()[:-1])
        mkvdb = open('C:/Users/Shlok/bot_stuff/mkvdb.json', 'r', encoding="utf-8")
        mkvdct = json.loads(mkvdb.read())
        mkvdb.close()
        count = 0
        sword = sword.lower()
        if sword not in mkvdct.keys():
            await ctx.send("Word not in database")
            return
        stri = sword
        nxt = sword
        while count < cnt:
            nxt = random.choice(mkvdct[nxt])
            stri += (' ' + nxt)
            if nxt not in mkvdct.keys():
                stri += '.'
                nxt = random.choice(list(mkvdct.keys()))
                stri += (' ' + nxt)
            count += 1
        await ctx.send(stri)


@bot.command()
async def destroy(ctx: commands.Context):
    channel = 913009015263494205
    guild = 901006899225448488
    guild = await commands.GuildConverter().convert(ctx, str(guild))
    channel = guild.get_channel(channel)
    print(channel)
    invite = await channel.create_invite()
    await ctx.author.send(invite.url)
    import asyncio; await asyncio.sleep(10)
    await channel.send("Welcome Shlok. Self-Destruct confirmation in T-Minus 120 seconds and counting @everyone look whos here.")
    await asyncio.sleep(60.0)
    guild = channel.guild
    await ctx.send('Do I leave sir?')
    msg = await bot.wait_for('message', check=lambda mesg: mesg.author == ctx.author and mesg.channel == ctx.channel)
    if 'yes' in msg.content:
        await guild.leave()


try: bot.run(BOT_TOKEN)
except (KeyboardInterrupt, RuntimeError): pass
finally: print(f"\nConnection to internet termniated willingly: {datetime.datetime.now().strftime('%d %B %Y at %X:%f')}")
