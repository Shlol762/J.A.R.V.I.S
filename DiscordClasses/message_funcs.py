import asyncio
import json
import re, random
from discord import Forbidden, Invite, Message, Member
from discord.ext.commands import Context, Bot
from typing import Optional, Union, Any


webhooks = [861660340617084968, 861660166193807430, 861660711037960243, 861660517746999356, 880318607643521075]
src_was_bot = "Message was by bot"
x_was_not_in_msg = "No {0} in message"


async def forbidden_word(ctx: Context) -> Union[Message, str]:
    """Checks for the forbidden word Shlol#2501 has set"""
    bot: Bot = ctx.bot
    author: Member = ctx.author
    if re.search(r'\b([bh]( )*a)(( )*i)+\b', str(ctx.message.content).strip().lower()):
        if author.name != bot.user.name:
            invite_link: Invite = await ctx.channel.create_invite(max_uses=1)
            message_hai_kick: Message = await author.send(invite_link)
            try:
                await author.kick(reason=f"{author.name} used the unholy words")
            except Forbidden:
                await message_hai_kick.delete()
                await invite_link.delete()
                return await ctx.reply(f"Sorry guys.. can't kick {author.mention}... No perms!")
        else: return src_was_bot
    else: return x_was_not_in_msg.format("forbidden word")


async def noswear(ctx: Context) -> Union[Message, str]:
    """Checks and alerts users if they are using foul language."""
    bot: Bot = ctx.bot
    author: Member = ctx.author
    if re.search(
            r'\b(asshole|whore|cunt)\b|\b(fuck|fk|fuk|bitch)',
            ctx.message.content.strip().lower()):
        if author.name != bot.user.name:
            watch_ur_lang_gifs: str = random.choice([
                'https://tenor.com/view/your-language-is-offensive-watch-your-mouth-zach-galifianakis-gif-13885320',
                'https://tenor.com/view/funny-or-die-will-ferrell-watch-your-mouth-filthy-mouth-mouth-gif-4427315',
                'https://tenor.com/view/avengers-language-captain-america-age-of-ultron-gif-5285201',
                'https://tenor.com/view/watch-your-language-words-talk-dont-be-harsh-derek-luke-gif-15626011',
                'https://tenor.com/view/iron-man-language-galactic-republic-gif-20457940'])
            return await ctx.reply(watch_ur_lang_gifs)
        else: return src_was_bot
    else: return x_was_not_in_msg.format("swear words")


async def greetings(ctx: Context, random_ = True) -> Union[Message, str]:
    """Checks for greetings and responds randomly"""
    author: Member = ctx.author
    bot: Bot = ctx.bot
    response = random.choice([True, False, True, False, False, True]) if random_ else True
    if re.search(r'\b(h(i)+|he(y)+|(wh(a)+(s)*)*s(u)+(p)+|(he[nl]l(o)+)(w)*)\b',
                 ctx.message.content.strip().lower()):
        if author.name != bot.user.name:
            hi_response: str = random.choice(['Hello there {}!',
                                              "How ya doin' {}?",
                                              'Whazzup {}?',
                                              "G'day {}!",
                                              'Oh Hello {}!',
                                              'Hi {}!',
                                              'Konnichiva!',
                                              'Namaste!',
                                              'Bonjour!',
                                              'Namaskaragalu!',
                                              'Hola!',
                                              'Ola!',
                                              'Howdy {}!',
                                              'Ciao!'
                                              ])
            if response: return await ctx.reply(hi_response.format(author.mention))
        else: return x_was_not_in_msg
    else: return x_was_not_in_msg.format("greetings")


async def farewells(ctx: Context) -> Union[Message, str]:
    """Checks for farewells and responds randomly"""
    author: Member = ctx.author
    bot: Bot = ctx.bot
    response = random.choice([True, True, True, False, True, True])
    if re.search(r"\b(by(e)+|i(')*m out)\b", ctx.message.content.strip().lower()):
        if author.name != bot.user.name:
            bye_response: str = random.choice(['See you later...',
                                               'Sayonara!',
                                               'C u latah!',
                                               'Have a good day!... or night!',
                                               'Have a good time!',
                                               'Adios!',
                                               'Au revoir!',
                                               "You're going already?",
                                               'Bye!',
                                               'Ciao!'
                                               ])
            if response: await ctx.reply(bye_response.format(author.name))
        else: return src_was_bot
    else: return x_was_not_in_msg.format("farewells")


