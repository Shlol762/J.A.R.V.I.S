import asyncio
import random
import datetime
import json
import re
import sys
import string
import nltk
import discord
import logging
import numpy as np
from . import command_log_and_err,\
    loop, Cog, Context, command, Client, Guild, Role, TextChannel,\
    Member, NotFound, Status, Activity, ActivityType, Embed, Colour, Invite,\
    Forbidden, GuildChannel, MemberConverter, CommandError, CommandNotFound,\
    CommandOnCooldown, MemberNotFound, UserNotFound, RoleNotFound, MessageNotFound,\
    ChannelNotFound, NoPrivateMessage, Message, MessageConverter, BadUnionArgument,\
    trim, forbidden_word, noswear, greetings, farewells, nou, urnotgod, timeto, Bot,\
    ThreadNotFound, train, CheckFailure, eastereggs, who_pinged, ErrorView, HTTPException,\
    stopwatch, time_set, AllowedMentions, IST, Member

log = logging.getLogger(__name__)

chnls = [833995745690517524, 817299815900643348,
         817300015176744971, 859801379996696576]
webhooks = [861660340617084968, 861660166193807430,
            861660711037960243, 938268473623212053]

# model = None
# if load:
#     from nltk.stem import WordNetLemmatizer
#     from . import load_model
#     lemmatizer = WordNetLemmatizer()
#
#     model, words, classes, data = load_model(lemmatizer)
#
#     def clean_text(_text):
#         _tokens = nltk.word_tokenize(_text)
#         _tokens = [lemmatizer.lemmatize(word) for word in _tokens]
#         return _tokens
#
#     def bag_of_words(_text, vocab):
#         _tokens = clean_text(_text)
#         bow = [0] * len(vocab)
#         for w in _tokens:
#             for idx, word in enumerate(vocab):
#                 if word == w:
#                     bow[idx] = 1
#         return np.array(bow)
#
#     def pred_class(_text, vocab, labels):
#         bow = bag_of_words(_text, vocab)
#         result = model.predict(np.array([bow]))[0]
#         thresh = 0.2
#         y_pred = [[idx, res] for idx, res in enumerate(result) if res > thresh]
#
#         y_pred.sort(key=lambda x: x[1], reverse=True)
#         return_list = []
#         for r in y_pred:
#             return_list.append(labels[r[0]])
#         return return_list
#
#     def get_response(intents_list, intents_json):
#         tag = intents_list[0]
#         list_of_intents = intents_json["intents"]
#         for i in list_of_intents:
#             if i["tag"] == tag:
#                 result = random.choice(i["responses"])
#                 break
#         return result


