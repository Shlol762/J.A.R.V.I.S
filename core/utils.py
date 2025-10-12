import argparse
import discord
from datetime import datetime
from discord.ext import commands
import re
import sqlite3


def isValidToken(token_str: str) -> bool:
    """
    Checks any given string for the pattern of a valid discord token.

    Args:
        token_str (str): The string to check for token.

    Returns:
        bool: 
    """
    return (True if re.search(r"[A-Za-z0-9\-_]{24,26}\.[\w-]{6}\.[\w-]{27,38}", token_str) else False)


def snowflake_time(snowflake_id: int) -> datetime:
    """
    Return creation time from a Discord snowflake ID.

    Args:
        snowflake_id (int): Discord snowflake identifier.

    Returns:
        datetime: Naive datetime from the ID's embedded timestamp.

    Raises:
        TypeError: If snowflake_id is not an int.
        ValueError: If snowflake_id is negative.
    """
    if not isinstance(snowflake_id, int):
        raise TypeError("snowflake_id must be an int")
    if snowflake_id < 0:
        raise ValueError("snowflake_id must be non-negative")

    time = ((snowflake_id >> 22) + 1420070400000) / 1000
    return datetime.fromtimestamp(time)


def get_args() -> argparse.Namespace:
    """
    Builds argument parser for main bot file.

    Returns:
        argpase.Namsespace: User input arguments
    """

    parser = argparse.ArgumentParser(description="Run JARVIS in various configurations.")
    parser.add_argument("--token", type=str, help="Bot token (overrides .env).")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging.")
    parser.add_argument("--guild", type=int, help="Limit slash commands to a test guild ID.")
    parser.add_argument("--cogs", nargs="+", help="List of cogs/extensions to load only.")
    parser.add_argument("--env", type=str, default="dev", help="Environment: dev/prod/etc.")
    parser.add_argument("--reload", action="store_true", help="Enable hot-reload for cogs.")
    parser.add_argument("--safe-mode", action="store_true", help="Load minimal features.")  

    return parser.parse_args()


def load_db(name: str):
    connection = sqlite3.connect(f"{name}.db")

    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS guild_settings ( guild_id INTEGER PRIMARY KEY, prefix TEXT DEFAULT '$' )")

    connection.commit()
    connection.close()


async def get_prefix(bot: commands.Bot, message: discord.Message) -> str:
    """
    Multi-Prefix modifier for the bot.
    
    Args:
        bot (commands.Bot): The active bot instance which will use returned prefix.
        message (discord.Message): The message in which prefix is to be parsed.

    Returns:
        str: Prefix for given context.
    """

    id = str(message.guild.id) if message.guild else "20250814"
    for_guild = bot.prefixes.get(id) or bot.prefixes.get(int(id))
    return for_guild


def prefixExists(bot: commands.Bot, message: discord.Message) -> bool:
    """
    Checks if a prefix exists for a given guild.
    
    Args:
        bot (commands.Bot): The active bot instance which will check for prefix.
        message (discord.Message): The message in which prefix is to be parsed.

    Returns:
        bool: Whether or not a prefix exists for the guild.
    """
    return bool(bot.prefixes.get(str(message.guild.id)))
