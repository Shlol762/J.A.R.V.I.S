from discord.ext import commands
import discord
import wikipedia
from PyDictionary import PyDictionary
from typing import Any, Tuple, Optional
from MyCogs import timeto as tt, command_log_and_err, set_timestamp,\
    WorldoMeter, Embed, Colour, Context, find_nth_occurrence,\
    send_to_paste_service
import datetime, re, requests
from datetime import datetime
from io import StringIO
import inspect, contextlib, textwrap, traceback


class Misc(commands.Cog):
    def __init__(self, client: discord.Client):
        self.client = client
        self.name = 'Miscellaneous'
        self.description = "Random stuff do whatever the heck you want."
        self.cocase = WorldoMeter()

    @commands.command(aliases=['latency'],
                      help='Gets latency of the reply time of the bot in milliseconds', name='Ping',
                      usage="ping|latency", brief='📶901')
    async def ping(self, ctx: commands.Context):
        await command_log_and_err(ctx, self.client, 'Success')
        await ctx.send(embed=await set_timestamp(
            Embed(title='Ping', description=f'`{round(self.client.latency * 1000)}` ms',
                          colour=discord.Colour.random())))

    @commands.command(name='Leap', aliases=['le'], usage='leap <year>',
                      help='Checks whether or not a given year is a leap one.',
                      brief='🗓902')
    async def leap(self, ctx: commands.Context, year: int = None):
        year = str(year)
        if year:
            if len(year) <= 5:
                now = datetime.datetime.now()
                now = int(now.strftime("%Y"))
                int_yr = int(year)
                was_is = ''
                if int_yr > now:
                    was_is = 'is{}going to be a `leap year`'
                elif int_yr < now:
                    was_is = 'was{}a `leap year`'
                elif int_yr == now:
                    was_is = 'is{}a `leap year`'
                if year[2] != '0':
                    if int_yr % 4 == 0:
                        await ctx.send(f'`{str(year)}` {was_is.format(" ")}')
                    else:
                        await ctx.send(f"{str(year)} {was_is.format(' ')}")
                else:
                    if int_yr % 400 == 0:
                        await ctx.send(f'{str(year)} {was_is.format(" ")}')
                    else:
                        await ctx.send(f'{str(year)} {was_is.format(" ")}')
            else:
                await ctx.send("I'm *not* calculating years with more than 5 digits.")
            await command_log_and_err(ctx, self.client, 'Success')
        else:
            await command_log_and_err(ctx, self.client, err_code="Err_90248", text="Specify year pls.")

    @commands.command(aliases=['pdm'], name='Palindrome',
                      help='Checks whether or not a snippet of text is a palindrome.',
                      usage='palindrome|pdm <text>', brief='🔁903')
    async def palindrome(self, ctx: commands.Context, word: str = None):
        if word:
            if len(word) <= 14:
                word_len = len(word)
                fwd_idx = 0
                bckwd_idx = word_len - 1
                for char in word:
                    if word[fwd_idx] != word[bckwd_idx]:
                        await ctx.send(f"{word} is not a palindrome")
                        break
                    else:
                        if bckwd_idx - fwd_idx < 0:
                            await ctx.send(f"{word} is a palindrome.")
                            break
                    fwd_idx += 1
                    bckwd_idx -= 1
                await command_log_and_err(ctx, self.client, 'Success')
            else:
                await command_log_and_err(ctx, self.client, err_code="Err_90312",
                                          text="Max characters for a word is 14.")
        else:
            await command_log_and_err(ctx, self.client, err_code="Err_90348", text="Word = Give pls?")

    @commands.command(aliases=['wk', 'wiki'], name='Wikipedia',
                      help='Searches wikipedia and returns info based on a given query.',
                      usage='wiki|wk <query>', brief='🌐904')
    async def wiki(self, ctx: commands.Context, *, query: str = 'wikipedia'):
        async with ctx.typing():
            if query:
                query = query.title()
                try:
                    results = wikipedia.search(query, 1)[0]
                    # print(results)
                    msg = wikipedia.summary("'" + query + "'").split('\n')[0]
                    await command_log_and_err(ctx, self.client, 'Success')
                    await ctx.send(embed=await set_timestamp(
                        Embed(title=f'Result for "`{query[0].upper() + query[1:]}`"\n\n{results}',
                                      description=msg,
                                      colour=discord.Colour.random())))
                except wikipedia.DisambiguationError:
                    await command_log_and_err(ctx, self.client, err_code="Err_90412",
                                              text=f"Too many results found for '`{query}`'. Check spelling or try adding more keywords.")
                except IndexError:
                    await command_log_and_err(ctx, self.client, err_code="Err_90412",
                                              text=f"No results found for '`{query}`'. Check spelling or try adding more keywords.")
                except wikipedia.PageError:
                    await command_log_and_err(ctx, self.client, err_code="Err_90412",
                                              text=f"No results found for '`{query}`'. Check spelling or try adding more keywords.")
                except discord.HTTPException:
                    msg = msg.split()
                    await command_log_and_err(ctx, self.client, 'Success: split info')
                    message = await ctx.author.send(
                        embed=Embed(title=f'Result for "`{query[0].upper() + query[1:]}`"\n\n{results}',
                                            description=' '.join(msg[:300]), colour=discord.Colour.random()))
                    await ctx.author.send(
                        embed=Embed(description=' '.join(msg[300:]), colour=discord.Colour.random()))
                    await ctx.send(
                        embed=Embed(title=f'Result for "`{query[0].upper() + query[1:]}`"\n\n{results}',
                                            description=f'Since the results for this search exceeds the character limit of 2048, the info will be sent to you through DMs. Click [here]({message.jump_url}) to jump.',
                                            colour=discord.Colour.random())) if ctx.guild else None
                except requests.exceptions.ProxyError:
                    await command_log_and_err(ctx, self.client, err_code="Err90412",
                                              text=f'N/A: `Internet Connection Failure\\: Unable to retrieve information for "{query}" `{author.mention}')
            else:
                await command_log_and_err(ctx, self.client, err_code="Err_90412",
                                          text='Missing query. Please state query and try again.'.format(query,
                                                                                                         ctx.author.mention))

    @commands.command(aliases=['dct', 'dict'], name='Dictionary',
                      help='Searches the internet and returns definitions, synonyms and antonyms.',
                      usage='dct|dict|dictionary <word> (def/syn/ant)', brief='📔905')
    async def dict(self, ctx: commands.Context, word: str, *, synantdef: Optional[str]):
        async with ctx.typing():
            try:
                dcnry = PyDictionary()
                word = word[0].upper() + word[1:]
                embed = Embed(title=word, description='', colour=discord.Colour.random())
                if (await dcnry.meaning(word)) is None:
                    embed.description += f"Sorry either `{word}` isn't a word in the dictionary or there's a problem with the internet."
                    await command_log_and_err(ctx, self.client, 'Internet Problems/Non-Existent Word')
                else:
                    if not synantdef or synantdef.lower() == 'def':
                        for key, vals in (await dcnry.meaning(word)).items():
                            if '(' in vals[0]:
                                vals[0] += ')'
                            embed.description += f"""*`{key}`*:\n- {vals[0][0].upper() + vals[0][1:].replace("`", "'")}\n"""
                            if len(vals) > 1:
                                for val in vals[1:3]:
                                    if '(' in val:
                                        val += ')'
                                    embed.description += f"""- {val[0].upper() + val[1:].replace('`', "'")}\n"""
                    if not synantdef or synantdef.lower() == 'syn':
                        embed.description += f"""\n**`Synonyms`**:\n {', '.join((await dcnry.synonym(word))[:10]).title() if dcnry.synonym(word) is not None else f'`{word}` does not have synonyms'}\n"""
                    if not synantdef or synantdef.lower() == 'ant':
                        embed.description += f"""\n**`Antonyms`**:\n {', '.join((await dcnry.antonym(word))[:10]).title() if dcnry.antonym(word) is not None else f'`{word}` does not have antonyms'}"""
                    await command_log_and_err(ctx, self.client, 'Success')
                await ctx.send(embed=embed)
            except requests.exceptions.ProxyError:
                await command_log_and_err(ctx, self.client, err_code="Err_90512",
                                          text=f'N/A: `Internet Connection Failure\\: Unable to retrieve information for "{word}"` {ctx.author.mention}')

    @commands.command(name="Time to", aliases=['tto', 'timeto'], brief='⏱906',
                      help='Returns the countdown to the given timestamp.',
                      usage='$timeto|tto <timestamp in format of - "24hr:mins day/month/year">')
    async def timeto(self, ctx: commands.Context, *, time_str: str):
        async with ctx.typing():
            if time_str:
                try:
                    await ctx.send(tt(time_str))
                    await command_log_and_err(ctx, self.client, status="Success")
                except ValueError:
                    await command_log_and_err(ctx, self.client, err_code='Err_90612',
                                              text=f"`{time_str}` is not a valid format... 24hr:00 day/month/year")
            else:
                await command_log_and_err(ctx, self.client, err_code="Err_90648",
                                          text="You haven't given the timestamp to compare time.")

    @commands.command(aliases=['cd', 'covidata'], name='Covid Data',
                      help='Returns covid statistics for the whole world or a country',
                      usage='$covidata|cd (country)', brief='☣907')
    async def covidata(self, ctx: commands.Context, *, country: str = None):
        async with ctx.typing():
            wm_logo = 'https://www.worldometers.info/img/worldometers-logo.gif'
            if country:
                cdata = await self.cocase.compile_by_country(country.strip().lower())
                await ctx.send(embed=await set_timestamp(Embed(title=f'`{country.strip().title()}` - Covid Statistics',
                 description=
                 f"""
`Total     - {cdata.get("Total"):^12}`
`Recovered - {cdata.get("Recovered"):^12}`
`Deaths    - {cdata.get("Deaths"):^12}`
`Active    - {cdata.get("Active"):^12}`
""", colour=Colour.random()).set_thumbnail(url=wm_logo)))
            else:
                cdata = await self.cocase.compile_data()
                await ctx.send(embed=await set_timestamp(Embed(title='Worldwide Covid Statistics',
                description=
f"""
`Total     - {cdata.get("Total"):^12}`
`Recovered - {cdata.get("Recovered"):^12}`
`Deaths    - {cdata.get("Deaths"):^12}`
`Active    - {cdata.get("Active"):^12}`
"""
, colour=Colour.random()).set_thumbnail(url=wm_logo)))
            await command_log_and_err(ctx, self.client, status=country or 'Worldwide' + ' Successful')


def setup(client):
    client.add_cog(Misc(client))