import datetime
from asyncio import get_event_loop
import asyncio
import aiohttp
import bs4
import requests
from bs4 import BeautifulSoup
from .custom_funcs import time_set, number_system
import nest_asyncio

url_time = None
url = None


class Cricket:
    __slots__ = ['status', 'score1', 'score2', 'team1', 'team2',
                 'match_per', 'match_tim', 'match_num', 'match_loc', 'match_date',
                 'match_ser', 'pt_rank1', 'pt_rank2', 'pt_rank3', 'pt_rank4',
                 'pt_rank5', 'pt_rank6', 'pt_rank7', 'pt_rank8', 'pt_table',
                 'teams_short_long', 'pt_ipl_logo', 'ipl_team_logos_web',
                 'ipl_team_logos_local']
    __doc__ = """A class created for scraping IPL information from https://www.espncricinfo.com/live-cricket-score
            with the help of BeautifulSoup."""

    def __init__(self):
        global url_time
        global url
        hour: datetime.datetime = datetime.datetime.now().strftime('%I')
        try:
            if url_time != hour:
                url = "https://www.espncricinfo.com/live-cricket-score"
                soup = get_event_loop().run_until_complete(self.load_data(url))

                url_list: bs4.ResultSet = soup.select('.match-finder-body .match-score-block a')
                for link in url_list:
                    if '/ipl-2021-1249214/' in link.get('href'):
                        if 'https://wassets.hscicdn.com/' not in link.get('href'):
                            if 'live-cricket-score' in link.get('href'):
                                url_n: str = link.get('href')
                                break
                url = url.replace('/live-cricket-score', url_n)
                url_time = hour
            soup = get_event_loop().run_until_complete(self.load_data(url))
            teams, scores = soup.select('.match-header .teams .name-detail p'), soup.select(
                '.match-header .score-detail span')
            # teams, scores = [teams[0].text, teams[1].text], [scores[0].text, scores[1].text, scores[2].text, scores[3].text]
            try:
                self.status: str = soup.select('.match-header .status-text span')[0].text.replace('RRR', 'Req Run Rate')
                status_load: bool = True
            except IndexError:
                self.status = 'Match status is unknown.'
                status_load = False
        except UnboundLocalError:
            teams, scores = ['N/A', 'N/A'], ['', '', '', '']
            self.status = 'N/A'
            status_load = False
        if self.status.lower() == 'match yet to begin' or status_load is False:
            self.score1: str = ''
            self.score2: str = ''
        elif ('chose to' in self.status.lower()) or ('won by' in self.status.lower()) or (
                ' need ' in self.status.lower()) or ('innings break' in self.status.lower()):
            if len(scores) > 1:
                if scores[0].text == '':
                    self.score1 = f'{scores[1].text} in (20/20 ov)'
                else:
                    self.score1 = f'{scores[1].text} in {scores[0].text}'
            else:
                self.score1 = ''
            if len(scores) > 3:
                if scores[2].text == '':
                    self.score2 = f'{scores[3].text} in (20/20 ov)'
                else:
                    self.score2 = f'{scores[3].text} in {scores[2].text}'
            else:
                self.score2.text = ''
        try: self.team1, self.team2 = teams[0].text, teams[1].text
        except AttributeError: self.team1, self.team2 = teams[0], teams[1]
    # self.score1, self.score2, self.score3, self.score4 = scores[0], scores[1], scores[2], scores[3]
        try:
            description = soup.select('.match-header .event .description')[0].text.split(',')
        except IndexError:
            description = 'N/A'
        if description != 'N/A':
            if '(N)' in description[0]:
                self.match_per = 'Night'
                self.match_tim = '7:30 p.m.'
            elif '(D/N)' in description[0]:
                self.match_per = 'Day/Night'
                self.match_tim = '3:30 p.m.'
            self.match_num = description[0][:2]
            self.match_loc = description[1]
            self.match_date = description[2]
            self.match_ser = description[3]
        else:
            self.match_per = 'N/A'
            self.match_ser = 'N/A'
            self.match_num = 'N/A'
            self.match_tim = 'N/A'
            self.match_loc = 'N/A'
            self.match_date = 'N/A'
        # Points table attrs
        point_table_url = 'https://www.espncricinfo.com/series/ipl-2021-1249214/points-table-standings'
        soup = get_event_loop().run_until_complete(self.load_data(point_table_url))
        pt_teams = soup.select('.table-responsive .section-header h5')
        pt_table = soup.select('.table-responsive .table td')
        total_matches = [pt_table[1].text, pt_table[11].text, pt_table[21].text, pt_table[31].text,
                         pt_table[41].text, pt_table[51].text, pt_table[61].text, pt_table[71].text]
        wins = [pt_table[2].text, pt_table[12].text, pt_table[22].text, pt_table[32].text,
                pt_table[42].text, pt_table[52].text, pt_table[62].text, pt_table[72].text]
        loses = [pt_table[3].text, pt_table[13].text, pt_table[23].text, pt_table[33].text,
                 pt_table[43].text, pt_table[53].text, pt_table[63].text, pt_table[73].text]
        ties = [pt_table[4].text, pt_table[14].text, pt_table[24].text, pt_table[34].text,
                pt_table[44].text, pt_table[54].text, pt_table[64].text, pt_table[74].text]
        nr = [pt_table[5].text, pt_table[15].text, pt_table[25].text, pt_table[35].text,
              pt_table[45].text, pt_table[55].text, pt_table[65].text, pt_table[75].text]
        pt = [pt_table[6].text, pt_table[16].text, pt_table[26].text, pt_table[36].text,
              pt_table[46].text, pt_table[56].text, pt_table[66].text, pt_table[76].text]
        nrr = [pt_table[7].text, pt_table[17].text, pt_table[27].text, pt_table[37].text,
               pt_table[47].text, pt_table[57].text, pt_table[67].text, pt_table[77].text]
        self.pt_rank1 = [pt_teams[0].text,  # Team Name
                         total_matches[0],
                         wins[0],
                         loses[0],
                         ties[0],
                         nr[0],
                         pt[0],
                         nrr[0]]
        self.pt_rank2 = [pt_teams[1].text,  # Team Name
                         total_matches[1],
                         wins[1],
                         loses[1],
                         ties[1],
                         nr[1],
                         pt[1],
                         nrr[1]]
        self.pt_rank3 = [pt_teams[2].text,  # Team Name
                         total_matches[2],
                         wins[2],
                         loses[2],
                         ties[2],
                         nr[2],
                         pt[2],
                         nrr[2]]
        self.pt_rank4 = [pt_teams[3].text,  # Team Name
                         total_matches[3],
                         wins[3],
                         loses[3],
                         ties[3],
                         nr[3],
                         pt[3],
                         nrr[3]]
        self.pt_rank5 = [pt_teams[4].text,  # Team Name
                         total_matches[4],
                         wins[4],
                         loses[4],
                         ties[4],
                         nr[4],
                         pt[4],
                         nrr[4]]
        self.pt_rank6 = [pt_teams[5].text,  # Team Name
                         total_matches[5],
                         wins[5],
                         loses[5],
                         ties[5],
                         nr[5],
                         pt[5],
                         nrr[5]]
        self.pt_rank7 = [pt_teams[6].text,  # Team Name
                         total_matches[6],
                         wins[6],
                         loses[6],
                         ties[6],
                         nr[6],
                         pt[6],
                         nrr[6]]
        self.pt_rank8 = [pt_teams[7].text,  # Team Name
                         total_matches[7],
                         wins[7],
                         loses[7],
                         ties[7],
                         nr[7],
                         pt[7],
                         nrr[7]]
        self.pt_table = [self.pt_rank1, self.pt_rank2, self.pt_rank3, self.pt_rank4,
                         self.pt_rank5, self.pt_rank6, self.pt_rank7, self.pt_rank8]
        self.teams_short_long = {"rcb": "Royal Challengers Bangalore",
                                 "csk": "Chennai Super Kings",
                                 "pbks": "Punjab Kings",
                                 "mi": "Mumbai Indians",
                                 "rr": "Rajasthan Royals",
                                 "dc": "Delhi Capitals",
                                 "srh": "Sunrisers Hyderabad",
                                 "kkr": "Kolkata Knight Riders"}
        self.pt_ipl_logo = 'https://www.searchpng.com/wp-content/uploads/2019/05/IPL-Logo-Player-PNG.jpg'
        self.ipl_team_logos_web = {
            'Royal Challengers Bangalore': 'https://cricnerds.com/wp-content/uploads/2020/02/rcb-new-768x760.jpg',
            'Chennai Super Kings': 'https://t20ipl.co.in/wp-content/uploads/2020/06/CHENNAI-SUPER-KINGS-CSK.png',
            'Sunrisers Hyderabad': 'https://t20ipl.co.in/wp-content/uploads/2020/06/srh_wallpaper_logo_option-min.png',
            'Kolkata Knight Riders': 'https://fsa.zobj.net/crop.php?r=f_MwXqGgpc5VD2u10uQzN2auiG6QB0ttX0OMAslcH4b87HGX-9vO6k7QSZT9ESuBU0UMBgY8Mi6s-cb1MT0u807p6p4aLxr0hAN31kOJ9Qr_vyupMe4wzLnB0XIscWJMoDVG2cMR7r9qS3xF',
            'Mumbai Indians': 'https://t20ipl.co.in/wp-content/uploads/2020/06/mi_logo_option-min.png',
            'Punjab Kings': 'https://1.bp.blogspot.com/-TiKoe2N95Yg/YFmEDprNw6I/AAAAAAAAAEk/NsNqwuunci4YrmDAl9aMJgMryYisGZ44QCLcBGAsYHQ/s320/WhatsApp%2BImage%2B2021-03-23%2Bat%2B11.28.50%2BAM.jpeg',
            'Delhi Capitals': 'https://t20ipl.co.in/wp-content/uploads/2020/06/dc_wallpaper_logo_option-min.png',
            'Rajasthan Royals': 'https://www.passionateinmarketing.com/wp-content/uploads/2013/04/rr_logo.jpg'}
        path = 'C:/Users/Shlok/J.A.R.V.I.SV2021/image_resources/'
        self.ipl_team_logos_local = {
            'Royal Challengers Bangalore': path + 'rcb1.png',
            'Chennai Super Kings': path + 'csk1.png',
            'Sunrisers Hyderabad': path + 'srh1.png',
            'Kolkata Knight Riders': path + 'kkr1.png',
            'Mumbai Indians': path + 'mi1.png',
            'Punjab Kings': path + 'pbks1.png',
            'Delhi Capitals': path + 'dc1.png',
            'Rajasthan Royals': path + 'rr1.png'}

    async def load_data(self, url_to_parse: str) -> BeautifulSoup:
        """Loads the HTML data for scraping."""
        async with aiohttp.ClientSession() as session:
            async with session.get(url_to_parse) as req:
                return BeautifulSoup(await req.text(), 'lxml')

    def get_future_match(self, match_number: str = None, match_date: str = None, team1: str = None, team2: str = None):
        """No function yet."""
        url1 = 'https://www.espncricinfo.com/series/ipl-2021-1249214/match-schedule-fixtures'
        r = requests.get(url1, proxies={'https': None})
        soup = BeautifulSoup(r.text, "html.parser")
        statuses = soup.select('.team-scores-page .card .match-score-block .match-info .status span')
        for status in statuses:
            time = datetime.datetime.strptime(status.text, '%d-%b-%Y, %I:%M %p')
            print(time_set(time, "%d %b %Y at %I:%M %p"), ' - ', status.text)


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
