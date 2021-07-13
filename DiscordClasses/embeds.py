import datetime
import os
from typing import Optional, Union
import discord
from discord import Message, Embed
from discord.ext import commands
from DiscordClasses.web_scrapers import Cricket
from DiscordClasses.custom_funcs import  reaction, image_join, time_set, comm_log_local


class TypeDefError(Exception):
    pass


async def command_log_and_err(ctx: commands.Context = None, status: Optional[str] = None,error: Optional
                                [Union[commands.CommandOnCooldown, commands.NoPrivateMessage]] = None,
                              used_on: Optional[Union[discord.User, discord.Member, discord.Role, discord.abc.GuildChannel]] = None,
                              send=True, err_code: Optional[str] = None, text: Optional[str] = None,
                              invalid_comname: commands.CommandOnCooldown.args = None,
                              created: Optional
                              [Union[discord.Role, discord.abc.GuildChannel, discord.Message]] = None,
                              deleted: Optional
                              [Union[discord.Role, discord.abc.GuildChannel, discord.Message]] = None,
                              joined: Optional[discord.VoiceChannel] = None,
                              left: Optional[discord.VoiceChannel] = None) -> Optional[Message]:
    """Command logging system for the bot, logging every command's usage(except developer commands) to a channel on
    J.A.R.V.I.S's home server."""
    status = status if status else err_code
    bot: commands.Bot = ctx.bot
    if ctx and error:
        if isinstance(error, commands.CommandOnCooldown):
            embed_c = Embed(title=f"{ctx.command.qualified_name} is on cooldown.",
                                    description=f"Please wait for `{round(error.retry_after, 2)}` more seconds.",
                                    colour=discord.Colour.teal())
            embed_c.add_field(name=f"Cooldown period for {ctx.command.qualified_name}",
                              value=f"`{int(ctx.command._buckets._cooldown.per)}` seconds")
            await ctx.reply(embed=await set_timestamp(embed_c, "Cooldown"))
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.reply(f'**`{ctx.command.qualified_name}`** cannot be used in DMs')
            try: await reaction(ctx, False)
            except discord.Forbidden: pass
    if ctx and bot and err_code and text:
        embed = Embed(title="Error!", description=f"{text}\n\n", colour=discord.Colour.red())
        if err_code[-2:] != '24' and err_code[-2:] != '12':
            embed.description += f"`Usage`: {ctx.command.usage if ctx.command else 'Unusable'}"
        else: pass
        try: await reaction(ctx, False)
        except discord.Forbidden: pass
        embed.set_footer(icon_url=bot.user.avatar_url)
        embed.add_field(name="Code:", value=f"`{'Err_' + err_code if err_code[:2].lower() != 'err' and err_code[:-2].isnumeric() else err_code}`")
        await ctx.reply(embed=await set_timestamp(embed,
                                                 str(ctx.command.qualified_name if ctx.command else "Invalid"))) if send is True else None
    com_name: str = ctx.command.qualified_name if ctx.command else f"Invalid Command{f' - `{invalid_comname}`' if not ctx.command else ''}"
    time: datetime.datetime = datetime.datetime.now().strftime("%a, %b %dth %Y %I:%M:%S %p IST")
    e = Embed(title=f"{com_name}",
                      description=f"*`Used by`*: {ctx.author.mention}\n *`Timestamp`*: `{time}`\n *`Used in`*: {ctx.channel.mention if ctx.guild else ctx.author.dm_channel}{f'- `{ctx.guild.name}`' if ctx.guild else ''}\n *`Message Link`*: **[`Jump to message`]({ctx.message.jump_url})**\n",
                      colour=discord.Colour.red() if err_code else discord.Colour.green())
    chnl: discord.TextChannel = bot.get_channel(821677968967467068)
    if used_on: e.description += f'*`Used on`*: {used_on.mention}\n'
    if created:
        if isinstance(created, discord.Role):
            e.description += f'*`Created role`*: {created.mention}\n'
        elif isinstance(created, discord.abc.GuildChannel):
            if isinstance(created, discord.VoiceChannel):
                e.description += f'*`Created Voice channel`*: `{created.mention}`\n'
            elif isinstance(created, discord.TextChannel):
                e.description += f'*`Created Text channel`*: {created.mention}\n'
            elif isinstance(created, discord.CategoryChannel):
                e.description += f'*`Created category`*: `{created.mention}`\n'
        elif isinstance(created, discord.Message):
            e.description += f'*`Pinned Message`*: **[`Jump to message`]({created.jump_url})**\n'
        else: raise TypeDefError(f'{created} of type: {str(type(created))[1:-1]} cannot be used in command_log_and_err')
    if deleted:
        if isinstance(deleted, discord.Role):
            e.description += f'*`Deleted role`*: {deleted.name}\n'
        elif isinstance(deleted, discord.abc.GuildChannel):
            if isinstance(deleted, discord.VoiceChannel):
                e.description += f'*`Deleted Voice channel`*: `{deleted.name}`\n'
            elif isinstance(deleted, discord.TextChannel):
                e.description += f'*`Deleted Text channel`*: {deleted.name}\n'
            elif isinstance(deleted, discord.CategoryChannel):
                e.description += f'*`Deleted category`*: `{deleted.name}`\n'
        elif isinstance(deleted, discord.Message):
            e.description += f'*`Unpinned Message`*: **[link]({deleted.jump_url})**\n'
        else:
            raise TypeDefError(f'{created} of type: {str(type(created))[1:-1]} cannot be used in command_log_and_err')
    if joined:
        if isinstance(joined, discord.VoiceChannel):
            e.description += f'*`Joined`*: {joined.mention}\n'
        else:
            raise TypeDefError(f'{created} of type: {str(type(created))[1:-1]} cannot be used in command_log_and_err')
    if left:
        if isinstance(left, discord.VoiceChannel):
            e.description += f'*`Left`*: {joined.mention}\n'
        else:
            raise TypeDefError(f'{created} of type: {str(type(created))[1:-1]} cannot be used in command_log_and_err')
    e.description += f"*`Status`*: `{'Err_' + status if status[:2].lower() != 'err' and status[:-2].isnumeric() else status}`"
    e = await set_timestamp(e, "Logged")
    await reaction(ctx, True) if not err_code else None
    await comm_log_local(ctx, status)
    return await chnl.send(embed=e)


async def ipl_logo_maker(ctx: commands.Context, embed: discord.Embed, team1: str, team2: str) -> Optional[Message]:
    """Takes the logos of the 2 teams playing a match and combines them into one, while pasting it into
    the thumbnail of an Embed."""
    standby = "C:/Users/Shlok/J.A.R.V.I.SV2021/image_resources/pls_stand_by.jpg"
    cricket = Cricket()
    if (team1, team2) != ('N/A', 'N/A') and team1 in cricket.teams_short_long and team2 in cricket.teams_short_long:
        path: str = image_join(cricket.ipl_team_logos_local.get(team1) or standby,
                          cricket.ipl_team_logos_local.get(team2 or standby))
    else:
        path = standby
    img_name: str = path.split('/')[-1]
    file = discord.File(path, filename=img_name)
    embed.set_thumbnail(url=f"attachment://{img_name}")
    yield await ctx.reply(file=file, embed=embed)
    os.remove(path) if path != standby else None


async def set_timestamp(embed: discord.Embed,
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