async def nou(ctx: Context) -> Union[Message, str]:
    """Responds with 'No u' for certain keywords."""
    author: Member = ctx.author
    bot: Bot = ctx.bot
    message_text: str = ctx.message.content.strip().lower()
    if re.search(r'\b(kill urself)\b', message_text) or message_text == 'ok':
        if author.name != bot.user.name:
            return await ctx.reply('No u')
        else: return src_was_bot
    else: return x_was_not_in_msg.format("nou deserving content")


async def urnotgod(ctx: Context) -> Union[Message, str]:
    """Responds with a variety of messages that oppose a person who claims to be god."""
    if re.search(r"\b(i( )?('| a)?( )?m g( )?o( )?d)\b",
                   ctx.message.content.strip().lower()):
        am_i_g_response = random.choice(["🤮, No you're not.",
                                     "I strongly disagree",
                                     "*cough* The person who proclaims him/herself god, is no god at all."
                                     ])
        return await ctx.reply(am_i_g_response)
    else: return x_was_not_in_msg.format("conceitedness")


async def eastereggs(ctx: Context) -> Union[Message, str]:
    message = ctx.message
    response = random.choice([
        'Ya rang?', "'Sup?", "Heyyy!",
        f'At your service{" sir" if ctx.author.id == 613044385910620190 else ""}!',
        'Ayoooo whassuppp?', 'You summoned me?', 'Hello there! (gen kenobi vibes amirite?)',
        "https://tenor.com/view/%D0%BE%D0%B4%D0%B8%D0%BD%D0%B4%D0%BE%D0%B"
        "C%D0%B0-kevin-mc-callister-home-alone-wave-hi-gif-15750897"
    ])
    if (ctx.bot.user.mentioned_in(message) and not ctx.command and not re.search(r"(@everyone|@here)", message.content.lower())
        and ctx.author != ctx.bot.user and message.webhook_id not in webhooks and not message.reference) or re.search(
        r"\b(^((j\.?)+(a\.?)+((r\.?)+(v\.?)+((i\.?)+(s\.?)+)?|y))|"
        r"((j\.?)+(a\.?)+((r\.?)+(v\.?)+((i\.?)+(s\.?)+)?|y))$)\b", message.content.lower()):
        await ctx.reply(response)
        try:
            message = await ctx.bot.wait_for('message', timeout=5.0, check=lambda msg: msg.author == ctx.author)
            final_response: Message = await greetings(await ctx.bot.get_context(message), False) if not re.search(
                r"\b(y[eu][sap]?h?)\b", message.content) else await message.reply("Um I don't know how to converse any further :D")
        except asyncio.TimeoutError: pass


    return x_was_not_in_msg.format("eastereggs")



async def train(ctx: Context):
    rstring = r'\b(whores?|cunts?|tits?|boobs?|ass(holes?)?|milfs?|dick(s|heads?)?|cocks?|anals?|homos?' \
              r'|w?tf*|gays?|vaginas?|puss(y|ies))\b|\b((skull)?f(u)?(c+)?k|bitch|sex|cum|fuc+|porn)'
    if ctx.author.id == ctx.bot.user.id or re.search(
            rstring,
            ctx.message.content.strip().lower()) or ctx.channel.name == 'nsfw':
        return
    f = open('C:/Users/Shlok/bot_stuff/dump.txt', 'a', encoding="utf-8")
    with open('C:/Users/Shlok/bot_stuff/mkvdb.json', 'r') as mkvdb:
        mkvdct = json.load(mkvdb)
    counter = 0
    m_type = 0
    l_rex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    message = ctx.message
    if message.content != '':
        content = message.content.lower()
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
    # content = re.sub(":.*?:", '', content)
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
        # print(strn)
        # print('\n')
        counter += 1
    m_type = 0
    with open('C:/Users/Shlok/bot_stuff/mkvdb.json', 'w', encoding="utf-8") as mkvdb:
        json.dump(mkvdct, mkvdb, indent=3)



