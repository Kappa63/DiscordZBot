from numpy import random
import io
import asyncio
import discord
from Setup import Gmb
from PIL import Image
from typing import List
from pymongo.collection import ReturnDocument 
from Customs.AchievementHelper import BJAchievements
from Customs.UI.BlackJack import BlackJackView as BJView

class BJ:
    def __init__(self, ctx:discord.Interaction, bal:int, acm:List[int]) -> None:
        self.CARD_HORIZONTAL_SPACING = 10
        self.CARD_VERTICAL_SPACING = 41
        self.EMBED_COLOR = 0x00A36C
        self.DECKS_IN_SHOOT = 6
        self.SHUFFLE_PERCENTAGE = 0.5
        self.ASSETS_DIR = "./Customs/Assets/"
        self.DECK_DIR = self.ASSETS_DIR+"DeckCards2/"

        self.ctx = ctx
        self.bal = bal
        self.acm = acm
        self.acmHelper = BJAchievements([i[0] for i in acm])

        self.DeckCards = ['kc', '6h', '2s', 'qd', '10c', '5h', 'jh', '8h', 'qs', 'kd', 'ks', '5d', '3s',
                        '7h', '3d', '7s', '10h', 'kh', '8d', '8c', 'qh', 'ad', '2c', '2d', 'jd', '9d', 
                        '10s', 'ac', 'jc', '7c', '6s', 'js', '4s', '2h', '10d', '9s', '8s', '3c', '7d', 
                        '3h', 'ah', '5s', '6c', '9h', 'qc', 'as', '6d', '4h', '5c', '4d', '4c', '9c']
        self.shoot = self.DeckCards*self.DECKS_IN_SHOOT
        self.Dealer = []
        self.Player = [[]]
        self.handRes = []
        self.curHand = 0
        self.cache = None

        self.DEm = discord.Embed(title="Dealer", color=self.EMBED_COLOR)
        self.PEm = discord.Embed(title=self.ctx.user.display_name, color=self.EMBED_COLOR)
        self.mView = BJView(self.ctx.user, self.allowedChips(), self.plyrHit, self.plyrDouble, self.plyrSplit, self.plyrStnd, self.onDeal, self.clsTbl, self.addBet, self.onTm)

        self.bet = 0
        self.prft = 0
        self.TbData = [0, 0, 0]
        self.allTrigger = False

    def resText(self) -> str:
        t = []
        handBet = self.bet/len(self.Player)
        for k, v in enumerate(self.handRes):
            match v:
                case 0:
                    t.append(f"Hand-{k} {self.ctx.user.display_name} BUSTED! -{handBet:,}$")
                case 1:
                    t.append(f"Hand-{k} Dealer BUSTED! {handBet:,}$")
                case 2:
                    t.append(f"Hand-{k} {self.ctx.user.display_name} WINS! {handBet:,}$")
                case 3:
                    t.append(f"Hand-{k} Dealer WINS! -{handBet:,}$")
                case 4:
                    t.append(f"Hand-{k} DRAW! 0$")
                case 5:
                    t.append(f"Hand-{k} {self.ctx.user.display_name} BLACKJACK! {handBet:,}$")
                case 6:
                    t.append(f"Hand-{k} Dealer BLACKJACK! -{handBet:,}$")
                case 7:
                    t.append(f"Hand-{k} 2 BLACKJACKS DRAW! 0$")
        return "\n".join(t)

    def cardsValue(self, cards) -> None:
        vls = []
        aTrgr = 0
        for i in cards:
            v = i[:-1]
            if v not in ["j", "q", "k", "a"]: vls.append(int(v))
            elif v != "a": vls.append(10)
            else: aTrgr += 1
        vls = sum(vls)
        if aTrgr: 
            return (vls+(1*aTrgr), vls+11+(1*(aTrgr-1)))
        return (vls, vls)
        
    def addCard(self, c1:Image.Image, c2:Image.Image) -> Image.Image:
        w1, h1 = c1.size
        w2, h2 = c2.size
        wExt = w2//2
        In = Image.new("RGBA", (w1+wExt, h1))
        In.paste(c1, (0,0))
        In.paste(c2, (w1-wExt,0), c2) 
        c1.close()
        c2.close()
        return In

    def createTable(self, c:List[Image.Image]) -> Image.Image:
        maxW = sum(i.size[0] for i in c)
        if maxW <= 510:
            tblNum = 2
        elif maxW <= 765:
            tblNum = 3
        else: tblNum = 4  
        spaces = 3 #(len(c) + 1)
        In = Image.new("RGBA", (maxW+(self.CARD_HORIZONTAL_SPACING*spaces), 329))
        tbl = Image.open(f"{self.ASSETS_DIR}tbl{tblNum}.jpg")
        In.paste(tbl, (0,0))
        tbl.close()
        w0, h0 = c[0].size
        for k, v in enumerate(c):
            pos = ((self.CARD_HORIZONTAL_SPACING*(k+1))+(w0*k), self.CARD_VERTICAL_SPACING)
            In.paste(v, pos, v)
        return In

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
  
    def onWin(self) -> None:
        handBet = self.bet/len(self.Player)
        self.bal += handBet*2
        self.prft += handBet
        self.TbData[0] += 1
        self.acmHelper.updateStreak(1)
        if self.allTrigger:
            self.acmHelper.allInProfit(self.bet)

    def onDraw(self) -> None:
        handBet = self.bet/len(self.Player)
        self.bal += handBet
        self.TbData[2] += 1   
        self.acmHelper.updateStreak(0)

    def onLoss(self) -> None:
        handBet = self.bet/len(self.Player)
        self.TbData[1] += 1  
        self.prft -= handBet
        self.acmHelper.updateStreak(-1)
        if self.allTrigger:
            self.acmHelper.allInProfit(-self.bet)

    async def plyrHit(self) -> bool:
        self.Player[self.curHand].append(self.shoot.pop(0))
        self.PlayerCardsIm = self.addCard(self.PlayerCardsIm, Image.open(f"{self.DECK_DIR}{self.Player[self.curHand][-1]}.png"))

        self.ib1.seek(0)
        self.CdFD.close()
        self.CdFD = discord.File(self.ib1, filename="dlr.png")

        self.ib2.seek(0)
        self.PlayerCardsIm.save(self.ib2, "PNG")
        self.ib2.seek(0)
        self.CdFP.close()
        self.CdFP = discord.File(self.ib2, filename="plyr.png")

        pV = self.cardsValue(self.Player[self.curHand])

        self.PEm.description = f"Total: {str(pV[0])+'/'+str(pV[1]) if (pV[0] != pV[1] and pV[1] <= 21) else pV[0]}"

        await self.BJTbl.edit(embeds=[self.DEm, self.PEm], attachments=[self.CdFD, self.CdFP], view=self.mView)

        if (pV[0] > 21):
            await self.plyrBust()
            return False
        elif (pV[0] == 21 or pV[1] == 21):
            if len(self.Player[self.curHand]) >= 6:
                self.acmHelper.addAchieved(15)
            await self.plyrStnd()
            return False
        return True

    async def plyrStnd(self) -> None:
        self.handRes.append(-1)
        if await self.plyrNextHand():
            return
        await self.BJTbl.edit(view=None)
        await self.dlrRvl()
        dV = self.cardsValue(self.Dealer)
        self.DEm.description = f"Total: {str(dV[0])+'/'+str(dV[1]) if (dV[0] != dV[1] and dV[1] <= 21) else dV[0]}"
        
        await self.BJTbl.edit(embeds=[self.DEm, self.PEm], attachments=[self.CdFD, self.CdFP])

        while (self.checkDlrHit(dV)):
            await self.dlrHit()
            dV = self.cardsValue(self.Dealer)
            self.DEm.description = f"Total: {str(dV[0])+'/'+str(dV[1]) if (dV[0] != dV[1] and dV[1] <= 21) else dV[0]}"
            await self.BJTbl.edit(embeds=[self.DEm, self.PEm], attachments=[self.CdFD, self.CdFP])
        else:
            if (dV[0] > 21): await self.dlrBust()
            else: await self.onEnd()

    async def plyrDouble(self) -> None:
        handBet = self.bet/len(self.Player)
        await self.addBet(handBet)
        if await self.plyrHit():
            await self.plyrStnd()

    async def plyrSplit(self) -> None:
        await self.addBet(self.bet)
        handCards = self.Player[self.curHand]
        self.Player= [[handCards[0]], [handCards[1]]]
        self.Player[0].append(self.shoot.pop(0))
        self.Player[1].append(self.shoot.pop(0))

        self.PlayerCardsIm = self.createTable([self.addCard(Image.open(f"{self.DECK_DIR}{self.Player[0][0]}.png"), Image.open(f"{self.DECK_DIR}{self.Player[0][1]}.png")), 
                                               self.addCard(Image.open(f"{self.DECK_DIR}{self.Player[1][0]}.png"), Image.open(f"{self.DECK_DIR}{self.Player[1][1]}.png"))])
        self.ib1.seek(0)
        self.CdFD.close()
        self.CdFD = discord.File(self.ib1, filename="dlr.png")

        self.ib2.seek(0)
        self.PlayerCardsIm.save(self.ib2, "PNG")
        self.ib2.seek(0)
        self.CdFP.close()
        self.CdFP = discord.File(self.ib2, filename="plyr.png")

        pV1 = self.cardsValue(self.Player[0])
        pV2 = self.cardsValue(self.Player[1])
        self.PEm.description = f"Total (Hand 1): {str(pV1[0])+'/'+str(pV1[1]) if (pV1[0] != pV1[1] and pV1[1] <= 21) else pV1[0]}\nTotal (Hand 2): {str(pV2[0])+'/'+str(pV2[1]) if (pV2[0] != pV2[1] and pV2[1] <= 21) else pV2[0]}"
        await self.BJTbl.edit(embeds=[self.DEm, self.PEm], attachments=[self.CdFD, self.CdFP])
        await asyncio.sleep(1.5)
        self.PlayerCardsIm = self.addCard(Image.open(f"{self.DECK_DIR}{self.Player[self.curHand][0]}.png"), Image.open(f"{self.DECK_DIR}{self.Player[self.curHand][1]}.png"))
        self.ib1.seek(0)
        self.CdFD.close()
        self.CdFD = discord.File(self.ib1, filename="dlr.png")

        self.ib2.seek(0)
        self.PlayerCardsIm.save(self.ib2, "PNG")
        self.ib2.seek(0)
        self.CdFP.close()
        self.CdFP = discord.File(self.ib2, filename="plyr.png")

        pV = self.cardsValue(self.Player[self.curHand])

        self.PEm.description = f"Total: {str(pV[0])+'/'+str(pV[1]) if (pV[0] != pV[1] and pV[1] <= 21) else pV[0]}"
        self.mView.enableBase()
        await self.BJTbl.edit(embeds=[self.DEm, self.PEm], attachments=[self.CdFD, self.CdFP], view=self.mView)
        if pV[1] == 21:
            await self.onBJ(1)

    async def plyrBust(self) -> None:
        self.onLoss()
        self.handRes.append(0)
        if await self.plyrNextHand():
            return
        await self.BJTbl.edit(view=None)
        await self.dlrRvl()
        dV = self.cardsValue(self.Dealer)
        self.DEm.description = f"Total: {str(dV[0])+'/'+str(dV[1]) if (dV[0] != dV[1] and dV[1] <= 21) else dV[0]}"
        await self.BJTbl.edit(embeds=[self.DEm, self.PEm], attachments=[self.CdFD, self.CdFP])
        await self.BJTbl.edit(embeds=[self.DEm, self.PEm, discord.Embed(title=self.resText(), description=f"Current Balance: ${self.bal:,}", color=self.EMBED_COLOR)])
        await self.clsDeal()

    async def plyrNextHand(self) -> None:
        if self.curHand == len(self.Player)-1:
            return False
        
        self.cache = self.PlayerCardsIm
        self.curHand += 1
        self.PlayerCardsIm = self.addCard(Image.open(f"{self.DECK_DIR}{self.Player[self.curHand][0]}.png"), Image.open(f"{self.DECK_DIR}{self.Player[self.curHand][1]}.png"))

        self.ib1.seek(0)
        self.CdFD.close()
        self.CdFD = discord.File(self.ib1, filename="dlr.png")

        self.ib2.seek(0)
        self.PlayerCardsIm.save(self.ib2, "PNG")
        self.ib2.seek(0)
        self.CdFP.close()
        self.CdFP = discord.File(self.ib2, filename="plyr.png")

        pV = self.cardsValue(self.Player[self.curHand])

        self.PEm.description = f"Total: {str(pV[0])+'/'+str(pV[1]) if (pV[0] != pV[1] and pV[1] <= 21) else pV[0]}"

        await self.BJTbl.edit(embeds=[self.DEm, self.PEm], attachments=[self.CdFD, self.CdFP])
        if pV[1] == 21:
            await self.onBJ(1)
        return True

    def checkDlrHit(self, val) -> bool:
        return not ((val[1] >= 17 and val[1] <= 21) or (val[0] >= 17))

    async def dlrRvl(self) -> None:
        self.DealerCardsIm = self.addCard(Image.open(f"{self.DECK_DIR}{self.Dealer[1]}.png"), Image.open(f"{self.DECK_DIR}{self.Dealer[0]}.png"))

        if self.cache:
            self.PlayerCardsIm = self.createTable([self.cache, self.PlayerCardsIm])
            self.cache = None

        self.ib2.seek(0)
        self.PlayerCardsIm.save(self.ib2, "PNG")
        self.ib2.seek(0)
        self.CdFP.close()
        self.CdFP = discord.File(self.ib2, filename="plyr.png")

        self.ib2.seek(0)
        self.CdFP = discord.File(self.ib2, filename="plyr.png")

        self.ib1.seek(0)
        self.DealerCardsIm.save(self.ib1, "PNG")
        self.ib1.seek(0)
        self.CdFD = discord.File(self.ib1, filename="dlr.png")

    async def dlrHit(self) -> None:
        self.Dealer.append(self.shoot.pop(0))
        self.DealerCardsIm = self.addCard(self.DealerCardsIm, Image.open(f"{self.DECK_DIR}{self.Dealer[-1]}.png"))

        self.ib2.seek(0)
        self.CdFP.close()
        self.CdFP = discord.File(self.ib2, filename="plyr.png")

        self.ib1.seek(0)
        self.DealerCardsIm.save(self.ib1, "PNG")
        self.ib1.seek(0)
        self.CdFD.close()
        self.CdFD = discord.File(self.ib1, filename="dlr.png")

    async def dlrBust(self) -> None:
        for k, v in enumerate(self.handRes):
            if v == -1:
                self.onWin()
                self.handRes[k] = 1
        await self.BJTbl.edit(embeds=[self.DEm, self.PEm, discord.Embed(title=self.resText(), description=f"Current Balance: ${self.bal:,}", color=self.EMBED_COLOR)])
        await self.clsDeal()

    async def onEnd(self) -> None:
        dV = self.cardsValue(self.Dealer)
        dV = (dV[0] if dV[1] > 21 else dV[1])
        for k, v in enumerate(self.handRes):
            if v == -1:
                pV = self.cardsValue(self.Player[k])
                pV = (pV[0] if pV[1] > 21 else pV[1])
                if dV > pV:
                    self.handRes[k] = 3
                    self.onLoss()
                elif pV > dV:
                    self.handRes[k] = 2
                    self.onWin()
                else:
                    self.handRes[k] = 4
                    self.onDraw()

        await self.BJTbl.edit(embeds=[self.DEm, self.PEm, discord.Embed(title=self.resText(), description=f"Current Balance: ${self.bal:,}", color=self.EMBED_COLOR)])
        await self.clsDeal()  

    async def onBJ(self, forP:int) -> None:
        if forP == 1:
            self.handRes.append(5)
            self.acmHelper.onBJ(self.bet)
            self.onWin()
        elif forP == 2:
            self.handRes.append(6)
            self.onLoss()
        else:
            self.handRes.append(7)
            self.onDraw()
        if await self.plyrNextHand():
            return
        await self.BJTbl.edit(view=None)
        await self.dlrRvl()
        dV = self.cardsValue(self.Dealer)
        self.DEm.description = f"Total: {str(dV[0])+'/'+str(dV[1]) if (dV[0] != dV[1] and dV[1] <= 21) else dV[0]}"
        await self.BJTbl.edit(embeds=[self.DEm, self.PEm, discord.Embed(title=self.resText(), description=f"Current Balance: ${self.bal:,}", color=self.EMBED_COLOR)], attachments=[self.CdFD, self.CdFP])
        await self.clsDeal() 

    def clsBfrs(self) -> None:
        try:
            if(self.TbData[0]):
                self.ib1.close()
                self.ib2.close()
                self.CdFP.close()
                self.CdFD.close()
                self.DealerCardsIm.close()
                self.PlayerCardsIm.close()
        except:
            pass
        self.Dealer = []
        self.Player = [[]]
        self.curHand = 0
        self.bet = 0
        self.cache = None
        self.handRes = []

    async def rdyNDeal(self) -> None:
        self.mView.endDeal()
        await self.BJTbl.edit(view=self.mView)

    async def clsDeal(self) -> None:
        self.mView.chipLogUp(self.allowedChips())
        self.clsBfrs()
        await self.rdyNDeal()

    async def shuffle(self) -> None:
        await self.BJTbl.edit(embed=discord.Embed(title="Shuffling Cards...", color=self.EMBED_COLOR))
        self.shoot = self.DeckCards*self.DECKS_IN_SHOOT
        random.shuffle(self.shoot)

    async def addBet(self, amm) -> None:
        if amm == -1:
            amm = self.bal
            self.allTrigger = True

        self.bal-=amm
        self.bet+=amm
        self.mView.chipLogUp(self.allowedChips())
        await self.BJTbl.edit(embeds=[self.DEm, self.PEm, discord.Embed(title=f"Remaining: ${self.bal:,}", color=self.EMBED_COLOR)], view=self.mView)

    async def onDeal(self) -> None:
        if not self.bet:
            self.acmHelper.updateEmptyBet()
        if((len(self.shoot)/(52*self.DECKS_IN_SHOOT))<=self.SHUFFLE_PERCENTAGE or not sum(self.TbData)):
            await self.shuffle()

        self.Player[self.curHand].append(self.shoot.pop(0))
        self.Dealer.append(self.shoot.pop(0))
        self.Player[self.curHand].append(self.shoot.pop(0))
        self.Dealer.append(self.shoot.pop(0))

        pV = self.cardsValue(self.Player[self.curHand])
        dV = self.cardsValue([self.Dealer[0]])
        dVr = self.cardsValue(self.Dealer)

        self.DealerCardsIm = self.addCard(Image.open(f"{self.DECK_DIR}cb.png"), Image.open(f"{self.DECK_DIR}{self.Dealer[0]}.png"))
        self.PlayerCardsIm = self.addCard(Image.open(f"{self.DECK_DIR}{self.Player[self.curHand][0]}.png"), Image.open(f"{self.DECK_DIR}{self.Player[self.curHand][1]}.png"))

        self.ib1 = io.BytesIO()
        self.DealerCardsIm.save(self.ib1, "PNG")
        self.ib1.seek(0)
        self.CdFD = discord.File(self.ib1, filename="dlr.png")

        self.ib2 = io.BytesIO()
        self.PlayerCardsIm.save(self.ib2, "PNG")
        self.ib2.seek(0)
        self.CdFP = discord.File(self.ib2, filename="plyr.png")

        self.DEm = discord.Embed(title="Dealer", description=f"Total: {str(dV[0])+'/'+str(dV[1]) if (dV[0] != dV[1] and dVr[1] < 21) else 'BLACKJACK' if dVr[1]==21 else dV[0]}", color=self.EMBED_COLOR)
        self.DEm.set_image(url="attachment://dlr.png")
        self.PEm = discord.Embed(title=self.ctx.user.display_name, description=f"Total: {str(pV[0])+'/'+str(pV[1]) if (pV[0] != pV[1] and pV[1] < 21) else 'BLACKJACK' if pV[1]==21 else pV[0]}", color=self.EMBED_COLOR)
        self.PEm.set_image(url="attachment://plyr.png")

        canDouble = self.bal < self.bet
        splittableCheck = self.cardsValue([self.Player[self.curHand][0]]) != self.cardsValue([self.Player[self.curHand][1]])
        self.mView.startDeal(canDouble, splittableCheck or canDouble)
        await self.BJTbl.edit(embeds=[self.DEm, self.PEm], attachments=[self.CdFD, self.CdFP], view=self.mView)

        match (pV[1] == 21, dVr[1] == 21):
            case (True, True):
                await self.onBJ(0)
            case (True, False):
                await self.onBJ(1)
            case (False, True):
                await self.onBJ(2)

    async def autoRun(self) -> None:
        self.BJTbl = await self.ctx.followup.send(embed=discord.Embed(title="Opening Table...", description=f"Current Balance: ${self.bal:,}", color=self.EMBED_COLOR), view=self.mView)

    async def clsTbl(self) -> None:
        try:
            self.mView.stop()
            await self.BJTbl.edit(embeds=[discord.Embed(title="Table Closed.", description=f"W/L/D\n{self.TbData[0]}/{self.TbData[1]}/{self.TbData[2]}\n\nChip Balance: {(self.bal+self.bet):,}\n\nProfits: {self.prft:,}", color=self.EMBED_COLOR)], attachments=[], view=None)
            self.clsBfrs()
        except:
            pass
        Dt = Gmb.find_one_and_update({"_id":self.ctx.user.id}, {"$set": {"playing":False}, "$inc":{"bal":self.bal+self.bet, "bjProfits":self.prft, "bjWins":self.TbData[0], "bjDraws":self.TbData[2], "bjLosses":self.TbData[1]}}, projection={"bjProfits":True, "bal":True}, return_document=ReturnDocument.AFTER)
        self.acmHelper.dealsPlayed(sum(self.TbData))
        self.acmHelper.tableProfit(self.prft)
        self.acmHelper.allTimeProfits(Dt["bjProfits"])
        self.acmHelper.allTimeBalance(Dt["bal"])
        nAcm = self.acmHelper.getAchieved()[len(self.acm):]
        if nAcm:
            Gmb.update_one({"_id":self.ctx.user.id}, {"$push": {"achieved":{"$each":[[i,False] for i in nAcm]}}})

    async def onTm(self) -> None:
        await self.clsTbl()