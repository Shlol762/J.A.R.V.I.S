import discord, os
from discord.ext.commands import AutoShardedBot
from datetime import datetime
from DiscordClasses import FRIDAY_TOKEN


intents = discord.Intents.all()
friday = AutoShardedBot(command_prefix='friday ', strip_after_prefix=True,
                        intents=intents, status=discord.Status.dnd,
                        case_insensitive=True)

for cog in os.listdir("C:/Users/Shlok/J.A.R.V.I.SV2021/FriCogs"):
    if cog.endswith(".py") and cog != '__init__.py':
        friday.load_extension(f'FriCogs.{cog[:-3]}')


try: friday.run(FRIDAY_TOKEN)
except (KeyboardInterrupt, RuntimeError): pass
finally:  print(f"\nConnection to internet termniated willingly: {datetime.now().strftime('%d %B %Y at %X:%f')}")
