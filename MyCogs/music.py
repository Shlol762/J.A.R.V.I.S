import asyncio
import functools
import itertools
import math
import random
from typing import Optional
import discord
import youtube_dl
from async_timeout import timeout
from discord.ext import commands
from MyCogs import command_log_and_err, Context, Bot,\
    Cog, NoPrivateMessage, CommandError, command,\
    guild_only, PCMVolumeTransformer, FFmpegPCMAudio,\
    Embed, Colour, Client, VoiceChannel, comm_log_local

youtube_dl.utils.bug_reports_message = lambda: ''


class VoiceError(Exception):
    pass


class YTDLError(Exception):
    pass


class YTDLSource(PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: Context, source: FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return '**{0.title}** by **{0.uploader}**'.format(self)

    @classmethod
    async def create_source(cls, ctx: Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError(f'Couldn\'t find anything that matches `{search}`')

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError(f'Couldn\'t find anything that matches `{search}`')

        webpage_url = process_info['webpage_url']
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError(f'Couldn\'t fetch `{webpage_url}`')

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise YTDLError(f'Couldn\'t retrieve any matches for `{webpage_url}`')

        return cls(ctx, FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append(f'{days} days')
        if hours > 0:
            duration.append(f'{hours} hours')
        if minutes > 0:
            duration.append(f'{minutes} minutes')
        if seconds > 0:
            duration.append(f'{seconds} seconds')

        return ', '.join(duration)


class Song:
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        embed = (Embed(title='Now playing',
                               description='```css\n{0.source.title}\n```'.format(self),
                               color=Colour.blurple())
                 .add_field(name='Duration', value=self.source.duration)
                 .add_field(name='Requested by', value=self.requester.mention)
                 .add_field(name='Uploader', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
                 .add_field(name='URL', value='[`{0.source.title}`]({0.source.url})'.format(self))
                 .set_thumbnail(url=self.source.thumbnail))

        return embed


class SongQueue(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]


class VoiceState:
    def __init__(self, ctx: Context):
        self.bot: Bot = ctx.bot
        self._ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()

        self._loop = False
        self._volume = 0.5
        self.skip_votes = set()

        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()

            if not self.loop:
                # Try to get the next song within 3 minutes.
                # If no song will be added to the queue in time,
                # the player will disconnect due to performance
                # reasons.
                try:
                    async with timeout(180):  # 3 minutes
                        self.current = await self.songs.get()
                except asyncio.TimeoutError:
                    self.client.loop.create_task(self.stop())
                    return

            self.current.source.volume = self._volume
            self.voice.play(self.current.source, after=self.play_next_song)
            await self.current.source.channel.send(embed=self.current.create_embed())

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.songs.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None


class Music(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.voice_states = {}
        self.description = "A list of commands that control the bot's music functions."
        self.name = 'Music(ms)'

    def get_voice_state(self, ctx: Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(ctx, )
            self.voice_states[ctx.guild.id] = state
        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: Context):
        if not ctx.guild:
            raise NoPrivateMessage('This command can\'t be used in DM channels.')

        return True

    async def cog_before_invoke(self, ctx: Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: Context, error: CommandError):
        await ctx.reply(f'An error occurred: {str(error)}')

    @command(name='Join', aliases=['jn'], invoke_without_subcommand=True,
                      help="Joins a voice channel.", extras={'emoji': '⤵', 'number': '601'},
                      usage='join|jn')
    @guild_only()
    @comm_log_local
    async def _join(self, ctx: Context):
        destination = ctx.author.voice.channel
        await command_log_and_err(ctx, status='Success', joined=destination)
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return
        ctx.voice_state.voice = await destination.connect()

    @command(name='Summon', aliases=['smn'], extras={'emoji': '↙', 'number': '602'},
                      help="Summons the bot to a voice channel. If no channel was specified, it joins your channel.",
                      usage='summon|smn (channel)')
    @guild_only()
    @comm_log_local
    async def _summon(self, ctx: Context, *, channel: Optional[VoiceChannel] = None):
        if not channel and not ctx.author.voice:
            raise VoiceError('You are neither connected to a voice channel nor specified a channel to join.')
        destination: VoiceChannel = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return
        ctx.voice_state.voice = await destination.connect()
        await command_log_and_err(ctx, status='Success', joined=destination)

    @command(name='Leave', aliases=['disconnect', 'dc'],
                      help="Clears the queue and leaves the voice channel.",
                      usage='leave|disconnect|dc', extras={'emoji': '🚪', 'number': '603'})
    @guild_only()
    @comm_log_local
    async def _leave(self, ctx: Context):
        if not ctx.voice_state.voice:
            return await ctx.reply('Not connected to any voice channel.')
        await command_log_and_err(ctx, status='Success', left=ctx.author.voice.channel)
        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]

    @command(name='Volume', aliases=['v'], extras={'emoji': '🔊', 'number': '604'},
                      help="Sets the volume of the player.",
                      usage='volume|v <volume: out of hundred>')
    @guild_only()
    @comm_log_local
    async def _volume(self, ctx: Context, *, volume: int):
        if not ctx.voice_state.is_playing:
            return await ctx.reply('Nothing being played at the moment.')

        if 0 > volume > 100:
            return await ctx.reply('Volume must be between 0 and 100')

        await command_log_and_err(ctx, status='Success')
        ctx.voice_state.volume = volume / 100
        await ctx.reply(f'Volume of the player set to {volume}%')

    @command(name='Now', aliases=['n', 'current', 'playing'],
                      help='Displays the currently playing song.', extras={'emoji': '🎶', 'number': '605'},
                      usage='now|n|current|playing')
    @guild_only()
    @comm_log_local
    async def _now(self, ctx: Context):
        await command_log_and_err(ctx, status='Success')
        await ctx.reply(embed=ctx.voice_state.current.create_embed())

    @command(name='Pause', aliases=['ps'], extras={'emoji': '⏸', 'number': '606'},
                      help="Pauses the currently playing song.",
                      usage='pause|ps')
    @guild_only()
    @comm_log_local
    async def _pause(self, ctx: Context):
        await command_log_and_err(ctx, status='Success')
        if ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()

    @command(name='Resume', aliases=['res'], extras={'emoji': '▶', 'number': '607'},
                      help="Resumes a currently paused song.",
                      usage='resume|res')
    @guild_only()
    @comm_log_local
    async def _resume(self, ctx: Context):
        await command_log_and_err(ctx, status='Success')
        if ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()

    @command(name='Stop', aliases=['sp'], extras={'emoji': '⏹', 'number': '608'},
                      help="Stops playing song and clears the queue.",
                      usage='stop|sp')
    @guild_only()
    @comm_log_local
    async def _stop(self, ctx: Context):
        ctx.voice_state.songs.clear()
        await command_log_and_err(ctx, status='Success')
        if ctx.voice_state.voice.is_playing:
            ctx.voice_state.voice.stop()

    @command(name='Skip', aliases=['sk'], extras={'emoji': '⏭', 'number': '609'},
                      help="Vote to skip a song. The requester can automatically skip. 3 skip votes are needed for the song to be skipped.",
                      usage='skip|sk')
    @guild_only()
    @comm_log_local
    async def _skip(self, ctx: Context):
        if not ctx.voice_state.is_playing:
            return await ctx.reply('Not playing any music right now...')
        voter = ctx.message.author
        await command_log_and_err(ctx, status='Success')
        if voter == ctx.voice_state.current.requester:
            ctx.voice_state.skip()

        elif voter.id not in ctx.voice_state.skip_votes:
            ctx.voice_state.skip_votes.add(voter.id)
            total_votes = len(ctx.voice_state.skip_votes)

            if total_votes >= 3:
                ctx.voice_state.skip()
            else:
                await ctx.reply(f'Skip vote added, currently at **{total_votes}/3**')

        else:
            await ctx.reply('You have already voted to skip this song.')

    @command(name='Queue', aliases=['q'], extras={'emoji': '➡', 'number': '610'},
                      help="Shows the player's queue. You can optionally specify the page to show. Each page contains 10 elements.",
                      usage='queue|q (page number)')
    @guild_only()
    @comm_log_local
    async def _queue(self, ctx: Context, *, page: Optional[int] = 1):
        if len(ctx.voice_state.songs) == 0:
            return await ctx.reply('Empty queue.')

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += '`{0}.` [**{1.source.title}**]({1.source.url})\n'.format(i + 1, song)

        embed = (Embed(description='**{} tracks:**\n\n{}'.format(len(ctx.voice_state.songs), queue))
                 .set_footer(text='Viewing page {}/{}'.format(page, pages)))
        await command_log_and_err(ctx, status='Success')
        await ctx.reply(embed=embed)

    @command(name='Shuffle', aliases=['shfl'],
                      help="Shuffles the queue.", extras={'emoji': '🔀', 'number': '611'},
                      usage='shuffle|shfl')
    @guild_only()
    @comm_log_local
    async def _shuffle(self, ctx: Context):
        if len(ctx.voice_state.songs) == 0:
            return await ctx.reply('Empty queue.')

        await command_log_and_err(ctx, status='Success')
        ctx.voice_state.songs.shuffle()

    @command(name='Remove', aliases=['rem'], extras={'emoji': '➖', 'number': '612'},
                      help="Removes a song from the queue at a given index.",
                      usage='remove <index of song in queue>')
    @guild_only()
    @comm_log_local
    async def _remove(self, ctx: Context, index: int):
        if len(ctx.voice_state.songs) == 0:
            return await ctx.reply('Empty queue.')

        await command_log_and_err(ctx, status='Success')
        ctx.voice_state.songs.remove(index - 1)

    @command(name='Loop', aliases=['lp'], extras={'emoji': '🔁', 'number': '613'},
                      help="Loops the currently playing song. Invoke this command again to unloop the song.",
                      usage='loop|lp')
    @guild_only()
    @comm_log_local
    async def _loop(self, ctx: Context):
        if not ctx.voice_state.is_playing:
            return await ctx.reply('Nothing being played at the moment.')

        # Inverse boolean value to loop and unloop.
        await command_log_and_err(ctx, status='Success')
        ctx.voice_state.loop = not ctx.voice_state.loop

    @command(name='Play', aliases=['p'], extras={'emoji': '▶', 'number': '614'},
                      help="""Plays a song. If there are songs in the queue, this will be queued until the other songs finished playing. This command automatically searches from various sites if no URL is provided.""",
                      usage='play|p <query or url>')
    @guild_only()
    @comm_log_local
    async def _play(self, ctx: Context, *, search: str):
        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)
        async with ctx.typing():
            try:
                source = await YTDLSource.create_source(ctx, search, loop=ctx.bot.loop)
            except YTDLError as e:
                await ctx.reply(f'An error occurred while processing this request: {e}')
            else:
                song = Song(source)

                await ctx.voice_state.songs.put(song)
                await command_log_and_err(ctx, status='Success')
                await ctx.reply(f'Enqueued {str(source)}')

    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise CommandError('You are not connected to any voice channel.')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise CommandError('Bot is already in a voice channel.')


def setup(bot: Bot):
    bot.add_cog(Music(bot))
