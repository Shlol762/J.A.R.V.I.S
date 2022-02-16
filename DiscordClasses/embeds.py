from datetime import datetime as dt
from time import time as unixtim
import os
from typing import Optional, Union
import disnake
from disnake.abc import GuildChannel
from disnake import (
    Message,
    Embed,
    User,
    Role,
    TextChannel,
    VoiceChannel,
    CategoryChannel,
    Thread,
    Colour,
    File,
    Forbidden
        )
from disnake.ext import commands
from disnake.ext.commands import (
    Context,
    CommandOnCooldown,
    NoPrivateMessage,
    CommandError
        )
from pytz import timezone as tz
from DiscordClasses.web_scrapers import Cricket
from DiscordClasses.custom_funcs import reaction, image_join, time_set, download_images


class TypeDefError(Exception):
    pass


async def command_log_and_err(
        ctx: Context = None,
        status: Optional[str] = None,
        *,
        error: Optional[CommandError] = None,
        used_on: Optional[Union[User, Role, GuildChannel]] = None,
        send=True,
        err_code: Optional[str] = None,
        text: Optional[str] = None,
        invalid_comname: str = None,
        created: Optional[Union[Role, GuildChannel, Message]] = None,
        deleted: Optional[Union[Role, GuildChannel, Message]] = None,
        joined: Optional[Union[VoiceChannel, Thread]] = None,
        left: Optional[Union[VoiceChannel, Thread]] = None) -> Optional[Message]:
    """Command logging system for the bot, logging every command's usage(except developer commands) to a channel on
    J.A.R.V.I.S's home server."""
    status = status if status else err_code
    timestamp = dt.now(tz('Asia/Kolkata'))
    bot: Bot = ctx.bot
    if ctx and error:
        if isinstance(error, CommandOnCooldown):
            embed_c = Embed(title=f"{ctx.command.qualified_name} is on cooldown.",
                                    description=f"Please wait for `{round(error.retry_after, 2)}` more seconds.",
                                    colour=Colour.teal(), timestamp=timestamp)
            embed_c.add_field(name=f"Cooldown period for {ctx.command.qualified_name}",
                              value=f"`{int(ctx.command._buckets._cooldown.per)}` seconds")
            embed_c.set_footer(text="Cooldown")
            await ctx.reply(embed=embed_c)
        elif isinstance(error, NoPrivateMessage):
            await ctx.reply(f'**`{ctx.command.qualified_name}`** cannot be used in DMs')
            await reaction(ctx, False)
    if ctx and bot and err_code and text:
        file = None
        embed = Embed(title="Error!", description=f"{text}\n\n", colour=Colour.red(), timestamp=timestamp)
        if err_code[-2:] != '24' and err_code[-2:] != '12' and ctx.command:
            embed.description += f"**This is how you use this command**: `{ctx.command.usage}`"
        # elif err_code[-2:] == '24':
        #     path = "C:/Users/Shlok/J.A.R.V.I.SV2021/image_resources/403icon.png"
        #     file = File(path, '403icon.png')
        #     icon_url = f'attachment://403icon.png'
        #     embed.set_thumbnail(url=icon_url)
        await reaction(ctx, False)
        embed.set_footer(icon_url=bot.user.avatar.url, text=str(ctx.command.qualified_name if ctx.command else "Invalid"))
        await ctx.reply(embed=embed, file=file) if send else None
    com_name: str = ctx.command.qualified_name if ctx.command else f"Invalid Command{f' - `{invalid_comname}`' if not ctx.command else ''}"
    time: str = f"<t:{round(unixtim())}:F>"
    e = Embed(title=f"{com_name}",
                      description=f"*`Used by`*: {ctx.author.mention}\n *`Timestamp`*: {time}\n *`Used in`*: {ctx.channel.mention if ctx.guild else ctx.author.dm_channel}{f'- `{ctx.guild.name}`' if ctx.guild else ''}\n *`Message Link`*: **[`Jump to message`]({ctx.message.jump_url})**\n",
                      colour=Colour.red() if err_code else Colour.green(), timestamp=timestamp).set_footer(text="Logged")
    chnl: TextChannel = bot.get_channel(821677968967467068)
    if used_on: e.description += f'*`Used on`*: {used_on.mention}\n'
    creadeleted = created or deleted
    if creadeleted:
        if isinstance(creadeleted, Role):
            e.description += f'*`{"Crea" if created else "Dele"}ted role`*:' \
                             f' {created.mention if created else f"`{deleted.name}`"}\n'
        elif isinstance(creadeleted, GuildChannel):
            if isinstance(creadeleted, VoiceChannel):
                e.description += f'*`{"Crea" if created else "Dele"}ted Voice channel`*:' \
                                 f' {created.mention if created else f"`{deleted.name}`"}\n'
            elif isinstance(creadeleted, TextChannel):
                e.description += f'*`{"Crea" if created else "Dele"}ted Text channel`*:' \
                                 f' {created.mention if created else f"`{deleted.name}`"}\n'
            elif isinstance(creadeleted, CategoryChannel):
                e.description += f'*`{"Crea" if created else "Dele"}ted Category`*:' \
                                 f' `{created.mention if created else f"`{deleted.name}`"}\n'
        else: raise TypeDefError(f'{creadeleted} of type: {str(type(creadeleted))[1:-1]} cannot be used in command_log_and_err')
    if joined or left:
        if isinstance(joined or left, VoiceChannel):
            e.description += f'*`{"Joined" if joined else "Left"} Voice Channel`*: {(joined or left).mention}\n'
        elif isinstance(joined or left, Thread):
            e.description += f'*`{"Joined" if joined else "Left"} Thread Channel`*: {(joined or left).mention}\n'
        else:
            raise TypeDefError(f'{created} of type: {str(type(created))[1:-1]} cannot be used in command_log_and_err')
    status = 'Err_' + status if status[:2].lower() != 'err' and status[:-2].isnumeric() else status
    e.description += f"*`Status`*: `{status}`"
    await reaction(ctx, True) if not err_code else None
    return await chnl.send(embed=e)


async def logo_maker(ctx: Context, embed: Embed, team1_icon_url: str=None, team2_icon_url: str=None, online: bool = False) -> Optional[Message]:
    """Takes the logos of the 2 teams playing a match and combines them into one, while pasting it into
    the thumbnail of an Embed."""
    standby = "C:/Users/Shlok/J.A.R.V.I.SV2021/image_resources/pls_stand_by.jpg"
    paths = await download_images(team1_icon_url, team2_icon_url, file_names=['team1', 'team2']) if online is True else [team1_icon_url, team2_icon_url]
    path: str = image_join(paths[0] or standby,
                           paths[1] or standby)
    img_name: str = path.split('/')[-1]
    file = File(path, filename=img_name)
    embed.set_footer(icon_url=f"attachment://{img_name}", text=embed._footer['text'])
    return await ctx.reply(file=file, embed=embed), os.remove(path) if path != standby else None



async def set_timestamp(embed: Embed,
                        foot_text: str = "Requested") -> Embed:
    """Sets a timestamp in the footnotes of en Embed."""
    embed.timestamp = time_set(dt.now())
    if embed.footer:
        if embed._footer.get('text'):
            embed._footer['text'] += f"\n{foot_text}"
        else:
            embed._footer['text'] = f"\n{foot_text}"
    else:
        embed.set_footer(text=f"{foot_text}")
    return embed
