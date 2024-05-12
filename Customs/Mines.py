from numpy import random
import math
import discord
from Setup import Gmb
from typing import List
from Customs.UI.Mines import MinesView, MinesControls
from Customs.AchievementHelper import MAchievements

class Mines:
    def __init__(self, ctx:discord.Interaction, bal:int, acm:List[int]) -> None:
        self.HOUSE_EDGE = 0.985
        self.EMBED_COLOR = 0x5f86cd

        self.ctx = ctx
        self.nMines = 1
        self.bal = bal
        self.acm = acm
        self.acmHelper = MAchievements([i[0] for i in acm])
        
        self.collected = 0
        self.tCollected = 0
        self.bHits = 0
        self.rnds = 0

        self.bombHit = False
        self.bet = 0
        self.prft = 0
        self.grid = []

        self.mView = MinesView(self.ctx.user, self.onClick)
        self.mControls = MinesControls(self.ctx.user, self.allowedChips(), self.changeBomb, self.addBet, self.onStart, self.endRnd, self.closeMines)

    def calcMultiplier(self, d): 
        return round(self.HOUSE_EDGE*math.comb(25,d)/math.comb(25-self.nMines, d), 2)

    async def changeBomb(self, nBmb:int) -> None:
        self.nMines = nBmb
        await self.MinesTbl.edit(view=self.mView)

    def allowedChips(self):
        if self.bal >= 500:
            return [True, True, True, True]
        elif self.bal >= 100:
            return [True, True, True, False]
        elif self.bal >= 50:
            return [True, True, False, False]
        elif self.bal >= 25:
            return [True, False, False, False] 
        # elif self.bal >=5:
            # return [True, False, False, False, False] 
        else:
            return [False, False, False, False]

    async def onClick(self, pos:int) -> None:
        if not self.grid[pos]: 
            self.collected+=1
            self.mView.setBtn(pos, False)
            mlt = self.calcMultiplier(self.collected)
            await self.MinesMain.edit(embed=discord.Embed(title=f"Round Bet: ${self.bet}", description=f"Current Multiplier: {mlt}x\nProfit: ${(round(self.bet*mlt, 2)-self.bet):,}", color=self.EMBED_COLOR))
            if self.collected == 25-self.nMines:
                self.acmHelper.boardFinished()
                await self.endRnd()
        else:
            self.bombHit = True
            self.mView.setBtn(pos, True)
            await self.endRnd()
        await self.MinesTbl.edit(view=self.mView)
    
    async def addBet(self, amnt) -> None:
        if amnt == -1:
            amnt = self.bal
        if amnt == -2:
            self.bal += self.bet
            self.bet = 0
        else:
            self.bal-=amnt
            self.bet+=amnt

        self.mControls.chipLogUp(self.allowedChips())
        await self.MinesMain.edit(embed=discord.Embed(title=f"Remaining: ${self.bal:,}", color=self.EMBED_COLOR), view=self.mControls)

    async def endRnd(self) -> None:
        if self.bombHit:
            self.prft -= self.bet
            t = "MINE HIT"
        else:
            toPrft = round(self.bet*self.calcMultiplier(self.collected), 2)
            self.bal += toPrft
            self.prft += toPrft-self.bet
            t = "ROUND END"

        await self.MinesMain.edit(embed=discord.Embed(title=t, description=f"Current Balance: ${self.bal:,}", color=self.EMBED_COLOR))
        await self.clsRnd() 

    async def rdyNRnd(self) -> None:
        self.mControls.endRnd()
        self.mView.offAll(self.grid)
        await self.MinesMain.edit(view=self.mControls)
        await self.MinesTbl.edit(view=self.mView)

    async def clsRnd(self) -> None:
        self.mControls.chipLogUp(self.allowedChips())
        self.tCollected += self.collected
        self.rnds += 1
        self.bHits += self.bombHit
        self.bet = 0
        self.bombHit = False
        self.collected = 0
        await self.rdyNRnd()

    async def onStart(self) -> None:
        self.grid = [False, False, False, False, False,
                     False, False, False, False, False,
                     False, False, False, False, False,
                     False, False, False, False, False,
                     False, False, False, False, False]
        
        for i in random.choice(range(25), self.nMines, replace=False):
            self.grid[i] = True

        self.mView.rdyStart()
        self.mControls.startRnd()
        await self.MinesTbl.edit(view=self.mView)
        await self.MinesMain.edit(embed=discord.Embed(title=f"Round Bet: ${self.bet}", description=f"Current Multiplier: 0.97x\nProfit: ${(round(self.bet*0.97, 2)-self.bet):,}", color=self.EMBED_COLOR), view=self.mControls)

    async def autoRun(self) -> None:
        self.MinesMain = await self.ctx.followup.send(embed=discord.Embed(title=f"Remaining: ${self.bal:,}", color=self.EMBED_COLOR), view=self.mControls)
        self.MinesTbl = await self.ctx.channel.send(view=self.mView)

    async def closeMines(self) -> None:
        try:
            self.mView.stop()
            self.mControls.stop()
            await self.MinesMain.edit(embeds=[discord.Embed(title="Table Closed.", description=f"Chip Balance: ${(self.bal+self.bet):,}\n\nProfits: ${self.prft:,}", color=self.EMBED_COLOR)], view=None)
            await self.MinesTbl.delete()
        except:
            pass
            
        Gmb.update_one({"_id":self.ctx.user.id}, {"$set": {"playing":False}, "$inc":{"bal":self.bal+self.bet, "mProfits":self.prft, "mCollected":self.tCollected, "mExploded":self.bHits, "mPlayed":self.rnds}})
        self.acmHelper.inOutProfit(self.prft, self.rnds)
        nAcm = self.acmHelper.getAchieved()[len(self.acm):]
        if nAcm:
            Gmb.update_one({"_id":self.ctx.user.id}, {"$push": {"achieved":{"$each":[[i,False] for i in nAcm]}}})
