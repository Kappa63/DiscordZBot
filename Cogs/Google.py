import discord
from discord.ext import commands
from Setup import SendWait
import requests
from discord import app_commands
from CBot import DClient as CBotDClient
# import asyncio
from Customs.Navigators import ReactionNavigator as Navigator
# from googlesearch import search
from bs4 import BeautifulSoup
import re
# import numpy as np

class Google(commands.Cog):
    def __init__(self, DClient:CBotDClient) -> None:
        self.DClient = DClient

    # @commands.command(name="google")
    # @commands.cooldown(1, 2, commands.BucketType.user)
    # async def GoogleThat(self, ctx, *args):
    #     if not args: await SendWait(ctx, "No search argument :woozy_face:"); return
    #     await SendWait(ctx, ":desktop: Getting Results...")

    #     SearchResults = []
    #     ResultNum = 1
    #     ResultTotal = 20
    #     Colors = [0x4285F4, 0xEA4335, 0xFBBC05, 0x34A853] * 5
    #     for Result in search(" ".join(args), tld="com", num=20, pause=2, stop=20):
    #         IEm = discord.Embed(title=f'Google Results for **`{" ".join(args)}`**', description=f"Result: [{ResultNum}/{ResultTotal}]", color=Colors.pop(0))
    #         SearchResults.append((IEm, Result))
    #         ResultNum += 1
    #     ResultNum = 0
    #     EmbededResults = [i[0] for i in SearchResults]
    #     URLResults = [i[1] for i in SearchResults]
    #     await Navigator(ctx, EmbededResults, Type="No #", EmbedAndContent=True, ContItems=URLResults)
 
    # @commands.command(name="googleimagesearch", aliases=["gis", "imagesearch"], description="Look for an Image Relating to the Search.")
    # @app_commands.rename(srch="search")
    # @app_commands.describe(srch="Google Search Term")
    # @commands.cooldown(1, 5, commands.BucketType.user)
    # async def ImageSearching(self, ctx:commands.Context, *, srch:str) -> None:
    #     if not srch: await SendWait(ctx, "No search argument :woozy_face:"); return
    #     await SendWait(ctx, ":camera_with_flash: Looking for Images...")
    #     RefreshGISClient()
    #     GiClient.search(search_params={"q": srch, "num": 20, "safeundefined": "high"})
    #     ImageResults = []
    #     ImageNum = 1
    #     ImageTotal = 20
    #     Colors = [0x4285F4, 0xEA4335, 0xFBBC05, 0x34A853] * 5
    #     for Image in GiClient.results():
    #         IEm = discord.Embed(title=f'Google Image Results for **`{srch}`**', description=f"Image: [{ImageNum}/{ImageTotal}]", color=Colors.pop(0))
    #         IEm.set_image(url=Image.url)
    #         ImageResults.append(IEm)
    #         ImageNum += 1
    #     if not ImageResults: await SendWait(ctx, "No Images Found..."); return
    #     await Navigator(ctx, ImageResults, Type="No #").autoRun()

    @commands.hybrid_command(name="weather", description="Find Weather Data in Places.")
    @app_commands.describe(place="Place to Check Weather")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def GetTemp(self, ctx:commands.Context, *, place:str) -> None:
        if not place: await SendWait(ctx, "No search argument :woozy_face:"); return
        await SendWait(ctx, ":white_sun_small_cloud: Getting Weather...")
        RWeather = requests.get(f'https://google.com/search?q=weather+in+{place.replace(" ", "+")}')
        try:
            Soup = BeautifulSoup(RWeather.content, "html.parser")
            Temp = Soup.find("div", class_="BNeawe iBp4i AP7Wnd").text
            Weather = Soup.find("div", class_="BNeawe tAd8D AP7Wnd").text
            Weather = Weather.split("\n")
            Time = Weather[0]
            Atmosphere = Weather[1]
            TempCelsius = (str(int((int(re.findall("-?\d+", Temp)[0]) - 32) * 5 / 9)) + "°C")
            WEm = discord.Embed(title=f'Weather in **`{place}`**')
            WEm.add_field(name="Atmosphere:", value=f"**`{Atmosphere}`**", inline=False)
            WEm.add_field(name="Time:", value=f"**`{Time}`**", inline=False)
            WEm.add_field(name="Temperature:", value=f"**`{Temp} // {TempCelsius}`**", inline=False)
        except AttributeError: await SendWait(ctx, "Failed... :woozy_face:"); return
        await ctx.send(embed=WEm)

    async def cog_load(self) -> None:
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self) -> None:
        print(f"{self.__class__.__name__} unloaded!")


async def setup(DClient:CBotDClient) -> None:
    await DClient.add_cog(Google(DClient))