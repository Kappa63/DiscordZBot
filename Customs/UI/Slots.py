import discord

class SlotsView(discord.ui.View):
    def __init__(self, player:discord.User, log, onStart, onAdd, onLv) -> None: 
        self.player = player
        self.log = log
        self.onStart = onStart
        self.onAdd = onAdd
        self.onLv = onLv
        self.chips = [0, 0, 0, 0]
        super().__init__(timeout=90)
        self.endSpin()

    @discord.ui.button(label="SPIN", style=discord.ButtonStyle.green, row=0, disabled=False)
    async def hitter(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            await self.onStart()
        
    @discord.ui.button(label="REMOVE BETS", style=discord.ButtonStyle.grey, row=2, disabled=True)
    async def removeAll(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            button.disabled = True
            self.chips = [0, 0, 0, 0]
            for i in range(4):
                self.children[3+i].label = None
            await self.onAdd(-2)

    @discord.ui.button(label="LEAVE TABLE", style=discord.ButtonStyle.grey, row=2, disabled=False)
    async def lvr(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            await self.onLv()

    @discord.ui.button(emoji="<:25p:1229496854031372369>", style=discord.ButtonStyle.grey, row=1, disabled=False)
    async def add25G(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            self.chips[0] += 1
            button.label = f"x{self.chips[0]}"
            self.children[1].disabled = False
            await self.onAdd(25)
    
    @discord.ui.button(emoji="<:50p:1229496904275198104>", style=discord.ButtonStyle.grey, row=1, disabled=False)
    async def add50G(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            self.chips[1] += 1
            button.label = f"x{self.chips[1]}"
            self.children[1].disabled = False
            await self.onAdd(50)

    @discord.ui.button(emoji="<:100p:1229496944985116673>", style=discord.ButtonStyle.grey, row=1, disabled=False)
    async def add100G(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            self.chips[2] += 1
            button.label = f"x{self.chips[2]}"
            self.children[1].disabled = False
            await self.onAdd(100)

    @discord.ui.button(emoji="<:500p:1229496985497636945>", style=discord.ButtonStyle.grey, row=1, disabled=False)
    async def add500G(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            self.chips[3] += 1
            button.label = f"x{self.chips[3]}"
            self.children[1].disabled = False
            await self.onAdd(500)

    @discord.ui.button(label="ALL IN?", style=discord.ButtonStyle.grey, row=1, disabled=False)
    async def addAll(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            button.disabled = True
            button.label = f"WE IN"
            self.children[1].disabled = False
            await self.onAdd(-1)

    def endSpin(self) -> None:
        self.children[0].disabled = False
        self.children[1].disabled = True
        self.children[2].disabled = False
        self.children[7].disabled = False
        self.children[7].label = "ALL IN?"
        self.chips = [0, 0, 0, 0]
        for i in range(4):
            self.children[3+i].label = None
        self.upChips()
        
    def upChips(self) -> None:
        for i in range(4):
            self.children[3+i].disabled = not self.log[i]

    def startSpin(self) -> None:
        self.children[0].disabled = True
        self.children[1].disabled = True
        self.children[2].disabled = True
        self.children[3].disabled = True
        self.children[4].disabled = True
        self.children[5].disabled = True
        self.children[6].disabled = True
        self.children[7].disabled = True

    def chipLogUp(self, log) -> None:
        if log != self.log:
            self.log = log
            self.upChips()

    async def on_timeout(self) -> None:
        await self.onLv()