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
    group, SelectChannelCategoryView as Sccv, Guild, IST, slash_command,\
    Param, utils, NotFound, AppCmdInter, Permissions


permissions = Param(None, name='permissions', desc='The permissions you want to change for the person.',
                    choices=['add reactions',
 'administrator',
 'attach files',
 'ban members',
 'change nickname',
 'create public threads',
 'deafen members',
 'embed links',
 'external emojis',
 'external stickers',
 'kick members',
 'manage channels',
 'manage emojis',
 'manage guild',
 'manage messages',
 'manage nicknames',
 'manage roles',
 'manage threads',
 'mention everyone',
 'move members',
 'mute members',
 'send messages',
 'send messages in threads',
 'send tts messages',
 'view audit log'])


class Cc(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.name: str = 'Channel Control(cc)'
        self.description = "Controls functions over text, voice and category channels."

    @slash_command(name="createchannel", description="Creates a new text channel, voice channel or category")
    @cooldown(1, 15, BucketType.guild)
    async def createchnl(self, itxn: AppCmdInter,
            _type: str = Param(name='type', desc='What type of channel?', choices=['text', 'voice', 'category']),
            name: str = Param(name='name', desc='Name of new channel')):
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
                                    colour=Colour.red()), ephemeral=True) if err_code else None

    @slash_command(name='deletechannel', description='Deletes a text channel, voice channel or category.')
    @guild_only()
    async def delchnl(self, itxn: AppCmdInter, channel: GuildChannel = Param(
                      name='channel', desc='The channel you want to delete')):
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
                                    colour=Colour.red()), ephemeral=True) if err_code else None

    @slash_command(name='pin', description='Pins a message.')
    async def pin(self, itxn: AppCmdInter, message: str = Param(name='message', desc='The message you want to pin [ID or link]',
                                                                     )):
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

    @slash_command(name='unpin', description='Unpin a message.')
    async def unpin(self, itxn: AppCmdInter, message: str = Param(name='message',
                                                             desc='The message you want to unpin [ID or link]')):
        err_code = text = None
        timestamp = datetime.datetime.now(IST)
        pins = await itxn.channel.pins()
        try:
            message: Message = await itxn.channel.fetch_message(int(message.split('/')[-1]))
            in_pins = message in pins
            await message.unpin()
            time = f'<t:{int(message.created_at.timestamp() + 19800 / 1000)}:F>'
            await itxn.send("This isn't pinned btw." if not in_pins else None, embed=Embed(title="Unpinned a message.",
                                       description=f"""
`Message ID     `: `{message.id}`
`Message Content`: {message.content[:33] + ('...' if len(message.content)>33 else '')}
`Message Author `: {message.author.mention}
`Time of sending`: {time}""",
                               colour=Colour.random(), timestamp=timestamp) if in_pins else utils.MISSING,
                            ephemeral=True)
        except Forbidden: err_code, text = "Err_50424", "Missing `manage messages` permissions."
        except HTTPException: err_code, text = "Err_50412", "Failed to unpin message."
        await itxn.send(embed=Embed(title='Error', description=text, timestamp=timestamp,
                                    colour=Colour.red()), ephemeral=True) if err_code else None

    @slash_command(description="Edits a chosen channel")
    async def editchannel(self, itxn: AppCmdInter, channel: GuildChannel = Param(
                      name='channel', desc='The channel you want to edit'),
                          attribute: str = Param(name='property', desc='The property of channel you want to edit.',
                                                 choices=['name', 'topic', 'category',
                                                          'nsfw', 'sync perms', 'slowmo delay',
                                                          'bitrate', 'user limit', 'voice region']),
                          attr_val: str = Param(name='value')):
        f_error = None
        u_error = None
        attr_l = attribute.lower()
        attr_v_l = attr_val.lower()
        author: Member = itxn.author
        perm_key_pair = attr_v_l.split(':')
        target = attribute
        if attr_val == 'true':
            confirm = True
        elif attr_val == 'false':
            confirm = False
        else:
            confirm = None
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
                    for category in itxn.guild.categories:
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
                try: await channel.edit(nsfw=confirm)
                except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} to {attr_val}"
            else:  u_error = f"You can only edit `nsfw` for `Text Channels` and `Categories`, {channel.mention} isn't either of them."
        elif attr_l == 'sync perms':
            if not isinstance(channel, CategoryChannel):
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
            else:  u_error = f"You can only edit `Bitrate` for `Voice Channels`, and {channel.mention} is not a `Voice Channel`."
        elif attr_l == 'user limit':
            if isinstance(channel, VoiceChannel):
                try: await channel.edit(user_limit=int(attr_val))
                except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} to {attr_val}"
                except ValueError: u_error = f"You can only set `User limit` to a numeric value."
            else: u_error = f"You can only edit `User Limit` for `Voice Channels`, and {channel.mention} is not a `Voice Channel`."
        elif attr_l == 'voice region':
            if isinstance(channel, VoiceChannel):
                try: await channel.edit(rtc_region=attr_v_l)
                except Forbidden: f_error = f"Sorry {author.mention}, I can't set {channel.mention}'s {attribute.capitalize()} to {attr_val}"
                except HTTPException: u_error = f'`{attr_v_l.capitalize()}` is not a valid `RTC Region`'
            else: u_error = f"You can only edit `RTC Region` for `Voice Channels`, and {channel.mention} is not a `Voice Channel`."
        if f_error or u_error: pass
        elif pi == 'None': pass
        elif confirm is None: pass
        else:
            await itxn.send(embed=Embed(title='Edited Channel', description = f"""{channel.mention}'s `{attribute.capitalize()}` has been changed to `{attr_v_l.capitalize().strip()}`""",
            colour=Colour.random(), timestamp=datetime.datetime.now(IST)), ephemeral=True)



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
