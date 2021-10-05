import json
from MyCogs import Cog, command, Bot, Context, Embed,\
    Colour, caplist

caps = caplist


class Captains(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.name = "Captains(cs)"
        self.description = "For 2021 only... Captains stuff GEAR."

    async def cog_check(self, ctx: Context) -> bool:
        global caps
        return str(ctx.guild.id) in caps['servers']

    @command(name="Caplist", aliases=['cl'])
    async def caplist(self, ctx: Context, dept: str = 'all'):
        global caps
        scl, g, k, c, n = caps['School'], caps['Ganga'], caps['Krishna'], caps['Cauvery'], caps['Narmada']
        embed = Embed(title="Captains AY `2021-22` Batch 23",
                      url="https://drive.google.com/file/d/1Ji_0wjeyL9UY_XLYjdC8ZJfafA-mEzCV/view",
                      colour=Colour.random(), description='')
        embed.description += f"""
***School***
\t`  Cap'n  ` - <@{scl['Captain']['id']}>
\t`Associate` - <@{scl['Associate']['id']}>
\t`   Vice  ` - {', '.join([f"<@{vice['id']}>" for vice in scl['Vice']])}
""" if dept.lower() in ('all', 'school') else ''

        await ctx.reply(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Captains(bot))