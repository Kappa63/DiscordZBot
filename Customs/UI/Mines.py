import discord
from typing import List

class MinesView(discord.ui.View):
    def __init__(self, player:discord.User, onClck) -> None:
        self.player = player
        self.onClck = onClck
        super().__init__(timeout=180)
        for i in range(25):
            a = discord.ui.Button(label="\u200b", custom_id=str(i), disabled=True)
            a.callback = self.checkClck
            self.add_item(a)

    async def checkClck(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            await self.onClck(int(interaction.data["custom_id"]))

    def setBtn(self, idx:int, bomb:bool) -> None:
        if bomb:
            self.children[idx].style = discord.ButtonStyle.red
            self.children[idx].label = "💣"
        else:
            self.children[idx].style = discord.ButtonStyle.green
            self.children[idx].label = "💎"
            self.children[idx].disabled = True

    def offAll(self, grid:List[bool]) -> None:
        for i, v in enumerate(grid):
            self.children[i].disabled = True
            if v:
                self.children[i].label = "💣"
            else:   
                self.children[i].label = "💎"
    
    def rdyStart(self) -> None:
        for i in self.children:
            i.label = "\u200b"
            i.style = discord.ButtonStyle.gray
            i.disabled = False

class MinesControls(discord.ui.View):
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

    @discord.ui.select(placeholder="💣 1", options=[discord.SelectOption(label=i, emoji="💣") for i in range(1, 25)], max_values=1, row=0, disabled=False)
    async def bmbAddr(self, interaction: discord.Interaction, selector: discord.ui.Select) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            selector.placeholder = f'💣 {selector.values[0]}'
            await self.onSelBomb(int(selector.values[0]))

    @discord.ui.button(label="START", style=discord.ButtonStyle.blurple, row=2, disabled=False)
    async def hitter(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            await self.onStrt()

    @discord.ui.button(label="CASHOUT", style=discord.ButtonStyle.green, row=2, disabled=True)
    async def dlr(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            await self.onCOut()
    
    @discord.ui.button(label="REMOVE BETS", style=discord.ButtonStyle.grey, row=2, disabled=True)
    async def removeAll(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            button.disabled = True
            self.chips = [0, 0, 0, 0]
            for i in range(4):
                self.children[5+i].label = None
            await self.onAdd(-2)
    
    @discord.ui.button(label="LEAVE MINES", style=discord.ButtonStyle.grey, row=2, disabled=False)
    async def lvr(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            await self.onLeave()

    @discord.ui.button(emoji="<:25p:1229496854031372369>", style=discord.ButtonStyle.grey, row=1, disabled=False)
    async def add25G(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            self.chips[1] += 1
            button.label = f"x{self.chips[0]}"
            self.children[3].disabled = False
            await self.onAdd(25)
    
    @discord.ui.button(emoji="<:50p:1229496904275198104>", style=discord.ButtonStyle.grey, row=1, disabled=False)
    async def add50G(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            self.chips[2] += 1
            button.label = f"x{self.chips[1]}"
            self.children[3].disabled = False
            await self.onAdd(50)

    @discord.ui.button(emoji="<:100p:1229496944985116673>", style=discord.ButtonStyle.grey, row=1, disabled=False)
    async def add100G(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            self.chips[3] += 1
            button.label = f"x{self.chips[2]}"
            self.children[3].disabled = False
            await self.onAdd(100)

    @discord.ui.button(emoji="<:500p:1229496985497636945>", style=discord.ButtonStyle.grey, row=1, disabled=False)
    async def add500G(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if(self.player.id == interaction.user.id):
            self.chips[4] += 1
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