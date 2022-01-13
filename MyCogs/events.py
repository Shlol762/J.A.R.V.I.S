import asyncio
import random, datetime, json, re
import sys

from . import hypesquad_emoji, command_log_and_err, set_timestamp,\
    VERSION, loop, Cog, Context, command, Client, Guild, Role, TextChannel,\
    Member, NotFound, Status, Activity, ActivityType, Embed, Colour, Invite,\
    Forbidden, GuildChannel, MemberConverter, CommandError, CommandNotFound,\
    CommandOnCooldown, MemberNotFound, UserNotFound, RoleNotFound, MessageNotFound,\
    ChannelNotFound, NoPrivateMessage, Message, MessageConverter, BadUnionArgument,\
    trim, forbidden_word, noswear, greetings, farewells, nou, urnotgod, timeto, Bot,\
    ThreadNotFound, train, CheckFailure, eastereggs, who_pinged, ErrorView, HTTPException,\
    stopwatch

severed_time = 0
connect_time = 0
chnls = [833995745690517524, 817299815900643348, 817300015176744971, 859801379996696576, 880314505740046336]
webhooks = [861660340617084968, 861660166193807430, 861660711037960243, 861660517746999356, 880318607643521075]
prev_members = []


class Events(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.name = 'events'

    @loop(seconds=30.0)
    @stopwatch
    async def birthday(self):
        global prev_members
        now_ = datetime.datetime.now()
        nxt_day = now_.day + 1

        if (datetime.datetime(now_.year, now_.month, nxt_day) - now_).total_seconds() > 30:
            del nxt_day
            return

        del nxt_day
        date = now_.strftime("%d/%m")
        del now_

        with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/birthdays_.json") as f:
            birthdays: dict = json.load(f)

        current_birthdays = birthdays.get(date)
        guild = self.bot.get_guild(766356666273890314)
        birthday_role = guild.get_role(874909501617238048)
        general: TextChannel = await guild.fetch_channel(821278528108494878)

        if len(birthday_role.members) != 0:
            if [str(m.id) for m in birthday_role.members] != current_birthdays:
                for member in birthday_role.members:
                    try: await member.remove_roles(birthday_role)
                    except HTTPException: pass
                await general.edit(topic=None)
            else:
                return

        if date not in birthdays.keys():
            del date, birthdays
            return

        topic = ''
        for user_id in current_birthdays:
            m = await guild.fetch_member(user_id)
            await m.add_roles(birthday_role)
            if 'Happy' not in topic:
                topic += f"Happy birthday {m.name}!"
            else:
                topic = topic.replace('!', f", {m.name}!")

        await general.edit(topic = topic)

    @loop(minutes=5)
    async def timer(self):
        timchnl: TextChannel = await self.bot.fetch_channel(821278528108494878)
        tstr, now, till = timeto("00:00 1/1/2022")
        if now > till:
            print(tstr)
            try: time_ = re.search(r"(([0-9]+ days? )?([0-9]+ hrs? )?[0-9]+ mins?)", tstr).group(0)
            except AttributeError: time_ = timchnl.topic
            await asyncio.sleep(10)
            time_ = "T-Minus " + time_ + " and counting"
            await timchnl.edit(topic=time_)

    @Cog.listener()
    async def on_ready(self):
        global connect_time
        await self.bot.change_presence(status=Status.do_not_disturb,
                                       activity=Activity(type=ActivityType.watching,
                                                         name=f'people talk...    V{VERSION}'))
        ch: TextChannel = self.bot.get_channel(823216455733477387)
        embed = Embed(title="Connection to discord",
                              description=f"*`Successful`*: `Confirmed`\n *`Connection at`*: `{connect_time}`",
                              colour=Colour.gold())
        await ch.send(embed=await set_timestamp(embed, ""))
        embed = Embed(title="Bot is ready",
                      description=f'`{self.bot.user.name}` is ready, Version: `{VERSION}`\n',
                      colour=Colour.teal())
        await ch.send(embed=await set_timestamp(embed, ""))
        try: self.birthday.start()
        except RuntimeError: self.birthday.restart()
        # try: self.timer.start()
        # except RuntimeError: self.timer.restart()
        print(f"Connection to discord instantiation success: {datetime.datetime.now().strftime('%d %B %Y at %X:%f')}")

    @Cog.listener()
    async def on_message(self, message: Message):
        global chnls
        ctx: Context = await self.bot.get_context(message)
        # if ctx.guild.id in black_list:
        #     await ctx.guild.leave()
        channel: TextChannel = ctx.channel
        author: Member = ctx.author
        bot: Bot = ctx.bot
        with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/settings.json", 'r') as f:
            vals: dict = json.load(f)
        if ctx.guild:
            await who_pinged(ctx)
            if channel.id in chnls and ctx.message.webhook_id not in webhooks:
                text: str = f"{message.content}"
                if message.reference:
                    ref: Message = await MessageConverter().convert(await bot.get_context(message),
                                                                    message.reference.jump_url)
                    text: str = f"`╔═`***`{ref.author.name}`***: {ref.content[:50]}\n{message.content}"
                ch1, ch2, ch3, ch4, ch5 = await bot.fetch_webhook(webhooks[0]), await bot.fetch_webhook(webhooks[1]), await bot.fetch_webhook(webhooks[2]), await bot.fetch_webhook(webhooks[3]),\
                    await bot.fetch_webhook(webhooks[4])
                await ch1.send(content=text, username=ctx.author.name, avatar_url=ctx.author.avatar.url) if channel.id != chnls[0] else None
                await ch2.send(content=text, username=ctx.author.name, avatar_url=ctx.author.avatar.url) if channel.id != chnls[1] else None
                await ch3.send(content=text, username=ctx.author.name, avatar_url=ctx.author.avatar.url) if channel.id != chnls[2] else None
                await ch4.send(content=text, username=ctx.author.name, avatar_url=ctx.author.avatar.url) if channel.id != chnls[3] else None
                await ch5.send(content=text, username=ctx.author.name, avatar_url=ctx.author.avatar.url) if channel.id != chnls[4] else None
            else:
                try:
                    if bot.user == author: return
                    channel_id: str = str(channel.id)
                    guild_id: str = str(ctx.guild.id)
                    channel_config = vals.get(channel_id)
                    server_config = vals.get(guild_id)
                    if channel_config: options = channel_config
                    else: options = server_config
                    if options["suppressemb"]:
                        await message.edit(suppress=True)
                    if options["message"]:
                        if options["msghai"]:
                            await forbidden_word(ctx)
                        if options["noswear"]:
                            await noswear(ctx)
                        if options["convo"]:
                            if options['eastereggs']:
                                await eastereggs(ctx)
                            elif options["greetings"]:
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
                                datending = (lambda t: {'1': 'st', '2': 'nd', '3': 'rd'}.get(str(t)[-1]) or 'th')(time.day)
                                if time < datetime.datetime.now():
                                    time: str = re.sub(" to `00:00 [0-9]{2}/[0-9]{2}/[0-9]{4}`", "", time.strftime(f"""The next occurrance of . birthday is in {timeto(f'{time.day}/{time.month}/{time.year + 1}')[0]} on the `%d{datending} of %B in {time.year + 1}`"""))
                                else:
                                    time: str = re.sub(" to `00:00 [0-9]{2}/[0-9]{2}/[0-9]{4}`", "", time.strftime(f"""The next occurrance of . birthday is in {timeto(f'{time.day}/{time.month}/{time.year}')[0]} on the `%d{datending} of %B in %Y`"""))
                                await ctx.reply(time.replace(".", 'your' if person.id == author.id else person.name+"'s"))
                            else:
                                await ctx.reply(f"I'm sorry but I don't think I have that birthday stored anywhere. Contact Shlol#2501 to add the birthday")
                        except AttributeError: pass
                    await train(ctx)
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
            with open("C:/Users/Shlok/bot_stuff/safe_docs/command_logs.txt", "r") as f:
                lines: list[str] = f.readlines()
            if ctx.author.id == 613044385910620190: await ctx.reinvoke()
            elif str(ctx.command.extras.get('number')) in ''.join(lines[-4:]) and str(ctx.author.id) in ''.join(lines[-4:]) and "Err" in ''.join(lines[-4:]):
                await ctx.reinvoke()
            else: await command_log_and_err(ctx=ctx, status='Cooldown', error=error)
        elif isinstance(error, MemberNotFound):
            await command_log_and_err(ctx=ctx, err_code="Err_a11404",
                                      text=f"**`The Member:`**` `*`'{error.argument}'`*` doesn't exist` I don't know what you're looking for.")
        elif isinstance(error, RoleNotFound):
            await command_log_and_err(ctx=ctx, err_code="Err_b20404",
                                      text=f"**`The Role:`**` `*`'{error.argument}'`*` doesn't exist` I don't know what you're looking for.")
        elif isinstance(error, MessageNotFound):
            await command_log_and_err(ctx=ctx, err_code="Err_O30404",
                                      text=f"**`The Message:`**` `*`'{error.argument}'`*` doesn't exist` I don't know what you're looking for.")
        elif isinstance(error, UserNotFound):
            await command_log_and_err(ctx=ctx, err_code="Err_40bO404",
                                      text=f"**`The User:`**` `*`'{error.argument}'`*` doesn't exist` I don't know what you're looking for.")
        elif isinstance(error, ChannelNotFound):
            await command_log_and_err(ctx=ctx, err_code="Err_50Ob404",
                                      text=f"**`The Channel:`**` `*`'{error.argument}'`*` doesn't exist` I don't know what you're looking for.")
        elif isinstance(error, CheckFailure):
            pass
        elif isinstance(error, NoPrivateMessage):
            await command_log_and_err(ctx=ctx, status='Server Only', error=error)
        elif isinstance(error, ThreadNotFound):
            await command_log_and_err(ctx, err_code='TNFi404', text=f"**`The Thread:`**` `*`'{error.argument}'`*` doesn't exist` I don't know what you're looking for.")
        elif isinstance(error, BadUnionArgument):
            await command_log_and_err(ctx, err_code="Err_000b12",
                                      text=f"There is no channel called {error.param}")
        else:
            import traceback, sys
            err_embed = await set_timestamp(Embed(title=f"Error! - `{ctx.command.name}`", description="", colour=Colour.red()), "Unhandled Excpetion")
            lines = f'\nIgnoring exception in on_command_error:\n' + ''.join(
                traceback.format_exception(error.__class__, error, error.__traceback__))

            err_embed.description = f"""

`Author`: {ctx.author.mention}
`Channel`: {ctx.channel.mention}

[```nim
{lines[:3900]}
```]({ctx.message.jump_url})
**Check Command Prompt**
"""
            view = ErrorView(ctx, 20, embed=err_embed)
            try: view.message = await ctx.reply("Whoops! Something went wrong...", view=view)
            except HTTPException: pass
            error_channel: TextChannel = ctx.bot.get_channel(868640456328744960)
            await error_channel.send(embed=err_embed)
            print(lines, file=sys.stderr)

    @Cog.listener()
    async def on_command_completion(self, ctx: Context):
        pass

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
            "iamgod": True,
            "eastereggs": True
        }
        with open(settings_path, "w") as f: json.dump(settings, f, indent=3)
        with open(prefix_path, "r") as f: prefixes = json.load(f)
        prefixes[str(guild.id)] = "$"
        with open(prefix_path, "w") as f: json.dump(prefixes, f, indent=3)
        await guild.text_channels[0].send("Hello. I am J.A.R.V.I.S!")


def setup(bot: Bot):
    bot.add_cog(Events(bot))
