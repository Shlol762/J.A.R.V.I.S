import json
from datetime import datetime
import discord
from PIL import Image
from discord.ext import commands
from discord.ext.commands import RoleNotFound, RoleConverter, MemberConverter, Bot, Context, when_mentioned_or,\
    MessageConverter
from discord import Role, Member, Message, Emoji
from pytz import timezone
from typing import Union, Optional, List, Coroutine
import aiohttp
import re


__doc__ = "Module containing all sorts of custom functions."


def trim(string: str) -> str:
    """Takes in a string argument and trims every extra whitespace from in between as well as the ends."""
    return re.sub(" +", " ", string.strip())


def print_methods(obj: object, magic_methods: bool = False):
    """Prints all the callable attributes of an object, with an option to not print the default 'Magic'
    or 'Dunder' methods."""
    print("\n\n\nMethods of object are:\n")
    for method_name in dir(obj):
        if callable(getattr(obj, method_name)):
            if re.search(r"^__.*__$", method_name) and magic_methods is False: pass
            else: print(method_name + '\n')


def print_vars(obj):
    """Prints all the uncallable attributes of an object."""
    print("\n\n\nAttributes of object are:\n")
    for var_name in dir(obj):
        if not callable(getattr(obj, var_name)):
            print(f"{var_name} : {getattr(obj, var_name)}\n")


async def reaction(ctx: Context = None, success=None):
    """Adds a reaction to any command invoking message."""
    if success is False:
        await ctx.message.clear_reactions()
        await ctx.message.add_reaction('❌')
    if success is True:
        emoji: str = ctx.command.extras.get('emoji')
        emoji: Emoji = ctx.bot.get_emoji(int(emoji)) if emoji.isnumeric() else emoji
        try:
            await ctx.message.add_reaction(emoji)
        except discord.HTTPException:
            await ctx.message.add_reaction('✅')


def image_join(img1: str, img2: str) -> str:
    """Joins 2 images into 1, and returns the new image's file path."""
    im1: Image = Image.open(img1)
    im2: Image = Image.open(img2)
    new_image = Image.new('RGB', (im1.width + im2.width, im1.height))
    new_image.paste(im1, (0, 0))
    new_image.paste(im2, (im1.width, 0))
    path: str = "C:/Users/Shlok/J.A.R.V.I.SV2021/image_resources/ipl_vs_logo.png"
    new_image.save(path)
    return path


def time_set(time: datetime = None, time_format: str = None) -> Optional[datetime]:
    """Sets the time to IST from any other timezone."""
    return time.replace(
        tzinfo=timezone('UTC')).astimezone(
        timezone('Asia/Kolkata')
    ).strftime(
        time_format
    ) if time_format else time.astimezone(
        timezone('Asia/Kolkata'))


async def get_emoji(bot: Bot, emoji: int) -> Optional[Union[str, Emoji]]:
    """Getting the emoji from inside a Bot instance."""
    for squad in bot.emojis:
        if squad.id == emoji or squad.name == emoji:
            returned: bool = True
            break
        else:
            returned = False
    return "" if returned is False else squad


async def hypesquad_emoji(bot: Bot, squad: str) -> Optional[Union[str, Emoji]]:
    """Gets the emoji by the ID from https://discord.gg/zt6j4h7ep3"""
    emoji: int = {"Hypesquad Brilliance": 840464223326306305,
             "Hypesquad Balance": 840464223280824320,
             "Hypesquad Bravery": 840464223560663040,
             "Staff": 840464223602737192,
             "Legendary": 840464223632752670,
             "Bug Hunter": 840464223251333150,
             "Bug Hunter Level 2": 840464223251333150,
             "Early Supporter": 840464223770771496,
             "Hypesquad": 840464223326437386,
             "Bot": 840464223804325909,
             "VerifiedBot": 840464223975768095}.get(squad)
    return await get_emoji(bot=bot, emoji=emoji)


def timeto(time_str: str) -> str:
    """Calculates the difference between the present and any given timestamp."""
    now: datetime = datetime.now()
    num: bool = True if time_str.replace("/", "").replace(":", "").replace(" ", "").isdigit() else False
    time_str: str = time_str.replace(now.strftime("%Y")[-2:], now.strftime("%Y")) if time_str[-2:] == "21" and time_str[-4:] != "2021" else time_str
    if num is True:
        if len(time_str) in (10, 9, 8):
            till: datetime = datetime.strptime("00:00 " + time_str, "%H:%M %d/%m/%Y")
        elif len(time_str) == 5 or len(time_str) == 4:
            if len(time_str.split("/")) == 1:
                till: datetime = datetime.strptime(time_str + now.strftime(" %d/%m/%Y"), "%H:%M %d/%m/%Y")
            elif len(time_str.split("/")) == 2:
                till: datetime = datetime.strptime(now.strftime(" %d/%m/%Y"), "%H:%M %d/%m/%Y")

        else:
            till: datetime = datetime.strptime(time_str, "%H:%M %d/%m/%Y")
    elif num is False:
        if not time_str.isalpha():
            if len(time_str) == 4 or len(time_str) == 3:
                till = datetime.strptime(now.strftime(f"00:00 {time_str[:-2]}/%m/%Y"), "%H:%M %d/%m/%Y")

        elif time_str.isalpha():
            if len(time_str) == 3:
                till: datetime = datetime.strptime(now.strftime(f"00:00 01/{time_str}/%Y"), "%H:%M %d/%b/%Y")
            elif len(time_str) > 3:
                till: datetime = datetime.strptime(now.strftime(f"00:00 01/{time_str}/%Y"), "%H:%M %d/%B/%Y")
    diff = str(till - now).split(",")
    if len(diff) > 1:
        days: int = int(diff[0][:-4].replace("-", ""))
        if days >= 365:
            years: int = round(days/365, 4)
            y_str: str = str(years).split(".")[1]
            years: int = int(str(years).split(".")[0])
            days: int = round((int(y_str)/int('1' + len(y_str)*'0'))*365)
        else:
            years: int = 0
    else:
        years: int = 0
        days: int = 0
    diff: str = diff[1].split(":") if len(diff) > 1 else diff[0].split(":")
    time_: str = f"T-{'Minus' if till > now else 'Plus'} `"
    time_ += f"{years} year{'s' if years > 1 else ''} " if years != 0 else ""
    time_ += f"{days} day{'s' if days > 1 else ''} " if days != 0 else ""
    time_ += f"{diff[0].strip()} hr{'s' if int(diff[0].strip()) > 1 else ''} " if int(diff[0].strip()) != 0 else ""
    time_ += f"{diff[1].strip()} min{'s' if int(diff[1].strip()) > 1 else ''} " if int(diff[1].strip()) != 0 else ""
    time_ += f"{diff[2].strip().split('.')[0]} sec` {'to' if till > now else 'from'} `{till.strftime('%H:%M %d/%m/%Y')}`"
    return time_


