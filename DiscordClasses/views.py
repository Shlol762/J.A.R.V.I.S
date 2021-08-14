from discord.ui import View, Button, Item, button, Select, select
from discord import SelectOption
from discord.ext.commands import Context
from discord import Interaction, ButtonStyle
from .errors import ThreadNotSpecified
from discord import Thread


HOME_SERVER_INVITE = 'https://discord.gg/zt6j4h7ep3'


class BaseView(View):
    def __init__(self, ctx: Context, timeout: float = 180.0, **kwarks):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.extras = kwarks
        self.args_check()

    def args_check(self):
        pass

    async def disable_all(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)

    async def on_timeout(self):
        await self.disable_all()


class Confirmation(BaseView):
    def args_check(self):
        if 'confirm' not in self.extras.keys():
            self.extras['confirm'] = None
        elif self.extras['confirm'] not in (False, True, None):
            self.extras['confirm'] = None

    @button(label="Yes", custom_id="YesButton", style=ButtonStyle.green, emoji='👍')
    async def yes(self, _button: Button, interaction: Interaction):
        await interaction.message.edit(content="Yes")
        await self.disable_all()

    @button(label="No", custom_id="NoButton", style=ButtonStyle.red, emoji='👎')
    async def no(self, _button: Button, interaction: Interaction):
        await interaction.message.edit(content="No")
        await self.disable_all()


class ThreadJoinConfirmation(BaseView):
    def args_check(self):
        if 'thread' not in self.extras.keys():
            raise ThreadNotSpecified('Argument "thread" was not given.')
        if not isinstance(self.extras['thread'], Thread):
            raise ValueError('Argument "thread" is not of type Thread.')

    @button(label="Yes", custom_id="JoinThreadYes", style=ButtonStyle.green, emoji='👍')
    async def yes(self, _button: Button, interaction: Interaction):
        await self.extras['thread'].join()
        await interaction.message.edit(content=f'Joined thread: {self.extras["thread"].mention}')
        await self.disable_all()

    @button(label="No", custom_id="JoinThreadNo", style=ButtonStyle.red, emoji='👎')
    async def no(self, _button: Button, interaction: Interaction):
        await interaction.message.edit(content=f"Okay, not joining {self.extras['thread'].mention}")
        await self.disable_all()


class JoinHomeServer(BaseView):
    def __init__(self, ctx: Context, timeout: float = 180.0, **kwargs):
        super().__init__(ctx, timeout, **kwargs)
        self.add_item(Button(style=ButtonStyle.link, url=HOME_SERVER_INVITE, label='Join Home Server'))