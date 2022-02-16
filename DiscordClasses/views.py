import re, traceback, sys
from disnake.ui import View, Button, Item, button, Select, select
from disnake import SelectOption,\
    CategoryChannel, TextChannel,\
    VoiceChannel, Thread, Interaction,\
    ButtonStyle, Message, InteractionMessage
from disnake.ext.commands import Context
from .errors import *
from .components import *



HOME_SERVER_INVITE = 'https://discord.gg/zt6j4h7ep3'


class BaseView(View):
    def __init__(self, ctx: Interaction, timeout: float = 180.0, **kwargs):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.extras = kwargs
        self.message: Message = None
        self.args_check()

    def args_check(self):
        pass

    async def disable_all(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self) if self.message else await self.ctx.edit_original_message(view=self)

    async def on_timeout(self):
        await self.disable_all()

    async def interaction_check(self, interaction: Interaction) -> bool:
        return self.ctx.user == interaction.user

    async def kill(self):
        for item in self.children:
            if isinstance(item, Button):
                item.style = ButtonStyle.red
                item.label = 'Error!'
            else:
                item.placeholder = "Error! Contact Shlol#2501"
            item.disabled = True
        await self.message.edit(view=self) if self.message else await self.ctx.edit_original_message(view=self)

    async def on_error(self, error: Exception, item: Item, interaction: Interaction):
        await self.kill()
        file = sys.stderr
        lines = f'\nIgnoring exception in view {self.__class__.__name__} for item \'{item.custom_id}\':\n'+ ''.join(traceback.format_exception(error.__class__, error, error.__traceback__))
        print(lines, file=file)
        await interaction.response.send_message(f"**Error!** Contact <@613044385910620190>\n```nim\n{lines}\n```", ephemeral=True)


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
    def __init__(self, ctx: Interaction,  **kwargs):
        self.extras = kwargs
        self.args_check()
        self.ctx = ctx
        super().__init__(self.ctx, 10.0, **kwargs)
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


class ConfirmDeletion(BaseView):
    def args_check(self):
        if not self.extras.get('channel'):
            raise MissingArgument('Argument "channel" is missing.')
        if not isinstance(self.extras['channel'], (TextChannel, VoiceChannel, CategoryChannel, Thread)):
            raise TypeError("Argument 'channel' must be of type TextChannel, VoiceChannel, CategoryChannel or Thread.")


class HelpView(BaseView):
    def args_check(self):
        if not self.extras.get('options'):
            raise MissingArgument("'options' was not given.")
        for arg in self.extras['options']:
            if not isinstance(arg,  SelectOption):
                raise TypeError(f"option {self.extras['optins'].index(arg)} was of invalid type: {arg.__class__.__name__}")


class ConversionView(BaseView):
    def args_check(self):
        if not self.extras.get('text'):
            raise MissingArgument("'text' was not specified.")
        if not isinstance(self.extras['text'], (int, float, str)):
            raise TypeError(f"Object must be of type(s) str, int or float and not {self.extras['text'].__class__.__name__}")

    @button(label="ASCII", custom_id='asciibutton', style=ButtonStyle.grey)
    async def _ascii(self, _button: Button, interaction: Interaction):
        text: str = self.extras['text']
        if text.startswith('0x'):
            type_ = 'Hex'
            text = text.replace('0x', '').replace(' ', '')
            translated = ''.join([chr(int('0x'+val, base=16)) for val in re.findall(r'.{2}', text)])
        elif text.startswith('0b'):
            type_ = 'Binary'
            text = text.replace('0b', '').replace(' ', '')
            translated = ''.join([chr(int('0b' + val, base=2)) for val in re.findall(r'[01]{8}', text)])
        elif not text.isalpha():
            type_ = 'Decimal'
            text = text.split()
            translated = ''.join([chr(int(val)) for val in text])

        _button.style = ButtonStyle.green
        await self.disable_all()
        await interaction.response.send_message(f'Converted from {type_} to ASCII: `{translated}`', ephemeral=True)

    @button(label="Hex", custom_id='hexbutton', style=ButtonStyle.grey)
    async def _hex(self, _button: Button, interaction: Interaction):
        text: str = self.extras['text']
        if text.startswith('0b'):
            type_ = 'Binary'
            translated = hex(int(text, base=2))
        elif not text.isdigit():
            type_ = 'ASCII'
            translated = '0x' + ' '.join([hex(ord(ch)) for ch in text]).replace('0x', '')
        else:
            type_ = 'Decimal'
            translated = hex(int(text))

        _button.style = ButtonStyle.green
        await self.disable_all()
        await interaction.response.send_message(f'Converted from {type_} to Hex: `{translated}`', ephemeral=True)

    @button(label="Decimal", custom_id='decbutton', style=ButtonStyle.grey)
    async def _dec(self, _button: Button, interaction: Interaction):
        text: str = self.extras['text']
        if text.startswith('0b') and not text.isalpha():
            type_ = 'Binary'
            text = text.replace('0b', '')
            translated = ' '.join([str(int('0b'+val, base=2)) for val in text.split()])

        _button.style = ButtonStyle.green
        await self.disable_all()
        await interaction.response.send_message(f'Converted from {type_} to Hex: `{translated}`', ephemeral=True)

    @button(label="Binary", custom_id='binbutton', style=ButtonStyle.grey)
    async def _bin(self, _button: Button, interaction: Interaction):
        text: str = self.extras['text']
        if text.startswith('0b') and not text.isalpha():
            await interaction.response.send_message(f"Um. Why convert binary to binary??", ephemeral=True)
            return
        elif not text.isdigit():
            type_ = 'ASCII'
            translated = '0b' + ' '.join([bin(ord(ch)) for ch in text]).replace('0b', '')
        elif text.startswith('0x'):
            type_ = 'Hex'
            text = text.replace('0x', '').replace(' ', '')
            translated = ''.join([bin(int('0x'+val, base=16)) for val in re.findall(r'.{2}', text)])
        else:
            type_ = 'Decimal'
            translated = bin(int(text))
        await interaction.response.send_message(f'Converted from {type_} to Binary : `{translated}`', ephemeral=True)



class ErrorView(BaseView):
    def args_check(self):
        if 'embed' not in self.extras.keys():
            raise MissingArgument("Argument 'error' is required.")

    @button(label="View Error", custom_id='errorbutton', style=ButtonStyle.danger)
    async def error(self, _button: Button, interaction: Interaction):
        self.extras['embed'].description = self.extras['embed'].description.replace("**Check Command Prompt**", "")
        await interaction.response.send_message("Contact <@613044385910620190>.", embed=self.extras['embed'], ephemeral=True)
