import datetime
import re
from asyncio import get_event_loop
import asyncio
import aiohttp
import bs4
from bs4 import BeautifulSoup
from .custom_funcs import number_system, CricInfoCard
import nest_asyncio

url_time = None
url = None


class Cricket:
    __slots__ = [
        'tournament',
        '_tournament_url'
                ]

    ROOT_IMG_DIR = "C:/Users/Shlok/J.A.R.V.I.SV2021/image_resources/{}1.png"

    __TEAMS_INT__ = {
        'sri lanka': 'sl',
        'india': 'ind',
        'england': 'eng',
        'pakistan': 'pak',
        'australia': 'aus',
        'south africa': 'sa',
        'west indies': 'wi',
        'new zealand': 'nz',
        'zimbabwe': 'zim',
        'ireland': 'ire',
        'nottinghamshire': 'ntg',
        'hampshire': 'hms',

    }

    __TEAMS_IPL__ = {
        'royal challengers bangalore': 'rcb',
        'chennai super kings': 'csk',
        'kolkata knight riders': 'kkr',
        'punjab kings': 'pbks',
        'delhi capitals': 'dc',
        'rajasthan royals': 'rr',
        'mumbai indians': 'mi',
        'sunrisers hyderabad': 'srh'
                    }

    url = "https://www.espncricinfo.com"

    def __init__(self, tournament: str):
        self.tournament = tournament
        self._tournament_url = None

    def format_trnmnt_str(self, preformat_text: str):
        configs = [rf"(.)*{preformat_text.lower()}(.)*", ]
        if 'vs' in preformat_text:
            teams = preformat_text.split(" vs ")
            teams = [team_n for team_n in self.__TEAMS_INT__ for team in teams if re.search(r"^" + team, team_n)]
            configs.append("(.)*".join(teams).lower())
            configs.append("(.)*".join(teams[::-1]).lower())
        configs = [team.replace(' ', '-') for team in configs]
        return configs

    async def get_tournament_fixtures_link(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as request:
                soup = BeautifulSoup(await request.text(), 'lxml')
        self._tournament_url = '/'.join((self.url + ''.join([soup.find(href=re.compile(r'/series/' + t_url)).get('href') for t_url in self.format_trnmnt_str(self.tournament)
                                           if soup.find(href=re.compile(r'/series/' + t_url)) is not None])).split('/')[:5]) + '/match-schedule-fixtures'

    async def get_match_link(self) -> str:
        await self.get_tournament_fixtures_link()
        async with aiohttp.ClientSession() as session:
            async with session.get(self.tournament_url) as request:
                soup = BeautifulSoup(await request.text(), 'lxml')
        pattern = "^/" + '/'.join(self.tournament_url.split('/')[-3:-1]) + r'/(.)+/live-cricket-score'
        return self.url + (soup.find(href=re.compile(pattern)) or soup.find(href=re.compile(
            pattern.replace('/live-cricket-score', '/full-scorecard')))).get('href')

    async def get_match_data(self):
        async with aiohttp.ClientSession() as session:
            match_link = await self.get_match_link()
            async with session.get(match_link) as request:
                soup = BeautifulSoup(await request.text(), 'lxml')
        score = soup.select('.match-header .match-info .teams .team .score-detail .score-info')
        overs = soup.select('.match-header .match-info .teams .team .score-detail .score')
        dummy = ['', '']
        match = CricInfoCard(soup.find(class_=re.compile("^description")).text,
                             soup.select('.match-header .match-info .status span')[0].text,
                             soup.select('.match-header .match-info .status-text span')[0].text,
                             [team.text for team in soup.select('.match-header .match-info .teams .team .name-link p')],
                             ([scr.text for scr in score] or dummy) if score else dummy,
                             ([ovr.text for ovr in overs] or dummy) if overs else dummy,
                             dummy,
                             {'tournament': self.tournament_url, 'match': match_link})
        print(match.teams)
        match._icons = self.get_img(match.teams['team1']['name'], match.teams['team2']['name'])
        return match

    def get_img(self, *teams: str):
        return [self.ROOT_IMG_DIR.format(self.__TEAMS_IPL__.get(team.lower()) or self.__TEAMS_INT__.get(team.lower())) for team in teams]

    @property
    def tournament_url(self) -> str:
        return self._tournament_url


class WorldoMeter:
    __slots__ = ['url']
    __doc__ = """A class created for scraping Covid-19 information from https://www.worldometers.info"""

    def __init__(self):
        self.url = "https://www.worldometers.info"

    async def load_data(self, url_: str) -> BeautifulSoup:
        """Loads HTML data for scraping."""
        async with aiohttp.ClientSession() as session:
            async with session.get(url_) as req:
                soup = BeautifulSoup(await req.text(), "lxml")
                self.__setattr__('soup', soup)

    def get_wrldomtr_urls(self):
        """Get's href links to be processed"""
        confirm_url =[possible_url.get('href')
                      for possible_url in
                      self.soup.select('.container .navbar-collapse .nav a')]
        covid_weblink = self.url + confirm_url[0]
        self.__setattr__('covid_source', covid_weblink)
        # return covid_weblink

    def get_worldwide_covid_statistics(self) -> dict[str: int]:
        """Get's worldwide covid-19 data in the form of a dictionary."""
        get_event_loop().run_until_complete(self.load_data(self.covid_source))
        raw_data = self.soup.select(".container .row .content-inner .maincounter-number span")
        total, deaths, recovered = int(raw_data[0].text.replace(',', '')), int(raw_data[1].text.replace(',', '')), int(raw_data[2].text.replace(',', ''))
        data = {'Total': number_system(total),
                'Deaths': number_system(deaths),
                'Recovered': number_system(recovered),
                'Active': number_system(total-(deaths+recovered))}
        return data

    def get_by_country(self) -> dict[str: str]:
        """Get's each individual country's href link for countryvise data."""
        raw_data = self.soup.find_all('a', {'class': 'mt_a'})
        new_data: dict[str] = {}
        for data in raw_data:
            data: bs4.Tag = data
            if not isinstance(data, str):
                if 'country' in data.get('href') and 'coronavirus' not in data.get('href'):
                    new_data[data.text] = data.get('href')
        return new_data

    async def compile_data(self) -> dict[str: int]:
        """Compiles world Covid-19 data."""
        await self.load_data(self.url)
        self.get_wrldomtr_urls()
        return self.get_worldwide_covid_statistics()

    async def compile_by_country(self, country: str) -> dict[str: int]:
        """Get's covid info of specified country."""
        await self.compile_data()
        countries = self.get_by_country()
        for _country, link in countries.items():
            if country.lower().strip() in _country.lower(): break
            else: _country = None
        if _country is None: return None
        await self.load_data(self.covid_source + link)
        data = self.soup.select('.container .maincounter-number span')
        total, deaths, recovered = int(data[0].text.replace(',', '')), int(data[1].text.replace(',', '')), int(data[2].text.replace(',', ''))
        country_data = {'Total': number_system(total), 'Deaths': number_system(deaths), 'Recovered': number_system(recovered), 'Active': number_system(total-(deaths+recovered))}
        return country_data
