import disnake, datetime, os
from disnake.ext.commands import AutoShardedBot, Context
from DiscordClasses import ULTRON_TOKEN


intents = disnake.Intents.all()
ultron = AutoShardedBot(command_prefix='ultron ', case_insensitive=True, intents=intents,
                   allowed_mentions=disnake.AllowedMentions(),
                   strip_after_prefix=True, status=disnake.Status.dnd)


@ultron.command(name='kill')
async def kill(ctx: Context, member: disnake.Member):
    await ctx.send("Thought you'd never ask! With pleasure!")

@ultron.event
async def on_message(message: disnake.Message):
    await ultron.process_commands(message)


try: ultron.run(ULTRON_TOKEN)
except (KeyboardInterrupt, RuntimeError): pass
finally: print(f"\nConnection to internet termniated willingly: {datetime.datetime.now().strftime('%d %B %Y at %X:%f')}")
