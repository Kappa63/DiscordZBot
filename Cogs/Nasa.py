import discord
import random
import requests
from discord.ext import commands
from Setup import ChVote, ChVoteUser, ChPatreonT2, ChAdmin
from Setup import FormatTime, TimeTillMidnight, GetPatreonTier
from Setup import ErrorEmbeds
import asyncio


class Nasa(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.command(name="apod")
    @commands.check(ChVote)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def GetNasaApod(self, ctx):
        NASAapod = requests.get(
            "https://api.nasa.gov/planetary/apod?api_key=0dsw3SiQmYCeNnwKZROSQIyrcZqjoDzMBo4ggCwS",
            headers={"Accept": "application/json"},
        )
        JSONapod = NASAapod.json()
        if len(JSONapod["explanation"]) > 1021:
            Explanation = JSONapod["explanation"][0:1021]
            Explanation = Explanation + "..."
        else:
            Explanation = JSONapod["explanation"]
        DEm = discord.Embed(
            title=JSONapod["title"],
            description=f'Date {JSONapod["date"]}',
            color=0xA9775A,
        )
        DEm.add_field(name="Explanation:", value=Explanation, inline=False)
        try:
            DEm.set_image(url=JSONapod["hdurl"])
        except KeyError:
            DEm.add_field(
                name="\u200b", value=f'[Video Url]({JSONapod["url"]})', inline=False
            )
        try:
            DEm.set_footer(text=f'Copyright: {JSONapod["copyright"]}')
        except KeyError:
            pass
        await ctx.message.channel.send(embed=DEm)

    @commands.group(name="apoddaily", invoke_without_command=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def NasaApodDAILY(self, ctx):
        TimeLeft = FormatTime(TimeTillMidnight())
        await ctx.message.channel.send(
            embed=discord.Embed(
                title="APOD in...",
                description=f'The next Daily APOD is in {TimeLeft}.\n You can be added to APOD Daily with "zapoddaily start" (If patreon tier 2+).\n Check "zhelp apod" for more info',
            )
        )

    @NasaApodDAILY.command(name="start")
    @commands.check(ChPatreonT2)
    @commands.check(ChAdmin)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def StartNasaApodDAILY(self, ctx):
        TierApplicable = {"Tier 2 Super": 1, "Tier 3 Legend": 2, "Tier 4 Ultimate": 4}
        LineToCheckAdd = f"{ctx.author.id} {ctx.message.channel.id} {ctx.guild.id} \n"
        UserID = f"{ctx.author.id}"
        OpenAPODChannelUserFile = open("APODDaily.txt")
        APODChannelUserFile = OpenAPODChannelUserFile.readlines()
        OpenAPODChannelUserFile.close()
        TierLimit = TierApplicable[GetPatreonTier(ctx.author.id)]
        for Line in APODChannelUserFile:
            if Line == LineToCheckAdd:
                await ctx.message.channel.send(
                    embed=discord.Embed(
                        title="All Good",
                        description="This channel is already added to APOD daily",
                    )
                )
                return
        Channels = 0
        for Line in APODChannelUserFile:
            if Line.split(" ")[0] == UserID:
                Channels += 1
                if Channels == TierLimit:
                    await ctx.message.channel.send(
                        embed=discord.Embed(
                            title="Oops",
                            description="You already added the max amount of channels to APOD daily.\nDifferent patreon levels get more channels\nCheck 'zpatreon'",
                        )
                    )
                    return
        AppendAPODChannelUserFile = open("APODDaily.txt", "a")
        AppendAPODChannelUserFile.write(
            f"{ctx.author.id} {ctx.message.channel.id} {ctx.guild.id} \n"
        )
        AppendAPODChannelUserFile.close()
        await ctx.message.channel.send(
            embed=discord.Embed(
                title="Success", description="Added to APOD daily successfully"
            )
        )
        Upload = requests.post(
            url="https://file.io", files={"file": open("APODDaily.txt")}
        ).json()
        Channel = self.DClient.get_channel(794268659177488464)
        await Channel.send(
            embed=discord.Embed(
                title=f'APOD Upload Success: {Upload["success"]}',
                description=f'Key: {Upload["key"]}\n\nExpiry: {Upload["expiry"]}\n\nHard Link: {Upload["link"]}',
                url=Upload["link"],
                color=0x000000,
            )
        )

    @NasaApodDAILY.command(aliases=["stop","end"])
    @commands.check(ChPatreonT2)
    @commands.check(ChAdmin)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RemoveNasaApodDAILY(self, ctx):
        LineToCheckAdd = f"{ctx.author.id} {ctx.message.channel.id} {ctx.guild.id} \n"
        OpenAPODChannelUserFile = open("APODDaily.txt")
        APODChannelUserFile = OpenAPODChannelUserFile.readlines()
        OpenAPODChannelUserFile.close()
        LineNum = 0
        Exist = False
        for Line in APODChannelUserFile:
            if Line == LineToCheckAdd:
                del APODChannelUserFile[LineNum]
                Exist = True
                break
            LineNum += 1
        if Exist:
            FixAPODChannelUserFile = open("APODDaily.txt", "w+")
            for Line in APODChannelUserFile:
                FixAPODChannelUserFile.write(Line)
            FixAPODChannelUserFile.close()
            await ctx.message.channel.send(
                embed=discord.Embed(
                    title="Success", description="Removed from APOD daily successfully"
                )
            )
            return
        await ctx.message.channel.send(
            embed=discord.Embed(
                title="All Good", description="You are not in APOD daily"
            )
        )
        Upload = requests.post(
            url="https://file.io", files={"file": open("APODDaily.txt")}
        ).json()
        Channel = self.DClient.get_channel(794268659177488464)
        await Channel.send(
            embed=discord.Embed(
                title=f'APOD Upload Success: {Upload["success"]}',
                description=f'Key: {Upload["key"]}\n\nExpiry: {Upload["expiry"]}\n\nHard Link: {Upload["link"]}',
                url=Upload["link"],
                color=0x000000,
            )
        )

    @commands.command(name="nasa")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def GetNasaMars(self, ctx):
        def MakeEmbed(MarsImagesCH, ImageNum, ImagesExtracted):
            NEm = discord.Embed(
                title="Mars", description="By: Curiosity Rover (NASA)", color=0xCD5D2E
            )
            NEm.set_thumbnail(url="https://i.imgur.com/xmSmG0f.jpeg")
            NEm.add_field(
                name="Camera:",
                value=MarsImagesCH[ImageNum]["camera"]["full_name"],
                inline=True,
            )
            NEm.add_field(
                name="Taken on:",
                value=MarsImagesCH[ImageNum]["earth_date"],
                inline=True,
            )
            NEm.add_field(
                name=f"`Image: {ImageNum+1}/{ImagesExtracted}`",
                value="\u200b",
                inline=False,
            )
            NEm.set_image(url=MarsImagesCH[ImageNum]["img_src"])
            NEm.set_footer(text="Need help navigating? zhelp navigation")
            return NEm

        def ChCHEm(RcM, RuS):
            return (
                RuS.bot == False
                and RcM.message == NTEm
                and str(RcM.emoji) in ["⬅️", "❌", "➡️", "#️⃣"]
            )

        def ChCHEmFN(MSg):
            MesS = MSg.content.lower()
            RsT = False
            try:
                if int(MSg.content):
                    RsT = True
            except ValueError:
                if (MesS == "cancel") or (MesS == "c"):
                    RsT = True
            return (
                MSg.guild.id == ctx.guild.id
                and MSg.channel.id == ctx.channel.id
                and RsT
            )

        NASAmars = requests.get(
            "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key=0dsw3SiQmYCeNnwKZROSQIyrcZqjoDzMBo4ggCwS",
            headers={"Accept": "application/json"},
        )
        JSONmars = NASAmars.json()
        MarsImagesCH = random.sample(JSONmars["photos"], k=25)
        ImagesExtracted = len(MarsImagesCH)
        ImageNum = 0
        NTEm = await ctx.message.channel.send(
            embed=MakeEmbed(MarsImagesCH, ImageNum, ImagesExtracted)
        )
        await NTEm.add_reaction("⬅️")
        await NTEm.add_reaction("❌")
        await NTEm.add_reaction("➡️")
        await NTEm.add_reaction("#️⃣")
        while True:
            try:
                Res = await self.DClient.wait_for(
                    "reaction_add", check=ChCHEm, timeout=120
                )
                await NTEm.remove_reaction(Res[0].emoji, Res[1])
                if Res[0].emoji == "⬅️" and ImageNum != 0:
                    ImageNum -= 1
                    await NTEm.edit(
                        embed=MakeEmbed(MarsImagesCH, ImageNum, ImagesExtracted)
                    )
                elif Res[0].emoji == "➡️":
                    if ImageNum < ImagesExtracted - 1:
                        ImageNum += 1
                        await NTEm.edit(
                            embed=MakeEmbed(MarsImagesCH, ImageNum, ImagesExtracted)
                        )
                    else:
                        await NTEm.edit(
                            embed=MakeEmbed(MarsImagesCH, ImageNum, ImagesExtracted)
                        )
                        await NTEm.remove_reaction("⬅️", self.DClient.user)
                        await NTEm.remove_reaction("❌", self.DClient.user)
                        await NTEm.remove_reaction("➡️", self.DClient.user)
                        await NTEm.remove_reaction("#️⃣", self.DClient.user)
                        break
                elif Res[0].emoji == "#️⃣":
                    if await ChVoteUser(Res[1].id):
                        TemTw = await ctx.message.channel.send(
                            'Choose a number to open navigate to page. "c" or "cancel" to exit navigation.\n\n*The Navigation closes automatically after 10sec of inactivity.*'
                        )
                        try:
                            ResE = await self.DClient.wait_for(
                                "message", check=ChCHEmFN, timeout=10
                            )
                            await TemTw.delete()
                            await ResE.delete()
                            try:
                                try:
                                    pG = int(ResE.content)
                                    if 0 < pG <= ImagesExtracted - 1:
                                        ImageNum = pG - 1
                                    elif pG < 1:
                                        ImageNum = 0
                                        pass
                                    else:
                                        ImageNum = ImagesExtracted - 1
                                except TypeError:
                                    pass
                            except ValueError:
                                pass
                            await NTEm.edit(
                                embed=MakeEmbed(MarsImagesCH, ImageNum, ImagesExtracted)
                            )
                        except asyncio.exceptions.TimeoutError:
                            await TemTw.edit("Request Timeout")
                            await asyncio.sleep(5)
                            await TemTw.delete()
                    else:
                        await ctx.message.channel.send(embed=ErrorEmbeds("Vote"))
                elif Res[0].emoji == "❌":
                    await NTEm.edit(
                        embed=MakeEmbed(MarsImagesCH, ImageNum, ImagesExtracted)
                    )
                    await NTEm.remove_reaction("⬅️", self.DClient.user)
                    await NTEm.remove_reaction("❌", self.DClient.user)
                    await NTEm.remove_reaction("➡️", self.DClient.user)
                    await NTEm.remove_reaction("#️⃣", self.DClient.user)
                    break
            except asyncio.TimeoutError:
                await NTEm.edit(
                    embed=MakeEmbed(MarsImagesCH, ImageNum, ImagesExtracted)
                )
                await NTEm.remove_reaction("⬅️", self.DClient.user)
                await NTEm.remove_reaction("❌", self.DClient.user)
                await NTEm.remove_reaction("➡️", self.DClient.user)
                await NTEm.remove_reaction("#️⃣", self.DClient.user)
                break


def setup(DClient):
    DClient.add_cog(Nasa(DClient))