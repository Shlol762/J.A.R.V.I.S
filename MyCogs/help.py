import re
from typing import Optional
import discord
from MyCogs import command_log_and_err, set_timestamp, Cog,\
    Context, command, Client, Colour, Embed, HTTPException,\
    commands, Bot, comm_log_local, caplist

#discord.
caps = caplist

NO_HELP_COGS = ["help", "events"]


class Help(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.name = 'Help'

    @command(extras={'emoji': '✉'}, name='Help', aliases=['hp'],
             help="Displays the commands of me.",
             usage="help|hp (command|command alias|category|category alias)")
    @comm_log_local
    async def help(self, ctx: Context, *, arg: Optional[str]):
        global caps
        global NO_HELP_COGS
        if str(ctx.guild.id) not in caplist['servers']:
            NO_HELP_COGS.append('captains(cs)')
        else: NO_HELP_COGS = ["help", "events"]
        bot: Bot = self.bot
        icon = ctx.author.avatar.url
        help_col = Colour.random()
        try:
            if not arg:
                await command_log_and_err(ctx, status='Only Help')
                help = Embed(title='Category Listing',
                                     description='Use `$help <category>` to get a list of commands in them!',
                                     colour=help_col).set_footer(icon_url=icon,
                                                                 text="Note: The 2-4 letter words in brackets are short forms of the categories. You can do $help <short form> if you wish.")
                for cog in bot.cogs.values():
                    if cog.name.lower() not in NO_HELP_COGS:
                        help.add_field(value=f'[`Hover for description`](https://discord.gg/zt6j4h7ep3 "{cog.description}")', name=f'{cog.name}')
                await ctx.reply(embed=await set_timestamp(help, "Requested"))
            else:
                found = False
                for cog in bot.cogs.values():
                    if re.search(fr"({arg.lower()})", cog.name.lower()) and cog.name.lower() not in NO_HELP_COGS and not found:
                        formatted_cog_name = re.sub(r"\(.+\)", "", cog.name)
                        help = Embed(title=f'{formatted_cog_name} - `Command Listing`',
                                     description=f"Use `$help <command>` for more details on a specific command\n{cog.description}\n",
                                     colour=help_col)
                        for _commands in cog.get_commands():
                            if not _commands.hidden:
                                help.add_field(name=_commands.name, value=f'[`Hover for description`](https://discord.gg/zt6j4h7ep3 "{_commands.help}")',
                                               inline=True)
                        found = True
                if not found:
                    for _command in bot.commands:
                        for alias in _command.aliases:
                            if arg.lower() in (_command.name.lower(), alias.lower()) and not found:
                                help = Embed(title=_command.name.title(),
                                                     description=f"`{_command.help}`", colour=help_col)
                                help.add_field(name='Syntax:', value=f"`{_command.usage}`")
                                help.add_field(name='Aliases:', value=f"`{', '.join(_command.aliases)}`")
                                help.add_field(name='Cooldown period:',
                                               value=f"`{_command._buckets._cooldown.per}` seconds") if _command._buckets._cooldown else None
                                help.set_footer(text=
                                                    """
<> - required, () - optional, | - or    
Note: You do not need to actually put <> and () around the inputs they are for understanding purposes only
\n""", icon_url=icon)
                                found = True
                if not found:
                    help = Embed(title='Error!', description='How do you even use "' + arg + '"?',
                                 color=Colour.red())
                    await command_log_and_err(ctx, text='No cat or com found', err_code='Err_help007',
                                              send=False)
                else:
                    await command_log_and_err(ctx, 'Help - {}'.format(arg))
                await ctx.reply(embed=await set_timestamp(help, ""))
        except HTTPException:
            pass


def setup(bot: Bot):
    bot.add_cog(Help(bot))
