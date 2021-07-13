import datetime
from typing import Optional
import discord
from discord.ext import commands
from DiscordClasses.embeds import ipl_logo_maker, set_timestamp
from DiscordClasses.web_scrapers import Cricket
from . import command_log_and_err


class Sports(commands.Cog):
    def __init__(self, client: discord.Client):
        self.client = client
        self.name = 'Sports'
        self.description = 'Collects sports data from the internet and displays as Embeds.(UNDER DEVELOPMENT)'
        self.c = Cricket()

    @commands.command(name='Ipl score', aliases=['ipls', 'iplscore'],
                      usage='iplscore|ipls', brief='🏏801',
                      help='Gets the score of the next or live IPL match')
    async def iplscore(self, ctx: commands.Context):
        async with ctx.typing():
            match: Cricket = Cricket()
            embed = discord.Embed(title=f'{match.match_ser}\n`{match.team1}` vs `{match.team2}`', description='',
                                  colour=discord.Colour.random()).set_footer(
                text=match.status, icon_url=match.pt_ipl_logo)
            if match.match_ser != 'N/A':
                embed.description += f"""
        `{match.team1:<30}{match.score1:>35}`\n
        `{match.team2:<30}{match.score2:>35}`\n
        `{'Match Number':^12} - {match.match_num.replace("Qu", "Qualifier"):^12}`
        `{'Location':^12} - {match.match_loc:^12}`
        `{'Date':^12} - {match.match_date:^12}`
        `{'Period':^12} - {match.match_per:^12}`
        `{'Time':^12} - {match.match_tim:^12}`"""
            else:
                embed.description += f'Trouble getting info from [`ESPNcricinfo`](https://www.espncricinfo.com/).\n`Please Stand by`'
            await command_log_and_err(ctx, 'Success')
            await ipl_logo_maker(ctx, await set_timestamp(embed, ""), team1=match.team1, team2=match.team2)

    @commands.command(name='Ipl table', aliases=['iplt', 'ipltable'],
                      usage='ipltable|iplt (team)',
                      help='Gets the IPL table, or table statistics of a team based on your input', brief='🏆802')
    async def ipltable(self, ctx: commands.Context, *, team: Optional[str] = None):
        async with ctx.typing():
            cricket: Cricket = self.c
            if not team:
                ipl_table = cricket.pt_table
                time = datetime.datetime.now().strftime("%Y")
                embed = discord.Embed(title=f'Indian Premier League - `{time}`', description='',
                                      colour=discord.Colour.random())
                embed.description += f'**`{"Team":^28}{"Matches":^9}{"Win":^5}{"Loss":^6}{"Tie":^5}{"NR":^4}{"Pts":^5}{"NRR":^6}`**\n'
                for team in ipl_table:
                    embed.description += f'`{team[0]:<28}{team[1]:^9}{team[2]:^5}{team[3]:^6}{team[4]:^5}{team[5]:^4}{team[6]:^5}{team[7]:<6}`\n'
                embed.set_footer(icon_url=cricket.pt_ipl_logo, text="NR: No Result\nNRR: Net Run Rate")
                await command_log_and_err(ctx, 'Success')
                await ctx.reply(embed=await set_timestamp(embed, ""))
            else:
                if cricket.teams_short_long.get(team.lower()):
                    value = cricket.teams_short_long.get(team.lower())
                else:
                    for short, long in cricket.teams_short_long.items():
                        if team.lower() == long.lower():
                            value = long
                            break
                        else:
                            value = 'N/A'
                    if value == 'N/A':
                        return await ctx.reply(f"{team} ain't a known IPL team...")
                logo_url = None
                for team1, link in cricket.ipl_team_logos_web.items():
                    if value == team1:
                        logo_url = link
                        break
                for team in cricket.pt_table:
                    if team[0] == value:
                        embed = discord.Embed(title=team[0], description='', colour=discord.Colour.random())
                        team_attr_names = ['Matches', 'Wins', 'Losses', 'Ties', 'No Result', 'Points', 'Net Run Rate']
                        team_attr_names_index = 0
                        for attr in team[1:]:
                            embed.description += f"`{team_attr_names[team_attr_names_index]:<14} - {attr:>8}`\n"
                            team_attr_names_index += 1
                        embed.set_thumbnail(url=logo_url)
                        await ctx.reply(embed=await set_timestamp(embed, ""))
                        break


def setup(client):
    client.add_cog(Sports(client))
