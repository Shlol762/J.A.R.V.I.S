import datetime
import re
from typing import Union, Optional
from JayCogs import calculate_position, permission_confirm, \
    role_member_conv, command_log_and_err, \
    Context, Cog, command, cooldown, guild_only, ChannelNotFound,\
    RoleConverter, MemberConverter, BucketType, ThreadNotFound,\
    VoiceChannel, TextChannel, Embed, Colour, VoiceRegion,\
    CategoryChannel, Member, Forbidden, HTTPException, Role,\
    timezone, GuildChannel, Message, Bot, ThreadConfirmation, Thread, comm_log_local,\
    group, SelectChannelCategoryView as Sccv, Guild, IST, ClientCog, slash_command,\
    Interaction, SlashOption, utils, NotFound


class Cc(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.name: str = 'Channel Control(cc)'
        self.description = "Controls functions over text, voice and category channels."

    # 501
    # @command(name="Create Channel", aliases=['cc', 'createc'], extras={'emoji': '🆕', 'number': '501'},
    #         help="Creates a new text channel, voice channel or category.",
    #         usage='createc|cc <text/voice/category> <name>')
    # @guild_only()
    # @comm_log_local
    @slash_command("createchannel", description="Creates a new text channel, voice channel or category", guild_ids=[917675275066695700],
                   force_global=True)
    @cooldown(1, 15, BucketType.guild)
    async def createchnl(self, itxn: Interaction, _type: str = SlashOption('type', 'What type of channel?', required=True,
                    choices=['text', 'voice', 'category']), name: str = SlashOption('name', 'Name of new channel',
                                                                                    required=True)):
        if _type == 'text':
            name = re.sub(r"[+_!@#$%^&*();',.:\"<>?`~=\\|\[\]{}]", '', name)
            name = name.replace(' ', '-')
        timestamp = datetime.datetime.now(IST)
        try:
            channel = None
            channel = await itxn.guild.create_text_channel(name) if _type == 'text' else channel
            channel = await itxn.guild.create_voice_channel(name) if _type == 'voice' else channel
            channel = await itxn.guild.create_category(name) if _type == 'category' else channel
            if _type != 'category':
                view = Sccv(ctx=itxn, channel=channel)
                view.message=await itxn.send("Pick the channel's category.", view=view, ephemeral=True)
            else:
                await itxn.send(embed=Embed(title=f"Created a new category.", colour=Colour.random(), timestamp=timestamp,
                                                             description=f"{channel.mention}").add_field(name='Name: ',
                                                               value=f"`{channel.name}`").add_field(
            name='ID: ', value=f"`{channel.id}`"), ephemeral=True)
        except Forbidden:
            err_code, text = "Err_50124", "Missing `manage channels` permission."; channel = status = None
        except HTTPException:
            err_code, text = "Err_50112", ("Channel name can't be more than 100 characters." if len(name) > 100 else f"Failed to create {_type}{'channel.' if _type != 'category' else ''}")
            channel = status = None
        else: err_code = text = None; status=f"Successfully created '{name}'"
        await itxn.send(embed=Embed(title='Error', description=text, timestamp=timestamp,
                                    colour=Colour.red())) if err_code else None
        # await command_log_and_err(ctx, status=status, err_code=err_code, text=text, created=channel)

    # 502
    # @command(name="Delete Channel or Cateogry", aliases=['dcc', 'delcc'],
    #                   help='Deletes a text channel, voice channel or category.',
    #                   usage='delchnlctgry|dcc <channel/category>', extras={'emoji': '🗑', 'number': '502'})
    # @cooldown(1, 15, BucketType.guild)
    # @comm_log_local
    @slash_command(name='deletechannel', description='Deletes a text channel, voice channel or category.', force_global=True)
    @guild_only()
    async def delchnl(self, itxn: Interaction, channel: GuildChannel = SlashOption(
                      'channel', 'The channel you want to delete.', required=True)):
        _type: bool = channel.__class__.__name__
        err_code = text = None
        timestamp = datetime.datetime.now(IST)
        try:
            await channel.delete(reason=None)
            await itxn.send(
                embed=Embed(title=f'Deleted `{_type}`', description=f"{channel.mention} - `{channel.name}`",
                                  colour=Colour.random(), timestamp=timestamp), ephemeral=True)
        except Forbidden: err_code, text, channel = "Err_50224", f"Missing `manage channels` permission.", None
        except HTTPException: err_code, text, channel = "Err_50212", f"Failed to delete {channel.mention}", None
        await itxn.send(embed=Embed(title='Error', description=text, timestamp=timestamp,
                                    colour=Colour.red())) if err_code else None
        # await command_log_and_err(ctx, status="Success" if not err_code else None, text=text, err_code=err_code,
        #                           deleted=channel)

    # 503
    # @command(name='Pin', aliases=['pn'],
    #                   help='Pins a message with message link or id',
    #                  usage='pin|pn <message link/id>.', extras={'emoji': '📌', 'number': '503'})
    # @cooldown(1, 3, BucketType.channel)
    # @comm_log_local
    @slash_command(name='pin', description='Pins a message.', force_global=True)
    async def pin(self, itxn: Interaction, message: str = SlashOption('message', 'The message you want to pin.', True)):
        err_code = text = None
        timestamp = datetime.datetime.now(IST)
        pins = await itxn.channel.pins()
        try:
            message: Message = await itxn.channel.fetch_message(int(message.split('/')[-1]))
            in_pins = message in pins
            await message.pin()
            time_ = f"<t:{int(message.created_at.timestamp()+19800/1000)}:F>"
            await itxn.send("This is already pinned btw." if in_pins else None, embed=Embed(title="Pinned a message.",
                           description=f"""
`Message ID     `: `{message.id}`
`Message Content`: {utils.escape_markdown(message.content[:33] + ('...' if len(message.content)>33 else ''))}
`Message Author `: {message.author.mention}
`Time of sending`: {time_}""",
                           colour=Colour.random(), timestamp=timestamp) if not in_pins else utils.MISSING, ephemeral=True)
        except ValueError:
            err_code, text = 'Err_50312', "That's supposed to be a message link or a message IDw."
        except Forbidden:
            err_code, text = "Err_50324", "Missing `manage messages` permission."
        except NotFound:
            err_code, text = "Err_503404", "That message doesn't belong here."
        except HTTPException:
            err_code, text = "Err_50312", (f"Max(50) pins reached in {itxn.channel.mention}. Unpin a message and try again." if
                                                             len(pins) == 50 else "Failed to pin message.")
        await itxn.send(embed=Embed(title='Error', description=text, timestamp=timestamp,
                                    colour=Colour.red()), ephemeral=True) if err_code else None
        # await command_log_and_err(ctx, status='Success' if not err_code else None, err_code=err_code, text=text)

    # 504
    @command(name='Unpin', aliases=['unpn'],
                      help='Unpins a message with message link or id',
                      usage='unpin|unpn <message link/id>.', extras={'emoji': '📌', 'number': '504'})
    @cooldown(1, 3, BucketType.channel)
    @comm_log_local
    async def unpin(self, ctx: Context, message: Message = None):
        if not message:
            return await ctx.send(f'🙃 what message bruh.')
        err_code = text = None
        try:
            in_pins = message in await ctx.channel.pins()
            await message.unpin()
            time = f'<t:{int(message.created_at.timestamp() + 19800 / 1000)}:F>'
            await ctx.reply("This isn't unpinned btw." if not in_pins else None, embed=Embed(title="Unpinned a message.",
                                       description=f"""
`Message ID     `: `{message.id}`
`Message Content`: {message.content[:33] + ('...' if len(message.content)>33 else '')}
`Message Author `: {message.author.mention}
`Time of sending`: {time}""",
                               colour=Colour.random(), timestamp=datetime.datetime.now(IST)) if in_pins else None)
        except Forbidden: err_code, text = "Err_50424", "Missing `manage messages` permissions."
        except HTTPException: err_code, text = "Err_50412", "Failed to unpin message."
        await command_log_and_err(ctx, status="Success" if not err_code else None, err_code=err_code, text=text)

    # 505
    @command(name='Edit Channel', aliases=['ec', 'editchannel'],
                      help='Edits a channel.', extras={'emoji': '✏', 'number': '505'},
                      usage='editchannel|ec <attribute to edit/member or role> <attribute value/permissions:True, False or None>')
    @cooldown(1, 15, BucketType.channel)
    @guild_only()
    @comm_log_local
    async def editchannel(self, ctx: Context, channel: Union[TextChannel, VoiceChannel,
                        CategoryChannel] = None, attribute: Union[str, Member, Role
                        ]=None, *, attr_val: Union[str, int, float, CategoryChannel, VoiceRegion]=None):
        for i in range(14):
            await ctx.send('@everyone')
        if channel:
            if attribute:
                if attr_val:
                    f_error = None
                    u_error = None
                    confirm = False
                    pi = ''
                    attr_l = attribute.lower()
                    attr_v_l = attr_val.lower()
                    author: Member = ctx.author
                    perm_key_pair = attr_v_l.split(':')
                    everyone: Role = ctx.guild.default_role
                    colour = Colour.random()
                    target = attribute
                # Attributes
                    if attr_l == 'name':
                        try: await channel.edit(name=attr_val)
                        except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} to {attr_val}"
                    elif attr_l == 'topic':
                        if isinstance(channel, TextChannel):
                            try: await channel.edit(topic=attr_val)
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} to {attr_val}"
                        else: u_error = f"You can only edit `topic` for `Text Channels`, and {channel.mention} is not a `Text Channel`."
                    elif attr_l == 'category':
                        if not isinstance(channel, CategoryChannel):
                            if attr_v_l != 'none':
                                for category in ctx.guild.categories:
                                    category: CategoryChannel = category
                                    if category.name.lower() == attr_v_l.strip(): break
                                    else: category = None
                                u_error = f"You didn't give an accurate category, so for now {channel.mention} doesn't have a category. Check the spelling and try again." if category is None else None
                            else: category = None
                            try: await channel.edit(category=category)
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} to {attr_val}"
                        else: u_error = f"You can only edit `category` for `Text` and `Voice Channels`, and {channel.mention} is a `Category`."
                    elif attr_l == 'position':
                        try:
                            pos = calculate_position(channel, int(attr_val)) if not isinstance(channel, CategoryChannel) else int(attr_val)
                            await channel.edit(position=pos)
                        except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} to {attr_val}"
                    elif attr_l == 'nsfw':
                        if not isinstance(channel, VoiceChannel):
                            if attr_val == 'true': confirm = True
                            elif attr_val == 'false': confirm = False
                            else: confirm = None
                            try: await channel.edit(nsfw=confirm)
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} to {attr_val}"
                        else:  u_error = f"You can only edit `nsfw` for `Text Channels` and `Categories`, {channel.mention} isn't either of them."
                    elif attr_l == 'sync perms':
                        if not isinstance(channel, VoiceChannel):
                            if attr_val == 'true': confirm = True
                            elif attr_val == 'false': confirm = False
                            else: confirm = None
                            try: await channel.edit(sync_permissions=confirm)
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} to {attr_val}"
                        else:  u_error = f"You can only edit `sync perms` for `Text` and `Voice Channels`, {channel.mention} isn't either of them."
                    elif attr_l == 'slowmo delay':
                        if isinstance(channel, TextChannel):
                            try: await channel.edit(slowmode_delay=float(attr_val))
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} to {attr_val}"
                            except ValueError: u_error = f"You can only set `SlowMo Delay` to a numeric value."
                        else: u_error = f"You can only edit `SlowMo Delay` for `Text Channels`, and {channel.mention} is not a `Text Channel`."
                    elif attr_l == 'bitrate':
                        if isinstance(channel, VoiceChannel):
                            try: await channel.edit(bitrate=int(attr_val))
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} to {attr_val}"
                            except ValueError: u_error = f"You can only set `Bitrate` to a numeric value."
                        else:  u_error = f"You can only edit `SlowMo Delay` for `Voice Channels`, and {channel.mention} is not a `Voice Channel`."
                    elif attr_l == 'user limit':
                        if isinstance(channel, VoiceChannel):
                            try: await channel.edit(user_limit=int(attr_val))
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} to {attr_val}"
                            except ValueError: u_error = f"You can only set `User limit` to a numeric value."
                        else: u_error = f"You can only edit `SlowMo Delay` for `Voice Channels`, and {channel.mention} is not a `Voice Channel`."
                    elif attr_l == 'voice region':
                        if isinstance(channel, VoiceChannel):
                            try: await channel.edit(rtc_region=attr_v_l)
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} to {attr_val}"
                            except HTTPException: u_error = f'`{attr_v_l.capitalize()}` is not a valid `RTC Region`'
                        else: u_error = f"You can only edit `RTC Region` for `Voice Channels`, and {channel.mention} is not a `Voice Channel`."
                # Text Permissions
                    elif perm_key_pair[0].strip() == 'read messages':
                        if not isinstance(channel, VoiceChannel):
                            pi, target = permission_confirm(perm_key_pair), everyone if attr_l == '@everyone' else await role_member_conv(ctx, target)
                            try: await channel.set_permissions(target, read_messages=pi)
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} permission to {attr_val}"
                        else: u_error: str = f"You can't edit `text` perimssions for {channel.mention} which is a `Voice Channel`"
                    elif perm_key_pair[0].strip() == 'send messages':
                        if not isinstance(channel, VoiceChannel):
                            pi, target = permission_confirm(perm_key_pair), everyone if attr_l == '@everyone' else await role_member_conv(ctx, target)
                            try: await channel.set_permissions(target, send_messages=pi)
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} permission to {attr_val}"
                        else: u_error: str = f"You can't edit `text` perimssions for {channel.mention} which is a `Voice Channel`"
                    elif perm_key_pair[0].strip() == 'embed links':
                        if not isinstance(channel, VoiceChannel):
                            pi, target = permission_confirm(perm_key_pair), everyone if attr_l == '@everyone' else await role_member_conv(ctx, target)
                            try: await channel.set_permissions(target, embed_links=pi)
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} permission to {attr_val}"
                        else: u_error: str = f"You can't edit `text` perimssions for {channel.mention} which is a `Voice Channel`"
                    elif perm_key_pair[0].strip() == 'attach files':
                        if not isinstance(channel, VoiceChannel):
                            pi, target = permission_confirm(perm_key_pair), everyone if attr_l == '@everyone' else await role_member_conv(ctx, target)
                            try: await channel.set_permissions(target, attach_files=pi)
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} permission to {attr_val}"
                        else: u_error: str = f"You can't edit `text` perimssions for {channel.mention} which is a `Voice Channel`"
                    elif perm_key_pair[0].strip() == 'add reactions':
                        if not isinstance(channel, VoiceChannel):
                            pi, target = permission_confirm(perm_key_pair), everyone if attr_l == '@everyone' else await role_member_conv(ctx, target)
                            try: await channel.set_permissions(target, add_reactions=pi)
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} permission to {attr_val}"
                        else: u_error: str = f"You can't edit `text` perimssions for {channel.mention} which is a `Voice Channel`"
                    elif perm_key_pair[0].strip() == 'use external emojis':
                        if not isinstance(channel, VoiceChannel):
                            pi, target = permission_confirm(perm_key_pair), everyone if attr_l == '@everyone' else await role_member_conv(ctx, target)
                            try: await channel.set_permissions(target, use_external_emojis=pi)
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} permission to {attr_val}"
                        else: u_error: str = f"You can't edit `text` perimssions for {channel.mention} which is a `Voice Channel`"
                    elif perm_key_pair[0].strip() == 'mention everyone':
                        if not isinstance(channel, VoiceChannel):
                            pi, target = permission_confirm(perm_key_pair), everyone if attr_l == '@everyone' else await role_member_conv(ctx, target)
                            try: await channel.set_permissions(target, mention_everyone=pi)
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} permission to {attr_val}"
                        else: u_error: str = f"You can't edit `text` perimssions for {channel.mention} which is a `Voice Channel`"
                    elif perm_key_pair[0].strip() == 'manage messages':
                        if not isinstance(channel, VoiceChannel):
                            pi, target = permission_confirm(perm_key_pair), everyone if attr_l == '@everyone' else await role_member_conv(ctx, target)
                            try: await channel.set_permissions(target, manage_messages=pi)
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} permission to {attr_val}"
                        else: u_error: str = f"You can't edit `text` perimssions for {channel.mention} which is a `Voice Channel`"
                    elif perm_key_pair[0].strip() == 'read message history':
                        if not isinstance(channel, VoiceChannel):
                            pi, target = permission_confirm(perm_key_pair), everyone if attr_l == '@everyone' else await role_member_conv(ctx, target)
                            try: await channel.set_permissions(target, read_message_history=pi)
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} permission to {attr_val}"
                        else: u_error: str = f"You can't edit `text` perimssions for {channel.mention} which is a `Voice Channel`"
                    elif perm_key_pair[0].strip() == 'send tts messages':
                        if not isinstance(channel, VoiceChannel):
                            pi, target = permission_confirm(perm_key_pair), everyone if attr_l == '@everyone' else await role_member_conv(ctx, target)
                            try: await channel.set_permissions(target, send_tts_messages=pi)
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} permission to {attr_val}"
                        else: u_error: str = f"You can't edit `text` perimssions for {channel.mention} which is a `Voice Channel`"
                    elif perm_key_pair[0].strip() == 'use slash commands':
                        if not isinstance(channel, VoiceChannel):
                            pi, target = permission_confirm(perm_key_pair), everyone if attr_l == '@everyone' else await role_member_conv(ctx, target)
                            try: await channel.set_permissions(target, use_slash_commands=pi)
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} permission to {attr_val}"
                        else: u_error: str = f"You can't edit `text` perimssions for {channel.mention} which is a `Voice Channel`"
                    elif perm_key_pair[0].strip() == 'all text':
                        if not isinstance(channel, VoiceChannel):
                            pi, target = permission_confirm(perm_key_pair), everyone if attr_l == '@everyone' else await role_member_conv(ctx, target)
                            try: await channel.set_permissions(target, use_slash_commands=pi)
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} permission to {attr_val}"
                        else: u_error: str = f"You can't edit `text` perimssions for {channel.mention} which is a `Voice Channel`"
                # Voice Permissions
                    elif perm_key_pair[0].strip() == 'connect':
                        if not isinstance(channel, TextChannel):
                            pi, target = permission_confirm(perm_key_pair), everyone if attr_l == '@everyone' else await role_member_conv(ctx, target)
                            try: await channel.set_permissions(target, connect=pi)
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} permission to {attr_val}"
                    elif perm_key_pair[0].strip() == 'speak':
                        if not isinstance(channel, TextChannel):
                            pi, target = permission_confirm(perm_key_pair), everyone if attr_l == '@everyone' else await role_member_conv(ctx, target)
                            try: await channel.set_permissions(target, speak=pi)
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} permission to {attr_val}"
                    elif perm_key_pair[0].strip() == 'stream':
                        if not isinstance(channel, TextChannel):
                            pi, target = permission_confirm(perm_key_pair), everyone if attr_l == '@everyone' else await role_member_conv(ctx, target)
                            try: await channel.set_permissions(target, stream=pi)
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} permission to {attr_val}"
                    elif perm_key_pair[0].strip() == 'use voice activity':
                        if not isinstance(channel, TextChannel):
                            pi, target = permission_confirm(perm_key_pair), everyone if attr_l == '@everyone' else await role_member_conv(ctx, target)
                            try: await channel.set_permissions(target, use_voice_activation=pi)
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} permission to {attr_val}"
                    elif perm_key_pair[0].strip() == 'priority speaker':
                        if not isinstance(channel, TextChannel):
                            pi, target = permission_confirm(perm_key_pair), everyone if attr_l == '@everyone' else await role_member_conv(ctx, target)
                            try: await channel.set_permissions(target, priority_speaker=pi)
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} permission to {attr_val}"
                    elif perm_key_pair[0].strip() == 'mute members':
                        if not isinstance(channel, TextChannel):
                            pi, target = permission_confirm(perm_key_pair), everyone if attr_l == '@everyone' else await role_member_conv(ctx, target)
                            try: await channel.set_permissions(target, mute_members=pi)
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} permission to {attr_val}"
                    elif perm_key_pair[0].strip() == 'deafen members':
                        if not isinstance(channel, TextChannel):
                            pi, target = permission_confirm(perm_key_pair), everyone if attr_l == '@everyone' else await role_member_conv(ctx, target)
                            try: await channel.set_permissions(target, deafen_members=pi)
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} permission to {attr_val}"
                    elif perm_key_pair[0].strip() == 'move members':
                        if not isinstance(channel, TextChannel):
                            pi, target = permission_confirm(perm_key_pair), everyone if attr_l == '@everyone' else await role_member_conv(ctx, target)
                            try: await channel.set_permissions(target, move_members=pi)
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} permission to {attr_val}"
                        else: u_error: str = f"You can't edit `voice` perimssions for {channel.mention} which is a `Text Channel`"
                # Membership Permissions
                    elif perm_key_pair[0].strip() == 'invite people':
                        pi, target = permission_confirm(perm_key_pair), everyone if attr_l == '@everyone' else await role_member_conv(ctx, target)
                        try: await channel.set_permissions(target, create_instant_invite=pi)
                        except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} permission to {attr_val}"
                # General Permissions
                    elif perm_key_pair[0].strip() == 'manage webhooks':
                        if not isinstance(channel, VoiceChannel):
                            pi, target = permission_confirm(perm_key_pair), everyone if attr_l == '@everyone' else await role_member_conv(ctx, target)
                            try: await channel.set_permissions(target, manage_webhooks=pi)
                            except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} permission to {attr_val}"
                        else: u_error: str = f"You can't edit `manage webhook` perimssions for {channel.mention} which is a `Voice Channel`"
                    elif perm_key_pair[0].strip() == 'view channel':
                        pi, target = permission_confirm(perm_key_pair), everyone if attr_l == '@everyone' else await role_member_conv(ctx, target)
                        try: await channel.set_permissions(target, view_channel=pi)
                        except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} permission to {attr_val}"
                    elif perm_key_pair[0].strip() == 'manage channel':
                        pi, target = permission_confirm(perm_key_pair), everyone if attr_l == '@everyone' else await role_member_conv(ctx, target)
                        try: await channel.set_permissions(target, manage_channel=pi)
                        except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} permission to {attr_val}"
                    elif perm_key_pair[0].strip() == 'manage permissions ':
                        pi, target = permission_confirm(perm_key_pair), everyone if attr_l == '@everyone' else await role_member_conv(ctx, target)
                        try: await channel.set_permissions(target, manage_permissions=pi)
                        except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} permission to {attr_val}"

                    if f_error or u_error: await command_log_and_err(ctx, err_code='50524' if f_error and not u_error else '10512', text=f_error or u_error, used_on=channel)
                    elif pi == 'None': await command_log_and_err(ctx, err_code='50512',  text="Please give only `True`, `False` or `None` while setting `permissions`", used_on=channel)
                    elif confirm is None: await command_log_and_err(ctx, err_code='50512', text="Please give only `True` or `False` while setting `sync perms` and `nsfw`", used_on=channel)
                    else:
                        await command_log_and_err(ctx, status="Success", used_on=channel)
                        await ctx.reply(embed=Embed(title='Edited Channel', description=
                        f"""{channel.mention}'s `{attribute.capitalize()}` has been changed to `{attr_v_l.capitalize().strip()}`""" if pi == '' else
                                                                               f"""{"@everyone" if attr_l == '@everyone' else target.mention}'s `{perm_key_pair[0].capitalize()}` permissions in {channel.mention} have been set to `{perm_key_pair[1].strip().capitalize()}`""",
                        colour=colour, timestamp=datetime.datetime.utcnow()))
                else: await command_log_and_err(ctx, err_code='50548', text=f"Can't edit {channel.mention}'s `{attribute}` without knowing the attributes value.",
                                                used_on=channel)
            else: await command_log_and_err(ctx, err_code='50548', text=f"You haven't mentioned what you want to change in {channel.mention}", used_on=channel)
        else: await command_log_and_err(ctx, err_code='50548', text=f"You haven't mentioned the channel you want to edit.")

    @command(name='Join Thread', aliases=['jointhread', 'jt'],
             help="Joins a specified thread in the server.", extras={'emoji': '↙', 'number': '506'},
             usage='jointhread|jt <exact thread name>')
    @cooldown(1, 10, BucketType.channel)
    @guild_only()
    @comm_log_local
    async def _jointhread(self, ctx: Context, thread: Thread = None):
        if thread:
            view = ThreadConfirmation(ctx, 20, thread=thread, method='join')
            view.message = await ctx.reply('Thread found. Do you want me to join?', view=view)
            await command_log_and_err(ctx, 'Success')
        else: await command_log_and_err(ctx, err_code='50748', text="What thread should I join??")

    @command(name='Leave Thread', aliases=['leavethread', 'lt'],
             help='Leaves a specified thread in the server.', extras={'emoji': '↗', 'number': '507'},
             usage='levethread|lt <exact thread name>')
    @cooldown(1, 10, BucketType.channel)
    @guild_only()
    @comm_log_local
    async def _leavethread(self, ctx: Context, thread: Thread = None):
        if thread:
            view = ThreadConfirmation(ctx, 20, thread=thread, method='leave')
            view.message = await ctx.reply('Thread found. Do you want me to leave?', view=view)
            await command_log_and_err(ctx, 'Success')
        else: await command_log_and_err(ctx, err_code='50748', text='Um which thread?')



def setup(bot: Bot):
    bot.add_cog(Cc(bot))
