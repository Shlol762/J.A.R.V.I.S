import json
import re
from FriCogs import Cog, AutoShardedBot, Message
from datetime import datetime
from typing import Optional


class MentionPayload:
    def __init__(self, author: int, time: int, targets: dict[str, list[int]], jump_url: Optional[str]):
        self.author = author
        self.time = time
        self.channel_mentions = targets.get('channel', [])
        self.role_mentions = targets.get('role', [])
        self.mentions = targets.get('user', [])
        self.everyone = targets.get('everyone', [])
        print(targets)
        self.targets = targets
        self.message_link = jump_url

    def __str__(self):
        return f'{self.author} - {self.targets} @ {self.time}'

    def to_tuple(self):
        return str(self.author), f't{self.time};hl{self.message_link};tg{self.targets}'


class Events(Cog):
    message_count = 0
    ping_cache = {}


    def __int__(self, bot: AutoShardedBot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message):
        self.message_count += 1
        author_id = hex(message.author.id)
        now = hex(int(datetime.now().timestamp()*1000))
        targets = {}
        _type = None
        if message.mentions:
            if message.reference:
                _type = 'reply'
                targets[_type] = [hex(message.reference.cached_message.author.id)]
            else:
                _type = 'user'
                targets[_type] = [hex(user) for user in message.raw_mentions]
        if message.channel_mentions:
            _type = 'channel'
            targets[_type] = [hex(chnl) for chnl in message.raw_channel_mentions]
        if message.role_mentions:
            _type = 'role'
            targets[_type] = [hex(role) for role in message.raw_role_mentions]
        if message.mention_everyone:
            _type = 'everyone'
            targets[_type] = [hex(len(re.findall(r'@everyone|@here', message.content)))]
        if message.reference:
            _type = 'reply'
            targets[_type] = [hex(message.reference.cached_message.author.id)]
        if _type:
            payload = MentionPayload(author_id, now, targets, message.jump_url).to_tuple()
            print(payload)
            if not self.ping_cache.get(message.channel.id):
                self.ping_cache[str(message.channel.id)] = {}
            self.ping_cache[str(message.channel.id)][payload[0]] = payload[1]
        if re.search(r'^(\$w(ho)?p(inged)?|refresh pings?)', message.content) or len(self.ping_cache) > 10 or self.message_count > 20:
            path = "C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/pings.json"
            with open(path, 'r') as f:
                pings: dict = json.load(f)
            
            with open(path, "w") as f:
                pings.update(self.ping_cache)
                json.dump(pings, f, indent=3)




def setup(bot: AutoShardedBot):
    bot.add_cog(Events(bot))
#hex(snowflake)->dict[type:list(hex(snowflake))]@hex(unix(datetime.now))