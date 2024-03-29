import json
import os
from datetime import datetime
import discord
from PIL import Image
from discord.ext import commands
from discord.ext.commands import RoleNotFound, RoleConverter, MemberConverter, Bot, Context, when_mentioned_or,\
    MessageConverter
from discord import Role, Member, Message, Emoji, Forbidden
from pytz import timezone
from typing import Union, Optional, List, Coroutine, Tuple, Dict, Callable
import aiohttp, aiofiles
import re
from inspect import isawaitable
from functools import wraps
import asyncio
from time import time as unixtim

__doc__ = "Module containing all sorts of custom functions."


def trim(string_: str) -> str:
    """Takes in a string argument and trims every extra whitespace from in between as well as the ends."""
    return re.sub(" +", " ", string_.strip())


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
    try:
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
    except Forbidden:
        pass


def image_join(img1: Union[str, os.PathLike], img2: Union[str, os.PathLike]) -> Union[str, os.PathLike]:
    """Joins 2 images into 1, and returns the new image's file path."""
    im1: Image = Image.open(img1)
    im2: Image = Image.open(img2)
    new_image = Image.new('RGB', (im1.width + im2.width, im1.height))
    new_image.paste(im1, (0, 0))
    new_image.paste(im2, (im1.width, 0))
    path: os.PathLike = "C:/Users/Shlok/AppData/Local/JARVIScache/vs_logo.jpg"
    new_image.save(path)
    return path


async def download_images(*urls: str, file_names: Tuple[str]) -> str:
    """Downloads an image from a given url."""
    counter = 0
    files = []
    for url in urls:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as req:
                file = f"C:/Users/Shlok/AppData/Local/JARVIScache/{file_names[counter]}.jpg"
                f = await aiofiles.open(file, "wb")
                await f.write(await req.read())
                await f.close()
                files.append(file)
        counter += 1
    return files


def time_set(time: datetime = None, time_format: str = None) -> Optional[datetime]:
    """Sets the time to IST from any other timezone."""
    return time.replace(
        tzinfo=timezone('UTC')).astimezone(
        timezone('Asia/Kolkata')
    ).strftime(
        time_format
    ) if time_format else time.astimezone(
        timezone('Asia/Kolkata'))


async def get_emoji(bot: Bot, emoji: Union[int, str]) -> Optional[Emoji]:
    """Getting the emoji from inside a Bot instance."""
    return discord.utils.find(lambda e: emoji.lower().replace(' ', '') in e.name.lower(),
                                bot.emojis) if isinstance(emoji, str) else bot.get_emoji(emoji)


def timeto(time_str: str) -> Union[str, datetime, datetime]:
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
    return time_, now, till


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


def find_nth_occurrence(_string: str, substring: str, n: int) -> Optional[int]:
    """Return index of `n`th occurrence of `substring` in `string`, or None if not found."""
    index = 0
    for _ in range(n):
        index = _string.find(substring, index+1)
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


async def get_prefix(bot: Bot, message: Message) -> str:
    """Multi-Prefix modifier for the bot."""
    with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/prefixes.json", "r") as f:
        prefixes = json.load(f)
    id: str = str(message.guild.id) if message.guild else "DM(A113)"
    for_guild = prefixes[id]
    return for_guild

async def async_input(prompt: str = None):
    async def _async_input(_prompt: str = None):
        mtch = re.search("(ye?(ah|s)?)",
                              await asyncio.get_event_loop().run_in_executor(None, input, _prompt))
        return mtch
    try:
        _match = await asyncio.wait_for(_async_input(prompt), 5)
    except asyncio.TimeoutError:
        _match = False
        print('Request timed out.')

    return _match


def comm_log_local(command_: Callable):
    """Logs all command movement into a local text file."""
    @wraps(command_)
    async def wrapper(*args, **kwargs):
        ctx = [arg for arg in (args+tuple(kwargs.values())) if isinstance(arg, Context)][0]
        with open("C:/Users/Shlok/bot_stuff/safe_docs/command_logs.txt", "r") as f:
            lines: list[str] = f.read().split("\n")
        sl_no = "{0:0>6}".format(int(re.search(r'[0-9]{6}', lines[1]).group()) + 1)
        header = re.sub("[0-9]{6}", sl_no, lines[1])
        lines.pop(1), lines.insert(1, header)
        time = time_set(ctx.message.created_at, "%H:%M")
        date = time_set(ctx.message.created_at, "%d-%m-%y")
        com_name = ctx.command.name if ctx.command else "Invalid"
        cog_name = ctx.command.cog_name if ctx.command else "Invalid"
        com_num = str(ctx.command.extras.get('number')) if ctx.command else "Invalid"
        await command_(*args, **kwargs)
        lines.extend([
            f"+{'='*51}LOG-ENTRY-{sl_no}{'='*52}+",
            f"|    Name   : {com_name:<45}Command Number: {com_num:<45}|",
            f"|Timestamp  : {time + ' on ' + date + '({})'.format(unixtim()):<106}|",
            f"+{'-'*49}USAGE CONTEXT DETAILS{'-'*49}+",
            f"|Used by: {ctx.author.id:<55}Server  : {(ctx.guild if ctx.guild else ctx.author).id:<45}|",
            f"|Channel: {(ctx.channel if ctx.guild else ctx.author).id:<53}Message ID: {ctx.message.id:<45}|",
            f"|Message Link: {ctx.message.jump_url:<105}|"
            ])
        f = open("C:/Users/Shlok/bot_stuff/safe_docs/command_logs.txt", "w")
        f.write("\n".join(lines))
        f.close()

    return wrapper


