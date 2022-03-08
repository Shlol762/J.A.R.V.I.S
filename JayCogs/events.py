import asyncio
import random, datetime, json, re
import sys
import string, nltk
import disnake
import numpy as np
from . import command_log_and_err,\
    loop, Cog, Context, command, Client, Guild, Role, TextChannel,\
    Member, NotFound, Status, Activity, ActivityType, Embed, Colour, Invite,\
    Forbidden, GuildChannel, MemberConverter, CommandError, CommandNotFound,\
    CommandOnCooldown, MemberNotFound, UserNotFound, RoleNotFound, MessageNotFound,\
    ChannelNotFound, NoPrivateMessage, Message, MessageConverter, BadUnionArgument,\
    trim, forbidden_word, noswear, greetings, farewells, nou, urnotgod, timeto, Bot,\
    ThreadNotFound, train, CheckFailure, eastereggs, who_pinged, ErrorView, HTTPException,\
    stopwatch, time_set, AllowedMentions, load

severed_time = 0
connect_time = 0
chnls = [833995745690517524, 817299815900643348, 817300015176744971, 859801379996696576]
webhooks = [861660340617084968, 861660166193807430, 861660711037960243, 938268473623212053]
prev_members = []

model = None
if load:
    from nltk.stem import WordNetLemmatizer
    from . import load_model
    lemmatizer = WordNetLemmatizer()

    model, words, classes, data = load_model(lemmatizer)

    def clean_text(_text):
        _tokens = nltk.word_tokenize(_text)
        _tokens = [lemmatizer.lemmatize(word) for word in _tokens]
        return _tokens


    def bag_of_words(_text, vocab):
        _tokens = clean_text(_text)
        bow = [0] * len(vocab)
        for w in _tokens:
            for idx, word in enumerate(vocab):
                if word == w:
                    bow[idx] = 1
        return np.array(bow)


    def pred_class(_text, vocab, labels):
        bow = bag_of_words(_text, vocab)
        result = model.predict(np.array([bow]))[0]
        thresh = 0.2
        y_pred = [[idx, res] for idx, res in enumerate(result) if res > thresh]

        y_pred.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in y_pred:
            return_list.append(labels[r[0]])
        return return_list


    def get_response(intents_list, intents_json):
        tag = intents_list[0]
        list_of_intents = intents_json["intents"]
        for i in list_of_intents:
            if i["tag"] == tag:
                result = random.choice(i["responses"])
                break
        return result


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
        ch: TextChannel = self.bot.get_channel(823216455733477387)
        embed = Embed(title="Connection to discord",
                              description=f"*`Successful`*: `Confirmed`\n *`Connection at`*: `{connect_time}`",
                              colour=Colour.gold(), timestamp=datetime.datetime.utcnow())
        await ch.send(embed=embed)
        embed = Embed(title="Bot is ready",
                      description=f'`{self.bot.user.name}` is ready, Version: `{self.bot.VERSION}`\n',
                      colour=Colour.teal(), timestamp=datetime.datetime.utcnow())
        await ch.send(embed=embed)
        # try: self.birthday.start()
        # except RuntimeError: self.birthday.restart()
        # try: self.timer.start()
        # except RuntimeError: self.timer.restart()
        print(f"Connection to discord instantiation success: {datetime.datetime.now().strftime('%d %B %Y at %X:%f')}")

    @Cog.listener()
    async def on_message(self, message: Message):
        global chnls
        ctx: Context = await self.bot.get_context(message)
        channel: TextChannel = ctx.channel
        author: Member = ctx.author
        bot: Bot = ctx.bot
        with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/settings.json", 'r') as f:
            vals: dict = json.load(f)
        if re.search(r"[a-zA-Z0-9]{24}\.[a-zA-Z0-9]{6}\.[a-zA-Z0-9\-_]{27}", message.content):
            await ctx.send('none')
        if ctx.guild:
            if author == ctx.guild.owner and message.content.lower().startswith("jarvis disengage alpha lock"):
                [await channel.edit(overwrites={ctx.guild.default_role: disnake.PermissionOverwrite(send_messages=True)}) for channel in ctx.guild.text_channels]
                await ctx.send("Alpha lock disengaged")
            if re.search(r'ultron kill (<@!?749830638982529065>|j.?a.?r.?v.?i.?s.?)', message.content.lower()):
                await self.bot.wait_for('message', check=lambda m: m.author.id == 933591106950684712, timeout=2)
                await ctx.send(f'@everyone Secuirity warning! Ultron has breeched the network take cover.', allowed_mentions=AllowedMentions(everyone=False))
                await self.bot.change_presence(status=Status.idle,
                                               activity=Activity(type=ActivityType.watching,
                                                                 name=f"Ultron's movements"))
                await asyncio.sleep(1)
                await self.bot.change_presence(status=Status.online,
                                               activity=Activity(type=ActivityType.watching,
                                                                 name=f"Ultron's movements"))
                await asyncio.sleep(1)
                await self.bot.change_presence(status=Status.do_not_disturb,
                                               activity=Activity(name="Warning! Going offline"))
                await asyncio.sleep(1)
                await self.bot.change_presence(status=Status.invisible)
                await asyncio.sleep(10)
                await ctx.send(f'Systems back online...')
                await self.bot.change_presence(status=Status.dnd,
                                               activity=Activity(type=ActivityType.watching,
                                                                 name=f'people talk...    V{self.bot.VERSION}'))
                return
            await who_pinged(ctx)
            if channel.id in chnls and ctx.message.webhook_id not in webhooks:
                text: str = f"{message.content}"
                if message.reference:
                    ref: Message = await MessageConverter().convert(await bot.get_context(message),
                                                                    message.reference.jump_url)
                    text: str = f"`╔═`***`{ref.author.name}`***: {ref.content[:50]}\n{message.content}"
                ch1, ch2, ch3, ch4 = await bot.fetch_webhook(webhooks[0]), await bot.fetch_webhook(webhooks[1]), await bot.fetch_webhook(webhooks[2]), await bot.fetch_webhook(webhooks[3])
                # ch5 = await bot.fetch_webhook(webhooks[4])
                await ch1.send(content=text, username=ctx.author.name, avatar_url=ctx.author.avatar.url) if channel.id != chnls[0] else None
                await ch2.send(content=text, username=ctx.author.name, avatar_url=ctx.author.avatar.url) if channel.id != chnls[1] else None
                await ch3.send(content=text, username=ctx.author.name, avatar_url=ctx.author.avatar.url) if channel.id != chnls[2] else None
                await ch4.send(content=text, username=ctx.author.name, avatar_url=ctx.author.avatar.url) if channel.id != chnls[3] else None
                # await ch5.send(content=text, username=ctx.author.name, avatar_url=ctx.author.avatar.url) if channel.id != chnls[4] else None
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
                        if model:
                            intents = pred_class(message.content.lower(), words, classes)
                            _result = get_response(intents, data)
                            await ctx.send(_result)
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
                              colour=Colour.gold(), timestamp=datetime.datetime.utcnow())
        await ch.send(embed=embed)

    @Cog.listener()
    async def on_member_join(self, member: Member):
        if member.guild.id == 819515740490825771:
            if self.bot.MAINFRAME_MEMBERS.get(str(member.id)):
                return
            self.bot.MAINFRAME_MEMBERS[str(member.id)] = time_set(member.joined_at, '%d %b %Y at %X')
            with open('C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/mainframe_members.json', 'w') as f:
                json.dump(self.bot.MAINFRAME_MEMBERS, f, indent=3)
        channels: list[GuildChannel] = await member.guild.fetch_channels()
        try:
            for channel in channels:
                if ('hello' in channel.name or 'welcome' in channel.name or 'ello' in channel.name) and isinstance(channel, TextChannel):
                    await channel.send(f"Hello {member.name}, Welcome to {member.guild.name}.")
                    break
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
                                      invalid_comname=error.args[0][9:-14], send=False)
        elif isinstance(error, CommandOnCooldown):
            with open("C:/Users/Shlok/bot_stuff/safe_docs/command_logs.txt", "r") as f:
                lines: list[str] = f.readlines()
            if ctx.author.id == 613044385910620190: await ctx.reinvoke()
            if str(ctx.command.extras.get('number')) in ''.join(lines[-4:]) and str(ctx.author.id) in ''.join(lines[-4:]) and "Err" in ''.join(lines[-4:]):
                await ctx.reinvoke()
            else: await command_log_and_err(ctx=ctx, status='Cooldown', error=error)
        elif isinstance(error, MemberNotFound):
            await command_log_and_err(ctx=ctx, err_code="Err_a11404",
                                      text=f"The Member *`'{error.argument}'`* doesn't exist. I don't know what you're looking for.")
        elif isinstance(error, RoleNotFound):
            await command_log_and_err(ctx=ctx, err_code="Err_b20404",
                                      text=f"The Role *`'{error.argument}'`* doesn't exist. I don't know what you're looking for.")
        elif isinstance(error, MessageNotFound):
            await command_log_and_err(ctx=ctx, err_code="Err_O30404",
                                      text=f"The Message *`'{error.argument}'`* doesn't exist. I don't know what you're looking for.")
        elif isinstance(error, UserNotFound):
            await command_log_and_err(ctx=ctx, err_code="Err_40bO404",
                                      text=f"The User *`'{error.argument}'`* doesn't exist. I don't know what you're looking for.")
        elif isinstance(error, ChannelNotFound):
            await command_log_and_err(ctx=ctx, err_code="Err_50Ob404",
                                      text=f"The Channel *`'{error.argument}'`* doesn't exist. I don't know what you're looking for.")
        elif isinstance(error, CheckFailure):
            pass
        elif isinstance(error, NoPrivateMessage):
            await command_log_and_err(ctx=ctx, status='Server Only', error=error)
        elif isinstance(error, ThreadNotFound):
            await command_log_and_err(ctx, err_code='TNFi404', text=f"The Thread *`'{error.argument}'`* doesn't exist. I don't know what you're looking for.")
        elif isinstance(error, BadUnionArgument):
            if 'dcc' in ctx.command.aliases:
                await command_log_and_err(ctx, err_code="Err_000b12",
                                      text=f"That's not a channel bub.")
        else:
            import traceback, sys
            err_embed = Embed(title=f"Error! - `{ctx.command.name}`", description="", colour=Colour.red(), timestamp=datetime.datetime.utcnow()).set_footer(text="Unhandled Excpetion")
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
            "eastereggs": True,
            "suppressemb": False
        }
        with open(settings_path, "w") as f: json.dump(settings, f, indent=3)
        with open(prefix_path, "r") as f: prefixes = json.load(f)
        prefixes[str(guild.id)] = "$"
        with open(prefix_path, "w") as f: json.dump(prefixes, f, indent=3)
        await guild.text_channels[0].send("Hello. I am J.A.R.V.I.S!")


def setup(bot: Bot):
    bot.add_cog(Events(bot))
