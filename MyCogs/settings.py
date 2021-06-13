from typing import Union
import discord, json
from discord.ext import commands
from discord import Embed
from MyCogs import command_log_and_err, Cog, command,\
    guild_only, Context, Client, set_timestamp

#commands.
class Settings(Cog):
    def __init__(self, client: Client):
        self.client = client
        self.description = "The commands that control the bot's settings in the server."
        self.name = 'Settings'

    @command(name='Enable', aliases=['en'],
              help='Enables the selected setting the bot has for the server.',
              usage='enable|en <feature> <scope>',
              brief='⚙701')
    @guild_only()
    async def enable(self, ctx: Context, _command: str = 'none', server_or_channel: str = 'server'):
        c_low = _command.lower()
        guild_id = str(ctx.guild.id)
        channel_id = str(ctx.message.channel.id)
        author = ctx.message.author
        if author.id == ctx.guild.owner_id:
            if c_low == 'none':
                await command_log_and_err(ctx, self.client, err_code="Err_70148",
                                          text="Choose what you want to change please.")
            else:
                json_file = "C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/settings.json"
                template = {
                    "ban": True,
                    "kick": True,
                    "clear": True,
                    "message": True,
                    "msghai": True,
                    "noswear": True,
                    "convo": True,
                    "nou": True,
                    "greetings": True,
                    "farewells": True,
                    "iamgod": True
                }

                with open(json_file, "r") as f: bot_comm_config: dict = json.load(f)

                if bot_comm_config.get(channel_id) and server_or_channel == 'channel':
                    channel_config: Union[dict, None] = bot_comm_config.get(channel_id)
                    if channel_config:
                        func = channel_config.get(_command)
                        if func:
                            await ctx.send(f"`{_command}` was already enabled in this `Channel`")
                        elif func is False:
                            channel_config[_command] = True
                            await ctx.send(f"`{_command}` has been enabled in this `Channel`")
                        else:
                            await ctx.send(f"There isn't any setting called `{_command}`")
                        if channel_config == template: bot_comm_config.pop(channel_id)
                elif not bot_comm_config.get(channel_id) and server_or_channel == 'channel':
                    bot_comm_config[channel_id] = {
                        "ban": True,
                        "kick": True,
                        "clear": True,
                        "message": True,
                        "msghai": True,
                        "noswear": True,
                        "convo": True,
                        "nou": True,
                        "greetings": True,
                        "farewells": True,
                        "iamgod": True
                    }
                    channel_config: Union[dict, None] = bot_comm_config.get(channel_id)
                    if channel_config:
                        func = channel_config.get(_command)
                        if func: await ctx.send(f"`{_command}` was already enabled in this `Channel`")
                        elif func is False:
                            channel_config[_command] = True
                            await ctx.send(f"`{_command}` has been enabled in this `Channel`")
                        else: await ctx.send(f"There isn't any setting called `{_command}`")
                        if channel_config == template: bot_comm_config.pop(channel_id)
                if bot_comm_config.get(guild_id) and server_or_channel == 'server':
                    guild_config: Union[dict, None] = bot_comm_config.get(guild_id)
                    if guild_config:
                        func = guild_config.get(_command)
                        if func: await ctx.send(f"`{_command}` was already enabled in this `Server`")
                        elif func is False:
                            guild_config[_command] = True
                            await ctx.send(f"`{_command}` has been enabled in this `Server`")
                        else: await ctx.send(f"There isn't any setting called `{_command}`")
                elif not bot_comm_config.get(guild_id) and server_or_channel == 'server':
                    bot_comm_config[guild_id] = {
                        "ban": True,
                        "kick": True,
                        "clear": True,
                        "message": True,
                        "msghai": True,
                        "noswear": True,
                        "convo": True,
                        "nou": True,
                        "greetings": True,
                        "farewells": True,
                        "iamgod": True
                    }
                    guild_config: Union[dict, None] = bot_comm_config.get(guild_id)
                    if guild_config:
                        func = guild_config.get(_command)
                        if func: await ctx.send(f"`{_command}` was already enabled in this `Server`")
                        elif func is False:
                            guild_config[_command] = True
                            await ctx.send(f"`{_command}` has been enabled in this `Server`")
                        else: await ctx.send(f"There isn't any setting called `{_command}`")

                with open(json_file, "w") as f: json.dump(bot_comm_config, f, indent=3)
                await command_log_and_err(ctx, self.client, 'Success')
        else:
            await command_log_and_err(ctx, self.client, 'Not owner')
            await ctx.send("You need to be owner to change settings.")\

    @command(name='Disable', aliases=['da'],
      help='Disables the selected setting the bot has for the server.',
      usage='disable|da <feature> <scope>',
      brief='⚙702')
    @guild_only()
    async def disable(self, ctx: Context, _command: str = 'none', server_or_channel: str = 'server'):
        c_low = _command.lower()
        guild_id = str(ctx.guild.id)
        channel_id = str(ctx.message.channel.id)
        author = ctx.message.author
        if author.id == ctx.guild.owner_id:
            if c_low == 'none':
                await command_log_and_err(ctx, self.client, err_code="Err_70248",
                                          text="Choose what you want to change please.")
            else:
                json_file = "C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/settings.json"
                template = {
                    "ban": True,
                    "kick": True,
                    "clear": True,
                    "message": True,
                    "msghai": True,
                    "noswear": True,
                    "convo": True,
                    "nou": True,
                    "greetings": True,
                    "farewells": True,
                    "iamgod": True
                }

                with open(json_file, "r") as f: bot_comm_config: dict = json.load(f)

                if bot_comm_config.get(channel_id) and server_or_channel == 'channel':
                    channel_config: Union[dict, None] = bot_comm_config.get(channel_id)
                    if channel_config:
                        func = channel_config.get(_command)
                        if func:
                            channel_config[_command] = False
                            await ctx.send(f"`{_command}` has been disabled in this `Channel`")
                        elif func is False: await ctx.send(f"`{_command}` was already disabled in this `Channel`")
                        else: await ctx.send(f"There isn't any setting called `{_command}`")
                        if channel_config == template: bot_comm_config.pop(channel_id)
                elif not bot_comm_config.get(channel_id) and server_or_channel == 'channel':
                    bot_comm_config[channel_id] = {
                        "ban": True,
                        "kick": True,
                        "clear": True,
                        "message": True,
                        "msghai": True,
                        "noswear": True,
                        "convo": True,
                        "nou": True,
                        "greetings": True,
                        "farewells": True,
                        "iamgod": True
                    }
                    channel_config: Union[dict, None] = bot_comm_config.get(channel_id)
                    if channel_config:
                        func = channel_config.get(_command)
                        if func:
                            channel_config[_command] = False
                            await ctx.send(f"`{_command}` has been disabled in this `Channel`")
                        elif func is False: await ctx.send(f"`{_command}` was already disabled in this `Channel`")
                        else: await ctx.send(f"There isn't any setting called `{_command}`")
                        if channel_config == template: bot_comm_config.pop(channel_id)
                if bot_comm_config.get(guild_id) and server_or_channel == 'server':
                    guild_config: Union[dict, None] = bot_comm_config.get(guild_id)
                    if guild_config:
                        func = guild_config.get(_command)
                        if func:
                            guild_config[_command] = False
                            await ctx.send(f"`{_command}` has been disabled in this `Server`")
                        elif func is False: await ctx.send(f"`{_command}` was already disabled in this `Server`")
                        else: await ctx.send(f"There isn't any setting called `{_command}`")
                elif not bot_comm_config.get(guild_id) and server_or_channel == 'server':
                    bot_comm_config[guild_id] = {
                        "ban": True,
                        "kick": True,
                        "clear": True,
                        "message": True,
                        "msghai": True,
                        "noswear": True,
                        "convo": True,
                        "nou": True,
                        "greetings": True,
                        "farewells": True,
                        "iamgod": True
                    }
                    guild_config: Union[dict, None] = bot_comm_config.get(guild_id)
                    if guild_config:
                        if func:
                            guild_config[_command] = False
                            await ctx.send(f"`{_command}` has been disabled in this `Server`")
                        elif func is False: await ctx.send(f"`{_command}` was already disabled in this `Server`")
                        else: await ctx.send(f"There isn't any setting called `{_command}`")

                with open(json_file, "w") as f: json.dump(bot_comm_config, f, indent=3)
                await command_log_and_err(ctx, self.client, 'Success')
        else:
            await command_log_and_err(ctx, self.client, 'Not owner')
            await ctx.send("You need to be owner to change settings.")

    @command(name='Set Prefix', aliases=['setprefix', 'spf'],
             help='Sets the prefix for the server the command is called in.',
             usage='setprefix|sp <prefix>',
             brief='⚙703')
    @guild_only()
    async def set_prefix(self, ctx: Context, *, prefix: str):
        if prefix:
            with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/prefixes.json", "r") as f:
                prefixes = json.load(f)

            prefixes[str(ctx.guild.id)] = prefix

            with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/prefixes.json", "w") as f:
                json.dump(prefixes, f, indent=3)
            await command_log_and_err(ctx, self.client, status=f"Prefix set to {prefix}")
            await ctx.send(f"My prefix in this server has been set to `{prefix}`")
        else: await command_log_and_err(ctx, self.client, err_code="70248",
                                        text="Haven't given any prefix to set bub.")

    @command(name='Settings', aliases=['sts'],
             help='Shows the current settings of the server.',
             usage='settings|sts',
             brief='⚙704')
    @guild_only()
    async def settings(self, ctx: Context):
        with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/settings.json", "r") as f:
            settings: dict[str:dict[str:bool]] = json.load(f)
        embed = await set_timestamp(Embed(title=f"`J.A.R.V.I.S` configuration settings in `{ctx.channel.name}`",
                      description=""))

        if settings.get(str(ctx.channel.id)):
            for setting, bool_val in settings.get(str(ctx.channel.id)).items():
                embed.description = f"`{setting.title():^10} - {bool_val:>5}`\n"
        elif settings.get(str(ctx.guild.id)):
            for setting, bool_val in settings.get(str(ctx.channel.id)).items():
                embed.description = f"`{setting.title():^10} - {bool_val:>5}`\n"

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Settings(client))
