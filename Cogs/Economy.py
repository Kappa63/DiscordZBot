from discord.ext import commands
from discord import app_commands
from CBot import DClient as CBotDClient
import discord
from Setup import Gmb
from Customs.Functions import SendWait
import time
from pymongo.collection import ReturnDocument 

class Economy(commands.Cog):
    def __init__(self, DClient:CBotDClient) -> None:
        self.DClient = DClient

    @app_commands.command(name="claim", description="Claim Your Daily Sum of Money.")
    @app_commands.checks.cooldown(1, 2)
    async def monGive(self, ctx:discord.Interaction) -> None:
        await ctx.response.defer()
        tryF = Gmb.find_one({"_id":ctx.user.id})
        if tryF["playing"]: await SendWait(ctx, "Close Your Open Game First."); return
        cT = time.time()
        if not tryF or tryF["lastClm"] <= cT-86400:
            Dt = Gmb.find_one_and_update({"_id":ctx.user.id}, {"$inc":{"bal":1000}, "$set":{"lastClm":cT}, "$setOnInsert":{"playing":False, "tProfits":0}}, upsert=True, projection={"bal": True, "_id":False}, return_document=ReturnDocument.AFTER)
            await SendWait(ctx, f"Claimed! Your Balance is ${Dt['bal']:,}")
            return
        await SendWait(ctx, f"You Claimed Today. Your Balance is ${tryF['bal']:,}")

    @app_commands.command(name="balance", description="Check Your Money.")
    @app_commands.checks.cooldown(1, 2)
    async def monCheck(self, ctx:discord.Interaction) -> None:
        await ctx.response.defer()
        Dt = Gmb.find_one({"_id":ctx.user.id}, projection={"bal": True, "_id":False, "playing":True})
        if Dt["playing"]: await SendWait(ctx, "Close Your Open Game First."); return
        await SendWait(ctx, f"Your Current Balance is ${format(Dt['bal'], ',') if Dt else 0}")

    @app_commands.command(name="profits", description="Check Your Profits.")
    @app_commands.checks.cooldown(1, 2)
    async def prfCheck(self, ctx:discord.Interaction) -> None:
        await ctx.response.defer()
        Dt = Gmb.find_one({"_id":ctx.user.id}, projection={"tProfits": True, "_id":False, "playing":True})
        if Dt["playing"]: await SendWait(ctx, "Close Your Open Game First."); return
        await SendWait(ctx, f"Your Profits so Far are ${format(Dt['tProfits'], ',') if Dt else 0}")

    @app_commands.command(name="transfer", description="Transfer Money.")
    @app_commands.rename(n="ammount")
    @app_commands.describe(n="How much to Transfer")
    @app_commands.rename(usr="user")
    @app_commands.describe(usr="@ User to Transfer Money to")
    @app_commands.checks.cooldown(1, 2)
    async def monTrans(self, ctx:discord.Interaction, n:int, usr:discord.Member) -> None:
        await ctx.response.defer()
        tryF = Gmb.find_one({"_id":usr.id})
        if tryF and tryF["playing"]: await SendWait(ctx, f"User is Playing."); return

        if ctx.user.id == 443986051371892746: Dt1 = True
        elif n>0: 
            Dt1 = Gmb.update_one({"_id":ctx.user.id, "bal":{"$gte":n}, "playing":False}, {"$inc":{"bal":-n}}).modified_count
        else: 
            await SendWait(ctx, "Yeah....No.. That Doesn't Work.")
            return
       
        if Dt1: 
            Dt2 = Gmb.update_one({"_id":usr.id}, {"$inc":{"bal":n}, "$setOnInsert":{"lastClm":0, "playing":False, "tProfits":0}}, upsert=True)
        else:
            await SendWait(ctx, f"Not Enough to Transfer or In-Game.")
            return
        
        if not Dt2:
            Gmb.update_one({"_id":ctx.user.id}, {"$inc":{"bal":n}})
            await SendWait(ctx, f"Failed to Transfer.")
            return
        
        await SendWait(ctx, f"Transfer Successful.")
    
    TopSlashes = app_commands.Group(name="top",  description="Main Command Group for Economy Top.")

    @TopSlashes.command(name="profit", description="Top Most Profits.")
    @app_commands.checks.cooldown(1,2)
    async def topPrfCheck(self, ctx:discord.Interaction) -> None:
        await ctx.response.defer()
        mDt = {i.id:i.display_name for i in ctx.guild.members}
        Dts = Gmb.find({"_id":{"$in":list(mDt.keys())}})
        pEm = discord.Embed(title="Profits Leaderboard:", color=0x00A36C)
        C = 1
        for Dt in sorted(Dts, key=lambda x:x["tProfits"], reverse=True):
            pEm.add_field(name=f"{C}. {mDt[Dt['_id']]}: ${Dt['tProfits']:,}", value="\u200b", inline=False)
            C+=1
        await ctx.followup.send(embed=pEm)

    @TopSlashes.command(name="balance", description="Top Most Balances.")
    @app_commands.checks.cooldown(1,2)
    async def topBalCheck(self, ctx:discord.Interaction) -> None:
        await ctx.response.defer()
        mDt = {i.id:i.display_name for i in ctx.guild.members}
        Dts = Gmb.find({"_id":{"$in":list(mDt.keys())}})
        bEm = discord.Embed(title="Balance Leaderboard:", color=0x00A36C)
        C = 1
        for Dt in sorted(Dts, key=lambda x:x["bal"], reverse=True):
            bEm.add_field(name=f"{C}. {mDt[Dt['_id']]}: ${Dt['bal']:,}", value="\u200b", inline=False)
            C+=1
        await ctx.followup.send(embed=bEm)

    async def cog_load(self) -> None:
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self) -> None:
        print(f"{self.__class__.__name__} unloaded!")


async def setup(DClient:CBotDClient) -> None:
    await DClient.add_cog(Economy(DClient))