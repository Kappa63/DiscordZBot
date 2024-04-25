from numpy import random
import asyncio
import discord
from Setup import Gmb
from pymongo.collection import ReturnDocument 
from typing import List
from Customs.UI.RussianRoulette import RussianRoulette as RRView

class RR:
    def __init__(self, ctx:discord.Interaction, bet:int, acm:List[int]) -> None:
        self.ctx = ctx
        self.bet = bet
        self.acm = acm
        self.idAcm = [i[0] for i in acm]
        self.nAcm = []
        self.mView = RRView(ctx.user, self.onSpin, self.onPull, self.onSplit, self.chSplit, self.onPlayer, self.start, self.onTim, self.cancelGame)
        self.players = [[ctx.user, 1]]
        self.agreeSplit = 0
        self.voteSplit = 0
        self.nPlayers = 1
        self.dead = 0
        self.curP = 0
        self.onBullet = 0
        self.rnd = 1
        self.reloadURLs = ["https://media1.tenor.com/m/1l2ahrbFZ_sAAAAC/loading-gun.gif", "https://media1.tenor.com/m/p38XIgRTGMkAAAAd/gun.gif", "https://media1.tenor.com/m/5KBeg8bTVxgAAAAC/gold-rule.gif"]
        self.shotURLs = ["https://media1.tenor.com/m/PDXJWOZHIPIAAAAC/kim-pine-shoot.gif", "https://media1.tenor.com/m/7XCpJLcagyQAAAAC/joker-finger-gun.gif", "https://media1.tenor.com/m/bEkEbaP_67AAAAAC/shoot-me-kill.gif"]
        self.survivedURLs = ["https://media1.tenor.com/m/A_HXcBh96J0AAAAC/denzel-washington-gun.gif"]
        self.cylinder = [True, False, False, False, False, False]
        self.pEm = discord.Embed(title=f"Waiting For Players... (${self.bet:,} Entry)", description=f"1/6 (${self.bet:,} in Pot)", color=0xe44c22)
        self.pEm.add_field(name=ctx.user.display_name, value="\u200b", inline=False)
        self.sEm = discord.Embed(title="Loading Bullet...", description="Only one walks out alive\nReady to Die?", color=0xe44c22)
        self.sEm.set_thumbnail(url="https://media1.tenor.com/m/p38XIgRTGMkAAAAd/gun.gif")
        self.wsEm = discord.Embed(title=f"{self.players[self.curP]} suggests to SPLIT the Pot.", description=f"The Pot of ${(self.bet*self.nPlayers):,}")

    def bldSpinEm(self, plyr:discord.Member) -> discord.Embed:
        spEm = discord.Embed(title=f"{plyr.display_name} spins the chamber", description="FATE has NOT changed. Pull the Trigger.", color=0xe44c22)
        spEm.set_thumbnail(url=random.choice(self.reloadURLs))
        return spEm
    
    def bldKilledEm(self, plyr:discord.Member) -> discord.Embed:
        spEm = discord.Embed(title=f"{plyr.display_name} dies to the bullet of FATE", description=f"Another Dies. {self.nPlayers-self.dead} Remain.", color=0xe44c22)
        spEm.set_thumbnail(url=random.choice(self.shotURLs))
        return spEm
    
    def bldSrvdEm(self, plyr:discord.Member) -> discord.Embed:
        spEm = discord.Embed(title=f"{plyr.display_name}. dodges FATE.", description="Next Time. Fate Will Get You.", color=0xe44c22)
        spEm.set_thumbnail(url=random.choice(self.survivedURLs))
        return spEm

    def bldGameEm(self, plyr:discord.Member) -> discord.Embed:
        gEm = discord.Embed(title=f"{plyr.display_name}. Your Play", description="Pull? Spin?\nDeath Comes Regardless.", color=0xe44c22)
        gEm.set_thumbnail(url=plyr.display_avatar)
        for i in self.players:
            gEm.add_field(name=i[0].display_name, value="\u200b" if i[1] else "In The Depths of Hell", inline=False)
        return gEm
    
    async def chkGameEnd(self) -> bool:
        if self.dead == self.nPlayers-1:
            for i in self.players:
                if i[1]:
                    wnr = i[0]
                    break
            self.mView.stop()
            await self.RRTbl.edit(embed=discord.Embed(title=f"{wnr.display_name} FATE has decided that your life is worth keeping. You Win.", description=f"The Pot of ${(self.bet*self.nPlayers):,} is ALL yours", color=0xe44c22), view=None)
            await asyncio.sleep(1)
            await self.cancelGame(False)
            return True
        
    async def onSpin(self) -> None:
        random.shuffle(self.cylinder)
        self.onBullet = 0
        await self.RRTbl.edit(embed=self.bldSpinEm(self.players[self.curP][0]), view=self.mView)
    
    async def onPull(self) -> None:
        shot = self.cylinder[self.onBullet]
        self.onBullet += 1
        gEnd = False
        if shot:
            if self.curP == 0 and self.rnd == 1 and 6 not in self.idAcm:
                self.nAcm.append([6, False])
            self.dead += 1
            self.onBullet = 0
            self.players[self.curP][1] = 0
            await self.RRTbl.edit(embed=self.bldKilledEm(self.players[self.curP][0]), view=self.mView)
            await asyncio.sleep(1)
            gEnd = await self.chkGameEnd()
        else:
            await self.RRTbl.edit(embed=self.bldSrvdEm(self.players[self.curP][0]), view=self.mView)
            await asyncio.sleep(1)
        
        if not gEnd:
            fnd = False
            for i in range(self.curP+1, self.nPlayers):
                if self.players[i][1] == 1:
                    self.curP = i
                    fnd = True
                    break
            if not fnd:
                for i in range(0, self.curP):
                    if self.players[i][1] == 1:
                        self.curP = i
                        break
            self.mView.nextPlyr(self.players[self.curP][0])
            if shot:
                self.mView.unloaded()
                await self.RRTbl.edit(embed=self.sEm, view=self.mView)
            self.mView.loaded()
            await self.RRTbl.edit(embed=self.bldGameEm(self.players[self.curP][0]), view=self.mView)

    async def onPlayer(self, int:discord.Interaction) -> None:
        for i in self.players:
            if int.user.id == i[0].id: return

        if int.user.id == 443986051371892746 and 18 not in self.idAcm:
            self.nAcm.append([18, False])
      
        self.players.append([int.user, 1])
        Dt = Gmb.find_one_and_update({"_id":int.user.id, "bal":{"$gte":self.bet}}, {"$set":{"playing":True}, "$inc":{"bal":-self.bet}, "$setOnInsert":{"lastClm":0, "tProfits":0}}, return_document=ReturnDocument.BEFORE)
        if (Dt and not Dt["playing"]):
            self.nPlayers += 1
            self.pEm.description = f"{self.nPlayers}/6 (${(self.bet*self.nPlayers):,} in Pot)"
            self.pEm.add_field(name=int.user.display_name, value="\u200b", inline=False)
            
            if self.nPlayers >= 6:
                self.mView.fullTable()
                await self.RRTbl.edit(embed=self.pEm, view=self.mView)
                return
            
            await self.RRTbl.edit(embed=self.pEm)
        elif not Dt: 
            await int.followup.send(f"{int.user.display_name} NOT Enough Funds.", ephemeral=True)
        else: await int.followup.send(f"{int.user.display_name} Close Open Game First.", ephemeral=True)
        
        
    async def start(self) -> None:
        if self.bet == 0 and 8 not in self.idAcm:
            self.nAcm.append([8, False])
        random.shuffle(self.cylinder)
        await self.RRTbl.edit(embed=self.sEm, view=self.mView)
        self.mView.loaded()
        await asyncio.sleep(1.5)
        gEn = await self.chkGameEnd()
        if not gEn:
            await self.RRTbl.edit(embed=self.bldGameEm(self.players[self.curP][0]), view=self.mView)
    
    async def onSplit(self) -> None:
        self.agreeSplit = 1
        self.voteSplit = 1
        self.wsEm.add_field(name=self.players[self.curP][0].display_name, value="Wants to Split", inline=False)
        await self.RRTbl.edit(embed=self.wsEm)

    async def chSplit(self, usr:discord.Member, ch:bool) -> None:
        for i in self.players:
            if i[0].id == usr.id:
                if i[1] == 1:
                    break
                else:
                    return
        self.voteSplit += 1
        if ch:
            self.agreeSplit += 1
            self.wsEm.add_field(name=usr.display_name, value="Wants to Split", inline=False)
        else:
            self.wsEm.add_field(name=usr.display_name, value="Does NOT want to Split", inline=False)

        if self.agreeSplit > self.nPlayers/2:
            await self.cancelGame(True)

        if self.voteSplit == (self.nPlayers - self.dead):
            if self.agreeSplit > (self.voteSplit-self.agreeSplit):
                await self.cancelGame(True)
            else:
                self.mView.loaded()
                self.mView.onFail()
                await self.RRTbl.edit(embed=self.bldGameEm(self.players[self.curP][0]), view=self.mView)

    async def cancelGame(self, cncl) -> None:
        self.mView.stop()
        mE = (self.bet*self.nPlayers)/(self.nPlayers-self.dead)
        if cncl:
            await self.RRTbl.edit(embed=discord.Embed(title=f"Game Ended", description=f"The Pot of ${(self.bet*self.nPlayers):,} has been split back. ${mE:,} each", color=0xe44c22), view=None)
        Gmb.update_many({"_id":{"$in":[i[0].id for i in self.players if i[1]]}}, {"$inc":{"bal":mE, "rrProfits":mE-self.bet, "rrWins":1}, "$set":{"playing":False}})
        Gmb.update_many({"_id":{"$in":[i[0].id for i in self.players if not i[1]]}}, {"$inc":{"rrProfits":-self.bet, "rrLosses":1}, "$set":{"playing":False}})
        if self.nAcm:
            Gmb.update_one({"_id":self.ctx.user.id}, {"$push": {"achieved": {"$each":self.nAcm}}})

    async def onTim(self) -> None:
        await self.cancelGame(True)

    async def autoRun(self) -> None:
        self.RRTbl = await self.ctx.followup.send(embed=self.pEm, view=self.mView)