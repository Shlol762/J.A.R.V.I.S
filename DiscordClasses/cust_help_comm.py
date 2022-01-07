from nextcord import Embed
from nextcord.ext import commands

class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()
        self.pages: Embed = Embed(description=None)

    async def work_in_prog(self):
        await self.get_destination().send(f"Sorry {self.context.author.name}... The help command is going through"
                                          f" a slight `renovation`. Please wait until this weekend "
                                          f"or use the `help1` command(its like the old one), cuz `Shlol` might be `busy` with `9th grade`"
                                          f" sorry for the inconvenience")

    def get_bot_mapping(self):
        bot: commands.Bot = self.context.bot
        mapping = {
            cog: cog.get_commands()
            for cog in bot.cogs.values()
        }
        unwanted_cogs = []
        for cog in mapping.keys():
            if len(mapping[cog]) == 0: unwanted_cogs.append(cog)
        for cog in unwanted_cogs: mapping.pop(cog)
        return mapping

    async def send_bot_help(self, mapping: dict):
        print(len(mapping))

    async def send_command_help(self, command: commands.Command):
        await self.work_in_prog()

    async def send_cog_help(self, cog):
        await self.get_destination().send(f"{cog}: {cog.get_commands()}")

