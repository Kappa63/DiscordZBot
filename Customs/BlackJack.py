import random
import io
import discord
import gc
from PIL import Image
from Customs.UI.BlackJack import BlackJackView as BJView

class BJ:
    def __init__(self, ctx:discord.Interaction) -> None:
        self.ctx = ctx
        self.DeckCards = ['kc', '6h', '2s', 'qd', '10c', '5h', 'jh', '8h', 'qs', 'kd', 'ks', '5d', '3s',
                        '7h', '3d', '7s', '10h', 'kh', '8d', '8c', 'qh', 'ad', '2c', '2d', 'jd', '9d', 
                        '10s', 'ac', 'jc', '7c', '6s', 'js', '4s', '2h', '10d', '9s', '8s', '3c', '7d', 
                        '3h', 'ah', '5s', '6c', '9h', 'qc', 'as', '6d', '4h', '5c', '4d', '4c', '9c']
        self.shoot = self.DeckCards*6
        self.DeckDir = "./Customs/DeckCards/"
        self.Dealer = []
        self.Player = []
        self.mView = BJView(self.ctx.user, self.plyrHit, self.plyrStnd, self.onDeal, self.clsTbl, self.onTm)

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
        w, h = c1.size
        In = Image.new("RGBA", (w+250, h))
        In.paste(c1, (0,0))
        In.paste(c2, (w-250,0), c2) 
        c1.close()
        c2.close()
        return In
    
    async def plyrBust(self) -> None:
        await self.BJTbl.edit(view=None)
        await self.dlrRvl()
        dV = self.cardsValue(self.Dealer)
        self.DEm.description = f"Total: {str(dV[0])+'/'+str(dV[1]) if (dV[0] != dV[1] and dV[1] <= 21) else dV[0]}"
        await self.BJTbl.edit(embeds=[self.DEm, self.PEm], attachments=[self.CdFD, self.CdFP])
        await self.BJTbl.edit(embeds=[self.DEm, self.PEm, discord.Embed(title=f"{self.ctx.user.display_name} BUSTED!", color=0x00A36C)])
        # await self.ctx.followup.send(embed=discord.Embed(title=f"{self.ctx.user.display_name} BUSTED!", color=0x00A36C))
        await self.clsDeal()

    async def plyrHit(self) -> None:
        self.Player.append(self.shoot.pop(0))
        self.PlayerCardsIm = self.addCard(self.PlayerCardsIm, Image.open(f"{self.DeckDir}{self.Player[-1]}.png"))

        self.ib1.seek(0)
        self.CdFD.close()
        self.CdFD = discord.File(self.ib1, filename="dlr.png")

        self.ib2.seek(0)
        self.PlayerCardsIm.save(self.ib2, "PNG")
        self.ib2.seek(0)
        self.CdFP.close()
        self.CdFP = discord.File(self.ib2, filename="plyr.png")

        pV = self.cardsValue(self.Player)

        self.PEm.description = f"Total: {str(pV[0])+'/'+str(pV[1]) if (pV[0] != pV[1] and pV[1] <= 21) else pV[0]}"

        await self.BJTbl.edit(embeds=[self.DEm, self.PEm], attachments=[self.CdFD, self.CdFP])

        if (pV[0] > 21):
            await self.plyrBust()
        elif (pV[0] == 21 or pV[1] == 21):
            await self.plyrStnd()

    async def plyrStnd(self) -> None:
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

    def checkDlrHit(self, val) -> bool:
        return not ((val[1] >= 17 and val[1] <= 21) or (val[0] >= 17))

    async def dlrBust(self) -> None:
        await self.BJTbl.edit(embeds=[self.DEm, self.PEm, discord.Embed(title="Dealer BUSTED!", color=0x00A36C)])
        await self.clsDeal()

    async def clsTbl(self) -> None:
        await self.BJTbl.edit(view=None)
        self.clsBfrs()
        del self
        gc.collect()

    async def clsDeal(self) -> None:
        self.clsBfrs()
        await self.rdyNDeal()

    def clsBfrs(self) -> None:
        self.ib1.close()
        self.ib2.close()
        self.CdFP.close()
        self.CdFD.close()
        self.DealerCardsIm.close()
        self.PlayerCardsIm.close()
        self.Dealer = []
        self.Player = []
        

        # print(len(self.DeckCards))
        # del self
        # gc.collect()

    async def rdyNDeal(self) -> None:
        self.mView.endDeal()
        await self.BJTbl.edit(view=self.mView)

    async def dlrHit(self) -> None:
        self.Dealer.append(self.shoot.pop(0))
        self.DealerCardsIm = self.addCard(self.DealerCardsIm, Image.open(f"{self.DeckDir}{self.Dealer[-1]}.png"))

        self.ib2.seek(0)
        self.CdFP.close()
        self.CdFP = discord.File(self.ib2, filename="plyr.png")

        self.ib1.seek(0)
        self.DealerCardsIm.save(self.ib1, "PNG")
        self.ib1.seek(0)
        self.CdFD.close()
        self.CdFD = discord.File(self.ib1, filename="dlr.png")

        # await self.BJTbl.edit(embeds=[self.DEm, self.PEm], attachments=[self.CdFD, self.CdFP])

    async def dlrRvl(self) -> None:
        self.DealerCardsIm = self.addCard(Image.open(f"{self.DeckDir}{self.Dealer[1]}.png"), Image.open(f"{self.DeckDir}{self.Dealer[0]}.png"))

        self.ib2.seek(0)
        self.CdFP = discord.File(self.ib2, filename="plyr.png")

        self.ib1.seek(0)
        self.DealerCardsIm.save(self.ib1, "PNG")
        self.ib1.seek(0)
        self.CdFD = discord.File(self.ib1, filename="dlr.png")
        # self.DEm.description = f"Total: {'/'.join(dV) if dV[0] != dV[1] else dV[0]}"

        # await self.BJTbl.edit(embeds=[self.DEm, self.PEm], attachments=[self.CdFD, self.CdFP])

    async def onEnd(self) -> None:
        dV = self.cardsValue(self.Dealer)
        dV = (dV[0] if dV[1] > 21 else dV[1])
        pV = self.cardsValue(self.Player)
        pV = (pV[0] if pV[1] > 21 else pV[1])
        await self.BJTbl.edit(embeds=[self.DEm, self.PEm, discord.Embed(title="Dealer WINS!" if dV > pV else "Player WINS!" if pV > dV else "DRAW!", color=0x00A36C)])

        # await self.ctx.followup.send(embed=discord.Embed(title="Dealer WINS!" if dV > pV else "Player WINS!" if pV > dV else "DRAW!", color=0x00A36C))  
        await self.clsDeal()   

    async def onTm(self) -> None:
        await self.BJTbl.edit(view=None)

    async def shuffle(self) -> None:
        await self.BJTbl.edit(embed=discord.Embed(title="Shuffling Cards...", color=0x00A36C))
        self.shoot = self.DeckCards*5
        random.shuffle(self.shoot)

    async def onDeal(self) -> None:
        if((len(self.shoot)/(52*6))<=0.5):
            await self.shuffle()

        self.Player.append(self.shoot.pop(0))
        self.Dealer.append(self.shoot.pop(0))
        self.Player.append(self.shoot.pop(0))
        self.Dealer.append(self.shoot.pop(0))

        pV = self.cardsValue(self.Player)
        dV = self.cardsValue([self.Dealer[0]])

        self.DealerCardsIm = self.addCard(Image.open(f"{self.DeckDir}cb.png"), Image.open(f"{self.DeckDir}{self.Dealer[0]}.png"))
        self.PlayerCardsIm = self.addCard(Image.open(f"{self.DeckDir}{self.Player[0]}.png"), Image.open(f"{self.DeckDir}{self.Player[1]}.png"))
        
        self.ib1 = io.BytesIO()
        self.DealerCardsIm.save(self.ib1, "PNG")
        self.ib1.seek(0)
        self.CdFD = discord.File(self.ib1, filename="dlr.png")
            
        self.ib2 = io.BytesIO()
        self.PlayerCardsIm.save(self.ib2, "PNG")
        self.ib2.seek(0)
        self.CdFP = discord.File(self.ib2, filename="plyr.png")
            
        self.DEm = discord.Embed(title="Dealer", description=f"Total: {str(dV[0])+'/'+str(dV[1]) if (dV[0] != dV[1] and dV[1] <= 21) else dV[0]}", color=0x00A36C)
        self.DEm.set_image(url="attachment://dlr.png")
        self.PEm = discord.Embed(title=self.ctx.user.display_name, description=f"Total: {str(pV[0])+'/'+str(pV[1]) if (pV[0] != pV[1] and pV[1] <= 21) else pV[0]}", color=0x00A36C)
        self.PEm.set_image(url="attachment://plyr.png")
        self.mView.startDeal()
        await self.BJTbl.edit(embeds=[self.DEm, self.PEm], attachments=[self.CdFD, self.CdFP], view=self.mView)
        if pV[0] == 21 or pV[1] == 21:
            await self.plyrStnd()

    async def autoRun(self) -> None:
        self.BJTbl = await self.ctx.followup.send(embed=discord.Embed(title="Opening Table...", color=0x00A36C))
        await self.shuffle()
        await self.onDeal()