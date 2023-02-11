import datetime
import json
import logging
import discord

from . import loop, Cog, Bot, command, Context, TextChannel

log = logging.getLogger(__name__)


class Backup(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.name = 'backup'

    @Cog.listener()
    async def on_ready(self):
        self.backup_channels.start()

    async def _backup(self, chnl = None):
        path = 'C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/'

        with open(f'{path}backup_config.json', 'r') as f:
            config: dict[int, dict] = json.load(f)

        with open(f'{path}backup.json', 'r') as f:
            backup: dict = json.load(f)

        for channel, details in config.items():
            if chnl:
                channel = str(chnl)
                details = config[channel]

            last_updated = details.get('last_updated', datetime.datetime(datetime.date.today().year,
                                                                         datetime.date.today().month,
                                                                         int(datetime.date.today().day) - 1).timestamp())

            try: source = await self.bot.fetch_channel(int(channel))
            except discord.Forbidden: pass
            else:
                messages = {message.id: {
                    'author': message.author.id,
                    'url': message.jump_url,
                    'attachments': {
                        attachment.id: {
                            'spoiler': attachment.is_spoiler(),
                            'url': attachment.url
                        }
                        for attachment in message.attachments
                    },
                    'content': message.content,
                    'created': message.created_at.timestamp(),
                    'embeds': [embed.to_dict() for embed in message.embeds],
                    'pinned': message.pinned,
                    'reactions': [str(reaction.emoji) for reaction in message.reactions]
                } async for message in source.history(after=datetime.datetime.fromtimestamp(last_updated, tz=datetime.datetime.now().tzinfo), oldest_first=True, limit=None)}

                backup[channel].update(messages)

                details['last_updated'] = datetime.datetime.now().timestamp()

            if chnl:
                break


        with open(f'{path}backup_config.json', 'w') as f:
            json.dump(config, f, indent=3)


        with open(f'{path}backup.json', 'w') as f:
            json.dump(backup, f, indent=3)

        return last_updated

    @loop(time=datetime.time(23, 30))
    async def backup_channels(self):
        await self._backup()

    @command()
    async def backup(self, ctx: Context, channel: TextChannel = None):
        if not channel:
            channel = ctx.channel

        last_updated = await self._backup(channel.id)

        await ctx.reply(
            f'Previous succesful backup of {channel.mention}: '
            f'`{datetime.datetime.fromtimestamp(last_updated, tz=datetime.datetime.now().tzinfo).strftime("%d %B %Y at %X:%f")}`\n'
            f'Finished backing up.')


async def setup(bot: Bot):
    await bot.add_cog(Backup(bot))
