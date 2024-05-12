import discord
from typing import List

class RouletteView(discord.ui.View):
    def __init__(self, srange, batch, reds, player:discord.User, onClck) -> None:
        self.reds = reds
        self.player = player
        self.onClck = onClck
        super().__init__(timeout=180)
        r = 0 if batch else 1
        for i in range(srange, srange+12):
            a = discord.ui.Button(label=i, custom_id=str(i), row=r, disabled=False,
                                  style=discord.ButtonStyle.red if i in reds else discord.ButtonStyle.gray)
            a.callback = self.checkClck
            self.add_item(a)
            if i%3 == 0:
                r += 1

        match batch:
            case 0:
                self.add_item(discord.ui.Button(label="\u200b", custom_id="Nan0", row=0, disabled=True, style=discord.ButtonStyle.green))
                self.add_item(discord.ui.Button(label="0", custom_id="0", row=0, disabled=False, style=discord.ButtonStyle.green))
                self.add_item(discord.ui.Button(label="\u200b", custom_id="Nan1", row=0, disabled=True, style=discord.ButtonStyle.green))
                self.add_item(discord.ui.Button(label="‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ 1 ‎ ‎ ‎ to ‎ ‎ ‎ 12 ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎", custom_id="1to12", row=2, disabled=False, style=discord.ButtonStyle.blurple))
                self.add_item(discord.ui.Button(label="1 to 18", custom_id="1to18", row=3, disabled=False, style=discord.ButtonStyle.blurple))
                self.add_item(discord.ui.Button(label="‎ Even ‎", custom_id="even", row=3, disabled=False, style=discord.ButtonStyle.blurple))
            case 1:
                self.add_item(discord.ui.Button(label="‎ ‎ ‎ ‎ ‎ ‎ 13 ‎ ‎ ‎ to ‎ ‎ ‎ 24 ‎ ‎ ‎ ‎ ‎ ‎", custom_id="13to24", row=1, disabled=False, style=discord.ButtonStyle.blurple))
                self.add_item(discord.ui.Button(label="red", custom_id="red", row=2, disabled=False, style=discord.ButtonStyle.red))
                self.add_item(discord.ui.Button(label="black", custom_id="black", row=2, disabled=False, style=discord.ButtonStyle.gray))
            case 2:
                self.add_item(discord.ui.Button(label="2:1", custom_id="col121", row=4, disabled=False, style=discord.ButtonStyle.blurple))
                self.add_item(discord.ui.Button(label="2:1", custom_id="col221", row=4, disabled=False, style=discord.ButtonStyle.blurple))
                self.add_item(discord.ui.Button(label="2:1", custom_id="col321", row=4, disabled=False, style=discord.ButtonStyle.blurple))
                self.add_item(discord.ui.Button(label="‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ 25 ‎ ‎ ‎ to ‎ ‎ ‎ 36 ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎", custom_id="25to36", row=1, disabled=False, style=discord.ButtonStyle.blurple))
                self.add_item(discord.ui.Button(label="Odd", custom_id="odd", row=2, disabled=False, style=discord.ButtonStyle.blurple))
                self.add_item(discord.ui.Button(label="19 to 36", custom_id="19to36", row=2, disabled=False, style=discord.ButtonStyle.blurple))

    async def checkClck(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            await self.onClck(int(interaction.data["custom_id"]))

class RouletteInnerView(discord.ui.View):
    def __init__(self, player:discord.User, onClck) -> None:
        self.player = player
        self.onClck = onClck
        super().__init__(timeout=180)

    @discord.ui.button(label="2:1", style=discord.ButtonStyle.blurple, row=0, disabled=False)
    async def col121(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            pass
    
    @discord.ui.button(label="2:1", style=discord.ButtonStyle.blurple, row=0, disabled=False)
    async def col221(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            pass

    @discord.ui.button(label="2:1", style=discord.ButtonStyle.blurple, row=0, disabled=False)
    async def col321(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            pass
    
    @discord.ui.button(label="LEAVE ROULETTE", style=discord.ButtonStyle.grey, row=2, disabled=False)
    async def lvr(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            await self.onLeave()

    @discord.ui.button(emoji="<:25p:1229496854031372369>", style=discord.ButtonStyle.grey, row=1, disabled=False)
    async def add25G(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            self.chips[0] += 1
            button.label = f"x{self.chips[0]}"
            self.children[3].disabled = False
            await self.onAdd(25)
    
    @discord.ui.button(emoji="<:50p:1229496904275198104>", style=discord.ButtonStyle.grey, row=1, disabled=False)
    async def add50G(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            self.chips[1] += 1
            button.label = f"x{self.chips[1]}"
            self.children[3].disabled = False
            await self.onAdd(50)

    @discord.ui.button(emoji="<:100p:1229496944985116673>", style=discord.ButtonStyle.grey, row=1, disabled=False)
    async def add100G(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            self.chips[2] += 1
            button.label = f"x{self.chips[2]}"
            self.children[3].disabled = False
            await self.onAdd(100)

    @discord.ui.button(emoji="<:500p:1229496985497636945>", style=discord.ButtonStyle.grey, row=1, disabled=False)
    async def add500G(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            self.chips[3] += 1
            button.label = f"x{self.chips[3]}"
            self.children[3].disabled = False
            await self.onAdd(500)

    @discord.ui.button(label="ALL IN?", style=discord.ButtonStyle.grey, row=1, disabled=False)
    async def addAll(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            button.disabled = True
            button.label = f"WE IN"
            self.children[3].disabled = False
            await self.onAdd(-1)      

    async def checkClck(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            await self.onClck(int(interaction.data["custom_id"]))

class RouletteControls(discord.ui.View):
    def __init__(self,  player:discord.User, log, onSelBomb, onAdd, onStrt, onCOut, onLeave) -> None:
        self.player = player
        self.log = log
        self.onSelBomb = onSelBomb
        self.onAdd = onAdd
        self.onStrt = onStrt
        self.onCOut = onCOut
        self.onLeave = onLeave
        self.chips = [0, 0, 0, 0]
        super().__init__(timeout=180)
        self.endRnd()

    @discord.ui.button(label="START", style=discord.ButtonStyle.blurple, row=2, disabled=False)
    async def hitter(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            await self.onStrt()
    
    @discord.ui.button(label="REMOVE BETS", style=discord.ButtonStyle.grey, row=2, disabled=True)
    async def removeAll(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            button.disabled = True
            self.chips = [0, 0, 0, 0]
            for i in range(4):
                self.children[5+i].label = None
            await self.onAdd(-2)
    
    @discord.ui.button(label="LEAVE ROULETTE", style=discord.ButtonStyle.grey, row=2, disabled=False)
    async def lvr(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            await self.onLeave()

    @discord.ui.button(emoji="<:25p:1229496854031372369>", style=discord.ButtonStyle.grey, row=1, disabled=False)
    async def add25G(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            self.chips[0] += 1
            button.label = f"x{self.chips[0]}"
            self.children[3].disabled = False
            await self.onAdd(25)
    
    @discord.ui.button(emoji="<:50p:1229496904275198104>", style=discord.ButtonStyle.grey, row=1, disabled=False)
    async def add50G(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            self.chips[1] += 1
            button.label = f"x{self.chips[1]}"
            self.children[3].disabled = False
            await self.onAdd(50)

    @discord.ui.button(emoji="<:100p:1229496944985116673>", style=discord.ButtonStyle.grey, row=1, disabled=False)
    async def add100G(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            self.chips[2] += 1
            button.label = f"x{self.chips[2]}"
            self.children[3].disabled = False
            await self.onAdd(100)

    @discord.ui.button(emoji="<:500p:1229496985497636945>", style=discord.ButtonStyle.grey, row=1, disabled=False)
    async def add500G(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            self.chips[3] += 1
            button.label = f"x{self.chips[3]}"
            self.children[3].disabled = False
            await self.onAdd(500)

    @discord.ui.button(label="ALL IN?", style=discord.ButtonStyle.grey, row=1, disabled=False)
    async def addAll(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            button.disabled = True
            button.label = f"WE IN"
            self.children[3].disabled = False
            await self.onAdd(-1)

    def endRnd(self) -> None:
        self.children[0].disabled = False
        self.children[1].disabled = False
        self.children[2].disabled = True
        self.children[3].disabled = True
        self.children[4].disabled = False
        self.children[8].disabled = False
        self.children[8].label = "ALL IN?"
        self.chips = [0, 0, 0, 0]
        for i in range(4):
            self.children[5+i].label = None
        self.upChips()
        
    def upChips(self) -> None:
        for i in range(4):
            self.children[5+i].disabled = not self.log[i]

    def startRnd(self) -> None:
        self.children[0].disabled = True
        self.children[1].disabled = True
        self.children[2].disabled = False
        self.children[3].disabled = True
        self.children[4].disabled = True
        self.children[5].disabled = True
        self.children[6].disabled = True
        self.children[7].disabled = True
        self.children[8].disabled = True
        self.children[9].disabled = True
        
    def chipLogUp(self, log) -> None:
        if log != self.log:
            self.log = log
            self.upChips()

    async def on_timeout(self) -> None:
        await self.onLeave()