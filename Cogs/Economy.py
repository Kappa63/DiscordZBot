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
    async def monGive(self, ctx:discord.Interaction) -> None:
        await ctx.response.defer()
        tryF = Gmb.find_one({"_id":ctx.user.id})
        cT = time.time()
        if not tryF or tryF["lastClm"] <= cT-86400:
            Dt = Gmb.find_one_and_update({"_id":ctx.user.id}, {"$inc":{"bal":100}, "$set":{"lastClm":cT}, "$setOnInsert":{"playing":False}}, upsert=True, projection={"bal": True, "_id":False}, return_document=ReturnDocument.AFTER)
            await SendWait(ctx, f"Claimed! Your Balance is ${Dt['bal']}")
            return
        await SendWait(ctx, f"You Claimed Today. Your Balance is ${tryF['bal']}")

    @app_commands.command(name="balance", description="Check Your Money.")
    async def monCheck(self, ctx:discord.Interaction) -> None:
        await ctx.response.defer()
        Dt = Gmb.find_one({"_id":ctx.user.id}, projection={"bal": True, "_id":False})
        await SendWait(ctx, f"Your Current Balance is ${Dt['bal'] if Dt else 0}")

    async def cog_load(self) -> None:
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self) -> None:
        print(f"{self.__class__.__name__} unloaded!")


async def setup(DClient:CBotDClient) -> None:
    await DClient.add_cog(Economy(DClient))