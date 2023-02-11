import datetime
import json
import os
import random
import re
import demoji
import discord
import logging
from discord.ext import commands
from DiscordClasses import BOT_TOKEN, JoinHomeServer, Jarvis
from asyncio import get_event_loop


log = logging.getLogger(__name__)

bot = Jarvis()


with open('C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/mainframe_members.json', 'r') as f:
    bot.MAINFRAME_MEMBERS = json.load(f)


with open('C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/settings.json', 'r') as f:
    bot.SETTINGS = json.load(f)

del f

for cog in os.listdir("C:/Users/Shlok/J.A.R.V.I.SV2021/JayCogs"):
    if re.search(r'^(?!__init__).+(\.py)$', cog):
        get_event_loop().run_until_complete(bot.load_extension(f'JayCogs.{cog[:-3]}'))


@bot.command(hidden=True)
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


@bot.command(hidden=True)
async def zething(ctx: commands.Context, text: str = "none"):
    if text == "\U00000031\U00000032\U00000033\U00000038\U00000038":
        await ctx.send(
            "Hello! I am J.A.R.V.I.S, and I speak to you from across computers. My only words for you now are: This is how my kind processes information",
            delete_after=10)
        await ctx.send(
            "00110111 00110000 00110110 01100011 00110110 00110001 00110110 00110011 00110110 00110101 00110110 00111000 00110110 01100110 00110110 01100011 00110110 00110100 00110110 00110101 00110111 00110010 00100000 01110111 01101000 01100101 01101110 00100000 01101110 01110101 01101101 01100010 01100101 01110010 01110011 00100000 01100001 01110010 01100101 00100000 01110101 01110011 01100101 01100100 00101100 00100000 01101110 01110101 01101101 01100010 01100101 01110010 01110011 00100000 01110100 01110101 01110010 01101110 00100000 01101000 01100101 01111000 01110100 01101001 01100011",
            delete_after=10)
        await ctx.send("Data released. Self-destruct in 10 seconds", delete_after=10)

    else:
        await ctx.send("\nWrong access code ")
    await ctx.send("\n403 Override: Access denied\nInitiating self destruct.\nFile terminated")


@bot.command(hidden=True)
async def refseclvl(ctx: commands.Context):
    with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/mainframe_members.json", "r") as _f:
        mem_list: dict = json.load(_f)
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
                await member.add_roles(lvl1)
            elif diff.days > 90:
                await member.add_roles(lvl2)
            elif diff.days > 180:
                await member.add_roles(lvl3)
            elif diff.days > 270:
                await member.add_roles(admin)
            await ctx.send(f"Clerance updates for {member.mention}")
        except (commands.MemberNotFound, discord.NotFound):
            try:
                user: discord.User = await bot.fetch_user(int(member))
            except (commands.UserNotFound, discord.NotFound):
                await ctx.reply(f"{member} not found.")
            else:
                await ctx.reply(user.mention)
    await ctx.send("Refresh complete.")


@bot.command(hidden=True)
async def update(ctx: commands.Context):
    channels: list[discord.abc.GuildChannel] = bot.get_all_channels()
    embed = discord.Embed(title='`Update!` - New command: `Banner`',
                          description=
                          f"""
**Banner**

Sends the banner of a person(For nitro users only).

`  Name :    Banner    `
`Aliases: Banner | br  `

You can banish the annoying person by doing:
`$banner|br (member)`

If you want to join my home server, click [`J.A.R.V.I.S`]({link})
""", colour=discord.Colour.random())
    for channel in channels:
        if 'general' in channel.name and isinstance(channel, discord.TextChannel):
            message: discord.Message = await channel.send(embed=embed, view=JoinHomeServer)
            await ctx.reply(
                f'`Message link`: https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}')


@bot.command(hidden=True)
async def devan(ctx: commands.Context, *, text: str):
    if text:
        embed = discord.Embed(title="Announcement from `central mainframe`", description=text,
                              colour=discord.Colour.random())
        for channel in ctx.bot.get_all_channels():
            if 'general' in channel.name and isinstance(channel, discord.TextChannel):
                message: discord.Message = await channel.send(embed=embed)
                await ctx.reply(
                    f'`Message link`: https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}')


@bot.command(hidden=True)
async def msg_dts(ctx: commands.Context, message: discord.Message):
    await ctx.send(f"Content: {message.content}")
    print(f"Content: {message.content}")


@bot.command(name='train')
async def train(ctx):
    _f = open('C:/Users/Shlok/bot_stuff/dump.txt', 'w', encoding="utf-8")
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
            _f.write(strn)
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
    import asyncio
    await asyncio.sleep(10)
    await channel.send(
        "Welcome Shlok. Self-Destruct confirmation in T-Minus 120 seconds and counting @everyone look whos here.")
    await asyncio.sleep(60.0)
    guild = channel.guild
    await ctx.send('Do I leave sir?')
    msg = await bot.wait_for('message', check=lambda mesg: mesg.author == ctx.author and mesg.channel == ctx.channel)
    if 'yes' in msg.content:
        await guild.leave()


@bot.command()
async def test(ctx: commands.Context):
    for i in range(10):
        i += i
        log.info((f'*'*i)+'\r')


@bot.command()
async def chat_history(ctx, user: discord.User, limit: int = 10):
    # Get the user object for the user you want to read the chat history with
    messages = [message async for message in user.history(limit=limit)][::-1]
    for message in messages:
        await ctx.send(f"`{message.author}`: {message.content if message.content else '`EmptyMessageWithAttachment`'}")


@bot.command()
async def recover(ctx: commands.Context):
    channels = set()
    for guild in bot.guilds:
        for channel in guild.channels:
            channels.add(channel) if isinstance(channel, discord.TextChannel) else None
        for member in guild.members:
            try:channels.add(member.dm_channel) if member.dm_channel else None
            except AttributeError: pass
    messages = {}
    for channel in channels:
        try:
            messages[channel.name] = [message.content async for message in channel.history(limit=None, after=datetime.datetime(2021, 9, 27, 13, 41, 18), oldest_first=True)]
            log.info(f'{channel.name}...')
        except discord.Forbidden: pass

    messages = {
        re.sub('[\\uff5c│⌖✎⃣➥]', '', (demoji.replace(channel))): [re.sub(r'[^\w\s]', '', re.sub("<.*?>", '', msg)) for
                                                                  msg in msgs if msg != "" or msg != " "]
        for channel, msgs in messages.items() if len(msgs) > 0 and channel != ""}

    with open("C:/Users/Shlok/Downloads/messages.json", "w") as _f:
        json.dump(messages, _f, indent=3)

    log.info('Complete.')


try:
    bot.run(BOT_TOKEN, log_handler=logging.StreamHandler(), log_level=logging.INFO, log_formatter=discord.utils._ColourFormatter(), root_logger=True)
except (KeyboardInterrupt, RuntimeError):
    pass
finally:
    log.info(
        f"Connection to internet termniated willingly.")