def calculate_position(channel: Union[discord.TextChannel, discord.VoiceChannel], pos: int) -> int:
    """Calculates the heirarchy position of channels and categories in a discord server."""
    ctgry_pos = channel.category.position
    index_start = 0
    for category in channel.guild.categories:
        if category.position < ctgry_pos:
            index_start += len(category.channels)
    return index_start+pos


def permission_confirm(perm_key_pair: list) -> Union[bool, str, None]:
    """Converts string versions of bool inputs to raw bool values."""
    if perm_key_pair[1].strip() == 'true': pi = True
    elif perm_key_pair[1].strip() == 'false': pi = False
    elif perm_key_pair[1].strip() == 'none': pi = None
    else: pi = 'None'
    return pi


async def role_member_conv(ctx: commands.Context, target: str) -> Union[Role, Member]:
    """Converts inputs such as names and IDs to Role or Member instances"""
    try: target: Role = await RoleConverter().convert(ctx, target)
    except RoleNotFound: target: Member = await MemberConverter().convert(ctx, target)
    return target


def number_system(num: int) -> str:
    """Converts raw integers to the international number system"""
    num = str(num)
    num = list(num)
    num.reverse()
    divider = 0
    new_num = ''
    for numeral in num:
        divider += 1
        if divider % 4 == 0:
            new_num += f',{numeral}'
            divider = 1
        else: new_num += numeral
    return new_num[::-1]


def find_nth_occurrence(string: str, substring: str, n: int) -> Optional[int]:
    """Return index of `n`th occurrence of `substring` in `string`, or None if not found."""
    index = 0
    for _ in range(n):
        index = string.find(substring, index+1)
        if index == -1:
            return None
    return index


async def send_to_paste_service(content: str) -> str:
    """Redirects and pastes content to https://paste.pythondiscord.com/ in case of
    message exceeding the discord API's character limit of 4000 for bots."""
    url = 'https://paste.pythondiscord.com/{key}'
    async with aiohttp.ClientSession() as session:
        async with session.post(url.format(key="documents"), data=content) as req:
            json_req = await req.json()
    try: url = url.format(key=json_req['key']) + '.py'
    except KeyError: url = url.format(key='documents')
    return url


def file_opener(file: str, option: str = 'read') -> str:
    """Redundant function. Being removed soon."""
    path = re.sub("{}", file, "C:/Users/Shlok/J.A.R.V.I.SV2021/text_files/{}_forbidden_list.txt")
    path = file if "C:/Users" in file else path
    f = open(path, 'r')
    lines, read = f.readlines(), f.read()
    f.close()
    return "".join(lines)


async def get_prefix(bot: Bot, message: Message) -> str:
    """Multi-Prefix modifier for the bot."""
    with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/prefixes.json", "r") as f:
        prefixes = json.load(f)
    id: str = str(message.guild.id) if message.guild else "DM(A113)"
    for_guild = prefixes[id]
    return for_guild

async def comm_log_local(ctx: Context, status: str):
    """Logs all command movement into a local text file."""
    with open("C:/Users/Shlok/bot_stuff/command_logs.txt", "r") as f:
        lines: list[str] = f.read().split("\n")
    sl_no: str = "{0:0>4}".format(int(re.search(r'[0-9]{4}', lines[1]).group()) + 1)
    header: str = re.sub("[0-9]{4}", sl_no, lines[1])
    lines.pop(1)
    lines.insert(1, header)
    time: str = time_set(ctx.message.created_at, "%H:%M")
    date: str = time_set(ctx.message.created_at, "%d-%m-%y")
    com_name = ctx.command.name[:6] if ctx.command else "Invalid"
    cog_name = ctx.command.cog_name[:4] if ctx.command else "Invalid"
    com_num = ctx.command.extras['number'] if ctx.command else "Invalid"
    status = "404" if "404" in status else status
    lines.append(f"|{sl_no:^11}|{com_name:^9}|{cog_name:^10}|{com_num:^8}|{status:^44}|{time:^6}|{date:^8}| {ctx.author.id} | {ctx.channel.id if ctx.channel else ctx.author.id} | {ctx.guild.id if ctx.guild else ctx.author.id} |")
    f = open("C:/Users/Shlok/bot_stuff/command_logs.txt", "w")
    f.write("\n".join(lines))
    f.close()
