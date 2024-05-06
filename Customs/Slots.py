from numpy import random
import math
import discord
from Setup import Gmb
import asyncio
from typing import List
from Customs.UI.Slots import SlotsView

class Slots:
    def __init__(self, ctx:discord.Interaction, bal:int, acm:List[int]) -> None:
        self.SYMBOLS = ["🍒", "🍉", "🍋", "🍫", "🔔", "7️⃣"]
        self.REEL_WEIGHTS = [[5, 6, 4, 3, 1, 1], [5, 5, 5, 2, 2, 1], [6, 4, 5, 3, 1, 1]]
        self.HOUSE_EDGE = 0.9
        self.NUMBER_OF_REELS = 3
        self.WINDOW_SIZE = 3
        self.PAYLINE_POS = 1
        self.EMBED_COLOR = 0xA8140C

        self.ctx = ctx
        self.bal = bal
        self.acm = acm
        
        self.jp = 0
        self.wins = 0
        self.spins = 0

        self.bet = 0
        self.payline = []
        self.prft = 0

        self.window = [["⬛"]*self.WINDOW_SIZE for _ in range(self.NUMBER_OF_REELS)]

        self.slotReels = [[v for k, v in enumerate(self.SYMBOLS) for _ in range(self.REEL_WEIGHTS[i][k])] for i in range(self.NUMBER_OF_REELS)]
        for i in range(self.NUMBER_OF_REELS):
            random.shuffle(self.slotReels[i])

        self.mEm = discord.Embed(title=f"Remaining: ${self.bal:,}", description=self.createWinEm(), color=self.EMBED_COLOR)

        self.mView = SlotsView(self.ctx.user, self.allowedChips(), self.onStart, self.addBet, self.onLv)

    def calcMultiplier(self, a, b=0, c=0): 
        return (self.HOUSE_EDGE*math.comb(20, 1)/math.comb(a, 1))*((self.HOUSE_EDGE*math.comb(20, 1)/math.comb(b, 1)) if b else 1)*((self.HOUSE_EDGE*math.comb(20,1)/math.comb(c,1)) if c else 1)

    def allowedChips(self):
        if self.bal >= 500:
            return [True, True, True, True]
        elif self.bal >= 100:
            return [True, True, True, False]
        elif self.bal >= 50:
            return [True, True, False, False]
        elif self.bal >= 25:
            return [True, False, False, False]
        else:
            return [False, False, False, False]
        
    def getWeight(self, reel, sym):
        return self.REEL_WEIGHTS[reel][self.SYMBOLS.index(sym)]
        
    def spinReels(self):
        p = []
        for _ in range(self.NUMBER_OF_REELS):
            a = random.randint(0, 20)
            p.append((a-1, a, a+1 if a<19 else 0))
        return p
    
    def createWinEm(self):
        t = []
        for i in range(self.WINDOW_SIZE):
            l = ""
            if i == self.PAYLINE_POS:
                l += "<:plr:1236819693424214048>"
            else:
                l += "<:trnp:1236820040964374538>"
            for j in range(self.NUMBER_OF_REELS):
                l += self.window[j][i]
            if i == self.PAYLINE_POS:
                l += "<:pll:1236819660922421348>"
            t.append(l)
        return "\n".join(t)
        
    async def addBet(self, amnt) -> None:
        if amnt == -1:
            amnt = self.bal
        if amnt == -2:
            self.bal += self.bet
            self.bet = 0
        else:
            self.bal-=amnt
            self.bet+=amnt

        self.mView.chipLogUp(self.allowedChips())
        self.mEm.title = f"Remaining: ${self.bal:,}"
        await self.sltsTbl.edit(embed=self.mEm, view=self.mView)

    async def endRnd(self, mlt) -> None:
        self.spins += 1
        if mlt:
            self.wins += 1
            if self.payline[0] == "7️⃣":
                self.jp += 1
        toPrft = round(self.bet*mlt, 2)
        self.bal += toPrft
        self.prft += toPrft-self.bet
        self.mEm.title = f"Remaining: ${self.bal:,}"

        await self.sltsTbl.edit(embed=self.mEm)
        await self.clsRnd() 

    async def rdyNRnd(self) -> None:
        self.mView.endSpin()
        await self.sltsTbl.edit(view=self.mView)

    async def clsRnd(self) -> None:
        self.mView.chipLogUp(self.allowedChips())
        self.bet = 0
        self.payline = []
        await self.rdyNRnd()

    async def onStart(self) -> None:
        self.mView.startSpin()
        self.window = [["<a:ss2:1236754989532057714>"]*self.WINDOW_SIZE for _ in range(self.NUMBER_OF_REELS)]
        self.mEm.title = "Current Multiplier: 0.0x"
        self.mEm.description = self.createWinEm()
        await self.sltsTbl.edit(embed=self.mEm, view=self.mView)
        reelPos = self.spinReels()
        for i in range(self.NUMBER_OF_REELS):
            await asyncio.sleep(0.8)
            curReelPos = reelPos[i]
            for j in range(self.WINDOW_SIZE):
                self.window[i][j] = self.slotReels[i][curReelPos[j]]
                if j == self.PAYLINE_POS:
                    self.payline.append(self.window[i][j])
            mult = self.calcMultiplier(*(self.getWeight(k, self.payline[0]) for k in range(i+1))) if len(set(self.payline)) == 1 else 0
            self.mEm.title = f"Current Multiplier: {mult}x"
            self.mEm.description = self.createWinEm()
            await self.sltsTbl.edit(embed=self.mEm, view=self.mView)

        await self.endRnd(mult)

    async def autoRun(self) -> None:
        self.sltsTbl = await self.ctx.followup.send(embed=self.mEm, view=self.mView)

    async def onLv(self) -> None:
        try:
            self.mView.stop()
            await self.sltsTbl.edit(embed=discord.Embed(title="Table Closed.", description=f"Chip Balance: ${(self.bal+self.bet):,}\n\nProfits: ${self.prft:,}", color=self.EMBED_COLOR), view=None)
        except:
            pass
            
        Gmb.update_one({"_id":self.ctx.user.id}, {"$set": {"playing":False}, "$inc":{"bal":self.bal+self.bet, "sProfits":self.prft, "sWins":self.wins, "sJackpot":self.jp, "sPlayed":self.spins}})
        