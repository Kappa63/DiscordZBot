import discord
import numpy as np
from PIL import Image
import io

class BlackJackView(discord.ui.View):
    def __init__(self, player:discord.User, onHit, onStand, onTout) -> None: 
        self.player = player
        self.onHit = onHit
        self.onStand = onStand
        self.onTout = onTout
        super().__init__(timeout=30)

    @discord.ui.button(label="HIT", style=discord.ButtonStyle.green, row=1)
    async def Sq1(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            await self.onHit()

    @discord.ui.button(label="STAND", style=discord.ButtonStyle.red, row=1)
    async def Sq7(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            await self.onStand()

    async def on_timeout(self) -> None:
        await self.onTout()