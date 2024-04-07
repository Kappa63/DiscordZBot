import discord
from discord.ext import commands
# from Setup import ChVote, ChVoteUser, ChNSFW, SendWait, ErrorEmbeds, Navigator
from Setup import Navigator, SendWait
import asyncio
import random
import rule34

def MakeEmbed(Rule, Total=0, RuleNum = 0, Type="R"):
    Tags = ", ".join(Rule.tags)[0:253]
    REm = discord.Embed(title="Rule34", description=Tags, color=0xDFE31E)
    REm.add_field(name="Score: ", value=Rule.score)
    if Type == "S": REm.add_field(name=f"`Page: {RuleNum+1}/{Total}`", value="\u200b")
    REm.set_image(url=Rule.file_url)
    REm.set_thumbnail(url=Rule.preview_url)
    if Type == "S": REm.set_footer(text=f"{Rule.created_at}\n\nNeed help navigating? zhelp navigation")
    else: REm.set_footer(text=Rule.created_at)
    return REm

class Rule34(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.group(aliases=["rule34", "r34"], invoke_without_command=True)
    async def GetRule34(self, ctx, *args):
        if not args: await SendWait(ctx, "No arguments :no_mouth:"); return
        try:
            Rule34 = rule34.Rule34(asyncio.get_event_loop())
            if ctx.guild.id != 586940644153622550: 
                Rule34Choices = await Rule34.getImages(f'-underage -loli -lolicon -lolita -lolita_channel -shota -shotacon {"_".join(args).lower()}')
            else: Rule34Choices = await Rule34.getImages(f'{"_".join(args).lower()}')
            ShowRule = random.choice(Rule34Choices)
        except TypeError: await SendWait(ctx, "Nothing Found :no_mouth:"); return
        await ctx.message.channel.send(embed=MakeEmbed(ShowRule))

    # @commands.check(ChVote)
    # @commands.check(ChNSFW)
    # @commands.cooldown(1, 1, commands.BucketType.user)
    @GetRule34.command(name="surf")
    async def SurfRule34(self, ctx, *args):
        if not args: await SendWait(ctx, "No arguments :no_mouth:"); return
        try:
            Rule34 = rule34.Rule34(asyncio.get_event_loop())
            if ctx.guild.id != 586940644153622550: 
                Rule34Surf = await Rule34.getImages(f'-underage -loli -lolicon -lolita -lolita_channel -shota -shotacon {"_".join(args).lower()}')
            else: Rule34Surf = await Rule34.getImages(f'{"_".join(args).lower()}')
        except TypeError: await SendWait(ctx, "Nothing Found :no_mouth:"); return
        Rule34Total = len(Rule34Surf)
        Rules = [MakeEmbed(i, Total=Rule34Total, RuleNum=v, Type="S") for v, i in enumerate(Rule34Surf)] 
        await Navigator(ctx, Rules)

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded!")

async def setup(DClient):
    await DClient.add_cog(Rule34(DClient))