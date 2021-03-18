import discord
from discord.ext import commands
from Setup import ChDev, SendWait
import random
import requests
from Setup import AQd

Doing = [
    "Playing with the laws of physics",
    "Torture",
    "Just Vibin'",
    "With my toes",
    "Chess with god",
    "With Leona",
]


class OnlyMods(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.command(name="checkzbot")
    @commands.check(ChDev)
    async def BotStatus(self, ctx):
        SEm = discord.Embed(title="Current ZBot Status", color=0x000000)
        SEm.add_field(name="Guilds in: ", value=len(self.DClient.guilds), inline=False)
        SEm.add_field(name="Latency: ", value=self.DClient.latency * 100, inline=False)
        SEm.add_field(name="ShardCount: ", value=self.DClient.shard_count, inline=False)
        await ctx.message.channel.send(embed=SEm)

    @commands.command(name="embed")
    @commands.check(ChDev)
    async def Embedder(self, ctx, *args):
        args = (" ".join(args)).split("_")
        for i in args:
            if i[:2].lower() == "-t":
                Title = i[3:]
            if i[:2].lower() == "-d":
                Desc = i[3:]
            if i[:2].lower() == "-c":
                Color = 0xff0000 if i[3:].lower() == "red" else 0x3a62d8 if i[3:].lower() == "blue" else 0xc4c4c4
        await ctx.message.delete()
        await ctx.message.channel.send(embed=discord.Embed(title=Title, description = Desc, color = Color))

    @commands.command(name="makedown")
    @commands.check(ChDev)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def MakeBotOff(self, ctx):
        await self.DClient.change_presence(status=discord.Status.invisible)
        StateFile = open("OpenState.txt", "w+")
        StateFile.write("Down")
        StateFile.close()
        await SendWait(ctx, "Bot Invisible (Down)")

    @commands.command(name="makeup")
    @commands.check(ChDev)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def MakeBotOn(self, ctx):
        await self.DClient.change_presence(
            status=discord.Status.online,
            activity=discord.Game(f"zhelp || {random.choice(Doing)}"),
        )
        StateFile = open("OpenState.txt", "w+")
        StateFile.write("Up")
        StateFile.close()
        await SendWait(ctx, "Bot Visible (Up)")

    @commands.command(name="numapod")
    @commands.check(ChDev)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def GetAPODNum(self, ctx):
        await SendWait(ctx, f'{AQd.count_documents({"Type":"APOD"})} in APOD Daily')

    @commands.command(name="numqotd")
    @commands.check(ChDev)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def GetQOTDNum(self, ctx):
        await SendWait(ctx, f'{AQd.count_documents({"Type":"QOTD"})} in QOTD Daily')

    @commands.command(name="numcptd")
    @commands.check(ChDev)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def GetCPTDNum(self, ctx):
        await SendWait(ctx, f'{AQd.count_documents({"Type":"CPTD"})} in CPTD Daily')


def setup(DClient):
    DClient.add_cog(OnlyMods(DClient))