from discord.ui import View, Button, Item, button
from discord.ext.commands import Context
from discord import Interaction, ButtonStyle

class BaseView(View):
    def __init__(self, ctx: Context, timeout: float = 180.0, **kwarks):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.kwargs = kwarks
        self.extras = {}

    async def disable_all(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)

    async def on_timeout(self):
        self.counter.disabled = True
        self.hey.disabled = True
        await self.message.edit(view=self)


class Confirmation(BaseView):
    @button(label="Yes", custom_id="YesButton", style=ButtonStyle.green, emoji='👍')
    async def yes(self, _button: Button, interaction: Interaction):
        await interaction.message.edit(content="Yes")
        await self.disable_all()

    @button(label="No", custom_id="NoButton", style=ButtonStyle.red, emoji='👎')
    async def no(self, _button: Button, interaction: Interaction):
        await interaction.message.edit(content="No")
        await self.disable_all()
