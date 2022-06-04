import discord

from typing import Optional
from discord.ext import commands



class ConfirmView(discord.ui.View):
    confirmed:bool
    def __init__(self, *, timeout: float = 180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label='Yes', style=discord.ButtonStyle.success)
    async def btn_yes_clbk(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        self.confirmed = True
        self.stop()
    

    @discord.ui.button(label='No', style=discord.ButtonStyle.danger)
    async def btn_no_clbk(self, interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        self.confirmed = False
        self.stop()