import discord
from discord.ext import commands
from Setup import ChDev
import random
import requests

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

    @commands.command(name="makedown")
    @commands.check(ChDev)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def MakeBotOff(self, ctx):
        await self.DClient.change_presence(status=discord.Status.invisible)
        StateFile = open("OpenState.txt", "w+")
        StateFile.write("Down")
        StateFile.close()
        await ctx.message.channel.send("Bot Invisible (Down)")

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
        await ctx.message.channel.send("Bot Visible (Up)")

    @commands.command(name="uploadqotd")
    @commands.check(ChDev)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def GetQOTDFile(self, ctx):
        Upload = requests.post(
            url="https://file.io", files={"file": open("QOTDaily.txt")}
        ).json()
        await ctx.message.channel.send(
            embed=discord.Embed(
                title=f'Success: {Upload["success"]}',
                description=f'Key: {Upload["key"]}\n\nExpiry: {Upload["expiry"]}\n\nHard Link: {Upload["link"]}',
                url=Upload["link"],
                color=0x000000,
            )
        )

    @commands.command(name="uploadapod")
    @commands.check(ChDev)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def GetAPODFile(self, ctx):
        Upload = requests.post(
            url="https://file.io", files={"file": open("APODDaily.txt")}
        ).json()
        await ctx.message.channel.send(
            embed=discord.Embed(
                title=f'Success: {Upload["success"]}',
                description=f'Key: {Upload["key"]}\n\nExpiry: {Upload["expiry"]}\n\nHard Link: {Upload["link"]}',
                url=Upload["link"],
                color=0x000000,
            )
        )


def setup(DClient):
    DClient.add_cog(OnlyMods(DClient))