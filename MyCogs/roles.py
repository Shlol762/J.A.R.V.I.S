from typing import Optional, Union
import discord
from discord.ext import commands
from MyCogs import command_log_and_err, set_timestamp, command,\
    Cog, cooldown, guild_only, BucketType, Context, has_permissions,\
    Client, Forbidden, Role, Member, Colour, Embed, HTTPException,\
    InvalidArgument

#commands.


class Roles(Cog):
    def __init__(self, client: Client):
        self.client = client
        self.description = 'Commands that deal with roles of server.'
        self.name = 'Roles'

    # 101
    @command(name="Create Role", aliases=['cr', 'createrole'],
                      help='Creates a role with a default name "New role"',
                      usage='createrole|cr (role name)', brief='🆕101')
    @cooldown(1, 60, BucketType.guild)
    @guild_only()
    async def createrole(self, ctx: Context, *,
                         name: Optional[str] = 'New role.'):
        author = ctx.message.author
        if name:
            try:
                guild = ctx.guild
                role = await guild.create_role(name=name)
                await command_log_and_err(ctx, self.client, status='Success',
                                          created=role)
                await ctx.reply(f"New role {role.mention} has been created")
            except Forbidden:
                await command_log_and_err(ctx=ctx, client=self.client, err_code='Err_10124',
                        text=f'Unable to comply {author.mention}. Check $ecl for more info.')
        else:
            await command_log_and_err(ctx=ctx, client=self.client, err_code='Err_10148',
                                      text=f'Give the new role a name {author.mention}.')

    # 102
    @command(name="Delete Role", aliases=['dr', 'delrole'],
                      help='Deleted a selected role.',
                      usage='delrole|dr <role>', brief='🗑102')
    @cooldown(1, 60, BucketType.guild)
    @guild_only()
    async def delrole(self, ctx: Context, *, role: Role = None):
        author = ctx.message.author
        role_b4_del = role.name
        if role:
            try:
                await command_log_and_err(ctx, self.client, 'Success', deleted=role)
                await role.delete(reason=None)
                await ctx.reply(f"The role {role_b4_del} has been deleted!")
            except Forbidden:
                await command_log_and_err(ctx=ctx, client=self.client, err_code='Err_10224',
                        text=f'Unable to comply {author.mention}. Check $ecl for more info.')
        else:
            await command_log_and_err(ctx=ctx, client=self.client, err_code='Err_10248',
                                      text=f'Give a role to delete {author.mention}.')

    # 103
    @command(name="Add Role", aliases=['ar', 'addrole'],
                      help='Adds a role onto a member.',
                      usage='addrole|ar <member> <role>', brief='➕103')
    @cooldown(1, 10, BucketType.member)
    @guild_only()
    @has_permissions(manage_roles=True)
    async def addrole(self, ctx: Context, member: Member = None,
                      role: Role = None):
        author = ctx.message.author
        if member:
            if role:
                if role.permissions.administrator:
                    await ctx.reply(
    f"Well {author.mention}... Your trying to add a role that has admin permissions. Sorry!")
                    await command_log_and_err(ctx, self.client,
                                           f'{role.mention} has `Administrator` permissions')
                else:
                    try:
                        await command_log_and_err(
                            ctx, self.client, 'Success', used_on=member)
                        await member.add_roles(role)
                        await ctx.reply(
                            f'{member.mention} has been given the role `{role.name}`.')
                    except Forbidden:
                        await command_log_and_err(ctx=ctx, client=self.client, err_code='Err_10324',
                                    text='Unable to comply {}. Check $ecl for more info.'.format(
                                                      author.mention))
            else:
                await command_log_and_err(ctx, self.client, err_code='Err_10348',
                                          text=f'Uhh {author.mention}, mention role please?')
        else:
            await command_log_and_err(ctx, self.client, err_code='Err_10348',
                                      text=f'Mention member, dumdum {author.mention}...')

    # 104
    @command(name="Remove Role", aliases=['rr', 'removerole'],
                      help='Removes a role from a member.',
                      usage='removerole|rr <member> <role>', brief='➖104')
    @cooldown(1, 10, BucketType.member)
    @guild_only()
    async def removerole(self, ctx, member: Member = None, role: Role = None):
        author = ctx.message.author
        if member:
            if role:
                try:
                    await command_log_and_err(ctx, self.client, 'Success', used_on=member)
                    await member.remove_roles(role)
                    await ctx.reply(f'{member.mention} has been removed from the role `{role.name}`.')
                except Forbidden:
                    await command_log_and_err(ctx=ctx, client=self.client, err_code='Err_10424',
                            text=f'Unable to comply {author.mention}. Check $ecl for more info.')
            else:
                await command_log_and_err(ctx, self.client, err_code='Err_10448',
                                          text=f'Uhh {author.mention}, mention role please?')
        else:
            await command_log_and_err(ctx, self.client, err_code='Err_10448',
                                      text=f'Mention member, dumdum {author.mention}...')

    # 105
    @command(name="Edit Role", aliases=['er'],
                      usage='editrole|er <role> <the attribute to be edited> <val of attr>',
                      help='Edits a role. In the "val of attr" slot, you type Numbers for Heirarchy,'
                      ' True/False for Permissions and displaying members seperately and Alphabets for Name',
                      brief="✏105")
    @cooldown(1, 60, BucketType.guild)
    @guild_only()
    async def editrole(self, ctx: Context, role: Role = None, attribute: str = None,
                       *, attr_val: Union[str, int, bool] = None):
        author: Member = ctx.author
        confirm = False
        pi = False
        f_error = None
        u_error = None
        colour = Colour.random()
        async with ctx.typing():
            if role:
                if attribute:
                    attr_l = attribute.lower()
                    if attr_val:
                        attr_v_l = attr_val.lower()
                        perms = role.permissions
                        if attr_l == 'name':
                            try: await role.edit(name=attr_val)
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {role.mention}'s name to {attr_val}"
                        # Permissions Start from here
                        elif attr_l == 'admin':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(administrator=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'add reaction':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(add_reactions=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'attach files':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(attach_files=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'ban members':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(ban_members=pi)
                                try:
                                    await role.edit(permissions=perms)
                                except Forbidden:
                                    f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'change nickname':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(change_nickname=pi)
                                try:
                                    await role.edit(permissions=perms)
                                except Forbidden:
                                    f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'connect':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(connect=pi)
                                try:
                                    await role.edit(permissions=perms)
                                except Forbidden:
                                    f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'create instant invite':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(create_instant_invite=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'deafen members':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(deafen_members=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'embed links':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(embed_links=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'external emoji':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(external_emoji=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'kick members':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(kick_members=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'manage channels':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(manage_channels=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'manage emojis':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(manage_emojis=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'manage guild':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(manage_guild=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'manage messages':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(manage_messages=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'manage nicknames':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(manage_nicknames=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'manage permissions':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(manage_permissions=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'manage roles':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(manage_roles=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'manage webhooks':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(manage_webhooks=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'mention everyone':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(mention_everyone=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'move members':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(move_members=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'mute members':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(mute_members=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'priority speaker':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(priority_speaker=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'read message history':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(read_message_history=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'read messages':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(read_messages=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'request to speak':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(request_to_speak=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'send messages':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(send_messages=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'send tts messages':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(send_tts_messages=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'speak':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(speak=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'stream':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(stream=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'use slash commands':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(use_slash_commands=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'use voice activation':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(use_voice_activation=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'view audit log':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(view_audit_log=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'view channel':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(view_channel=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'view guild insights':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            if pi is True or pi is False:
                                perms.update(view_guild_insights=pi)
                                try: await role.edit(permissions=perms)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'all':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            try: await role.edit(permissions=perms.all() if pi is True else perms.none())
                            except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        elif attr_l == 'general':
                            if attr_v_l == 'true': pi = True
                            elif attr_v_l == 'false': pi = False
                            else: pi = None
                            try: await role.edit(permissions=perms.general() if pi is True else perms.none())
                            except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` permission to `{pi}`"
                        # Permissions End here.
                        elif attr_l == 'colour' or attr_l == 'color':
                            rgb = attr_v_l.split(",")
                            hex = attr_v_l.removeprefix("0x")
                            if len(rgb) == 3:
                                for colour in rgb:
                                    if len(colour.strip()) > 3 or '.' in colour:
                                        u_error = f"Sorry {author.mention}, you have given an invlaid `RGB` colour code: `{attr_v_l}`. Take care not to include decimal points."
                                        break
                                if not u_error:
                                    colour = Colour.from_rgb(int(rgb[0]), int(rgb[1]), int(rgb[2]))
                                    try: await role.edit(colour=colour)
                                    except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` to {attr_v_l}"
                            elif len(hex) == 6:
                                colour = int('0x'+hex, base=16)
                                try: await role.edit(colour=colour)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` to {attr_v_l}"
                            else: u_error = f"Sorry {author.mention}, you have given an invlaid colour code: `{attr_v_l}`"
                        elif attr_l == 'display seperate' or attr_l == 'hoist':
                            if attr_v_l == 'true': confirm = True
                            elif attr_v_l == 'false': confirm = False
                            else: confirm = None
                            if confirm is True or confirm is False:
                                try: await role.edit(hoist=confirm)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` to `{confirm}`"
                        elif attr_l == 'mentionable':
                            if attr_v_l == 'true': confirm = True
                            elif attr_v_l == 'false': confirm = False
                            else: confirm = None
                            if confirm is True or confirm is False:
                                try: await role.edit(mentionable=confirm)
                                except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` to `{confirm}`"
                        elif attr_l == 'position':
                            try: await role.edit(position=len(ctx.guild.roles)-int(attr_v_l))
                            except Forbidden: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` to {attr_v_l}"
                            except HTTPException: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` to {attr_v_l}"
                            except InvalidArgument: f_error = f"Sorry {author.mention}, can't set {role.mention}'s `{attribute.capitalize()}` to below {len(ctx.guild.roles)-1}"
                        if f_error or u_error: await command_log_and_err(ctx, self.client, err_code='10524' if f_error and not u_error else '10512', text=f_error or u_error)
                        elif pi is None: await command_log_and_err(ctx, self.client, err_code='10512', text="Please give only `True` or `False` while setting `permissions`")
                        elif confirm is None: await command_log_and_err(ctx, self.client, err_code='10512', text="Please give only `True` or `False` while setting `mentionable` and `display seperately`")
                        else:
                            await command_log_and_err(ctx, self.client, status="Success")
                            await ctx.reply(embed=await set_timestamp(Embed(title='Edited Role', description=
                            f"""
        {role.mention if role.name != '@everyone' else '@everyone'}'s `{attribute}`{' permission' if pi else ''} has been set to `{attr_v_l.capitalize()}`""".replace("@@everyone", "@everyone"),
                                                               colour=colour), 'Edited'))
                    else:
                        await command_log_and_err(ctx, self.client, err_code="10548", text=f"{author.mention}, you haven't specified the value of {attribute}")
                else:
                    await command_log_and_err(ctx, self.client, err_code="10548", text=f"{author.mention}, you haven't given what to edit...")
            else:
                await command_log_and_err(ctx, self.client, err_code="10548", text=f"{author.mention}, you haven't given a role to edit.")

    @command(name="Add to all", aliases=['addtoall', 'ata'],
                      usage='addtoall|ata <role>',
                      help='Adds one role to all members', brief='➕106')
    @guild_only()
    @has_permissions(administrator=True)
    @cooldown(1, 20, BucketType.role)
    async def addtoall(self, ctx: Context, role: Role):
        async with ctx.typing():
            for member in ctx.guild.members:
                member: Member = member
                try:
                    await member.add_roles(role)
                except Forbidden:
                    await ctx.reply(f"Can't add the role `{role.name}` to `{member.name}`'s roles", delete_after=10)
            await ctx.reply("I've done all I can")


def setup(client):
    client.add_cog(Roles(client))
