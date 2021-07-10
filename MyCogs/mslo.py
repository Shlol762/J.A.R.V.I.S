import asyncio
import json
from typing import Optional, Union
import discord
from MyCogs import command_log_and_err, set_timestamp, Context,\
    Cog, Client, command, cooldown, guild_only, User, Member,\
    BucketType, UserNotFound, Embed, Colour, HTTPException,\
    Forbidden, commands
#commands.

class Mslo(Cog):
    def __init__(self, client: Client):
        self.client = client
        self.description = 'Commands that control a members stay/leave options.'
        self.name = 'Mslo'

    # 201
    @command(name="Invite", aliases=['i'], usage='invite|i <user>',
                      brief='🚪201',
    help='Invites people from outside the server. This can vary from user to user based on their privacy settings.')
    @cooldown(1, 5, BucketType.member)
    @guild_only()
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
                msg = await command_log_and_err(ctx=ctx, client=self.client, status="Success",
                                                used_on=member)
            except HTTPException:
                error = await command_log_and_err(ctx=ctx, client=self.client, used_on=member, err_code="Err_20112",
                                            text=f"Unable to invite {member.mention}")
                invite, msg = None, None
        else:
            await command_log_and_err(ctx=ctx, client=self.client, err_code="Err_20148",
                                      text="Specify the person to be invited.")
        return [invite, error, msg, invitelink]

    # 202
    @command(name="Kick", aliases=['k'], usage='kick|k <member> (reason)', brief='⛔202',
                      help='Kicks members from the server. Owners of servers have an option to skip the conformation message as well use the kick command when it is de-activated, to access this, type: "override 403" in the place of reason.')
    @guild_only()
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
                await command_log_and_err(ctx=ctx, client=self.client, status='Success', used_on=member)
                await ctx.reply(
                    f"{member.mention} you have been deemed unworthy to stay in this server by {author.mention}")
            else:
                await command_log_and_err(ctx=ctx, client=self.client, err_code="Err_20224", used_on=member,
                                          text="Sorry I can't do that, missing permissions.")
        elif reason.lower() == 'override 403' and author.id != ctx.guild.owner_id:
            await ctx.reply("Oi your not allowed to override me! Do it the old way peasant this only for owners!")
            await command_log_and_err(ctx=ctx, client=self.client, status='Not owner.', used_on=member)
        else:
            if settings[id]["kick"]:
                if member:
                    if member == author:
                        await ctx.reply("Ya can't kick yourself dummy!")
                    else:
                        await ctx.reply(f"Are you sure {author.mention}?")
                        try:
                            msg = await self.client.wait_for("message", timeout=10, check=lambda
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
                                    await command_log_and_err(ctx=ctx, client=self.client, status='Success',
                                                              used_on=member)
                                    await ctx.reply(
                                        f"{member.mention} you have been deemed unworthy to stay in this server by {author.mention}")
                                else:
                                    await command_log_and_err(ctx=ctx, client=self.client, err_code="Err_20224",
                                                              used_on=member,
                                                              text="Sorry I can't do that, missing permissions.")
                            else:
                                await command_log_and_err(ctx=ctx, client=self.client, status='Request Timeout')
                                await ctx.reply(
                                    f"It's your lucky day {member.mention}, {msg.author.mention} seems to have pity for you.")
                        except asyncio.TimeoutError:
                            await command_log_and_err(ctx=ctx, client=self.client, status='Confirmation Missing')
                            await ctx.reply('No kicking then.')
                else:
                    await command_log_and_err(ctx=ctx, client=self.client, err_code="Err_20248",
                                              text="You haven't given me a member to kick...")
            else:
                await command_log_and_err(ctx=ctx, client=self.client, status='Command disabled',
                                          used_on=member)
                await ctx.reply(f"`Kick` has been `disabled` for {ctx.channel.mention}")

    # 203
    @command(name="Ban", aliases=['b'], usage='ban|b <member> (reason)', brief='🚫203',
                      help='Bans members from the server. Owners of servers have an option to skip the conformation message as well use the ban command when it is de-activated, to access this, type: "override 403" in the place of reason.')
    @cooldown(1, 15, BucketType.guild)
    @guild_only()
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
                await command_log_and_err(ctx=ctx, client=self.client, status='Success', used_on=member)
                await ctx.reply(f'I am forced to ban you {member.mention}... Well I sorta agreed to it too but... :)')
            else:
                await command_log_and_err(ctx=ctx, client=self.client, err_code="Err_20324", used_on=member,
                                          text="Sorry I can't do that, missing permissions.")
        elif reason.lower() == 'override 403' and author.id != ctx.guild.owner_id:
            await command_log_and_err(ctx=ctx, client=self.client, status='Not owner.', used_on=member)
            await ctx.reply("Oi your not allowed to override me! Do it the old way peasant this only for owners!")
        else:
            if settings[id]["ban"]:
                if member:
                    if member == author:
                        await ctx.reply(
                            "Now I can't pretend I understand your motives, but what are you gonna gain by banning yourself?")
                        await command_log_and_err(ctx=ctx, client=self.client, status='Paradox', used_on=author)
                    else:
                        await ctx.reply(f"Are you sure {author.mention}? Respond with yes or no.")
                        try:
                            msg = await self.client.wait_for("message", timeout=10, check=lambda
                                message: message.author == author and message.channel == ctx.channel)
                            if msg.content.lower() == 'yes':
                                try:
                                    await member.ban(reason=reason, delete_message_days=0)
                                    success = 1
                                except Forbidden:
                                    success = 0
                                if success == 1:
                                    await command_log_and_err(ctx=ctx, client=self.client, status='Success',
                                                              used_on=member)
                                    await ctx.reply(
                                        f'I am forced to ban you {member.mention}... Well I sorta agreed to it too but... :)')
                                else:
                                    await command_log_and_err(ctx=ctx, client=self.client, err_code="Err_20324",
                                                              used_on=member,
                                                              text="Sorry I can't do that, missing permissions.")
                        except asyncio.TimeoutError:
                            await command_log_and_err(ctx=ctx, client=self.client, status="Request Timeout",
                                                      used_on=member)
                            await ctx.reply(f"Well then, no banning {member.mention} I suppose...")
                else:
                    await command_log_and_err(ctx=ctx, client=self.client, err_code="Err_20248",
                                              text="Gimme someone to ban...")
            else:
                await command_log_and_err(ctx=ctx, client=self.client, status="Command disabled here.", used_on=member)
                await ctx.reply(f"`Ban` is `disabled` in {ctx.channel.mention}")

    # 204
    @command(name="Unban", aliases=['ub'], usage='unban|ub <user>',
                      brief='🛂204', help='Unbans users from the server'
                      ' and invites them by looking through the servers'
                      ' bans list.')
    @guild_only()
    async def unban(self, ctx: Context, *, member: User = None):
        author = ctx.message.author
        if member:
            banned_users = await ctx.guild.bans()
            try:
                for ban_entry in banned_users:
                    user = ban_entry.user
                    if user.name == member.name or user.mention == member.mention:
                        await ctx.guild.unban(user)
                        await command_log_and_err(ctx=ctx, client=self.client,
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
                    client=self.client, err_code="Err_20424",
                    text=f"Unable to comply {author.mention}. Check $ecl"
                         f" for more info.")
        else:
            await command_log_and_err(ctx=ctx,
                    client=self.client, err_code="Err_20448",
                    text=f"Unbanning a person requires their username"
                         f" {author.mention}.")

    #205
    @command(name="Timeout", aliases=['to', 'isolate', 'isl'], usage="timeout|to|isolate|isl <member>",
             brief="205")
    @guild_only()
    async def g(self, ctx: Context):
        pass


def setup(client):
    client.add_cog(Mslo(client))
