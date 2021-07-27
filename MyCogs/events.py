import random, datetime, discord, json, re
from . import hypesquad_emoji, command_log_and_err, set_timestamp,\
    version, loop, Cog, Context, command, Client, Guild, Role, TextChannel,\
    Member, NotFound, Status, Activity, ActivityType, Embed, Colour, Invite,\
    Forbidden, GuildChannel, MemberConverter, CommandError, CommandNotFound,\
    CommandOnCooldown, MemberNotFound, UserNotFound, RoleNotFound, MessageNotFound,\
    ChannelNotFound, NoPrivateMessage, Message, MessageConverter,\
    trim, forbidden_word, noswear, greetings, farewells, nou, urnotgod, timeto, Bot

severed_time = 0
connect_time = 0
chnls = [833995745690517524, 817299815900643348, 817300015176744971, 859801379996696576]
webhooks = [861660340617084968, 861660166193807430, 861660711037960243, 861660517746999356]
prev_messages = []
members = {}

class Events(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.name = 'None'

    @loop(minutes=5)
    async def birthday(self):
        global members
        guild: Guild = await self.bot.fetch_guild(766356666273890314)
        birthday_role: Role = guild.get_role(774876349163765780)
        general: TextChannel = self.bot.get_channel(821278528108494878)
        now = datetime.datetime.now().strftime("%d/%m")
        f = open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/birthdays.json")
        birthdays: dict = json.load(f)
        f.close()
        for prev_bday_person in members.keys():
            prev_bday_person: Member = prev_bday_person
            if now != members.get(prev_bday_person):
                await prev_bday_person.remove_roles(birthday_role)
                await general.edit(topic=None)
        for member, date in birthdays.items():
            try: bday_persona: Member = await guild.fetch_member(int(member))
            except NotFound: pass
            if now == date:
                members[bday_persona] = now
            else:
                try: members.pop(bday_persona)
                except (ValueError, KeyError): pass
        topic = ''
        for bday_persona in members:
            if birthday_role not in bday_persona.roles:
                await bday_persona.add_roles(birthday_role)
                topic += f'Happy Birthday {bday_persona.name}! '
        await general.edit(topic=topic) if birthday_role not in bday_persona.roles else None

    @Cog.listener()
    async def on_ready(self):
        global connect_time
        await self.bot.change_presence(status=Status.do_not_disturb,
                                       activity=Activity(type=ActivityType.watching,
                                                                    name=f'people talk...    V{version}'))
        ch: TextChannel = self.bot.get_channel(823216455733477387)
        embed = Embed(title="Connection to discord",
                              description=f"*`Successful`*: `Confirmed`\n *`Connection at`*: `{connect_time}`",
                              colour=Colour.gold())
        await ch.send(embed=await set_timestamp(embed, ""))
        embed = Embed(title="Bot is ready",
                      description=f'`{self.bot.user.name}` is ready, Version: `{version}`\n',
                      colour=Colour.teal())
        await ch.send(embed=await set_timestamp(embed, ""))
        url: str = 'https://discord.com/api/oauth2/authorize?client_id=749830638982529065&permissions=8&scope=bot%20applications.commands'
        string: str = f"""
        [`{self.bot.user.name}`]({url}) - Version - `{version}`
        """
        embed = Embed(title=f"Build info - {self.bot.user}", description=string, colour=Colour.random())
        embed.set_footer(text="At your service!", icon_url=(await hypesquad_emoji(self.bot, "Staff")).url)
        ch: TextChannel = self.bot.get_channel(
            840478960478847006)
        msg: Message = await ch.fetch_message(840639817293496330)
        await msg.edit(embed=embed)
        # py_url = "https://www.python.org/downloads/"
        # py_url1 = "https://docs.python.org/3/"
        # url_d = 'https://pypi.org/project/discord.py/'
        # url_d1 = f'https://discordpy.readthedocs.io/en/v{discord.__version__}/'
        # url_w = 'https://pypi.org/project/wikipedia/'
        # url_w1 = f'https://wikipedia.readthedocs.io/en/stable/'
        # url_pd = 'https://pypi.org/project/PyDictionary/'
        # url_pd1 = f'https://pypi.org/project/PyDictionary/'
        # url_bs = 'https://pypi.org/project/beautifulsoup4/'
        # url_bs1 = f'https://www.crummy.com/software/BeautifulSoup/bs4/doc/'
        # url_py = 'https://pypi.org/project/pytz/'
        # url_py1 = f'https://pypi.org/project/pytz/'
        # url_req = 'https://pypi.org/project/requests/'
        # url_req1 = f'https://docs.python-requests.org/en/master/'
        # url_yt = 'https://pypi.org/project/youtube_dl/'
        # url_yt1 = f'https://pypi.org/project/youtube_dl/'
        # url_pil = 'https://pypi.org/project/Pillow/'
        # url_pil1 = f'https://pillow.readthedocs.io/en/stable/'
        # url_os = 'https://www.geeksforgeeks.org/os-module-python-examples/#:~:text=The%20OS%20module%20in%20Python,interact%20with%20the%20file%20system.'
        # url_os1 = f'https://docs.python.org/3/library/os.html'
        # url_tp = 'https://docs.python.org/3/library/typing.html'
        # url_tp1 = f'https://docs.python.org/3/library/typing.html'
        # url_dt = 'https://docs.python.org/3/library/datetime.html'
        # url_dt1 = f'https://docs.python.org/3/library/datetime.html'
        # url_re = 'https://docs.python.org/3/library/re.html'
        # url_re1 = f'https://docs.python.org/3/library/re.html'
        # url_rd = 'https://docs.python.org/3/library/random.html'
        # url_rd1 = f'https://docs.python.org/3/library/random.html'
        # url_ma = 'https://docs.python.org/3/library/math.html'
        # url_ma1 = f'https://docs.python.org/3/library/math.html'
        # url_it = 'https://docs.python.org/3/library/itertools.html'
        # url_it1 = f'https://docs.python.org/3/library/itertools.html'
        # url_ft = 'https://docs.python.org/3/library/functools.html'
        # url_ft1 = f'https://docs.python.org/3/library/functools.html'
        # url_at = 'https://pypi.org/project/async-timeout/'
        # url_at1 = f'https://pypi.org/project/async-timeout/'
        # url_as = 'https://docs.python.org/3/library/asyncio.html'
        # url_as1 = f'https://docs.python.org/3/library/asyncio.html'
        # str_web = f"""
        # [**Python**]({py_url}) - [**3.9.5**]({py_url1}) web resources
        #
        # **`{"Python Package":^15}`** - **`{"Version":^15}`**\n
        # [`{"discord":^15}`]({url_d}) - [`{discord.__version__:^15}`]({url_d1})
        # [`{"wikipedia":^15}`]({url_w}) - [`{wikipedia.__version__:^15}`]({url_w1})
        # [`{"pydictionary":^15}`]({url_pd}) - [`{PyDictionary.__version__:^15}`]({url_pd1})
        # [`{"bs4":^15}`]({url_bs}) - [`{bs4.__version__:^15}`]({url_bs1})
        # [`{"pytz":^15}`]({url_py}) - [`{__version__:^15}`]({url_py1})
        # [`{"requests":^15}`]({url_req}) - [`{requests.__version__:^15}`]({url_req1})
        # [`{"youtube_dl":^15}`]({url_yt}) - [`{youtube_dl.version.__version__:^15}`]({url_yt1})
        # [`{"pillow":^15}`]({url_pil}) - [`{PIL.__version__:^15}`]({url_pil1})
        # [`{"async-timeout":^15}`]({url_at}) - [`{async_timeout.__version__:^15}`]({url_at1})
        # """
        # emb1 = discord.Embed(title="Build resources", description=str_web, color=discord.Colour.random())
        # local_str = f"""
        # [**Python**]({py_url}) - [**3.9.5**]({py_url1}) local resources
        #
        # [`{"os":^15}`]({url_os}) - [`{"Builtin":^15}`]({url_os1})
        # [`{"typing":^15}`]({url_tp}) - [`{"Builtin":^15}`]({url_tp1})
        # [`{"datetime":^15}`]({url_dt}) - [`{"Builtin":^15}`]({url_dt1})
        # [`{"re":^15}`]({url_re}) - [`{"Builtin":^15}`]({url_re1})
        # [`{"random":^15}`]({url_rd}) - [`{"Builtin":^15}`]({url_rd1})
        # [`{"asyncio":^15}`]({url_as}) - [`{"Builtin":^15}`]({url_as1})
        # [`{"math":^15}`]({url_ma}) - [`{"Builtin":^15}`]({url_ma1})
        # [`{"itertools":^15}`]({url_it}) - [`{"Builtin":^15}`]({url_it1})
        # [`{"functools":^15}`]({url_ft}) - [`{"Builtin":^15}`]({url_ft1})
        # """
        # last_str = """
        # [`Jump to Custom funtions`]()
        # """
        # embed = discord.Embed(description=local_str, colour=discord.Colour.random())
        # emb2.set_footer(icon_url=(await hypesquad_emoji("Staff")).url)
        # await self.bot.get_channel(840478960478847006).send(embed=emb1)
        # await self.bot.get_channel(840478960478847006).send(embed=embed)
        try: self.birthday.start()
        except RuntimeError: self.birthday.restart()
        print("Confirmed")

    @Cog.listener()
    async def on_message(self, message: Message):
        global chnls
        global prev_messages
        ctx: Context = await self.bot.get_context(message)
        channel: TextChannel = ctx.channel
        author: Member = ctx.author
        bot: Bot = ctx.bot
        with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/settings.json", 'r') as f:
            vals: dict = json.load(f)
        if ctx.guild:
            if bot.user.mentioned_in(message)\
                    and not ctx.command and not\
                    re.search(r"(@everyone|@here)", message.content.lower()) \
                    and ctx.author != bot.user\
                    and ctx.message.webhook_id not in webhooks\
                    and not ctx.message.reference: await ctx.reply("What can I do for ya?")
            if channel.id in chnls and ctx.message.webhook_id not in webhooks:
                text: str = f"{message.content}"
                if message.reference:
                    ref: Message = await MessageConverter().convert(await bot.get_context(message),
                                                                    message.reference.jump_url)
                    text: str = f"`╔═`***`{ref.author.name}`***: {ref.content[:50]}\n{message.content}"
                ch1, ch2, ch3, ch4 = await bot.fetch_webhook(webhooks[0]), await bot.fetch_webhook(webhooks[1]), await bot.fetch_webhook(webhooks[2]), await bot.fetch_webhook(webhooks[3])
                await ch1.send(content=text, username=ctx.author.name, avatar_url=ctx.author.avatar_url) if channel.id != chnls[0] else None
                await ch2.send(content=text, username=ctx.author.name, avatar_url=ctx.author.avatar_url) if channel.id != chnls[1] else None
                await ch3.send(content=text, username=ctx.author.name, avatar_url=ctx.author.avatar_url) if channel.id != chnls[2] else None
                await ch4.send(content=text, username=ctx.author.name, avatar_url=ctx.author.avatar_url) if channel.id != chnls[3] else None
            else:
                try:
                    channel_id: str = str(channel.id)
                    guild_id: str = str(ctx.guild.id)
                    channel_config = vals.get(channel_id)
                    server_config = vals.get(guild_id)
                    if channel_config: options = channel_config
                    else: options = server_config
                    if options["message"]:
                        if options["msghai"]:
                            await forbidden_word(ctx)
                        if options["noswear"]:
                            await noswear(ctx)
                        if options["convo"]:
                            if options["greetings"]:
                                await greetings(ctx)
                            elif options['farewells']:
                                await farewells(ctx)
                            if options['nou']:
                                await nou(ctx)
                            if options['iamgod']:
                                await urnotgod(ctx)
                    message_text: str = re.sub(r"when(s|'s| is)?", "when", message.content.lower()).replace("my", author.mention).replace('your', bot.user.name).replace(
                        "birthday", "bday").replace("i", author.mention)
                    if re.search(r"\b(when (is )?(the next occurrance of |will)?((.)+ (next )?bday)| the day (.)+ was born)", message_text.lower()):
                        try:
                            person = re.search(r"<@(!)?[0-9]+>", message_text.replace("'s", ''))
                            person: Member = await MemberConverter().convert(ctx=ctx, argument=person.group())
                            path: str = "C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/birthdays.json"
                            f = open(path, 'r')
                            birthdays: dict[str: str] = json.load(f)
                            f.close()
                            if birthdays.get(str(person.id)):
                                time: datetime.datetime = datetime.datetime.strptime(birthdays[str(person.id)]+datetime.datetime.now().strftime("/%Y"), "%d/%m/%Y")
                                if time < datetime.datetime.now():
                                    time: str = re.sub(" to `00:00 [0-9]{2}/[0-9]{2}/[0-9]{4}`", "", time.strftime(f"""The next occurrance of {'your' if person.id == author.id else person.name+"'s"} birthday is in {timeto(f'{time.day}/{time.month}/{time.year + 1}')} on the `%dth of %B in {time.year + 1}`"""))
                                else:
                                    time: str = re.sub(" to `00:00 [0-9]{2}/[0-9]{2}/[0-9]{4}`", "", time.strftime(f"""The next occurrance of {'your' if person.id == author.id else person.name+"'s"} birthday is in {timeto(f'{time.day}/{time.month}/{time.year}')} on the `%dth of %B in %Y`"""))
                                await ctx.reply(time)
                            else:
                                await ctx.reply(f"I'm sorry but I don't think I have that birthday stored anywhere. Contact Shlol#2501 to add the birthday")
                        except AttributeError: pass
                except TypeError: print(ctx.message.content)

    @Cog.listener()
    async def on_disconnect(self):
        global severed_time
        severed_time = datetime.datetime.now().strftime("%d %b %Y at %I:%M %p")

    @Cog.listener()
    async def on_connect(self):
        global connect_time
        connect_time = datetime.datetime.now().strftime("%d %b %Y at %I:%M %p")

    @Cog.listener()
    async def on_resumed(self):
        global severed_time
        time: datetime.datetime = datetime.datetime.now().strftime("%d %b %Y at %I:%M %p")
        ch: TextChannel = self.bot.get_channel(823216455733477387)
        embed = Embed(title="Re-connection to discord",
                              description=f"*`Successful`*: `Confirmed`\n *`Last disconnect`*: `{severed_time}`\n*`Re-connection at`*: `{time}`",
                              colour=Colour.gold())
        await ch.send(embed=await set_timestamp(embed, ""))

    @Cog.listener()
    async def on_member_join(self, member: Member):
        channels: list[GuildChannel] = await member.guild.fetch_channels()
        try:
            for channel in channels:
                if ('hello' in channel.name or 'welcome' in channel.name or 'ello' in channel.name) and isinstance(channel, TextChannel):
                    await channel.send(f"Hello {member.name}, Welcome to {member.guild.name}.")
        except Forbidden:
            pass

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        try:
            channels: list[GuildChannel] = await member.guild.fetch_channels()
            for channel in channels:
                if 'goodbyes' in channel.name or 'ba-bye' in channel.name or 'bye' in channel.name:
                    await channel.send(f"Bye {member.name}, come back soon!.")
        except Forbidden:
            pass

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
        if isinstance(error, CommandNotFound):
            await command_log_and_err(ctx=ctx, err_code="Err_A113",
                                      text=f"Command not found {ctx.author.mention}",
                                      invalid_comname=error.args[0][9:-14])
        elif isinstance(error, CommandOnCooldown):
            with open("C:/Users/Shlok/bot_stuff/command_logs.txt", "r") as f:
                lines: list[str] = f.readlines()
            if ctx.author.id == 613044385910620190: await ctx.reinvoke()
            elif ctx.command.brief[1:] in lines[-1] and str(ctx.author.id) in lines[-1] and "Err" in lines[-1]:
                await ctx.reinvoke()
            else: await command_log_and_err(ctx=ctx, status='Cooldown', error=error)
        elif isinstance(error, MemberNotFound):
            await command_log_and_err(ctx=ctx, err_code="Err_α11404",
                                      text=f"**`The Member:`**` `*`'{error.argument}'`*` doesn't exist` I don't know what you're looking for.")
        elif isinstance(error, RoleNotFound):
            await command_log_and_err(ctx=ctx, err_code="Err_β20404",
                                      text=f"**`The Role:`**` `*`'{error.argument}'`*` doesn't exist` I don't know what you're looking for.")
        elif isinstance(error, MessageNotFound):
            await command_log_and_err(ctx=ctx, err_code="Err_θ30404",
                                      text=f"**`The Message:`**` `*`'{error.argument}'`*` doesn't exist` I don't know what you're looking for.")
        elif isinstance(error, UserNotFound):
            await command_log_and_err(ctx=ctx, err_code="Err_40βθ404",
                                      text=f"**`The User:`**` `*`'{error.argument}'`*` doesn't exist` I don't know what you're looking for.")
        elif isinstance(error, ChannelNotFound):
            await command_log_and_err(ctx=ctx, err_code="Err_50θβ404",
                                      text=f"**`The Channel:`**` `*`'{error.argument}'`*` doesn't exist` I don't know what you're looking for.")
        elif isinstance(error, NoPrivateMessage):
            await command_log_and_err(ctx=ctx, status='Server Only', error=error)
        else:
            err_embed = await set_timestamp(Embed(title=f"Error! - `{ctx.command.name}`", description="", colour=Colour.red()), "Unhandled Excpetion")
            err_embed.description = f"""
```py
{error.with_traceback(error.__traceback__)}
```
**Check Command Prompt**
"""
            error_channel: TextChannel = ctx.bot.get_channel(868640456328744960)
            await error_channel.send(embed=err_embed)
            raise error

    @Cog.listener()
    async def on_command_completion(self, ctx: Context):
        path: str = "C:/Users/Shlok/J.A.R.V.I.SV2021/text_files/command_logs.txt"
        f = open(path, "r")
        lines: list[str] = f.readlines()
        new_lines: list = []
        f.close()
        f = open(path, "w")
        if ctx.command.brief and len(ctx.command.brief) >= 3:
            if ctx.command.brief[1:] in "".join(lines):
                for line in lines:
                    if ctx.command.brief[1:] in line:
                        times_used: int = int(line.split(":")[1].strip()) + 1
                        next: str = f"{line.split(':')[0]}: {times_used}\n"
                        new_lines.append(next)
                    else:
                        new_lines.append(line)
                f.write("".join(new_lines))
                f.close()
            else:
                lines.append(f"{ctx.command.brief[1:]}: 1\n")
                f.write("".join(lines))
                f.close()

    @Cog.listener()
    async def on_guild_join(self, guild: Guild):
        settings_path = "C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/settings.json"
        prefix_path = "C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/prefixes.json"
        with open(settings_path, "r") as f: settings = json.load(f)
        settings[str(guild.id)] = {
            "ban": True,
            "kick": True,
            "clear": True,
            "message": True,
            "msghai": True,
            "noswear": True,
            "convo": True,
            "nou": True,
            "greetings": True,
            "farewells": True,
            "iamgod": True
        }
        with open(settings_path, "w") as f: json.dump(settings, f, indent=3)
        with open(prefix_path, "r") as f: prefixes = json.load(f)
        prefixes[str(guild.id)] = "$"
        with open(prefix_path, "w") as f: json.dump(prefixes, f, indent=3)
        await guild.text_channels[0].send("Hello. I am J.A.R.V.I.S!")


def setup(bot: Bot):
    bot.add_cog(Events(bot))