class CricInfoCard:
    __slots__ = ['_description', '_status', '_progress', '_teams',
                 '_scores', '_overs', 'link', "_icons"]

    def __init__(self, description: str, status: str, progress: str, teams: List[str], scores: List[str],
                 overs: List[str], icons: List[str], link: Dict[str, str]):
        self.link = link
        self._description = description.split(', ')
        self._status = status
        self._progress = progress
        self._teams = teams
        self._scores = scores
        self._scores.extend(['']) if len(scores) < 2 else scores
        self._overs = overs
        self._overs.extend(['']) if len(overs) < 2 else overs
        self._icons = icons

    def __str__(self):
        ret_string = f"""
[```prolog
{self.teams['team1']['name'].title():<28}{self.teams['team1']['score'].title():>32}\n
{self.teams['team2']['name'].title():<28}{self.teams['team2']['score'].title():>32}\n```]({self.link['match']})```nim
{'Match Number':^12} - {self.number:^12}
{'Location':^12} - {self.location:^12}
"""
        return ret_string + f"{'Date - Time' if self._status not in ('live', 'result', 'stumps') else 'Status':^12} - {self.date_time.capitalize():^12}\n```"\
            if self.date_time else ret_string + f"```"

    @property
    def number(self):
        return self._description[0]

    @property
    def location(self):
        return ', '.join(self._description[1:-2])

    @property
    def date_time(self):
        if self._status == '':
            self._status = 'Match yet to begin'
            return None
        if 'live' not in self._status and 'result' not in self._status and 'stumps' not in self._status:
            time = datetime.strptime(self._status.split(', ')[-1].upper(), "%I:%M %p")
            time = time_set(time, "%I:%M %p")
            return ', '.join(self._status.split(', ')[:-1]).title() + ", " + time[:-5]+ f"{int(int(time[-5:-3]) - 23)} {time[-2:]}"
        return self._status if self._status.lower() == 'live' or self._status.lower() == 'stumps' else None

    @property
    def progress(self):
        return self._progress

    @property
    def series(self):
        return self._description[-1]

    @property
    def teams(self):
        return {'team1': {
            'name': self._teams[0].lower(),
            'icon': self._icons[0],
            'score': self._overs[0] + ' ' + self._scores[0]
            },
            'team2': {
            'name': self._teams[1].lower(),
            'icon': self._icons[1],
            'score': self._overs[1] + ' ' + self._scores[1]
            }}


def stopwatch(coro: Coroutine):
    @wraps(coro)
    async def wrapper(*args, **kwargs):
        now = datetime.now()
        await coro(*args, **kwargs)
        later = datetime.now()
        diff = round((later-now).total_seconds()*1000, 3)
        print(str(diff)+' ms') if diff > 0 else None
    return wrapper

# load = False
#
# loop = asyncio.get_event_loop()
# match = loop.run_until_complete(async_input("Load model? "))
#
# if match:
#     import nltk
#     from nltk.stem import WordNetLemmatizer
#     from tensorflow.keras.models import load_model as lm
#     import string
#     load = True
#
#     def load_model(lemmatizer: WordNetLemmatizer):
#         with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/patterns.json", "r") as f:
#             data: dict = json.load(f)
#
#         words = []
#         classes = []
#         doc_X = []
#         doc_y = []
#         for intent in data["intents"]:
#             for pattern in intent["patterns"]:
#                 tokens = nltk.word_tokenize(pattern)
#                 words.extend(tokens)
#                 doc_X.append(pattern)
#                 doc_y.append(intent["tag"])
#             if intent["tag"] not in classes:
#                 classes.append(intent["tag"])
#         words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in string.punctuation]
#         words = sorted(set(words))
#         classes = sorted(set(classes))
#
#         model = lm('C:/Users/Shlok/Desktop/chatbot-model1.h5')
#         return model, words, classes, data

