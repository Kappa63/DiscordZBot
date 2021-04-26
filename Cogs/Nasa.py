import discord
import random
import requests
from discord.ext import commands
from Setup import ChVote, ChVoteUser, ChPatreonT2, ChAdmin, FormatTime, TimeTillMidnight, GetPatreonTier, SendWait, ErrorEmbeds, Navigator, AQd
import asyncio


class Nasa(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.command(name="apod")
    @commands.check(ChVote)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def GetNasaApod(self, ctx):
        NASAapod = requests.get("https://api.nasa.gov/planetary/apod?api_key=0dsw3SiQmYCeNnwKZROSQIyrcZqjoDzMBo4ggCwS", headers={"Accept": "application/json"}).json()
        Explanation = NASAapod["explanation"][:1021]
        DEm = discord.Embed(title=NASAapod["title"], description=f'Date {NASAapod["date"]}', color=0xA9775A)
        DEm.add_field(name="Explanation:", value=Explanation, inline=False)
        if "hdurl" in NASAapod: DEm.set_image(url=NASAapod["hdurl"])
        else: DEm.add_field(name="\u200b", value=f'[Video Url]({NASAapod["url"]})', inline=False)
        if "copyright" in NASAapod: DEm.set_footer(text=f'Copyright: {NASAapod["copyright"]}')
        await ctx.message.channel.send(embed=DEm)

    @commands.group(name="apoddaily", invoke_without_command=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def NasaApodDAILY(self, ctx):
        TimeLeft = FormatTime(TimeTillMidnight())
        await SendWait(ctx, f'The next Daily APOD is in {TimeLeft}.\n You can be added to APOD Daily with "zapoddaily start" (If donator tier 2+).\n Check "zhelp apod" for more info')

    @NasaApodDAILY.command(name="start")
    @commands.check(ChPatreonT2)
    @commands.check(ChAdmin)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def StartNasaApodDAILY(self, ctx):
        TierApplicable = {"Tier 2 Super": 1, "Tier 3 Legend": 2, "Tier 4 Ultimate": 4}
        TierLimit = TierApplicable[GetPatreonTier(ctx.author.id)]
        if AQd.count_documents({"Type": "APOD", "IDd": ctx.author.id}) >= TierLimit:
            await SendWait(ctx, "You already added the max amount of channels to APOD daily.\nDifferent donator levels get more channels\nCheck 'zpatreon'")
            return
        UserToCheckAdd = {"Type": "APOD", "IDd": ctx.author.id, "IDg": ctx.guild.id, "Channel": ctx.message.channel.id}
        if AQd.count_documents(UserToCheckAdd): await SendWait(ctx, "This channel is already added to APOD daily"); return
        AQd.insert_one(UserToCheckAdd)
        await SendWait(ctx, "Added to APOD daily successfully")

    @NasaApodDAILY.command(aliases=["stop", "end"])
    @commands.check(ChPatreonT2)
    @commands.check(ChAdmin)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RemoveNasaApodDAILY(self, ctx):
        UserToCheckRemove = {"Type": "APOD", "IDd": ctx.author.id, "IDg": ctx.guild.id, "Channel": ctx.message.channel.id}
        if AQd.count_documents(UserToCheckRemove):
            User = AQd.find(UserToCheckRemove)[0]
            AQd.delete_one(User)
            await SendWait(ctx, "Removed from APOD daily successfully")
            return
        await SendWait(ctx, "You are already not in APOD daily")

    @commands.command(name="nasa")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def GetNasaMars(self, ctx):
        def MakeEmbed(MarsImage, ImageNum, Total):
            NEm = discord.Embed(title="Mars", description="By: Curiosity Rover (NASA)", color=0xCD5D2E)
            NEm.set_thumbnail(url="https://i.imgur.com/xmSmG0f.jpeg")
            NEm.add_field(name="Camera:", value=MarsImage["camera"]["full_name"], inline=True)
            NEm.add_field(name="Taken on:", value=MarsImage["earth_date"], inline=True)
            NEm.add_field(name=f"`Image: {ImageNum+1}/{Total}`", value="\u200b", inline=False)
            NEm.set_image(url=MarsImage["img_src"])
            NEm.set_footer(text="Need help navigating? zhelp navigation")
            return NEm
        NASAmars = requests.get("https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key=0dsw3SiQmYCeNnwKZROSQIyrcZqjoDzMBo4ggCwS", headers={"Accept": "application/json"}).json()
        MarsImages = random.sample(NASAmars["photos"], k=25)
        Images = [MakeEmbed(i, v, len(MarsImages)) for v, i in enumerate(MarsImages)]
        await Navigator(ctx, Images)

def setup(DClient):
    DClient.add_cog(Nasa(DClient))