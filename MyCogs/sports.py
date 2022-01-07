import datetime
from typing import Optional
import nextcord
from nextcord.ext import commands
from MyCogs import Bot, Cog, Context, command_log_and_err, Cricket,\
    logo_maker, set_timestamp, comm_log_local


class Sports(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.name = 'Sports(sps)'
        self.description = 'Collects sports data from the internet and displays as Embeds.(UNDER DEVELOPMENT)'

    @commands.command(name='Cricket Score', aliases=['cs', 'cricscore', 'cricketscore'],
                      usage='cricscore|cricketscore|cs <series>', extras={'emoji': '🏏', 'number': '801'},
                      help='Gets the score of the next or live match from any series.')
    @comm_log_local
    async def cricscore(self, ctx: Context, *, tournament: str = None):
        if tournament:
            async with ctx.typing():
                match = await Cricket(tournament).get_match_data()
                embed = nextcord.Embed(title=f'{match.series}\n`{match.teams["team1"]["name"].title()}` vs `{match.teams["team2"]["name"].title()}`', description='',
                                      colour=nextcord.Colour.random(), url=match.link['tournament']).set_footer(
                                      text=match.progress)
                embed.description += str(match)
                await command_log_and_err(ctx, 'Success')
                await logo_maker(ctx, await set_timestamp(embed, ""), match._icons[0], match._icons[1])
                return
        await command_log_and_err(ctx, err_code="80148", text="Which series bub?")

    @commands.command(name='Ipl table', aliases=['iplt', 'ipltable'],
                      usage='ipltable|iplt (team)',
                      help='Gets the IPL table, or table statistics of a team based on your input | Command under reconfig.', extras={'emoji': '🏆', 'number': '802'})
    @comm_log_local
    async def ipltable(self, ctx: Context, *, team: Optional[str] = None):
        # async with ctx.typing():
        #     cricket: Cricket = self.c
        #     if not team:
        #         ipl_table = cricket.pt_table
        #         time = datetime.datetime.now().strftime("%Y")
        #         embed = nextcord.Embed(title=f'Indian Premier League - `{time}`', description='',
        #                               colour=nextcord.Colour.random())
        #         embed.description += f'**`{"Team":^28}{"Matches":^9}{"Win":^5}{"Loss":^6}{"Tie":^5}{"NR":^4}{"Pts":^5}{"NRR":^6}`**\n'
        #         for team in ipl_table:
        #             embed.description += f'`{team[0]:<28}{team[1]:^9}{team[2]:^5}{team[3]:^6}{team[4]:^5}{team[5]:^4}{team[6]:^5}{team[7]:<6}`\n'
        #         embed.set_footer(icon_url=cricket.pt_ipl_logo, text="NR: No Result\nNRR: Net Run Rate")
        #         await command_log_and_err(ctx, 'Success')
        #         await ctx.reply(embed=await set_timestamp(embed, ""))
        #     else:
        #         if cricket.teams_short_long.get(team.lower()):
        #             value = cricket.teams_short_long.get(team.lower())
        #         else:
        #             for short, long in cricket.teams_short_long.items():
        #                 if team.lower() == long.lower():
        #                     value = long
        #                     break
        #                 else:
        #                     value = 'N/A'
        #             if value == 'N/A':
        #                 return await ctx.reply(f"{team} ain't a known IPL team...")
        #         logo_url = None
        #         for team1, link in cricket.ipl_team_logos_web.items():
        #             if value == team1:
        #                 logo_url = link
        #                 break
        #         for team in cricket.pt_table:
        #             if team[0] == value:
        #                 embed = nextcord.Embed(title=team[0], description='', colour=nextcord.Colour.random())
        #                 team_attr_names = ['Matches', 'Wins', 'Losses', 'Ties', 'No Result', 'Points', 'Net Run Rate']
        #                 team_attr_names_index = 0
        #                 for attr in team[1:]:
        #                     embed.description += f"`{team_attr_names[team_attr_names_index]:<14} - {attr:>8}`\n"
        #                     team_attr_names_index += 1
        #                 embed.set_thumbnail(url=logo_url)
        #                 await ctx.reply(embed=await set_timestamp(embed, ""))
        #                 break
        await ctx.reply("Command under reconfig.")


def setup(bot: Bot):
    bot.add_cog(Sports(bot))
