from typing import Optional
import discord
from MyCogs import command_log_and_err, set_timestamp, Cog,\
    Context, command, Client, Colour, Embed, HTTPException,\
    commands
#discord.


class Help(Cog):
    def __init__(self, client: Client):
        self.client = client
        self.name = 'Help'

    @command(brief='✉', name='Help', aliases=['hp'])
    async def help(self, ctx: Context, *, cog: Optional[str]):
        icon = self.client.user.avatar_url
        help_col = Colour.random()
        try:
            if not cog:
                await command_log_and_err(ctx, self.client, status='Only Help')
                help = Embed(title='Category Listing',
                                     description='Use `$help <category>` to find out more about them!',
                                     colour=help_col)
                cogs_desc = ''
                for x, y in self.client.cogs.items():
                    x: str = x
                    y: Cog = y
                    if str(x).lower() != 'help' and str(x).lower() != 'events':
                        cogs_desc += f'__**{y.name}**__ - `{y.description}`\n'
                help.add_field(name='_ _', value=cogs_desc[0:len(cogs_desc) - 1], inline=False)
                await ctx.send(embed=await set_timestamp(help, ""))
            else:
                found = False
                for key, val in self.client.cogs.items():
                    for _command in self.client.commands:
                        if str(key).lower() == str(cog).lower() or self.client.get_cog(key).name.lower() == str(cog).lower():
                            help = Embed(title=f'__{val.name}__ - `Command Listing`',
                                                 description=f"Use `$help <command>` for more details on a specific command\n{self.client.cogs[key].__doc__}\n",
                                                 colour=help_col)
                            for c in self.client.get_cog(key).get_commands():
                                if not c.hidden:
                                    help.add_field(name="{} - `{}`".format(c.name, ', '.join(c.aliases)), value=c.help,
                                                   inline=False)
                            found = True
                        for alias in _command.aliases:
                            if str(_command.name).lower() == str(cog).lower() or str(alias).lower() == str(cog).lower():
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
                    help = Embed(title='Error!', description='How do you even use "' + cog + '"?',
                                         color=Colour.red())
                    await command_log_and_err(ctx, self.client, text='No cat or com found', err_code='Err_help007',
                                              send=False)
                else:
                    await command_log_and_err(ctx, self.client, 'Help - {}'.format(cog))
                await ctx.send(embed=await set_timestamp(help, ""))
        except HTTPException:
            pass


def setup(client):
    client.add_cog(Help(client))
