import discord
import logging
import os
from core import exceptions, utils, bot, setup_logging
from discord.ext import commands
from dotenv import load_dotenv


# --- Parse arguments ---
args = utils.get_args()


# --- Logging ---
setup_logging(logging.DEBUG if args.debug else logging.INFO)
log = logging.getLogger(__name__)

log.info("Starting...")

# --- Load environment variables ---
load_dotenv()
TOKEN = args.token or os.getenv("TOKEN")
try:
    if not utils.isValidToken(TOKEN):
        raise exceptions.InvalidToken(f"Given token: {TOKEN} is INVALID.")
except exceptions.InvalidToken:
    log.exception("User tried to start bot with invalid discord token.")


# --- Initialise Bot ---
bot = bot.Jarvis(modes=args)


# --- Sync commands to guild (fast for dev) ---
# @bot.event
# async def on_ready():
#     logging.info(f"Logged in as {bot.user} (env: {args.env})")
#     if args.guild:
#         guild = discord.Object(id=args.guild)
#         bot.tree.copy_global_to(guild=guild)
#         await bot.tree.sync(guild=guild)
#         logging.info(f"Slash commands synced to guild {args.guild}")
#     else:
#         await bot.tree.sync()
#         logging.info("Slash commands synced globally (may take 1h).")


if __name__ == "__main__":
    try:
        bot.run(TOKEN, log_handler=None)
    except KeyboardInterrupt:
        log.info("Shutdown requested (Ctrl+C).")
else:
    raise exceptions.NotImportableError("This is the bot file. There's nothing here. "
                                         "What on earth are you importing??")

