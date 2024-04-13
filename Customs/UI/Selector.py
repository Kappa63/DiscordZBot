import discord
from typing import List, Optional

class SelectionView(discord.ui.View):
    def __init__(self, selectFunc, exitFunc, labels:List[str], emojis:Optional[List[discord.Emoji]]) -> None:
        self.selectFunc = selectFunc
        self.exitFunc = exitFunc
        self.SELECTIONS = [discord.SelectOption(label=i, emoji=j) for i, j in zip(labels, emojis)] if emojis else [discord.SelectOption(label=i) for i in labels]

        self.selector = discord.ui.Select(placeholder="Select Number", options=self.SELECTIONS, max_values=1, row=1)
        self.selector.callback = self.selectorCall
        super().__init__(timeout=30)
        self.add_item(self.selector)
    
    # @discord.ui.select(placeholder="Select Number", options=self.SELECTIONS, max_values=1)
    async def selectorCall(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        await self.selectFunc(self.selector.values[0])

    @discord.ui.button(label="x", style=discord.ButtonStyle.danger, row=2)
    async def ExitSelector(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        await self.exitFunc()

    async def on_timeout(self) -> None:
        await self.exitFunc()