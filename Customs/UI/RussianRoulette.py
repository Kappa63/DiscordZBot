import discord

class RussianRoulette(discord.ui.View):
    def __init__(self, player:discord.Member, onSpin, onPull, onSplt, onCh, onJoin, onStrt, onTout, onCncl) -> None: 
        self.mainPlayer = player
        self.turnPlayer = player
        self.onSpin = onSpin
        self.onPull = onPull
        self.onSplt = onSplt
        self.onCh = onCh
        self.onJoin = onJoin
        self.onStrt = onStrt
        self.onTout = onTout
        self.onCncl = onCncl

        self.yesB = discord.ui.Button(label="AGREE SPLIT", style=discord.ButtonStyle.gray, row=0)
        self.noB = discord.ui.Button(label="REJECT SPLIT", style=discord.ButtonStyle.gray, row=0)
        self.yesB.callback = self.chSlctdOk
        self.noB.callback = self.chSlctdNot

        super().__init__(timeout=120)

    @discord.ui.button(label="SPIN", style=discord.ButtonStyle.green, row=1, disabled=True)
    async def spinner(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.turnPlayer.id == interaction.user.id):
            button.disabled = True
            await self.onSpin()

    @discord.ui.button(label="PULL", style=discord.ButtonStyle.danger, row=1, disabled=True)
    async def puller(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.turnPlayer.id == interaction.user.id):
            self.children[0].disabled = True
            button.disabled = True
            self.children[2] = True
            await self.onPull()

    @discord.ui.button(label="SPLIT", style=discord.ButtonStyle.gray, row=1, disabled=True)
    async def splitter(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.turnPlayer.id == interaction.user.id):
            self.children[0].disabled = True
            self.children[1].disabled = True
            button.disabled = True
            self.add_item(self.yesB)
            self.add_item(self.noB)
            await self.onSplt()

    @discord.ui.button(label="START", style=discord.ButtonStyle.blurple, row=2, disabled=False)
    async def startRR(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.mainPlayer.id == interaction.user.id):
            self.remove_item(self.children[3])
            self.remove_item(self.children[3])
            self.remove_item(self.children[3])
            # self.children[3].disabled = True
            # self.children[4].disabled = True
            # self.children[5].disabled = True
            await self.onStrt()

    @discord.ui.button(label="CANCEL", style=discord.ButtonStyle.blurple, row=2, disabled=False)
    async def cancelRR(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.mainPlayer.id == interaction.user.id):
            await self.onCncl(True)
    
    @discord.ui.button(label="JOIN TABLE", style=discord.ButtonStyle.gray, row=3, disabled=False)
    async def joinRR(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        await self.onJoin(interaction)

    async def chSlctdOk(self, interaction: discord.Interaction) -> None:
        await self.onCh(interaction.user, True)

    async def chSlctdNot(self, interaction: discord.Interaction) -> None:
        await self.onCh(interaction.user, False)

    def fullTable(self) -> None:
        self.children[5].disabled = True

    def onFail(self) -> None:
        self.remove_item(self.children[3])
        self.remove_item(self.children[3])


    def loaded(self) -> None:
        self.children[0].disabled = False
        self.children[1].disabled = False
        self.children[2].disabled = False
    
    def unloaded(self) -> None:
        self.children[0].disabled = True
        self.children[1].disabled = True
        self.children[2].disabled = True

    def nextPlyr(self, usr:discord.Member) -> None:
        self.turnPlayer = usr

    async def on_timeout(self) -> None:
        await self.onTout()