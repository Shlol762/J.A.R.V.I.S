from .codec import *
from .custom_funcs import *
from .embeds import *
from .message_funcs import *
from .version import *
from .web_scrapers import *
from .views import *
from .myclasses import *

BOT_DIR = "C:/Users/Shlok/bot_stuff/safe_docs/"


with open(BOT_DIR+"-... --- - ! - --- -.- . -..txt", "r") as f:
    BOT_TOKEN: str = f.read()

with open(BOT_DIR+"pingultron.txt", "r") as f:
    ULTRON_TOKEN: str = f.read()

with open(BOT_DIR+"friday.txt", "r") as f:
    FRIDAY_TOKEN: str = f.read()

__discord__ = discord.__version__
__version__ = '0.00.0'
