from MyCogs import Cog, command, Bot


class Captains(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.name = "Captains(cs)"
        self.description = ""


def setup(bot: Bot):
    bot.add_cog(Captains(bot))