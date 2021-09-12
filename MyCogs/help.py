import re
from typing import Optional
import discord
from MyCogs import command_log_and_err, set_timestamp, Cog,\
    Context, command, Client, Colour, Embed, HTTPException,\
    commands, Bot, comm_log_local
#discord.

NO_HELP_COGS = ("help", "events")


class Help(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.name = 'Help'

    @command(extras={'emoji': '✉'}, name='Help', aliases=['hp'])
    @comm_log_local
    async def help(self, ctx: Context, *, arg: Optional[str]):
        bot: Bot = self.bot
        icon = bot.user.avatar.url
        help_col = Colour.random()
        try:
            if not arg:
                await command_log_and_err(ctx, status='Only Help')
                help = Embed(title='Category Listing',
                                     description='Use `$help <category>` to find out more about them!',
                                     colour=help_col)
                cogs_desc = ''
                for cog_name, cog in bot.cogs.items():
                    if cog_name.lower() not in NO_HELP_COGS:
                        help.add_field(value=f'[`Hover for more info`](https://discord.gg/zt6j4h7ep3 "{cog.description}")', name=f'{cog.name}')
                await ctx.reply(embed=await set_timestamp(help, ""))
            else:
                found = False
                for cog_name, cog in bot.cogs.items():
                    for _command in bot.commands:
                        if str(cog_name).lower() == str(arg).lower() or re.search(fr"({arg.lower()})", bot.get_cog(cog_name).name.lower()):
                            formatted_cog_name = re.sub(r"\(.+\)", "", cog.name)
                            help = Embed(title=f'{formatted_cog_name} - `Command Listing`',
                                         description=f"Use `$help <command>` for more details on a specific command\n{bot.cogs[cog_name].__doc__}\n",
                                         colour=help_col)
                            for c in bot.get_cog(cog_name).get_commands():
                                if not c.hidden:
                                    help.add_field(name="{} - `{}`".format(c.name, ', '.join(c.aliases)), value=c.help,
                                                   inline=False)
                            found = True
                        for alias in _command.aliases:
                            if str(_command.name).lower() == str(arg).lower() or str(alias).lower() == str(arg).lower():
                                help = Embed(title=str(_command.name)[0].upper() + str(_command.name)[1:],
                                                     description="`{}`".format(str(_command.help)), colour=help_col)
                                help.add_field(name='Syntax:', value="`{}`".format(str(_command.usage)))
                                help.add_field(name='Aliases:', value="`{}`".format(', '.join(_command.aliases)))
                                help.add_field(name='Cooldown period:', value="`{}` seconds".format(
                                    _command._buckets._cooldown.per) if _command._buckets._cooldown else '`None`')
                                help.set_footer(text=
                                                """
<> - required
() - optional                                    
                                                """, icon_url=icon)
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
