from discord.ext import commands
from discord import app_commands
from CBot import DClient as CBotDClient
import discord
from Setup import Gmb, AchievementList, GmbOnSetData, BadgesList
from Customs.Functions import SendWait, FormatTime
import time
from pymongo.collection import ReturnDocument 
from typing import Optional

class Economy(commands.Cog):
    def __init__(self, DClient:CBotDClient) -> None:
        self.DClient = DClient

    @app_commands.command(name="claim", description="Claim Your Daily Sum of Money.")
    @app_commands.checks.cooldown(1, 2)
    async def monGive(self, ctx:discord.Interaction) -> None:
        await ctx.response.defer()
        tryF = Gmb.find_one({"_id":ctx.user.id}, projection={"playing":True, "lastClm":True})
        if tryF and tryF["playing"]: await SendWait(ctx, "Close Your Open Game First."); return
        cT = time.time()
        if not tryF or tryF["lastClm"] <= cT-86400:
            Dt = Gmb.find_one_and_update({"_id":ctx.user.id}, {"$inc":{"bal":1000}, "$set":{"lastClm":cT}, "$setOnInsert":{"tLoans":0, "lastLoan":0, "debt":0, "playing":False, **GmbOnSetData}}, upsert=True, projection={"bal": True}, return_document=ReturnDocument.AFTER)
            await SendWait(ctx, f"Claimed $1,000! Your Balance is ${Dt['bal']:,}")
            return
        await SendWait(ctx, f"You Claimed Today. You Can Claim Again in {FormatTime(int(86400-(cT-tryF['lastClm'])))}")

    @app_commands.command(name="stats", description="Check Your Game Stats.")
    @app_commands.rename(usr="user")
    @app_commands.describe(usr="User to Check Stats For")
    @app_commands.checks.cooldown(1, 2)
    async def statsLookup(self, ctx:discord.Interaction, usr:Optional[discord.Member]) -> None:
        await ctx.response.defer()
        if usr and usr.bot: await SendWait(ctx, f"That's a Bot!"); return
        Dt = Gmb.find_one_and_update({"_id":(usr if usr else ctx.user).id}, {"$setOnInsert":{"tLoans":0, "lastLoan":0, "debt":0, "bal":0, "lastClm":0, "playing":False, **GmbOnSetData}}, upsert=True, return_document=ReturnDocument.AFTER)
        bdge = ""
        if Dt["activeBadge"]:
            for i in BadgesList:
                if i["id"] == Dt["activeBadge"]:
                    bdge = i["badge"]
                    break
        UEm = discord.Embed(title=f"{(usr if usr else ctx.user).display_name} {bdge}", description=f"**Balance:** ${Dt['bal']:,}\n**Debt:** ${format(Dt['debt']*(1+(((time.time()-Dt['lastLoan'])//86400)*0.02)), ',') }\n**Total Loans:** ${Dt['tLoans']:,}", color=0x415f78)
        UEm.add_field(name="Blackjack Profits: ", value=f"${Dt['bjProfits']:,}", inline=True)
        UEm.add_field(name="Roulette Profits: ", value=f"${Dt['rrProfits']:,}", inline=True)
        UEm.add_field(name="Mines Profits: ", value=f"${Dt['mProfits']:,}", inline=True)
        UEm.add_field(name="Slots Profits: ", value=f"${Dt['sProfits']:,}", inline=False)
        # UEm.add_field(name="Total Profits: ", value=f"${(Dt['rrProfits']+Dt['bjProfits']):,}", inline=True)
        UEm.add_field(name="Blackjack Win/Loss/Draw: ", value=f"{Dt['bjWins']}/{Dt['bjLosses']}/{Dt['bjDraws']}", inline=True)
        UEm.add_field(name="Roulette Win/Death/Split: ", value=f"{Dt['rrWins']}/{Dt['rrDeaths']}/{Dt['rrSplits']}", inline=True)
        UEm.add_field(name="Mines Rnds/Diam./Mines: ", value=f"{Dt['mPlayed']}/{Dt['mCollected']}/{Dt['mExploded']}", inline=True)
        UEm.add_field(name="Slots Spins/Wins/JP: ", value=f"{Dt['sPlayed']}/{Dt['sWins']}/{Dt['sJackpot']}", inline=True)
        # UEm.add_field(name="Total W/L/D: ", value=f"{Dt['bjWins']+Dt['rrWins']}/{Dt['bjLosses']+Dt['rrDeaths']}/{Dt['bjDraws']+Dt['rrSplits']}", inline=True)
        UEm.set_thumbnail(url=(usr if usr else ctx.user).display_avatar)
        await ctx.followup.send(embed=UEm)

    @app_commands.command(name="balance", description="Check Your Money.")
    @app_commands.checks.cooldown(1, 2)
    async def monCheck(self, ctx:discord.Interaction) -> None:
        await ctx.response.defer()
        Dt = Gmb.find_one({"_id":ctx.user.id}, projection={"bal": True, "playing":True})
        if Dt and Dt["playing"]: await SendWait(ctx, "Close Your Open Game First."); return
        await SendWait(ctx, f"Your Current Balance is ${format(Dt['bal'], ',') if Dt else 0}")

    @app_commands.command(name="profits", description="Check Your Profits.")
    @app_commands.checks.cooldown(1, 2)
    async def prfCheck(self, ctx:discord.Interaction) -> None:
        await ctx.response.defer()
        Dt = Gmb.find_one({"_id":ctx.user.id}, projection={"bjProfits": True, "playing":True, "rrProfits":True, "mProfits":True, "sProfits":True})
        if Dt and Dt["playing"]: await SendWait(ctx, "Close Your Open Game First."); return
        await SendWait(ctx, f"Your Profits so Far are ${format((Dt['rrProfits']+Dt['sProfits']+Dt['bjProfits']+Dt['mProfits']), ',') if Dt else 0}")

    @app_commands.command(name="debt", description="Check Your Debt.")
    @app_commands.checks.cooldown(1, 2)
    async def debtCheck(self, ctx:discord.Interaction) -> None:
        await ctx.response.defer()
        Dt = Gmb.find_one({"_id":ctx.user.id}, projection={"debt": True, "lastLoan":True})
        await SendWait(ctx, f"You're Currently ${format(Dt['debt']*(1+(((time.time()-Dt['lastLoan'])//86400)*0.02)), ',') if Dt else 0} in Debt")

    @app_commands.command(name="debt-payment", description="Pay Your Debts.")
    @app_commands.checks.cooldown(1, 2)
    async def debtPay(self, ctx:discord.Interaction) -> None:
        await ctx.response.defer()
        tryF = Gmb.find_one({"_id":ctx.user.id}, projection={"playing":True, "lastLoan":True, "debt":True, "bal":True})
        if tryF["playing"]: await SendWait(ctx, "Close Your Open Game First."); return
        if tryF["debt"] <= 0: await SendWait(ctx, "No Debts to Pay."); return
        debtVal = tryF['debt']*(1+(((time.time()-tryF['lastLoan'])//86400)*0.02))
        if tryF["bal"] >= debtVal:
            Dt = Gmb.find_one_and_update({"_id":ctx.user.id}, {"$inc":{"bal":-debtVal}, "$set":{"debt":0}},  projection={"bal": True}, return_document=ReturnDocument.AFTER)
            await SendWait(ctx, f"Paid ${debtVal:,}! You are now Debt Free! Your Balance is ${Dt['bal']:,}")
            return
        await SendWait(ctx, "Not Enough Funds to Pay Debt.")

    @app_commands.command(name="loan", description=r"Take out a Loan. 2% interest/Day.")
    @app_commands.rename(amt="amount")
    @app_commands.describe(amt="Amount to Loan.")
    @app_commands.checks.cooldown(1, 2)
    async def takeLoan(self, ctx:discord.Interaction, amt:int) -> None:
        await ctx.response.defer()
        tryF = Gmb.find_one({"_id":ctx.user.id}, projection={"playing":True, "lastLoan":True, "debt":True})
        if tryF["playing"]: await SendWait(ctx, "Close Your Open Game First."); return
        if not tryF or tryF["debt"] <= 0:
            if amt > 10000: await SendWait(ctx, "Max loan is $10,000."); return
            Dt = Gmb.find_one_and_update({"_id":ctx.user.id}, {"$inc":{"bal":amt, "debt":amt, "tLoans":amt}, "$set":{"lastLoan":time.time()}, "$setOnInsert":{"lastClm":0, "playing":False, **GmbOnSetData}}, upsert=True, projection={"bal": True}, return_document=ReturnDocument.AFTER)
            await SendWait(ctx, f"Taken a ${amt:,} Loan! Your Balance is ${Dt['bal']:,}")
            return
        await SendWait(ctx, "You can't take Loans while in Debt.")

    @app_commands.command(name="transfer", description="Transfer Money.")
    @app_commands.rename(n="amount")
    @app_commands.describe(n="How much to Transfer")
    @app_commands.rename(usr="user")
    @app_commands.describe(usr="@ User to Transfer Money to")
    @app_commands.checks.cooldown(1, 2)
    async def monTrans(self, ctx:discord.Interaction, n:int, usr:discord.Member) -> None:
        await ctx.response.defer()
        if usr.bot: await SendWait(ctx, f"That's a Bot!"); return
        tryF = Gmb.find_one({"_id":usr.id})
        if tryF and tryF["playing"]: await SendWait(ctx, f"User is Playing."); return

        if ctx.user.id == 443986051371892746: Dt1 = True
        elif n>0: 
            Dt1 = Gmb.find_one_and_update({"_id":ctx.user.id, "bal":{"$gte":n}, "playing":False}, {"$inc":{"bal":-n}}, projection={"achieved": True})
            acm = [i[0] for i in Dt1["achieved"]]
        else: 
            await SendWait(ctx, "Yeah....No.. That Doesn't Work.")
            return
       
        if Dt1: 
            Dt2 = Gmb.update_one({"_id":usr.id}, {"$inc":{"bal":n}, "$setOnInsert":{"tLoans":0, "lastLoan":0, "debt":0, "lastClm":0, "playing":False, **GmbOnSetData}}, upsert=True)
        else:
            await SendWait(ctx, f"Not Enough to Transfer or In-Game.")
            return
        
        if not Dt2:
            Gmb.update_one({"_id":ctx.user.id}, {"$inc":{"bal":n}})
            await SendWait(ctx, f"Failed to Transfer.")
            return
        
        if ctx.user.id != 443986051371892746:
            toAdd = []
            if n>=10000 and 21 not in acm:
                toAdd.append([21, False])
            if n>=1000000 and 22 not in acm:
                toAdd.append([22, False])
            if toAdd:
                Gmb.update_one({"_id":ctx.user.id}, {"$push": {"achieved": {"$each":toAdd}}})

        await SendWait(ctx, f"Transfer of ${n:,} to {usr.display_name} Successful.")
    

    TopSlashes = app_commands.Group(name="top",  description="Main Command Group for Economy Top.")

    @TopSlashes.command(name="profit", description="Top Most Profits.")
    @app_commands.checks.cooldown(1,2)
    async def topPrfCheck(self, ctx:discord.Interaction) -> None:
        await ctx.response.defer()
        mDt = {i.id:i.display_name for i in ctx.guild.members}
        Dts = Gmb.find({"_id":{"$in":list(mDt.keys())}}, projection={"bjProfits":True, "rrProfits":True, "mProfits":True, "sProfits":True})
        pEm = discord.Embed(title="Profits Leaderboard:", color=0x4d6c03)
        C = 1
        for Dt in sorted(Dts, key=lambda x:x["bjProfits"]+x["rrProfits"]+x["mProfits"]+x["sProfits"], reverse=True):
            pEm.add_field(name=f"{C}. {mDt[Dt['_id']]}: ${(Dt['bjProfits']+Dt['rrProfits']+Dt['mProfits']+Dt['sProfits']):,}", value="\u200b", inline=False)
            C+=1
        await ctx.followup.send(embed=pEm)

    @TopSlashes.command(name="balance", description="Top Most Balances.")
    @app_commands.checks.cooldown(1,2)
    async def topBalCheck(self, ctx:discord.Interaction) -> None:
        await ctx.response.defer()
        mDt = {i.id:i.display_name for i in ctx.guild.members}
        Dts = Gmb.find({"_id":{"$in":list(mDt.keys())}}, projection={"bal":True})
        bEm = discord.Embed(title="Balance Leaderboard:", color=0x4d6c03)
        C = 1
        for Dt in sorted(Dts, key=lambda x:x["bal"], reverse=True):
            bEm.add_field(name=f"{C}. {mDt[Dt['_id']]}: ${Dt['bal']:,}", value="\u200b", inline=False)
            C+=1
        await ctx.followup.send(embed=bEm)


    AchievementSlashes = app_commands.Group(name="achievements",  description="Main Command Group for Economy Achievements.")

    @AchievementSlashes.command(name="list", description="List Available Achievements.")
    @app_commands.checks.cooldown(1,2)
    async def achList(self, ctx:discord.Interaction) -> None:
        await ctx.response.defer()
        Dt = Gmb.find_one({"_id":ctx.user.id}, projection={"achieved": True, "_id":False})
        aEm = discord.Embed(title="Achievements", color=0x4d6c03)
        added = []
        for i in Dt["achieved"]:
            added.append(i[0])
            for j in AchievementList:
                if i[0] == j["id"]:
                    aEm.add_field(name=f"{j['title']} - UNLOCKED", value=f"{j['desc']}\nReward: ${j['reward']:,} - {'Claimed' if i[1] else 'Unclaimed'}")
                    break
        for i in AchievementList:
            if i["id"] in added: continue
            aEm.add_field(name=f"{i['title']} - LOCKED", value="HIDDEN ACHIEVEMENT" if i["hidden"] else f"{i['desc']}\nReward: ${i['reward']:,}", inline=False)
        await ctx.followup.send(embed=aEm)
    
    # @AchievementSlashes.command(name="user", description="Check Your Unlocked Achievements")
    # @app_commands.checks.cooldown(1,2)

    @AchievementSlashes.command(name="claimall", description="Claim Achievement Rewards.")
    @app_commands.checks.cooldown(1,2)
    async def clmAch(self, ctx:discord.Interaction) -> None:
        await ctx.response.defer()
        Dt = Gmb.find_one({"_id":ctx.user.id}, projection={"_id":False, "achieved":True, "playing":True})
        if not Dt: await SendWait(ctx, "Nothing to Claim"); return
        if Dt and Dt["playing"]: await SendWait(ctx, "Close Your Open Game First."); return
        toClm = [i[0] for i in Dt["achieved"] if not i[1]]
        if not toClm: await SendWait(ctx, "Nothing to Claim"); return
        rwrdVal = 0
        for i in AchievementList:
            if i["id"] in toClm:
                rwrdVal += i["reward"]
        Dt = Gmb.find_one_and_update({"_id":ctx.user.id}, {"$inc":{"bal":rwrdVal}, "$set":{"achieved":[[i[0], True] for i in Dt["achieved"]]}}, projection={"bal": True, "_id":False}, return_document=ReturnDocument.AFTER)
        await SendWait(ctx, f"Claimed ${rwrdVal:,}! Your Balance is ${Dt['bal']:,}")

    async def cog_load(self) -> None:
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self) -> None:
        print(f"{self.__class__.__name__} unloaded!")


async def setup(DClient:CBotDClient) -> None:
    await DClient.add_cog(Economy(DClient))