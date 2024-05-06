import discord

class BlackJackView(discord.ui.View):
    def __init__(self, player:discord.User, log, onHit, dDown, onSplt, onStand, onDeal, onLv, onAdd, onTout) -> None: 
        self.player = player
        self.log = log
        self.onHit = onHit
        self.dDown = dDown
        self.onSplt = onSplt
        self.onStand = onStand
        self.onDeal = onDeal
        self.onLv = onLv
        self.onAdd = onAdd
        self.onTout = onTout
        self.chips = [0, 0, 0, 0]
        super().__init__(timeout=90)
        self.endDeal()

    @discord.ui.button(label="HIT", style=discord.ButtonStyle.green, row=0, disabled=True)
    async def hitter(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            self.children[1].disabled = True
            self.children[2].disabled = True
            await self.onHit()

    @discord.ui.button(label="DOUBLE", style=discord.ButtonStyle.blurple, row=0, disabled=True)
    async def dblr(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            for i in range(4):
                self.chips[i] += self.chips[i]
                if self.chips[i]:
                    self.children[6+i].label = f"x{self.chips[i]}"
            await self.dDown()
            
    @discord.ui.button(label="SPLIT", style=discord.ButtonStyle.blurple, row=0, disabled=True)
    async def splttr(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            self.children[0].disabled = True
            self.children[1].disabled = True
            self.children[2].disabled = True
            self.children[3].disabled = True
            await self.onSplt()

    @discord.ui.button(label="STAND", style=discord.ButtonStyle.red, row=0, disabled=True)
    async def stndr(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            await self.onStand()

    @discord.ui.button(label="REMOVE BETS", style=discord.ButtonStyle.grey, row=2, disabled=True)
    async def removeAll(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            button.disabled = True
            self.chips = [0, 0, 0, 0]
            for i in range(4):
                self.children[7+i].label = None
            await self.onAdd(-2)

    @discord.ui.button(label="DEAL", style=discord.ButtonStyle.blurple, row=2, disabled=False)
    async def dlr(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            await self.onDeal()
    
    @discord.ui.button(label="LEAVE TABLE", style=discord.ButtonStyle.grey, row=2, disabled=False)
    async def lvr(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            await self.onLv()

    # @discord.ui.button(emoji="<:5p:1229496788436779028>", style=discord.ButtonStyle.grey, row=1, disabled=False)
    # async def add5G(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
    #     await interaction.response.defer()
    #     if(self.player.id == interaction.user.id):
    #         self.chips[0] += 1
    #         button.label = f"x{self.chips[0]}"
    #         await self.onAdd(5)
    
    @discord.ui.button(emoji="<:25p:1229496854031372369>", style=discord.ButtonStyle.grey, row=1, disabled=False)
    async def add25G(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            self.chips[0] += 1
            button.label = f"x{self.chips[0]}"
            self.children[4].disabled = False
            await self.onAdd(25)
    
    @discord.ui.button(emoji="<:50p:1229496904275198104>", style=discord.ButtonStyle.grey, row=1, disabled=False)
    async def add50G(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            self.chips[1] += 1
            button.label = f"x{self.chips[1]}"
            self.children[4].disabled = False
            await self.onAdd(50)

    @discord.ui.button(emoji="<:100p:1229496944985116673>", style=discord.ButtonStyle.grey, row=1, disabled=False)
    async def add100G(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            self.chips[2] += 1
            button.label = f"x{self.chips[2]}"
            self.children[4].disabled = False
            await self.onAdd(100)

    @discord.ui.button(emoji="<:500p:1229496985497636945>", style=discord.ButtonStyle.grey, row=1, disabled=False)
    async def add500G(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            self.chips[3] += 1
            button.label = f"x{self.chips[3]}"
            self.children[4].disabled = False
            await self.onAdd(500)

    @discord.ui.button(label="ALL IN?", style=discord.ButtonStyle.grey, row=1, disabled=False)
    async def addAll(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            button.disabled = True
            button.label = f"WE IN"
            self.children[4].disabled = False
            await self.onAdd(-1)

    def endDeal(self) -> None:
        self.children[0].disabled = True
        self.children[1].disabled = True
        self.children[2].disabled = True
        self.children[3].disabled = True
        self.children[4].disabled = True
        self.children[5].disabled = False
        self.children[6].disabled = False
        self.children[11].disabled = False
        self.children[11].label = "ALL IN?"
        self.chips = [0, 0, 0, 0]
        for i in range(4):
            self.children[7+i].label = None
        self.upChips()
        
    def upChips(self) -> None:
        for i in range(4):
            self.children[7+i].disabled = not self.log[i]

    def startDeal(self, canDouble, canSplit) -> None:
        self.children[0].disabled = False
        self.children[1].disabled = canDouble
        self.children[2].disabled = canSplit
        self.children[3].disabled = False
        self.children[4].disabled = True
        self.children[5].disabled = True
        self.children[6].disabled = True
        self.children[7].disabled = True
        self.children[8].disabled = True
        self.children[9].disabled = True
        self.children[10].disabled = True
        self.children[11].disabled = True

    def enableBase(self) -> None:
        self.children[0].disabled = False
        self.children[1].disabled = False
        self.children[3].disabled = False
    
    def chipLogUp(self, log) -> None:
        if log != self.log:
            self.log = log
            self.upChips()

    async def on_timeout(self) -> None:
        await self.onTout()