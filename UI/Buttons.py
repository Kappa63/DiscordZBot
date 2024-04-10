import discord
from discord.ext import commands 


class EditButton(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Button",style=discord.ButtonStyle.gray)
    async def gray_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.edit_message(content=f"This is an edited button response!")
