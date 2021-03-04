import discord
from discord.ext import commands
from Setup import GiClient
from Setup import SendWait
import requests
import asyncio
from googlesearch import search
from bs4 import BeautifulSoup
import re


class Google(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.command(name="google")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def GoogleThat(self, ctx, *args):
        if not args:
            await SendWait(ctx, "No search argument :woozy_face:")
            return
        await SendWait(ctx, ":desktop: Getting Results...")

        def ChCHEm(RcM, RuS):
            return (
                RuS.bot == False
                and RcM.message == ResURL
                and str(RcM.emoji) in ["⬅️", "❌", "➡️"]
            )

        SearchResults = []
        ResultNum = 1
        ResultTotal = 20
        Colors = [0x4285F4, 0xEA4335, 0xFBBC05, 0x34A853] * 5
        for Result in search(" ".join(args), tld="com", num=20, pause=2, stop=20):
            IEm = discord.Embed(
                title=f'Google Results for **`{" ".join(args)}`**',
                description=f"Result: [{ResultNum}/{ResultTotal}]",
                color=Colors.pop(0),
            )
            SearchResults.append((IEm, Result))
            ResultNum += 1
        ResultNum = 0
        ResEmbed = await ctx.message.channel.send(embed=SearchResults[ResultNum][0])
        ResURL = await ctx.message.channel.send(content=SearchResults[ResultNum][1])
        await ResURL.add_reaction("⬅️")
        await ResURL.add_reaction("❌")
        await ResURL.add_reaction("➡️")
        while True:
            try:
                Res = await self.DClient.wait_for(
                    "reaction_add", check=ChCHEm, timeout=120
                )
                await ResURL.remove_reaction(Res[0].emoji, Res[1])
                if Res[0].emoji == "⬅️" and ResultNum != 0:
                    ResultNum -= 1
                    await ResEmbed.edit(embed=SearchResults[ResultNum][0])
                    await ResURL.edit(content=SearchResults[ResultNum][1])
                elif Res[0].emoji == "➡️":
                    if ResultNum < ResultTotal - 1:
                        ResultNum += 1
                        await ResEmbed.edit(embed=SearchResults[ResultNum][0])
                        await ResURL.edit(content=SearchResults[ResultNum][1])
                    else:
                        await ResEmbed.edit(embed=SearchResults[ResultNum][0])
                        await ResURL.edit(content=SearchResults[ResultNum][1])
                        await ResURL.remove_reaction("⬅️", self.DClient.user)
                        await ResURL.remove_reaction("❌", self.DClient.user)
                        await ResURL.remove_reaction("➡️", self.DClient.user)
                        break
                elif Res[0].emoji == "❌":
                    await ResEmbed.edit(embed=SearchResults[ResultNum][0])
                    await ResURL.edit(content=SearchResults[ResultNum][1])
                    await ResURL.remove_reaction("⬅️", self.DClient.user)
                    await ResURL.remove_reaction("❌", self.DClient.user)
                    await ResURL.remove_reaction("➡️", self.DClient.user)
                    break
            except asyncio.TimeoutError:
                await ResEmbed.edit(embed=SearchResults[ResultNum][0])
                await ResURL.edit(content=SearchResults[ResultNum][1])
                await ResURL.remove_reaction("⬅️", self.DClient.user)
                await ResURL.remove_reaction("❌", self.DClient.user)
                await ResURL.remove_reaction("➡️", self.DClient.user)
                break

    @commands.command(aliases=["gis", "googleimagesearch", "imagesearch"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ImageSearching(self, ctx, *args):
        if not args:
            await SendWait(ctx, "No search argument :woozy_face:")
            return
        await SendWait(ctx, ":camera_with_flash: Looking for Images...")

        def ChCHEm(RcM, RuS):
            return (
                RuS.bot == False
                and RcM.message == Imager
                and str(RcM.emoji) in ["⬅️", "❌", "➡️"]
            )

        GiClient.search(
            search_params={"q": " ".join(args), "num": 20, "safeundefined": "high"}
        )
        ImageResults = []
        ImageNum = 1
        ImageTotal = 20
        Colors = [0x4285F4, 0xEA4335, 0xFBBC05, 0x34A853] * 5
        for Image in GiClient.results():
            IEm = discord.Embed(
                title=f'Google Image Results for **`{" ".join(args)}`**',
                description=f"Image: [{ImageNum}/{ImageTotal}]",
                color=Colors.pop(0),
            )
            IEm.set_image(url=Image.url)
            ImageResults.append(IEm)
            ImageNum += 1
        ImageNum = 0
        Imager = await ctx.message.channel.send(embed=ImageResults[ImageNum])
        await Imager.add_reaction("⬅️")
        await Imager.add_reaction("❌")
        await Imager.add_reaction("➡️")
        while True:
            try:
                Res = await self.DClient.wait_for(
                    "reaction_add", check=ChCHEm, timeout=120
                )
                await Imager.remove_reaction(Res[0].emoji, Res[1])
                if Res[0].emoji == "⬅️" and ImageNum != 0:
                    ImageNum -= 1
                    await Imager.edit(embed=ImageResults[ImageNum])
                elif Res[0].emoji == "➡️":
                    if ImageNum < ImageTotal - 1:
                        ImageNum += 1
                        await Imager.edit(embed=ImageResults[ImageNum])
                    else:
                        await Imager.edit(embed=ImageResults[ImageNum])
                        await Imager.remove_reaction("⬅️", self.DClient.user)
                        await Imager.remove_reaction("❌", self.DClient.user)
                        await Imager.remove_reaction("➡️", self.DClient.user)
                        break
                elif Res[0].emoji == "❌":
                    await Imager.edit(embed=ImageResults[ImageNum])
                    await Imager.remove_reaction("⬅️", self.DClient.user)
                    await Imager.remove_reaction("❌", self.DClient.user)
                    await Imager.remove_reaction("➡️", self.DClient.user)
                    break
            except asyncio.TimeoutError:
                await Imager.edit(embed=ImageResults[ImageNum])
                await Imager.remove_reaction("⬅️", self.DClient.user)
                await Imager.remove_reaction("❌", self.DClient.user)
                await Imager.remove_reaction("➡️", self.DClient.user)
                break

    @commands.command(name="weather")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def GetTemp(self, ctx, *args):
        if not args:
            await SendWait(ctx, "No search argument :woozy_face:")
            return
        await SendWait(ctx, ":white_sun_small_cloud: Getting Weather...")
        RWeather = requests.get(
            f'https://google.com/search?q=weather+in+{" ".join(args)}'
        )
        try:
            Soup = BeautifulSoup(RWeather.content, "html.parser")
            Temp = Soup.find("div", class_="BNeawe iBp4i AP7Wnd").text
            Weather = Soup.find("div", class_="BNeawe tAd8D AP7Wnd").text
            Weather = Weather.split("\n")
            Time = Weather[0]
            Atmosphere = Weather[1]
            TempCelsius = (
                str(int((int(re.findall("-?\d+", Temp)[0]) - 32) * 5 / 9)) + "°C"
            )
            WEm = discord.Embed(title=f'Weather in **`{" ".join(args)}`**')
            WEm.add_field(name="Atmosphere:", value=f"**`{Atmosphere}`**", inline=False)
            WEm.add_field(name="Time:", value=f"**`{Time}`**", inline=False)
            WEm.add_field(
                name="Temperature:",
                value=f"**`{Temp} // {TempCelsius}`**",
                inline=False,
            )
        except AttributeError:
            await SendWait(ctx, "Failed... :woozy_face:")
            return
        await ctx.message.channel.send(embed=WEm)


def setup(DClient):
    DClient.add_cog(Google(DClient))