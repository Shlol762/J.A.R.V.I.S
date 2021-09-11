import datetime
import json

import discord
from discord.ext import commands
from typing import Optional, Union
from MyCogs import VERSION, command_log_and_err,\
    set_timestamp, time_set, hypesquad_emoji, Cog,\
    Bot, command, guild_only, cooldown, Context, BucketType,\
    Embed, Colour, Member, Forbidden, CustomActivity, Spotify,\
    Game, Activity, ActivityType, Status, HTTPException, User,\
    comm_log_local, UserConverter


bot_ver = VERSION


class Utilities(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.description = 'Commands that can be used as tools.'
        self.name = 'Utilities'

    # 301
    @command(name="Clear", aliases=['cl'],
                      help='Deletes any number of messages below 20.',
                      usage="clear|cl (amt of msgs to be deleted)",
                      extras={'emoji': '♻', 'number': '301'})
    @cooldown(1, 30, BucketType.member)
    @guild_only()
    @comm_log_local
    async def _clear(self, ctx: Context, amount: Optional[int] = 1):
        default_clear_amt = amount + 1
        author = ctx.message.author
        guild_id = str(ctx.guild.id)
        channel_id = str(ctx.message.channel.id)
        with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/settings.json", "r") as f:
            settings: dict = json.load(f)
        id: str = channel_id if settings.get(channel_id) else guild_id
        if settings[id]["clear"]:
            if amount > 20:
                await command_log_and_err(ctx, 'Amt exceeded limit'.format(amount))
                await ctx.reply(f"Sorry {author.mention}, can't clear more than 20 messages")
            else:
                try:
                    await command_log_and_err(ctx, f'Deleted {amount} messages')
                    await ctx.channel.purge(limit=default_clear_amt)
                except Forbidden:
                    await command_log_and_err(ctx, err_code='Err_30124',
                                              text='Unable to comply. Check $ecl for more info.')
        else:
            await ctx.reply(f"`Clear` is disabled in `{ctx.guild.name}`")
            await command_log_and_err(ctx, 'Command disabled')

    # 303
    @command(aliases=['calc'],
                      help="Calculates and gives result based on input. If 'help arith' or 'help compare' is put in the expression argument, you'll get a list of Operators.",
                      name="Calculator", extras={'emoji': '🧮', 'number': '302'},
                      usage="calculator|calc <expression>")
    @comm_log_local
    async def calculator(self, ctx: Context, *, expression: Optional[str]):
        author = ctx.message.author
        if expression:
            if expression.lower() == 'help arith':
                await command_log_and_err(ctx, 'Success')
                await ctx.reply(embed=await set_timestamp(Embed(title='Calculator - `Matchematical Operators`',
                                                                       description=
                                                                       f"""
`{'Addition':^30}-{"'+'":^15}`
`{'Subtraction':^30}-{"'-'":^15}`
`{'Multiplication':^30}-{"'*'":^15}`
`{'Exponentiation':^30}-{"'**' or '^'":^15}`
`{'Division':^30}-{"'/'":^15}`
`{'Rounded off Division':^30}-{"'//'":^15}`
""", colour=Colour.random())))
            elif expression.lower() == 'help compare':
                await command_log_and_err(ctx, 'Success')
                await ctx.reply(embed=await set_timestamp(Embed(title='Calculator - `Comparison Operators`',
                                                                       description=
                                                                       f"""
`{'Equivalence Check':^30}-{"'=='":^15}`
`{'Difference Check':^30}-{"'!='":^15}`
`{'Greater than Check':^30}-{"'>'":^15}`
`{'Smaller than Check':^30}-{"'<'":^15}`
`{'Greater than/Equal to Check':^30}-{"'>='":^15}`
`{'Smaller than/Equal to Check':^30}-{"'<='":^15}`
""", colour=Colour.random())))
            elif expression.lower() == 'help logical':
                await command_log_and_err(ctx, 'Success')
                await ctx.reply(embed=await set_timestamp(Embed(title='Calculator - `Logical Operators`',
                                                                       description=
                                                                       f"""
`{'And':^5}- {"'True' if both conidtions are True":^50}`
`{'Or':^5}- {"'True' if either one or both conditions are True":^50}`
`{'Not':^5}- {"'False' if True, 'True' if false":^50}`
""", colour=Colour.random())))
            else:
                try:
                    expression = expression.replace("^", "**")
                    result = eval(expression)
                    await command_log_and_err(ctx, 'Success')
                    await ctx.reply(embed=await set_timestamp(Embed(title='Calculator',
                                                                           description=f"*`Expression`*: `{expression}`\n\n*`Result`*: `{result}`",
                                                                           colour=Colour.random())))
                except SyntaxError:
                    await command_log_and_err(ctx, err_code='Err_30212',
                                              text=f'Invalid expression. Try again {author.mention}')
                except NameError:
                    await command_log_and_err(ctx, err_code="Err_30212",
                                              text=f"`{expression}` is not a valid expression")
                except ZeroDivisionError:
                    await command_log_and_err(ctx, err_code="Err_30212",
                                              text=f"`Runtime Error`: Cannot divide by `Zero`")
        else:
            await command_log_and_err(ctx, err_code="Err_30248",
                                      text="You haven't given the expression for computing your answer")

    # 303
    @command(name="Change nickname", aliases=['cn', 'changenick'],
                      help="Changes the nickname of a given Member.",
                      usage='changenick|cn <member> <new nickname>',
                      extras={'emoji': '🎭', 'number': '303'})
    @cooldown(1, 30, BucketType.member)
    @guild_only()
    @comm_log_local
    async def changenick(self, ctx, member: Member = None, *, new_nick=None):
        author = ctx.message.author
        if member:
            if new_nick:
                try:
                    if new_nick.lower() == 'reset':
                        await member.edit(nick=None)
                        await command_log_and_err(ctx, 'Success', used_on=member)
                        await ctx.reply(f"{member.mention}'s nickname has been reset")
                    else:
                        await member.edit(nick=new_nick)
                        await command_log_and_err(ctx, 'Success', used_on=member)
                        await ctx.reply(f"{member.name}'s nickname has been changed to {member.mention}")
                except Forbidden:
                    await command_log_and_err(ctx, err_code="Err_30324",
                                              text=f"Unable to comply {author.mention}. Check $ecl for more info.")
            else:
                await command_log_and_err(ctx, err_code='Err_30348',
                                          text=f'New nickname for {member.name} is not mentioned...')
        else:
            await command_log_and_err(ctx, err_code='Err_30348',
                                      text=f'Next time give me a name to edit their nickname, {author.mention}')

    # 305
    @command(aliases=['minfo', 'memberinfo'], name='Member Info',
                      help="Displays the info of a given Member.",
                      usage='memberinfo|minfo (member)', extras={'emoji': '📃', 'number': '304'})
    @guild_only()
    @comm_log_local
    async def memberinfo(self, ctx: Context, member: Optional[Member]):
        async with ctx.typing():
            bot: Bot = ctx.bot
            if not member:
                member = ctx.message.author
            mber = await bot.fetch_user(member.id)
            pfp = member.avatar.url
            name = member.name
            disc = member.discriminator
            nick = f'"{member.display_name}"' if member.nick else 'No nickname...'
            status = member.status
            activities = []
            for activity in member.activities:
                if isinstance(activity, CustomActivity):
                    activities.append(activity.name)
                elif isinstance(activity, Spotify):
                    activities.append(f'Listening to "{activity.title}" on Spotify')
                elif isinstance(activity, Activity):
                    if activity.type == ActivityType.watching:
                        activities.append(f'Watching "{activity.name}"')
                    elif activity.type == ActivityType.playing:
                        activities.append(f'Playing "{activity.name}"')
                    elif activity.type == ActivityType.streaming:
                        activities.append(f'Streaming "{activity.name}"')
            activities = ', '.join(activities) if None not in activities else 'None'
            public_flags = ', '.join(
                [str(house).replace("UserFlags.", "").replace("_", " ").title() for house in member.public_flags.all()])
            flag_logos = ''.join([str(await hypesquad_emoji(bot, emoji)) for emoji in public_flags.split(", ")])
            if member.bot and member.public_flags.verified_bot:
                flag_logos += str(await hypesquad_emoji(bot, "VerifiedBot"))
            elif member.bot and not member.public_flags.verified_bot:
                flag_logos += str(await hypesquad_emoji(bot, "Bot"))
            joined_at = time_set(member.joined_at, "%d %b %Y at %I:%M %p")
            created_at = time_set(member.created_at, "%d %b %Y at %I:%M %p")
            emb1 = Embed(title=f'Member Statistics - {name}  {flag_logos}', description='',
                                 colour=mber.accent_colour or Colour.default())
            emb1.set_thumbnail(url=pfp)
            emb1.description += f'`{"Name":^27}:{name:^31}`\n`{"Discriminator":^27}:{disc:^31}`\n'
            emb1.description += f'`{"Nickname on this server":^27}:{nick:^31}`\n'
            emb1.description += f"`{'Joined this server on':^27}:{joined_at:^31}`\n"
            emb1.description += f"`{'Account created on':^27}:{created_at:^31}`\n"
            emb1.description += f"`{'Public Flags':^27}:{public_flags:^31}`"
            emb1.set_footer(icon_url=pfp, text=f"Status: {status}\nActivities: {activities}")
            emb1 = await set_timestamp(emb1)
            await command_log_and_err(ctx, 'Success', used_on=member)
            await ctx.reply(embed=emb1)

    # 306
    @command(aliases=['sinfo', 'serverinfo'], usage='serverinfo|sinfo',
                      help="Displays info of the server.",
                      name="Server Info", extras={'emoji': '📜', 'number': '305'})
    @guild_only()
    @comm_log_local
    async def serverinfo(self, ctx: Context):
        async with ctx.typing():
            server = ctx.guild
            name = server.name
            bot_count = 0
            for member in ctx.guild.members:
                if member.bot is True:
                    bot_count += 1
            boosters = ', '.join([member.name for member in server.premium_subscribers]) if len(server.premium_subscribers) > 0 else None
            server_region = server.region[0][0].upper() + server.region[0][1:]
            created_at = time_set(server.created_at, "%d %b %Y at %I:%M %p")
            server_info = Embed(title=name, description=f'Details of `{name}`\n\n', colour=Colour.random())
            server_info.description += f'`{"Name":^17}: {name:^30}`\n`{"Id":^17}: {server.id:^30}`\n'
            server_info.description += f'`{"Region":^17}: {server_region:^30}`\n`{"Owner":^17}: {str(server.owner):^30}`\n'
            server_info.description += f'`{"Emoji Limit":^17}: {server.emoji_limit:^30}`\n`{"Bitrate Limit":^17}: {f"{server.bitrate_limit / 1000} kbps":^30}`\n'
            server_info.description += f'`{"File Size Limit":^17}: {f"{round(server.filesize_limit / 1000000)} mb":^30}`\n`{"Boosters":^17}: {boosters or "No boosters":^30}`\n'
            server_info.description += f'`{"Created on":^17}: {created_at:^30}`\n'
            server_info.description += f'`{"Member Count":^17}: {f"Total - {len(ctx.guild.members)}, Bots - {bot_count}":^30}`'
            server_info.set_thumbnail(url=server.icon.url)
            server_info = await set_timestamp(server_info)
            await command_log_and_err(ctx, 'Success')
            await ctx.reply(embed=server_info)

    # 307
    @command(aliases=['ecl', 'errorcodelist'], name="Error Code List",
                      help="Gives a list of error codes that the bot gives out in an error, and the codes' meanings.",
                      usage='errorcodelist|ecl <err code>', extras={'emoji': '📄', 'number': '306'})
    @comm_log_local
    async def errorcodelist(self, ctx: Context, error: str = None):
        bot: Bot = ctx.bot
        async with ctx.typing():
            if not error:
                await command_log_and_err(ctx, 'Success')
                await ctx.reply(
                    embed=await set_timestamp(Embed(title=f'{botuser.name} - Error Code List', description=
                    """
`Error Code Classification`
```nim
Categories    : 1 = Roles
                2 = Member Stay/Leave Options(mslo)
                3 = Utilities
                4 = Games
                5 = Channels and Categories(cac)
                6 = Music
                7 = Settings
                8 = Sports
                9 = Miscellaneous(Misc)
                P = Python

Type of Errors: 24  = Missing Permissions
                48  = Missing Arguments
                12  = Operation Failed
                404 = Not found
                  
Special Errors: A113404 = No Command Found.
                α11404  = Member Not Found.
                β20404  = Role Not Found.
                θ30404  = Message Not Found.
                40βθ404 = User Not Found.
                50θβ404 = Channel Not Found.

For Example:- 1)Err_10124 means command '1' under category
                '10' which is roles, can't operate due to 
                err type '24' which is Missing Permissions
                 
              2)Err_20348 means command '3' under category
                '20' which is mslo, can't operate due to 
                err type '48' which is Missing Arguments.
```""", colour=Colour.random())))
            else:
                if len(error) == 5:
                    err_comm = None
                    err_ctgry = None
                    for _command in bot.commands:
                        if str(_command.brief)[1:] == error[:-2]:
                            err_comm = _command.name
                            err_ctgry = _command.cog_name
                    if error[-2:] == '12':
                        err_type = 'Operation Failiure'
                    elif error[-2:] == '24':
                        err_type = 'Missing Permissions'
                    elif error[-2:] == '48':
                        err_type = 'Missing Arguments'
                    await command_log_and_err(ctx, 'Success')
                    embed = await set_timestamp(
                        Embed(title=f'Error - `{error}`', description='', colour=Colour.random()),
                        "Decrypted")
                    embed.description += f'`{"Error Type":^15}:{err_type:^25}`\n`{"Command":^15}:{err_comm:^25}`\n`{"Category":^15}:{err_ctgry:^25}`'
                    await ctx.reply(embed=embed)
                elif error[-3:] == '404':
                    err_comm = None
                    if error[:-3] == 'A113':
                        err_comm = 'Command not found'
                    elif error[:-3] == 'α11':
                        err_comm = 'Member not found'
                    elif error[:-3] == 'β20':
                        err_comm = 'Role not found'
                    elif error[:-3] == 'θ30':
                        err_comm = 'Message not found'
                    elif error[:-3] == '40βθ':
                        err_comm = 'User not found'
                    elif error[:-3] == '50θβ':
                        err_comm = 'Channel not found'
                    await command_log_and_err(ctx, 'Success')
                    embed = await set_timestamp(
                        Embed(title=f'Error - `{error}`', description='', colour=Colour.random()),
                        "Decrypted")
                    embed.description += f'`{"Error Type":^20}:{"Not found":^25}`\n`{"Item not found":^20}:{err_comm:^25}`'
                    await ctx.reply(embed=embed)
                else:
                    await command_log_and_err(ctx, err_code="Err_30612",
                                              text="Not a valid error code or info option...")

    # 308
    @command(aliases=['cinfo', 'clientinfo'], name="Client Info",
                      help='Displays information about the bot',
                      usage='clientinfo|cinfo', extras={'emoji': '📃', 'number': '307'})
    @comm_log_local
    async def clientinfo(self, ctx: Context):
        async with ctx.typing():
            bot: Bot = ctx.bot
            c = bot.user
            cinfo = await set_timestamp(
                Embed(title=bot.user.name, description='', colour=Colour.random()),
                f"At your service {ctx.author.name}")
            cinfo.description += f"""
    `{"Name":^15}-{c.name:^25}`
    `{"Discriminator":^15}-{c.discriminator:^25}`
    `{"ID":^15}-{c.id:^25}`
    `{"Version":^15}-{bot_ver:^25}`
    `{"Created on":^15}-{time_set(c.created_at, "%d %b %Y at %I:%M %p"):^25}`"""
            await command_log_and_err(ctx, 'Success')
            cinfo.set_thumbnail(url=c.avatar.url)
            await ctx.reply(embed=cinfo)

    # 309
    @command(aliases=['di'], name='Delinvs',
                      help='Deletes all active invites of the server.',
                      usage='delinvs|di', extras={'emoji': '🚷', 'number': '308'})
    @guild_only()
    @comm_log_local
    async def delinvs(self, ctx: Context):
        async with ctx.typing():
            await ctx.reply(f"Deleting all access points to `{ctx.guild.name}`...")
            invites = await ctx.guild.invites()
            for invite in invites:
                await invite.delete()
            await command_log_and_err(ctx, 'Success')
            await ctx.reply(f"Breaches sealed. `{ctx.guild.name}` is in comfirmed isolation for the time being")

    # 314
    @command(aliases=['st'], name='Status',
                      help='Displays the Status of a given member',
                      usage='status|st (member)', extras={'emoji': '📲', 'number': '309'})
    @guild_only()
    @comm_log_local
    async def status(self, ctx: Context, member: Member = None):
        async with ctx.typing():
            m = member if member else ctx.author
            if m.activities:
                for s in m.activities:
                    if isinstance(s, CustomActivity):
                        await ctx.reply(f"{m.mention}'s status is: `{s}`")
                    elif isinstance(s, Spotify):
                        await ctx.reply(embed=Embed(title=s.title,
                                                           description="{0} is Listening to:\n*`{1:^6}`*`: {2:<}`\n*`{3:^6}`*`: {4:<}`\n*`{5:^6}`*`: {6:<}`".format(
                                                               m.mention, 'Song',
                                                               s.title,
                                                               'Artists' if isinstance(s.artist, list) else 'Artist',
                                                               ', '.join(s.artist) if isinstance(s.artist,
                                                                                                 list) else s.artist,
                                                               'Album',
                                                               s.album.title()),
                                                           colour=s.colour).set_thumbnail(url=s.album_cover_url))
                    elif isinstance(s, Activity):
                        if s.type == ActivityType.watching:
                            await ctx.reply(f"{m.mention} is watching `{s}`")
                        elif s.type == ActivityType.playing:
                            await ctx.reply(f"{m.mention} is playing `{s}`")
                        elif s.type == ActivityType.streaming:
                            await ctx.reply(f"{m.mention} is streaming `{s}`")
            else:
                if m.status == Status.offline:
                    await ctx.reply(f"""{m.mention}'s: ```py
    Status = Offline```""")
                else:
                    await ctx.reply(f"""{m.mention}'s: ```py
    Status = None```""")
            await command_log_and_err(ctx, 'Success')

    @command(aliases=['abts', 'addbottoserver'], name='Add bot to server', extras={'emoji': '🔗', 'number': '310'},
                      usage='addbottoserver|abts', help='Generates and sends a link to add the bot to your server')
    @comm_log_local
    async def addbottoserver(self, ctx: Context):
        await command_log_and_err(ctx, 'Success')
        bot: Bot = ctx.bot
        await ctx.reply(embed=Embed(title=f'Hello my name is `{bot.user.name}`',
                                            description='It stands for `Just A Rather Very Intelligent System`\n\nClick [`J.A.R.V.I.S`]({}) to add me to your server.'.format(
                                               'https://discord.com/api/oauth2/authorize?client_id=749830638982529065&permissions=8&scope=bot%20applications.commands'
                                           ), colour=Colour.random()).set_thumbnail(
            url=bot.user.avatar.url))

    # 316
    @command(name='Announce', aliases=['an'], extras={'emoji': '📢', 'number': '311'},
                      help='Announces to every member in the server.', usage='$announce|an <text>')
    @cooldown(60, 1, BucketType.guild)
    @comm_log_local
    async def announce(self, ctx: Context, *, text: str = None):
        async with ctx.typing():
            bot: Bot = ctx.bot
            if text:
                if int(ctx.author.id) == int(ctx.guild.owner_id):
                    await command_log_and_err(ctx, 'Success')
                    for member in ctx.guild.members:
                        if member != bot.user and member != ctx.author:
                            try:
                                await member.send(embed=Embed(title=f'Announcement from {ctx.author.name}',
                                                                      description=text,
                                                                      colour=Colour.random()).set_thumbnail(
                                    url=bot.user.avatar.url))
                            except HTTPException:
                                await ctx.reply(f"Cant send message to {member}")
                else:
                    await command_log_and_err(ctx, f'{ctx.author.name} is not owner')
                    await ctx.reply(f"{ctx.author.mention}, you are not the owner of `{ctx.guild.name}`")
            else: await command_log_and_err(ctx, err_code='31148', text="You haven't given anything to announce pal")

    @command(name='Member List', aliases=['ml', 'members', 'memberlist'], extras={'emoji': '📋', 'number': '312'},
                      help='Returns a member list of everyone in the server.', usage='$members|memberlist|ml')
    @cooldown(1, 10, BucketType.guild)
    @comm_log_local
    async def memberlist(self, ctx: Context):
        async with ctx.typing():
            await command_log_and_err(ctx, 'Success')
            embed = Embed(title=f'Member list - {ctx.guild.name}', description='', colour=Colour.random())
            for member in ctx.guild.members:
                embed.description += f'`{member.name:^30} - `{member.mention}\n'
            embed.set_thumbnail(url=ctx.guild.icon.url)
            if len(embed.description) >= 4096:
                third_1 = '\n'.join(embed.description.split('\n')[:40])
                third_2 = '\n'.join(embed.description.split('\n')[40:])
                embed.description = third_1
                await ctx.reply(embeds=[embed, Embed(description=third_2, colour=Colour.random())])
            else:
                await ctx.reply(embed=embed)

    @command(name="Profile Pic", aliases=['pfp', 'profilepic'], extras={'emoji': '🎭', 'number': '313'},
                      help="Displays the profile picture of a given user.",
                      usage="$profilepic|pfp (user)")
    @comm_log_local
    async def _pfp(self, ctx: Context, user = None):
        user = await UserConverter().convert(ctx, user) if user else ctx.author
        await command_log_and_err(ctx, status="Success")
        await ctx.reply(embed=await set_timestamp(Embed(description="_ _", type="image", colour=user.colour).set_image(url=user.avatar.url)))

    @command(name="Banner", aliases=['br'], extras={'emoji': '🖼', 'number': '314'},
                      help="Displays the banner of a nitro user.",
                      usage='$banner|b (member)')
    @comm_log_local
    async def _banner(self, ctx: Context, member: Union[Member, User] = None):
        await command_log_and_err(ctx, status="Success")
        member = await self.bot.fetch_user(member.id if member else ctx.author.id)
        if member.banner:
            await ctx.reply(embed=await set_timestamp(Embed(description="_ _", colour=Colour.random()).set_image(url=member.banner.url)))
        else: await ctx.reply(f"The banner feature is for nitro user exclusively.")


def setup(bot: Bot):
    bot.add_cog(Utilities(bot))
