import asyncio
import json
import re
from typing import Optional, Union
import discord
from MyCogs import command_log_and_err, set_timestamp, Context,\
    Cog, Client, command, cooldown, guild_only, User, Member,\
    BucketType, UserNotFound, Embed, Colour, HTTPException,\
    Forbidden, commands, has_guild_permissions, Message, TextChannel,\
    Role, TextChannelConverter, RoleConverter, Bot, UserConverter, comm_log_local
#commands.

class Moderation(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.description = 'Moderation commands.'
        self.name = 'Moderation(mod)'

    # 201
    @command(name="Invite", aliases=['i'], usage='invite|i <user>',
                      extras={'emoji': '🚪', 'number': '201'},
    help='Invites people from outside the server. This can vary from user to user based on their privacy settings.')
    @cooldown(1, 5, BucketType.member)
    @guild_only()
    @comm_log_local
    async def invite(self, ctx: Context, member: Union
    [User, Member, str] = None):
        invitelink = await ctx.channel.create_invite(max_uses=1)
        error = None
        if member:
            if isinstance(member, str):
                raise UserNotFound(argument=member)
            try:
                invite = await member.send(
                    embed=await set_timestamp(Embed(
                        title=f"You are being invited to `{ctx.guild.name}`",
                        description=f"Click ***[here]({invitelink})*** to join `{ctx.guild.name}`.\n `Author`: {ctx.author.mention}\n `Uses`: Only 1",
                        colour=Colour.random()), ""))
                msg = await command_log_and_err(ctx=ctx, status="Success",
                                                used_on=member)
            except HTTPException:
                error = await command_log_and_err(ctx=ctx, used_on=member, err_code="Err_20112",
                                            text=f"Unable to invite {member.mention}")
                invite, msg = None, None
        else:
            await command_log_and_err(ctx=ctx, err_code="Err_20148",
                                      text="Specify the person to be invited.")
        return [invite, error, msg, invitelink]

    # 202
    @command(name="Kick", aliases=['k'], usage='kick|k <member> (reason)', extras={'emoji': '⛔', 'number': '202'},
                      help='Kicks members from the server. Owners of servers have an option to skip the conformation message as well use the kick command when it is de-activated, to access this, type: "override 403" in the place of reason.')
    @guild_only()
    @comm_log_local
    async def kick(self, ctx: Context, member: Member = None, *, reason: Optional[str] = ''):
        author = ctx.message.author
        guild_id = str(ctx.guild.id)
        channel_id = str(ctx.message.channel.id)
        with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/settings.json", "r") as f:
            settings: dict = json.load(f)
        id: str = channel_id if settings.get(channel_id) else guild_id
        if reason.lower() == 'override 403' and author.id == ctx.guild.owner_id:
            try:
                invite, error, msg, invitelnk = await self.invite(ctx, member)
                await member.kick(reason=reason)
                await msg.delete()
                if error:
                    await error
                success = 1
            except Forbidden:
                await invite.delete()
                await msg.delete()
                await invitelnk.delete()
                success = 0
            if success == 1:
                await command_log_and_err(ctx=ctx, status='Success', used_on=member)
                await ctx.reply(
                    f"{member.mention} you have been deemed unworthy to stay in this server by {author.mention}")
            else:
                await command_log_and_err(ctx=ctx, err_code="Err_20224", used_on=member,
                                          text="Sorry I can't do that, missing permissions.")
        elif reason.lower() == 'override 403' and author.id != ctx.guild.owner_id:
            await ctx.reply("Oi your not allowed to override me! Do it the old way peasant this only for owners!")
            await command_log_and_err(ctx=ctx, status='Not owner.', used_on=member)
        else:
            if settings[id]["kick"]:
                if member:
                    if member == author:
                        await ctx.reply("Ya can't kick yourself dummy!")
                    else:
                        await ctx.reply(f"Are you sure {author.mention}?")
                        try:
                            msg = await ctx.bot.wait_for("message", timeout=10, check=lambda
                                message: message.author == author and message.channel == ctx.channel)
                            if msg.content.lower() == "yes":
                                try:
                                    invite, error, msg1, invitelink = await self.invite(ctx, member)
                                    await member.kick(reason=reason)
                                    if error:
                                        await error
                                    success = 1
                                except Forbidden:
                                    await invite.delete()
                                    await msg1.delete()
                                    await invitelink.delete()
                                    success = 0
                                if success == 1:
                                    await command_log_and_err(ctx=ctx, status='Success',
                                                              used_on=member)
                                    await ctx.reply(
                                        f"{member.mention} you have been deemed unworthy to stay in this server by {author.mention}")
                                else:
                                    await command_log_and_err(ctx=ctx, err_code="Err_20224",
                                                              used_on=member,
                                                              text="Sorry I can't do that, missing permissions.")
                            else:
                                await command_log_and_err(ctx=ctx, status='Request Timeout')
                                await ctx.reply(
                                    f"It's your lucky day {member.mention}, {msg.author.mention} seems to have pity for you.")
                        except asyncio.TimeoutError:
                            await command_log_and_err(ctx=ctx, status='Confirmation Missing')
                            await ctx.reply('No kicking then.')
                else:
                    await command_log_and_err(ctx=ctx, err_code="Err_20248",
                                              text="You haven't given me a member to kick...")
            else:
                await command_log_and_err(ctx=ctx, status='Command disabled',
                                          used_on=member)
                await ctx.reply(f"`Kick` has been `disabled` for {ctx.channel.mention}")

    # 203
    @command(name="Ban", aliases=['b'], usage='ban|b <member> (reason)', extras={'emoji': '🚫', 'number': '203'},
                      help='Bans members from the server. Owners of servers have an option to skip the conformation message as well use the ban command when it is de-activated, to access this, type: "override 403" in the place of reason.')
    @cooldown(1, 15, BucketType.guild)
    @guild_only()
    @has_guild_permissions(ban_members=True)
    @comm_log_local
    async def ban(self, ctx: Context, member: Member = None, *, reason: Optional[str] = 'None'):
        author = ctx.message.author
        guild_id = str(ctx.guild.id)
        channel_id = str(ctx.message.channel.id)
        with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/settings.json", "r") as f:
            settings: dict = json.load(f)
        id: str = channel_id if settings.get(channel_id) else guild_id
        if reason.lower() == 'override 403' and author.id == ctx.guild.owner_id:
            try:
                await member.ban(reason=reason, delete_message_days=0)
                success = 1
            except Forbidden:
                success = 0
            if success == 1:
                await command_log_and_err(ctx=ctx, status='Success', used_on=member)
                await ctx.reply(f'I am forced to ban you {member.mention}... Well I sorta agreed to it too but... :)')
            else:
                await command_log_and_err(ctx=ctx, err_code="Err_20324", used_on=member,
                                          text="Sorry I can't do that, missing permissions.")
        elif reason.lower() == 'override 403' and author.id != ctx.guild.owner_id:
            await command_log_and_err(ctx=ctx, status='Not owner.', used_on=member)
            await ctx.reply("Oi your not allowed to override me! Do it the old way peasant this only for owners!")
        else:
            if settings[id]["ban"]:
                if member:
                    if member == author:
                        await ctx.reply(
                            "Now I can't pretend I understand your motives, but what are you gonna gain by banning yourself?")
                        await command_log_and_err(ctx=ctx, status='Paradox', used_on=author)
                    else:
                        await ctx.reply(f"Are you sure {author.mention}? Respond with yes or no.")
                        try:
                            msg = await ctx.bot.wait_for("message", timeout=10, check=lambda
                                message: message.author == author and message.channel == ctx.channel)
                            if msg.content.lower() == 'yes':
                                try:
                                    await member.ban(reason=reason, delete_message_days=0)
                                    success = 1
                                except Forbidden:
                                    success = 0
                                if success == 1:
                                    await command_log_and_err(ctx=ctx, status='Success',
                                                              used_on=member)
                                    await ctx.reply(
                                        f'I am forced to ban you {member.mention}... Well I sorta agreed to it too but... :)')
                                else:
                                    await command_log_and_err(ctx=ctx, err_code="Err_20324",
                                                              used_on=member,
                                                              text="Sorry I can't do that, missing permissions.")
                        except asyncio.TimeoutError:
                            await command_log_and_err(ctx=ctx, status="Request Timeout",
                                                      used_on=member)
                            await ctx.reply(f"Well then, no banning {member.mention} I suppose...")
                else:
                    await command_log_and_err(ctx=ctx, err_code="Err_20248",
                                              text="Gimme someone to ban...")
            else:
                await command_log_and_err(ctx=ctx, status="Command disabled here.", used_on=member)
                await ctx.reply(f"`Ban` is `disabled` in {ctx.channel.mention}")

    # 204
    @command(name="Unban", aliases=['ub'], usage='unban|ub <user>',
                      extras={'emoji': '🛂', 'number': '204'}, help='Unbans users from the server'
                      ' and invites them by looking through the servers'
                      ' bans list.')
    @guild_only()
    @comm_log_local
    async def unban(self, ctx: Context, *, member = None):
        author = ctx.message.author
        member = await UserConverter().convert(ctx, member)
        if member:
            banned_users = await ctx.guild.bans()
            try:
                for ban_entry in banned_users:
                    user = ban_entry.user
                    if user.name == member.name or user.mention == member.mention:
                        await ctx.guild.unban(user)
                        await command_log_and_err(ctx=ctx,
                                status='Success', used_on=user)
                        await ctx.reply(f"{user.mention} hath been"
                                       f" unbanned.")
                        invite,\
                        error, msg, invitelnk = await self.invite(ctx,
                                                                  user)
                        await msg.delete()
                        if error:
                            await error
                        return
            except Forbidden:
                await command_log_and_err(ctx=ctx,
                    err_code="Err_20424",
                    text=f"Unable to comply {author.mention}. Check $ecl"
                         f" for more info.")
        else:
            await command_log_and_err(ctx=ctx,
                    err_code="Err_20448",
                    text=f"Unbanning a person requires their username"
                         f" {author.mention}.")

    #205
    @command(name="Timeout", aliases=['to', 'isolate', 'isl'], usage="timeout|to|isolate|isl <member>",
             extras={'emoji': '🔒', 'number': '205'},
             help="Keeps an annoying person in a timeout channel with no contact except those who have "
                               "access to that channel.")
    @guild_only()
    @has_guild_permissions(administrator=True)
    @comm_log_local
    async def _timeout(self, ctx: Context, member: Member = None):
        async with ctx.typing():
            if member:
                role_names: list[str] = [role.name.lower() for role in ctx.guild.roles]
                channel_names: list[str] = [channel.name.lower() for channel in ctx.guild.text_channels]
                if "timeout" not in role_names:
                    try:
                        await ctx.reply(f"{ctx.author.mention}, **I need to create a role** called 'timeout' for this to work"
                                        f" and there seem to be no roles like this in the server. **May I create one?** Respond "
                                        f"with Y(es) or N(o) in the next 15 seconds.")
                        message: Message = await ctx.bot.wait_for("message", check=lambda m: m.author == ctx.author and \
                                                                                              m.channel == ctx.channel and (re.search(r"(y(es)*|n(o)*)", m.content.lower())), timeout=15.0)
                        if re.search(r"y(es)*", message.content.lower()):
                            await ctx.reply("Creating a role named `timeout`")
                            try: t_role: Role = await ctx.guild.create_role(name="timeout")
                            except Forbidden: return await command_log_and_err(ctx, err_code="20524",
                                                                        text="Missing permissions to create role.")
                        elif re.search(r"n(o)*", message.content.lower()):
                            return await ctx.reply("Well then you would have to create a role called 'timeout' and "
                                            "try this command again.")
                    except TimeoutError:
                        return await ctx.reply(f"Stopping `timeout` procedure for {member.name}")
                else: t_role: Role = discord.utils.get(ctx.guild.roles, name="timeout")
                if "timeout" not in channel_names:
                    try:
                        await ctx.reply(f"{ctx.author.mention}, **I need to create a channel** called 'timeout' for this to work"
                                        f" and there seem to be no channels like this in the server. **May I create one?** Respond "
                                        f"with Y(es) or N(o) in the next 15 seconds.")
                        message: Message = await ctx.bot.wait_for("message", check=lambda m: m.author == ctx.author and \
                                                                                              m.channel == ctx.channel and (re.search(r"(y(es)*|n(o)*)", m.content.lower())), timeout=15.0)
                        if re.search(r"y(es)*", message.content.lower()):
                            await ctx.reply("Creating a channel named `timeout`")
                            try:
                                t_channel: TextChannel = await ctx.guild.create_text_channel(name="timeout")
                                await t_channel.set_permissions(ctx.guild.default_role, view_channel=False)
                                await t_channel.set_permissions(t_role, view_channel=True)
                            except Forbidden: return await command_log_and_err(ctx, err_code="20524",
                                                                        text="Missing permissions to create channel.")
                        elif re.search(r"n(o)*", message.content.lower()):
                            return await ctx.reply("Well then you would have to create a channel called 'timeout' and "
                                            "try this command again.")
                    except TimeoutError:
                        return await ctx.reply(f"Stopping `timeout` procedure for {member.name}")
                else:
                    t_channel: TextChannel = discord.utils.get(ctx.guild.channels, name="timeout")
                [await member.remove_roles(rl) if rl.name != "@everyone" and rl.permissions.administrator else None for rl in member.roles]
                [await channel.set_permissions(t_role, view_channel=False) for channel in ctx.guild.channels]
                await member.add_roles(t_role)
                await command_log_and_err(ctx, status="Succesful", used_on=member)
                await ctx.reply(f"{member.mention} is in {t_channel.mention}")
            else: await command_log_and_err(ctx, err_code="20548", text="You've not given me who to isolte by the way.")


def setup(bot: Bot):
    bot.add_cog(Moderation(bot))
