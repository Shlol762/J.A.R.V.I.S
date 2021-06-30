import re, random
from discord import Forbidden, Invite, Message, Member
from discord.ext.commands import Context, Bot
from typing import Optional, Union, Any


src_was_bot = "Message was by bot"
x_was_not_in_msg = "No {0} in message"


async def forbidden_word(ctx: Context, bot: Bot) -> Union[Message, str]:
    """Checks for the forbidden word Shlol#2501 has set"""
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


async def noswear(ctx: Context, bot: Bot) -> Union[Message, str]:
    """Checks and alerts users if they are using foul language."""
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


async def greetings(ctx: Context, bot: Bot) -> Union[Message, str]:
    """Checks for greetings and responds randomly"""
    author: Member = ctx.author
    response = random.choice([True, True, True, False, True, True])
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


async def farewells(ctx: Context, bot: Bot) -> Union[Message, str]:
    """Checks for farewells and responds randomly"""
    author: Member = ctx.author
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


async def nou(ctx: Context, bot: Bot) -> Union[Message, str]:
    """Responds with 'No u' for certain keywords."""
    author: Member = ctx.author
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



