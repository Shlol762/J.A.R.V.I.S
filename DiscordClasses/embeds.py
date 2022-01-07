import datetime
import os
from typing import Optional, Union
import nextcord
from nextcord import Message, Embed
from nextcord.ext import commands
from DiscordClasses.web_scrapers import Cricket
from DiscordClasses.custom_funcs import  reaction, image_join, time_set, download_images


class TypeDefError(Exception):
    pass


async def command_log_and_err(ctx: commands.Context = None, status: Optional[str] = None, *, error: Optional
                                [Union[commands.CommandOnCooldown, commands.NoPrivateMessage]] = None,
                              used_on: Optional[Union[nextcord.User, nextcord.Member, nextcord.Role, nextcord.abc.GuildChannel]] = None,
                              send=True, err_code: Optional[str] = None, text: Optional[str] = None,
                              invalid_comname: commands.CommandOnCooldown.args = None,
                              created: Optional
                              [Union[nextcord.Role, nextcord.abc.GuildChannel, nextcord.Message]] = None,
                              deleted: Optional
                              [Union[nextcord.Role, nextcord.abc.GuildChannel, nextcord.Message]] = None,
                              joined: Optional[nextcord.VoiceChannel] = None,
                              left: Optional[nextcord.VoiceChannel] = None) -> Optional[Message]:
    """Command logging system for the bot, logging every command's usage(except developer commands) to a channel on
    J.A.R.V.I.S's home server."""
    status = status if status else err_code
    bot: commands.Bot = ctx.bot
    if ctx and error:
        if isinstance(error, commands.CommandOnCooldown):
            embed_c = Embed(title=f"{ctx.command.qualified_name} is on cooldown.",
                                    description=f"Please wait for `{round(error.retry_after, 2)}` more seconds.",
                                    colour=nextcord.Colour.teal())
            embed_c.add_field(name=f"Cooldown period for {ctx.command.qualified_name}",
                              value=f"`{int(ctx.command._buckets._cooldown.per)}` seconds")
            await ctx.reply(embed=await set_timestamp(embed_c, "Cooldown"))
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.reply(f'**`{ctx.command.qualified_name}`** cannot be used in DMs')
            try: await reaction(ctx, False)
            except nextcord.Forbidden: pass
    if ctx and bot and err_code and text:
        embed = Embed(title="Error!", description=f"{text}\n\n", colour=nextcord.Colour.red())
        if err_code[-2:] != '24' and err_code[-2:] != '12':
            embed.description += f"`Usage`: {ctx.command.usage if ctx.command else 'Unusable'}"
        else: pass
        try: await reaction(ctx, False)
        except nextcord.Forbidden: pass
        embed.set_footer(icon_url=bot.user.avatar.url)
        embed.add_field(name="Code:", value=f"`{'Err_' + err_code if err_code[:2].lower() != 'err' and err_code[:-2].isnumeric() else err_code}`")
        await ctx.reply(embed=await set_timestamp(embed,
                                                 str(ctx.command.qualified_name if ctx.command else "Invalid"))) if send is True else None
    com_name: str = ctx.command.qualified_name if ctx.command else f"Invalid Command{f' - `{invalid_comname}`' if not ctx.command else ''}"
    time: datetime.datetime = datetime.datetime.now().strftime("%a, %b %dth %Y %I:%M:%S %p IST")
    e = Embed(title=f"{com_name}",
                      description=f"*`Used by`*: {ctx.author.mention}\n *`Timestamp`*: `{time}`\n *`Used in`*: {ctx.channel.mention if ctx.guild else ctx.author.dm_channel}{f'- `{ctx.guild.name}`' if ctx.guild else ''}\n *`Message Link`*: **[`Jump to message`]({ctx.message.jump_url})**\n",
                      colour=nextcord.Colour.red() if err_code else nextcord.Colour.green())
    chnl: nextcord.TextChannel = bot.get_channel(821677968967467068)
    if used_on: e.description += f'*`Used on`*: {used_on.mention}\n'
    if created:
        if isinstance(created, nextcord.Role):
            e.description += f'*`Created role`*: {created.mention}\n'
        elif isinstance(created, nextcord.abc.GuildChannel):
            if isinstance(created, nextcord.VoiceChannel):
                e.description += f'*`Created Voice channel`*: `{created.mention}`\n'
            elif isinstance(created, nextcord.TextChannel):
                e.description += f'*`Created Text channel`*: {created.mention}\n'
            elif isinstance(created, nextcord.CategoryChannel):
                e.description += f'*`Created category`*: `{created.mention}`\n'
        elif isinstance(created, nextcord.Message):
            e.description += f'*`Pinned Message`*: **[`Jump to message`]({created.jump_url})**\n'
        else: raise TypeDefError(f'{created} of type: {str(type(created))[1:-1]} cannot be used in command_log_and_err')
    if deleted:
        if isinstance(deleted, nextcord.Role):
            e.description += f'*`Deleted role`*: {deleted.name}\n'
        elif isinstance(deleted, nextcord.abc.GuildChannel):
            if isinstance(deleted, nextcord.VoiceChannel):
                e.description += f'*`Deleted Voice channel`*: `{deleted.name}`\n'
            elif isinstance(deleted, nextcord.TextChannel):
                e.description += f'*`Deleted Text channel`*: {deleted.name}\n'
            elif isinstance(deleted, nextcord.CategoryChannel):
                e.description += f'*`Deleted category`*: `{deleted.name}`\n'
        elif isinstance(deleted, nextcord.Message):
            e.description += f'*`Unpinned Message`*: **[link]({deleted.jump_url})**\n'
        else:
            raise TypeDefError(f'{created} of type: {str(type(created))[1:-1]} cannot be used in command_log_and_err')
    if joined:
        if isinstance(joined, nextcord.VoiceChannel):
            e.description += f'*`Joined`*: {joined.mention}\n'
        else:
            raise TypeDefError(f'{created} of type: {str(type(created))[1:-1]} cannot be used in command_log_and_err')
    if left:
        if isinstance(left, nextcord.VoiceChannel):
            e.description += f'*`Left`*: {left.mention}\n'
        else:
            raise TypeDefError(f'{created} of type: {str(type(created))[1:-1]} cannot be used in command_log_and_err')
    status = 'Err_' + status if status[:2].lower() != 'err' and status[:-2].isnumeric() else status
    e.description += f"*`Status`*: `{status}`"
    e = await set_timestamp(e, "Logged")
    await reaction(ctx, True) if not err_code else None
    return await chnl.send(embed=e)


