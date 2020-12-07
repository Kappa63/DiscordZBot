import discord
from discord.ext import commands
from CBot import Ignore
from CBot import ChAdMo

class OnlyMods(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.command(name = "checkzbot")
    @commands.check(ChAdMo)
    async def BotSttSF(self, ctx):
        SEm = discord.Embed(title = "Current ZBot Status", color = 0x000000)
        SEm.add_field(name = "Guilds in: ", value = len(self.DClient.guilds), inline = False)
        SEm.add_field(name = "Latency: ", value = self.DClient.latency * 100, inline = False)
        SEm.add_field(name = "ShardCount: ", value = self.DClient.shard_count, inline = False)
        await ctx.message.channel.send(embed = SEm)

    @commands.command(name = "makedown")
    @commands.check(ChAdMo)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def DfManiT(self, ctx):
        global BoDowNFn
        await self.DClient.change_presence(status = discord.Status.invisible)
        BoDowNFn = True
        await ctx.message.channel.send("Bot Invisible (Down)")

    @commands.command(name = "makeup")
    @commands.check(ChAdMo)
    @commands.cooldown(1, 1, commands.BucketType.user)
        async def UfManiT(self, ctx):
        global BoDowNFn
        await self.DClient.change_presence(status = discord.Status.online, activity = discord.Game(random.choice(Doing)))
        BoDowNFn = False
        await ctx.message.channel.send("Bot Visible (Up)")

def setup(DClient):
    DClient.add_cog(OnlyMods(DClient))