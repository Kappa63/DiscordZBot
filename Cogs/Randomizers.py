import discord
from discord.ext import commands
import random
import randfacts
import cv2
import numpy
import requests
import os
from Setup import GClient, GApi, Imgur
from Setup import ChVote


class Randomizers(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.command(name="advice")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RandomAdvice(self, ctx):
        Advice = requests.get("https://api.adviceslip.com/advice", headers = {"Accept": "application/json"}).json()
        await ctx.message.channel.send(
            embed=discord.Embed(title="Some Advice", description = Advice["slip"]["advice"], color=0x7dd7d8)
        )

    @commands.command(name="kanye")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ShitByKanye(self, ctx):
        KanyeSays = requests.get("https://api.kanye.rest", headers = {"Accept": "application/json"}).json()
        await ctx.message.channel.send(
            embed=discord.Embed(title="Kanye Says Alot, Here's One", description = KanyeSays["quote"], color=0x53099b)
        )

    @commands.command(name="qotd")
    @commands.check(ChVote)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def QuoteOfTheDay(self, ctx):
        TodayQuote = requests.get("https://favqs.com/api/qotd", headers = {"Accept": "application/json"}).json()
        QEm = discord.Embed(title="Quote Of The Day", description = TodayQuote["quote"]["body"], color=0x8d42ee)
        QEm.set_footer(text=f'By: {TodayQuote["quote"]["author"]}')
        await ctx.message.channel.send(embed=QEm)
    
    @commands.command(name="insult")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RandomInsult(self, ctx):
        InsultGot = requests.get(
            "https://evilinsult.com/generate_insult.php?lang=en&type=json",
            headers={"Accept": "application/json"},
        )
        InsultJSON = InsultGot.json()
        await ctx.message.channel.send(
            embed=discord.Embed(title= "Insult", description = InsultJSON["insult"], color=0xBD2DB8)
        )

    @commands.command(name="roll")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RollTheDice(self, ctx):
        DiceFaces = {
            1: "https://i.imgur.com/A3winYh.png",
            2: "https://i.imgur.com/JFuawqi.png",
            3: "https://i.imgur.com/2tufStP.png",
            4: "https://i.imgur.com/GdtEPw4.png",
            5: "https://i.imgur.com/7hgCUOq.png",
            6: "https://i.imgur.com/5iyDeF1.png",
        }
        DiceRolls = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six"}
        FaceNumber = random.randint(1, 6)
        DEm = discord.Embed(
            title="Dice Roll",
            description=f"**The Dice Rolled a:** *{FaceNumber} ({DiceRolls[FaceNumber]})*",
            color=0xFAC62D,
        )
        DEm.set_thumbnail(url=DiceFaces[FaceNumber])
        await ctx.message.channel.send(embed=DEm)

    @commands.command(name="fact")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def GetAFact(self, ctx):
        await ctx.message.channel.send(
            embed=discord.Embed(
                title="Fact", description=randfacts.getFact(), color=0x1F002A
            )
        )

    @commands.command(aliases=["color", "colour"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ColorRandom(self, ctx):
        MakeClear = numpy.zeros((360, 360, 3), numpy.uint8)
        R = random.randint(0, 255)
        G = random.randint(0, 255)
        B = random.randint(0, 255)
        MakeClear[:, 0:360] = (B, G, R)
        RGBtoHEX = "%02x%02x%02x" % (R, G, B)
        cv2.imwrite("Color.png", MakeClear)
        ColoredImage = Imgur.upload_from_path("Color.png")["link"]
        os.remove("Color.png")
        ColorObject = discord.Color(value=int(RGBtoHEX, 16))
        CEm = discord.Embed(
            title="Color",
            description=f"```-Hex: #{RGBtoHEX}\n-RGB: ({R},{G},{B})```",
            color=ColorObject,
        )
        CEm.set_thumbnail(url=ColoredImage)
        await ctx.message.channel.send(embed=CEm)

    @commands.command(name="giphy")
    async def RandomGif(self, ctx, *args):
        if args:
            try:
                QRGifs = GApi.gifs_search_get(GClient, " ".join(args), limit=50)
                GifSAl = list(QRGifs.data)
                GifF = random.choices(GifSAl)
                await ctx.message.channel.send(GifF[0].url)
            except IndexError:
                await ctx.message.channel.send("No gifs found :expressionless:")
        else:
            await ctx.message.channel.send("No search term given :confused:")

def setup(DClient):
    DClient.add_cog(Randomizers(DClient))