async def logo_maker(ctx: commands.Context, embed: nextcord.Embed, team1_icon_url: str=None, team2_icon_url: str=None, online: bool = False) -> Optional[Message]:
    """Takes the logos of the 2 teams playing a match and combines them into one, while pasting it into
    the thumbnail of an Embed."""
    standby = "C:/Users/Shlok/J.A.R.V.I.SV2021/image_resources/pls_stand_by.jpg"
    paths = await download_images(team1_icon_url, team2_icon_url, file_names=['team1', 'team2']) if online is True else [team1_icon_url, team2_icon_url]
    path: str = image_join(paths[0] or standby,
                           paths[1] or standby)
    img_name: str = path.split('/')[-1]
    file = nextcord.File(path, filename=img_name)
    embed.set_footer(icon_url=f"attachment://{img_name}", text=embed._footer['text'])
    return await ctx.reply(file=file, embed=embed), os.remove(path) if path != standby else None



async def set_timestamp(embed: nextcord.Embed,
                        foot_text: str = "Requested") -> Embed:
    """Sets a timestamp in the footnotes of en Embed."""
    embed.timestamp = time_set(datetime.datetime.now())
    if embed.footer:
        if embed._footer.get('text'):
            embed._footer['text'] += f"\n{foot_text}"
        else:
            embed._footer['text'] = f"\n{foot_text}"
    else:
        embed.set_footer(text=f"{foot_text}")
    return embed
