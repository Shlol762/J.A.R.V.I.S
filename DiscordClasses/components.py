from .errors import *
from discord.ui import Select
from discord import SelectOption, TextChannel, VoiceChannel,\
    Interaction, CategoryChannel, Embed, Colour
from typing import Union
import re


class CategorySelect(Select):
    def __init__(self, channel: Union[TextChannel, VoiceChannel]):
        super().__init__(custom_id='selectcategory', placeholder="Select Category(Optional)",
                         options=[SelectOption(label='None', description='Pick this if you dont '
                                                     'want the channel to be in any category.')])
        self.channel = channel

    async def callback(self, interaction: Interaction):
        chnl = self.channel
        if self.values[0] != 'None':
            ctgry: CategoryChannel = await chnl.guild.fetch_channel(int(self.values[0]))
            await chnl.edit(category=ctgry)
        c_type = re.search(r"'.+'", str(type(chnl))).group().replace("'", '').split('.')[-1]
        embed = Embed(title=f"Created a new {c_type}", colour=Colour.random(),
                      description=f"{chnl.mention}").add_field(name='Name: ',
                                                               value=f"`{chnl.name}`").add_field(
            name='ID: ', value=f"`{chnl.id}`").add_field(name='Category: ',
                                                         value=f"`{ctgry.name if self.values[0] != 'None' else 'None'}`")
        await interaction.response.send_message(embed=embed,
                                                    ephemeral=True)
        self.disabled = True
        await self.view.message.edit(view=self.view)
