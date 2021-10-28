from discord.ui import View, Button, Item, button, Select, select
from discord import SelectOption, CategoryChannel, TextChannel, VoiceChannel
from discord.ext.commands import Context
from discord import Interaction, ButtonStyle
from .errors import *
from .components import *
from discord import Thread


HOME_SERVER_INVITE = 'https://discord.gg/zt6j4h7ep3'


class BaseView(View):
    def __init__(self, ctx: Context, timeout: float = 180.0, **kwargs):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.extras = kwargs
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


class ThreadConfirmation(BaseView):
    def args_check(self):
        kwrgs = self.extras.keys()
        if 'thread' not in kwrgs or 'method' not in kwrgs:
            missing_arg = '"thread"' if 'thread' not in kwrgs else '"method"'
            missing_arg = '"thread" and "method"' if 'thread' not in kwrgs and 'method' not in kwrgs else missing_arg
            raise ThreadNotSpecified(f'Argument {missing_arg} was not given.')
        if not isinstance(self.extras['thread'], Thread):
            raise TypeError('Argument "thread" is not of type Thread.')
        if self.extras['method'].lower() not in ('leave', 'join'):
            raise ValueError('Incorrect values passed to argument "method"')

    @button(label="Yes", custom_id="JoinThreadYes", style=ButtonStyle.green)
    async def yes(self, _button: Button, interaction: Interaction):
        if self.extras['method'].lower() == 'join':
            await self.extras['thread'].join()
            verb = 'Joined'
        else:
            await self.extras['thread'].leave()
            verb = 'Left'
        await interaction.response.send_message(content=f'{verb} {self.extras["thread"].mention}', ephemeral=True)
        await self.disable_all()

    @button(label="No", custom_id="JoinThreadNo", style=ButtonStyle.red)
    async def no(self, _button: Button, interaction: Interaction):
        verb = 'join' if self.extras['method'].lower() == 'join' else 'leav'
        await interaction.response.send_message(content=f"Okay, not {verb}ing {self.extras['thread'].mention}", ephemeral=True)
        await self.disable_all()


class JoinHomeServer(BaseView):
    def __init__(self, ctx: Context, timeout: float = 180.0, **kwargs):
        super().__init__(ctx, timeout, **kwargs)
        self.add_item(Button(style=ButtonStyle.link, url=HOME_SERVER_INVITE, label='Join Home Server'))


class SelectChannelCategoryView(BaseView):
    def __init__(self, ctx: Context,  **kwargs):
        self.extras = kwargs
        self.args_check()
        super().__init__(ctx, 10.0, **kwargs)
        options = [
            SelectOption(label=cat.name, value=str(cat.id)) for cat in ctx.guild.categories
        ]
        select_ = CategorySelect(self.extras['channel'])
        [select_.append_option(option) for option in options]
        self.add_item(select_)


    def args_check(self):
        if not self.extras.get('channel'):
            raise MissingArgument('Argument "channel" is missing.')
        if not isinstance(self.extras['channel'], (TextChannel, VoiceChannel)):
            raise TypeError("Arg 'channel' is not of type TextChannel or VoiceChannel")
