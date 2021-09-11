from typing import Union, Optional
from MyCogs import calculate_position, permission_confirm, \
    role_member_conv, set_timestamp, command_log_and_err, \
    Context, Cog, command, cooldown, guild_only, ChannelNotFound,\
    RoleConverter, MemberConverter, BucketType, ThreadNotFound,\
    VoiceChannel, TextChannel, Embed, Colour, VoiceRegion,\
    CategoryChannel, Member, Forbidden, HTTPException, Role,\
    timezone, GuildChannel, Message, Bot, ThreadConfirmation, Thread, comm_log_local


class Cc(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.name: str = 'Channel Control(cc)'
        self.description = "Controls functions over text, voice and category channels."

    # 501
    @command(name="Create Channel or Category", aliases=['ccc', 'createcc'], extras={'emoji': '🆕', 'number': '501'},
                      help="Creates a new text channel, voice channel or category. Note that the cateogry arg will not be required if you are creating a category.",
                      usage='createcc|ccc <name> <text/voice/category> (cateogry new channel will be in)')
    @cooldown(1, 15, BucketType.guild)
    @guild_only()
    @comm_log_local
    async def createchnlctgry(self, ctx: Context, name: str = None, ch_tp: str = None, *,
                              category: Optional[Union[str, CategoryChannel]] = None):
        author: Member = ctx.message.author
        ctgry: str = 'None'
        if category:
            channels: list[CategoryChannel] = ctx.guild.categories
            for channel in channels:
                if channel.name.lower() == category.lower(): ctgry: CategoryChannel = channel
        if name:
            if ch_tp:
                try:
                    if ch_tp.lower() == 'text':
                        type: str = 'text channel'
                        chnl: TextChannel = await ctx.guild.create_text_channel(name=name, category=ctgry)
                    elif ch_tp.lower() == 'voice':
                        type: str = 'voice channel'
                        chnl: VoiceChannel = await ctx.guild.create_voice_channel(name=name, category=ctgry)
                    elif ch_tp.lower() == 'category':
                        type: str = 'category'
                        chnl: CategoryChannel = await ctx.guild.create_category(name=name)
                    embed = Embed(title=f"Created a new {type}", colour=Colour.random(),
                                          description=f"{chnl.mention}").add_field(name='Name: ',
                                                                                   value=f"`{chnl.name}`").add_field(
                        name='ID: ', value=f"`{chnl.id}`").add_field(name='Category: ',
                                                                     value=f"`{ctgry.name if ctgry != 'None' else ctgry}`")
                    await command_log_and_err(ctx, status='success', created=chnl)
                    await ctx.reply(embed=await set_timestamp(embed, ""))
                except Forbidden: await command_log_and_err(ctx, err_code="Err_50124",
                                              text=f"Can't do that {author.mention}, sorry I'm missing permissions")
            else: await command_log_and_err(ctx, err_code="Err_50148",
                                          text="Give channel type please.")
        else: await command_log_and_err(ctx, err_code="Err_50148",
                                      text='Give name for new channel please...')

    # 502
    @command(name="Delete Channel or Cateogry", aliases=['dcc', 'delcc'],
                      help='Deletes a text channel, voice channel or category.',
                      usage='delchnlctgry|dcc <channel/category>', extras={'emoji': '🗑', 'number': '502'})
    @cooldown(1, 15, BucketType.guild)
    @guild_only()
    @comm_log_local
    async def delchnlctgry(self, ctx: Context, *, channel: Union[CategoryChannel, VoiceChannel, TextChannel] = None):
        author: Member = ctx.message.author
        del_chnl: GuildChannel = channel
        if channel:
            type: bool = None
            if isinstance(channel, TextChannel): type: str = 'text channel'
            elif isinstance(channel, VoiceChannel): type: str = 'voice channel'
            elif isinstance(channel, CategoryChannel): type: str = 'category'
            elif isinstance(channel, str): raise ChannelNotFound(argument=channel)
            try:
                await channel.delete(reason=None)
                await command_log_and_err(ctx, status="Success",
                                          deleted=del_chnl)
                await ctx.reply(
                    embed=await set_timestamp(
                        Embed(title=f'Deleted `{type}`', description=f"{channel.mention} - `{channel.name}`",
                                      colour=Colour.random()), "Created"))
            except Forbidden: await command_log_and_err(ctx, err_code="Err_50224",
                                          text=f"Missing permissions to delete `{type}` - {channel.mention}")
        else: await command_log_and_err(ctx, err_code="Err_50248",
                                      text=f"{author.mention}, Channel was not given to be deleted.")

    # 503
    @command(name='Pin', aliases=['pn'],
                      help='Pins a message with message link or id',
                      usage='pin|pn <message link/id>.', extras={'emoji': '📌', 'number': '503'})
    @cooldown(1, 3, BucketType.channel)
    @comm_log_local
    async def pin(self, ctx: Context, message: Message = None):
        author: Member = ctx.message.author
        if message:
            try:
                await message.pin()
                await command_log_and_err(ctx, status='Success', created=message)
                time: str = message.created_at.replace(tzinfo=timezone("UTC")).astimezone(timezone("Asia/Kolkata")).strftime(
                    "%d %b %Y at %I:%M %p")
                await ctx.reply(embed=await set_timestamp(Embed(title="Pinned a message.",
                               description=f"ID: `{message.id}`\n Content: {message.content}\n Author: {message.author.mention}\n Time of sending: `{time}`\n Pinned by: {author.mention}",
                               colour=Colour.random()), "Pinned"))
            except Forbidden: await command_log_and_err(ctx, err_code="Err_50324",
                                          text="Missing permissions to pin message.")
            except HTTPException: await command_log_and_err(ctx, err_code="Err_50312",
                                          text="Max pins reached. Unpin a message and try again.")
        else: await command_log_and_err(ctx, err_code="Err_50348",
                                      text="Give message to pin.")

    # 504
    @command(name='Unpin', aliases=['unpn'],
                      help='Unpins a message with message link or id',
                      usage='unpin|unpn <message link/id>.', extras={'emoji': '📌', 'number': '504'})
    @cooldown(1, 3, BucketType.channel)
    @comm_log_local
    async def unpin(self, ctx: Context, message: Message = None):
        author: Member = ctx.message.author
        if message:
            try:
                await message.unpin()
                await command_log_and_err(ctx=ctx, status="Success", deleted=message)
                time = message.created_at.replace(tzinfo=timezone("UTC")).astimezone(timezone("Asia/Kolkata")).strftime(
                    "%d %b %Y at %I:%M %p")
                await ctx.reply(embed=await set_timestamp(Embed(title="Unpinned a message.",
                                                                       description=f"ID: `{message.id}`\n Content: {message.content}\n Author: {message.author.mention}\n Time of sending: `{time}`",
                                                                       colour=Colour.random()), "Unpinned"))
            except Forbidden:
                await command_log_and_err(ctx=ctx, err_code="Err_50424",
                                          text=f"Missing permissions {author.mention}")
        else:
            await command_log_and_err(ctx=ctx, err_code="Err_50448",
                                      text="Give message to unpin.")

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
                        await ctx.reply(embed=await set_timestamp(Embed(title='Edited Channel', description=
                        f"""{channel.mention}'s `{attribute.capitalize()}` has been changed to `{attr_v_l.capitalize().strip()}`""" if pi == '' else
                                                                               f"""{"@everyone" if attr_l == '@everyone' else target.mention}'s `{perm_key_pair[0].capitalize()}` permissions in {channel.mention} have been set to `{perm_key_pair[1].strip().capitalize()}`""",
                        colour=colour), 'Edited'))
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
