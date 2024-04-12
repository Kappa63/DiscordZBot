import discord

class NavigationView(discord.ui.View):
    def __init__(self, prevFunc, nextFunc, exitFunc, numFunc) -> None:
        self.prevFunc = prevFunc
        self.nextFunc = nextFunc
        self.exitFunc = exitFunc
        self.numFunc = numFunc   
        super().__init__(timeout=30)

    @discord.ui.button(label="<<", style=discord.ButtonStyle.primary)
    async def FarPrevPage(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        await self.prevFunc(10)

    @discord.ui.button(label="<", style=discord.ButtonStyle.primary)
    async def PrevPage(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        await self.prevFunc(1)

    @discord.ui.button(label="x", style=discord.ButtonStyle.danger)
    async def ExitNav(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        await self.exitFunc()


    @discord.ui.button(label=">", style=discord.ButtonStyle.primary)
    async def NextPage(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        await self.nextFunc(1)

    @discord.ui.button(label=">>", style=discord.ButtonStyle.primary)
    async def FarNextPage(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        await self.nextFunc(10)

    # @discord.ui.button(label="#", style=discord.ButtonStyle.secondary, custom_id="num")
    # async def Selector(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
    #     await interaction.response.defer()
    #     await self.numFunc()

    async def on_timeout(self) -> None:
        await self.exitFunc()


    
