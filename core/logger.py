import logging
from discord.utils import _ColourFormatter 


def setup_logging(level=logging.INFO):
    """
    Set up root level logging project wide.
    """
    
    root = logging.getLogger()
    root.setLevel(level)

    
    if root.hasHandlers():
        root.handlers.clear()

    
    handler = logging.StreamHandler()
    handler.setFormatter(_ColourFormatter())
    root.addHandler(handler)


    file_handler = logging.FileHandler("./logs/bot.log", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)-8s] %(name)s: %(message)s"))
    root.addHandler(file_handler)
