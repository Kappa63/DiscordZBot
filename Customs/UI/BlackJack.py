import discord
import numpy as np
from PIL import Image

class BlackJackView(discord.ui.View):
    def __init__(self, player:discord.User, onHit, onStand, onDeal, onLv, onTout) -> None: 
        self.player = player
        self.onHit = onHit
        self.onStand = onStand
        self.onDeal = onDeal
        self.onLv = onLv
        self.onTout = onTout
        super().__init__(timeout=30)

    @discord.ui.button(label="HIT", style=discord.ButtonStyle.green, row=1)
    async def hitter(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            await self.onHit()

    @discord.ui.button(label="STAND", style=discord.ButtonStyle.red, row=1)
    async def stndr(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            await self.onStand()

    @discord.ui.button(label="DEAL", style=discord.ButtonStyle.blurple, row=1, disabled=True)
    async def dlr(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            await self.onDeal()
    
    @discord.ui.button(label="LEAVE TABLE", style=discord.ButtonStyle.grey, row=1, disabled=True)
    async def lvr(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            await self.onLv()

    def endDeal(self) -> None:
        self.children[0].disabled = True
        self.children[1].disabled = True
        self.children[2].disabled = False
        self.children[3].disabled = False

    def startDeal(self) -> None:
        self.children[0].disabled = False
        self.children[1].disabled = False
        self.children[2].disabled = True
        self.children[3].disabled = True

    async def on_timeout(self) -> None:
        await self.onTout()