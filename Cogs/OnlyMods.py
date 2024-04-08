import discord
from discord.ext import commands
# from Setup import ChDev, SendWait, AQd
from Setup import SendWait, ChDev
import random
import requests

Doing = ["Playing with the laws of physics", "Torture", "Just Vibin'", "With my toes",
         "Chess with god", "With Leona"]

class OnlyMods(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.command(name="status")
    @commands.check(ChDev)
    async def BotStatus(self, ctx):
        SEm = discord.Embed(title="Current ZBot Status", color=0x000000)
        SEm.add_field(name="Guilds in: ", value=len(self.DClient.guilds), inline=False)
        SEm.add_field(name="Latency: ", value=self.DClient.latency * 100, inline=False)
        SEm.add_field(name="ShardCount: ", value=self.DClient.shard_count, inline=False)
        SEm.add_field(name="Loaded Cogs: ", value="\n".join(self.DClient.LoadedCogs), inline=False)
        await ctx.message.channel.send(embed=SEm)

    @commands.command(name="embed")
    @commands.check(ChDev)
    async def Embedder(self, ctx, *args):
        # print(args)
        args = (" ".join(args)).split("_")
        # print(args)
        for i in args:
            if i[:2].lower() == "-t": Title = i[3:]
            if i[:2].lower() == "-d": Desc = i[3:]
            if i[:2].lower() == "-c": Color = 0xff0000 if i[3:].lower() == "red" else 0x3a62d8 if i[3:].lower() == "blue" else 0xc4c4c4
        await ctx.message.delete()
        await ctx.message.channel.send(embed=discord.Embed(title=Title, description = Desc, color = Color))

    @commands.command(name="reloadall")
    @commands.check(ChDev)
    async def MassCogReloader(self, ctx):
        await self.DClient.reload_all_cogs()
        REm = discord.Embed(title="ZBot Reloaded", color = 0x000000)
        REm.add_field(name="Cogs Reloaded: ", value="\n".join(self.DClient.LoadedCogs), inline=False)
        await ctx.message.channel.send(embed=REm)

    @commands.command(name="reload")
    @commands.check(ChDev)
    async def CogReloader(self, ctx, *args):
        await self.DClient.reload_cogs(args)
        REm = discord.Embed(title="ZBot Reloaded", color = 0x000000)
        REm.add_field(name="Cogs Reloaded: ", value="\n".join(args), inline=False)
        await ctx.message.channel.send(embed=REm)

    @commands.command(name="unload")
    @commands.check(ChDev)
    async def CogUnloader(self, ctx, *args):
        await self.DClient.unload_cogs(args)
        REm = discord.Embed(title="ZBot Unloaded", color = 0x000000)
        REm.add_field(name="Cogs Unloaded: ", value="\n".join(args), inline=False)
        await ctx.message.channel.send(embed=REm)
    
    @commands.command(name="load")
    @commands.check(ChDev)
    async def CogLoader(self, ctx, *args):
        await self.DClient.load_cogs(args)
        REm = discord.Embed(title="ZBot Loaded", color = 0x000000)
        REm.add_field(name="Cogs loaded: ", value="\n".join(args), inline=False)
        await ctx.message.channel.send(embed=REm)

    # @commands.command(name="makedown")
    # @commands.check(ChDev)
    # async def MakeBotOff(self, ctx):
    #     await self.DClient.change_presence(status=discord.Status.invisible)
    #     StateFile = open("OpenState.txt", "w+")
    #     StateFile.write("Down")
    #     StateFile.close()
    #     await SendWait(ctx, "Bot Invisible (Down)")

    # @commands.command(name="makeup")
    # @commands.check(ChDev)
    # async def MakeBotOn(self, ctx):
    #     await self.DClient.change_presence(status=discord.Status.online, activity=discord.Game(f"zhelp || {random.choice(Doing)}"))
    #     StateFile = open("OpenState.txt", "w+")
    #     StateFile.write("Up")
    #     StateFile.close()
    #     await SendWait(ctx, "Bot Visible (Up)")

    # @commands.command(name="numapod")
    # @commands.check(ChDev)
    # async def GetAPODNum(self, ctx):
    #     await SendWait(ctx, f'{AQd.count_documents({"Type":"APOD"})} in APOD Daily')

    # @commands.command(name="numqotd")
    # @commands.check(ChDev)
    # async def GetQOTDNum(self, ctx):
    #     await SendWait(ctx, f'{AQd.count_documents({"Type":"QOTD"})} in QOTD Daily')

    # @commands.command(name="numcptd")
    # @commands.check(ChDev)
    # async def GetCPTDNum(self, ctx):
    #     await SendWait(ctx, f'{AQd.count_documents({"Type":"CPTD"})} in CPTD Daily')

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded!")

async def setup(DClient):
    await DClient.add_cog(OnlyMods(DClient))