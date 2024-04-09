import discord
from discord import app_commands
from discord.ext import commands
import random
import cv2
import numpy
import requests
import os
# from Setup import GClient, GApi, SendWait
import pyimgbox


class Randomizers(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.hybrid_command(name="roll", description="Roll a Dice.")
    async def RollTheDice(self, ctx):
        # print("ANAL")
        DiceFaces = {1: "https://i.imgur.com/A3winYh.png", 2: "https://i.imgur.com/JFuawqi.png",
                     3: "https://i.imgur.com/2tufStP.png", 4: "https://i.imgur.com/GdtEPw4.png",
                     5: "https://i.imgur.com/7hgCUOq.png", 6: "https://i.imgur.com/5iyDeF1.png"}
        DiceRolls = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six"}
        FaceNumber = random.randint(1, 6)
        DEm = discord.Embed(title="Dice Roll", description=f"**The Dice Rolled a:** *{FaceNumber} ({DiceRolls[FaceNumber]})*", color=0xFAC62D)
        DEm.set_thumbnail(url=DiceFaces[FaceNumber])
        await ctx.send(embed=DEm)

    @commands.hybrid_command(name = "coinflip", aliases=["cf"], description="Flip a Coin.")
    async def FlipTheCoin(self, ctx):
        CoinFaces = {"Heads": "https://i.imgur.com/U6BxOan.png",
                     "Tails": "https://i.imgur.com/zWvC1Ao.png"}
        Face = random.choice(list(CoinFaces.keys()))
        CEm = discord.Embed(title="Coin Flip", description=f"**The Coin Landed on:** *{Face}*", color=0xFAC62D)
        CEm.set_thumbnail(url=CoinFaces[Face])
        await ctx.send(embed=CEm)

    # @commands.cooldown(1, 1, commands.BucketType.user)

    @commands.hybrid_command(name="color", aliases=["colour"], description="Generates a Random Color.")
    async def ColorRandom(self, ctx):
        MakeClear = numpy.zeros((360, 360, 3), numpy.uint8)
        R = random.randint(0, 255)
        G = random.randint(0, 255)
        B = random.randint(0, 255)
        MakeClear[:, 0:360] = (B, G, R)
        RGBtoHEX = "%02x%02x%02x" % (R, G, B)
        cv2.imwrite("Color.png", MakeClear)
        ClrImg = discord.File("Color.png")
        # PEm.set_image(url="attachment://Color.png")
        # await ctx.send(file=TpdeImg, embed=PEm)
        # async with pyimgbox.Gallery(title="The Color") as gallery: Img = await gallery.upload("Color.png")
        # ColoredImage = Img["image_url"]
        ColorObject = discord.Color(value=int(RGBtoHEX, 16))
        CEm = discord.Embed(title="Color", description=f"```-Hex: #{RGBtoHEX}\n-RGB: ({R},{G},{B})```", color=ColorObject)
        CEm.set_thumbnail(url="attachment://Color.png")
        await ctx.send(file=ClrImg, embed=CEm)
        os.remove("Color.png")

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded!")

    # @commands.command(name="giphy")
    # @commands.cooldown(1, 1, commands.BucketType.user)
    # async def RandomGif(self, ctx, *args):
    #     if not args: await SendWait(ctx, "No search term given :confused:"); return
    #     try:
    #         QRGifs = GApi.gifs_search_get(GClient, " ".join(args), limit=50)
    #         GifSAl = list(QRGifs.data)
    #         GifF = random.choices(GifSAl)
    #         await ctx.send(GifF[0].url)
    #     except IndexError: await SendWait(ctx, "No gifs found :expressionless:")


async def setup(DClient):
    await DClient.add_cog(Randomizers(DClient))