class Events(Cog):
    connect_time = None
    severed_time = None
    status_time = None
    statuses = ['online', 'online']

    def __init__(self, bot: Bot):
        self.bot = bot
        self.name = 'events'

    async def alphalock(self, ctx: Context, mode: str = 'ENGAGE', override: str = None):
        await ctx.send("Beginning alpha lock procedure.")
        if not override:
            await ctx.send("Are you sure? This will make the permissions in all channels very messy.")
            try:
                message = await self.bot.wait_for('message', timeout=10, check=lambda msg: msg.author == ctx.author)
            except asyncio.TimeoutError:
                return await ctx.send("Request timed out. Cancelling alpha lock procedure.")
            else:
                if not re.search(r'y(e[sa]h)?', message.content.lower()):
                    return await ctx.send("Cancelling alpha lock procedure.")

        overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(
            send_messages={'ENGAGE': False, 'DISENGAGE': True}.get(mode))}
        [await channel.edit(overwrites=overwrites) for channel in ctx.guild.text_channels]
        await ctx.send(f"Alpha lock {mode.lower()}d")

    @loop(time=datetime.time(hour=18, minute=30))
    async def birthday(self):
        date = datetime.date.today().strftime("%d/%m")
        with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/birthdays_.json") as f:
            birthdays: dict = json.load(f)

        current_birthdays = birthdays.get(date, [])
        guild = self.bot.get_guild(766356666273890314)
        birthday_role = guild.get_role(874909501617238048)
        birthday_members = [str(m.id) for m in birthday_role.members]
        general: TextChannel = await self.bot.fetch_channel(821278528108494878)
        topic = re.sub(
            f"((, )?Happy birthday .+(!)$)+", '', general.topic) if general.topic else ''

        if len(birthday_role.members) != 0:
            if not all([item in current_birthdays for item in birthday_members]):
                for member in birthday_role.members:
                    try:
                        await member.remove_roles(birthday_role)
                    except HTTPException:
                        pass
            else:
                return

        for user_id in current_birthdays:
            m = await guild.fetch_member(user_id)
            await m.add_roles(birthday_role)
            if m.name not in topic:
                topic += f"Happy birthday {m.name}! "
            else:
                topic = topic.replace('!', f" {m.name}!", 1)[
                    ::-1] if '!' in topic else topic + f" {m.name}!"

        await general.edit(topic=topic)

    @loop(seconds = 0.1)
    async def print_tasks(self):
        dt_fmt_str = "%d %b %Y at %I:%M:%S:\x1b[0m\x1b[34;1m%f\x1b[0m \x1b[30;1m%p"
        log.info(f'\x1b[30;1m{datetime.datetime.now().strftime(dt_fmt_str)}\x1b[0m \x1b[35m{", ".join([task.get_name() for task in asyncio.all_tasks() if not task.done()])}\x1b[0m')

    @Cog.listener()
    async def on_ready(self):
        now = datetime.datetime.now()
        ch: TextChannel = self.bot.get_channel(823216455733477387)
        embed = Embed(title="Connection to discord",
                      description=f"*`Successful`*: `Confirmed`\n *`Connection at`*: `{self.connect_time}`",
                      colour=Colour.gold(), timestamp=now)
        embed2 = Embed(title="Bot is ready",
                       description=f'`{self.bot.user.name}` is ready, Version: `{self.bot.VERSION}`\n',
                       colour=Colour.teal(), timestamp=now)
        await ch.send(embeds=[embed, embed2])
        try:
            self.birthday.start()
        except RuntimeError:
            self.birthday.restart()
        log.info(
            f"Connection to discord instantiation success")
        # self.print_tasks.start()

    @Cog.listener()
    async def on_message(self, message: Message):
        global chnls
        ctx: Context = await self.bot.get_context(message)
        channel: TextChannel = ctx.channel
        author: Member = ctx.author
        bot: Bot = self.bot
        vals: dict = bot.SETTINGS

        if re.search(r"[a-zA-Z\d]{24}\.[a-zA-Z\d]{6}\.[a-zA-Z\d\-_]{27}", message.content):
            mg = await message.author.send(embed=Embed(title='Delta Security Warning!',
                                                       description='**Security Warning! Discord Authentication token detected.'+(' Message will be deleted to prevent'
                                                                                                                                 ' malicous attacks. To cancel deletion type: `Abort Delta security` or `ADS` within 10 seconds.**' if ctx.guild else ' *Deletion advised*.**'),
                                                       colour=Colour.red()).set_thumbnail(url='https://cdn.discordapp.com/emojis/849902617185484810.png?v=1')
                                           )
            await ctx.send(embed=mg.embeds[0], delete_after=10.0) if ctx.guild else None
            try:
                _message: Message = await bot.wait_for('message', timeout=10, check=lambda msg: msg.author == message.author)
                if not re.search(r'a(bort )?d(elta )?s(ecurity)?', _message.content.lower()):
                    await message.delete()
            except asyncio.TimeoutError:
                try:
                    await message.delete()
                except Forbidden:
                    pass
            except Forbidden:
                pass

        if ctx.guild:
            if channel.id in [874672889255821352]:
                if match := re.search(r'^\d{5}', message.content):
                    retry = True
                    limit = 2
                    while retry:
                        last_message = [message async for message in channel.history(limit=limit)][limit-1]
                        try:
                            last_message_cntnt = int(
                                re.search(r'^\d{5}', last_message.content).group())
                            retry = False
                        except AttributeError:
                            limit += 1
                            if limit > 7:
                                retry = False
                                last_message_cntnt = 0
                    if int(match.group()) - 1 == last_message_cntnt and author != last_message.author:
                        pass
                    else:
                        await message.delete()
                else:
                    await message.delete(delay=15.0)
                return
            await who_pinged(ctx)
            if (match := re.search(r"jarvis ((dis)?engage) alpha lock( --override)?",
                                   ctx.message.content.lower())) and author == ctx.guild.owner:
                await self.alphalock(ctx, match.group(1).upper(), match.group(3))
                return

            if channel.id in chnls and ctx.message.webhook_id not in webhooks:
                text: str = f"{message.content}"
                if message.reference:
                    ref: Message = await MessageConverter().convert(ctx,
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
                    if bot.user == author:
                        return
                    channel_id = str(channel.id)
                    guild_id = str(ctx.guild.id)
                    channel_config = vals.get(channel_id)
                    server_config = vals.get(guild_id)
                    options = channel_config if channel_config else server_config

                    if options["suppressemb"]:
                        await message.edit(suppress=True)

                    if options["message"]:
                        # if model:
                        #     intents = pred_class(
                        #         message.content.lower(), words, classes)
                        #     _result = get_response(intents, data)
                        #     await ctx.send(_result)
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
                            person = re.search(
                                r"<@(!)?\d+>", message_text.replace("'s", ''))
                            person: Member = await MemberConverter().convert(ctx=ctx, argument=person.group())
                            path: str = "C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/birthdays.json"
                            with open(path, 'r') as f:
                                birthdays: dict[str: str] = json.load(f)

                            if birthdays.get(str(person.id)):
                                time: datetime.datetime = datetime.datetime.strptime(
                                    birthdays[str(person.id)]+datetime.datetime.now().strftime("/%Y"), "%d/%m/%Y")
                                datending = (lambda t: {'1': 'st', '2': 'nd', '3': 'rd'}.get(
                                    str(t)[-1]) or 'th')(time.day)
                                if time < datetime.datetime.now():
                                    time: str = re.sub(" to `00:00 \d{2}/\d{2}/\d{4}`", "", time.strftime(
                                        f"""The next occurrance of . birthday is in {timeto(f'{time.day}/{time.month}/{time.year + 1}')[0]} on the `%d{datending} of %B in {time.year + 1}`"""))
                                else:
                                    time: str = re.sub(" to `00:00 \d{2}/\d{2}/\d{4}`", "", time.strftime(
                                        f"""The next occurrance of . birthday is in {timeto(f'{time.day}/{time.month}/{time.year}')[0]} on the `%d{datending} of %B in %Y`"""))
                                await ctx.reply(time.replace(".", 'your' if person.id == author.id else person.name+"'s"))
                            else:
                                await ctx.reply(f"I'm sorry but I don't think I have that birthday stored anywhere. Contact Shlol#2501 to add the birthday")
                        except AttributeError:
                            pass
                    await train(ctx)
                except TypeError:
                    pass
            if random.randint(1, 1000) == 0:
                await ctx.send(f"<@")

    @Cog.listener()
    async def on_disconnect(self):
        self.severed_time = datetime.datetime.now().strftime("%d %b %Y at %I:%M %p")
        log.warning(f"Shard {shard_id} has disconnected from gateway")

    @Cog.listener()
    async def on_connect(self):
        self.connect_time = datetime.datetime.now().strftime("%d %b %Y at %I:%M %p")

    @Cog.listener()
    async def on_resumed(self):
        now: datetime.datetime = datetime.datetime.now()
        ch: TextChannel = self.bot.get_channel(823216455733477387)
        embed = Embed(title="Re-connection to discord",
                      description=f"*`Successful`*: `Confirmed`\n *`Last disconnect`*: `{self.severed_time}`\n*`Re-connection at`*: `{now.strftime('%d %b %Y at %I:%M %p')}`",
                      colour=Colour.gold(), timestamp=now)
        await ch.send(embed=embed)

    @Cog.listener()
    async def on_member_join(self, member: Member):
        if member.guild.id == 819515740490825771:
            if self.bot.MAINFRAME_MEMBERS.get(str(member.id)):
                return
            self.bot.MAINFRAME_MEMBERS[str(member.id)] = time_set(
                member.joined_at, '%d %b %Y at %X')
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
            if ctx.author.id == 613044385910620190:
                await ctx.reinvoke()
            if str(ctx.command.extras.get('number')) in ''.join(lines[-4:]) and str(ctx.author.id) in ''.join(lines[-4:]) and "Err" in ''.join(lines[-4:]):
                await ctx.reinvoke()
            else:
                await command_log_and_err(ctx=ctx, status='Cooldown', error=error)
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
            import traceback
            import sys
            err_embed = Embed(title=f"Error! - `{ctx.command.name}`", description="", colour=Colour.red(
            ), timestamp=datetime.datetime.utcnow()).set_footer(text="Unhandled Excpetion")
            lines = f'\nIgnoring exception in on_command_error:\n' + ''.join(
                traceback.format_exception(error.__class__, error, error.__traceback__))

            err_embed.description = f"""

`Author`: {ctx.author.mention}
`Channel`: {ctx.channel.mention if isinstance(ctx.channel, TextChannel) else 'DM'}

[```nim
{lines[:3900]}
```]({ctx.message.jump_url})
**Check Command Prompt**
"""
            view = ErrorView(ctx, 20, embed=err_embed)
            try:
                view.message = await ctx.reply("Whoops! Something went wrong...", view=view)
            except HTTPException:
                pass
            error_channel: TextChannel = ctx.bot.get_channel(
                868640456328744960)
            await error_channel.send(embed=err_embed)
            log.error(f"\x1b[31;1m{lines}")

    @Cog.listener()
    async def on_command_completion(self, ctx: Context):
        pass

    @Cog.listener()
    async def on_guild_join(self, guild: Guild):
        settings_path = "C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/settings.json"
        prefix_path = "C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/prefixes.json"
        with open(settings_path, "r") as f:
            settings = json.load(f)
        settings[str(guild.id)] = {
            "ban": True,
            "kick": True,
            "clear": True,
            "impersonate": True,
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
        with open(settings_path, "w") as f:
            json.dump(settings, f, indent=3)
        with open(prefix_path, "r") as f:
            prefixes = json.load(f)
        prefixes[str(guild.id)] = "$"
        with open(prefix_path, "w") as f:
            json.dump(prefixes, f, indent=3)
        await guild.text_channels[0].send("Hello. I am J.A.R.V.I.S!")

    @Cog.listener()
    async def on_presence_update(self, before, after):
        watch_ids = [613044385910620190,
                     728917592160469022, 809295130213089320]

        t = self.status_time
        n = datetime.datetime.now()
        if (t.second if t else None) == n.second:
            return

        self.status_time = n

        if before.status == after.status or before.id not in watch_ids:
            return

        current_status = 'online' if str(after.status) in [
            'dnd', 'online', 'idle'] else 'offline'

       # if before.id == watch_ids[2] and current_status != self.statuses[1]:
       #    await (await self.bot.fetch_user(watch_ids[1])).send(f"{before.mention} is now {after.status}.")
       #    self.statuses[1] = current_status

       # if before.id == watch_ids[1] and current_status != self.statuses[0]:
       #     await (await self.bot.fetch_user(watch_ids[2])).send(f"{before.mention} is now {after.status}.")
       #     self.statuses[0] = current_status


async def setup(bot: Bot):
    await bot.add_cog(Events(bot))
