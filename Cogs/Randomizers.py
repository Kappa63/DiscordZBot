import discord
from discord.ext import commands
import random
import randfacts
import cv2
import numpy
import requests
import os
from Setup import GClient, GApi, Imgur


class Randomizers(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.command(name="cat")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RandomCat(self, ctx):
        CatGot = requests.get(
            "https://aws.random.cat/meow", headers={"Accept": "application/json"}
        )
        CatJSON = CatGot.json()
        CEm = discord.Embed(title="Random Cat", color=0xA3D7C1)
        CEm.set_image(url=CatJSON["file"])
        await ctx.message.channel.send(embed=CEm)

    @commands.command(name="dog")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RandomDoggo(self, ctx):
        DoggoGot = requests.get(
            "https://random.dog/woof.json", headers={"Accept": "application/json"}
        )
        DoggoJSON = DoggoGot.json()
        DEm = discord.Embed(title="Random Dog", color=0xFF3326)
        DEm.set_image(url=DoggoJSON["url"])
        await ctx.message.channel.send(embed=DEm)

    @commands.command(name="fox")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RandomFox(self, ctx):
        FoxGot = requests.get(
            "https://randomfox.ca/floof/", headers={"Accept": "application/json"}
        )
        FoxJSON = FoxGot.json()
        FEm = discord.Embed(title="Random Fox", color=0x9DAA45)
        FEm.set_image(url=FoxJSON["image"])
        await ctx.message.channel.send(embed=FEm)

    @commands.command(name="insult")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RandomInsult(self, ctx):
        InsultGot = requests.get(
            "https://evilinsult.com/generate_insult.php?lang=en&type=json",
            headers={"Accept": "application/json"},
        )
        InsultJSON = InsultGot.json()
        await ctx.message.channel.send(
            embed=discord.Embed(title=InsultJSON["insult"], color=0xBD2DB8)
        )

    @commands.command(name="roll")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RollTheDice(self, ctx):
        ChORoDi = {
            1: "https://i.imgur.com/A3winYh.png",
            2: "https://i.imgur.com/JFuawqi.png",
            3: "https://i.imgur.com/2tufStP.png",
            4: "https://i.imgur.com/GdtEPw4.png",
            5: "https://i.imgur.com/7hgCUOq.png",
            6: "https://i.imgur.com/5iyDeF1.png",
        }
        NuToLe = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six"}
        RoDiRe = random.randint(1, 6)
        DEm = discord.Embed(
            title="Dice Roll",
            description=f"**The Dice Rolled a:** *{RoDiRe} ({NuToLe[RoDiRe]})*",
            color=0xFAC62D,
        )
        DEm.set_thumbnail(url=ChORoDi[RoDiRe])
        await ctx.message.channel.send(embed=DEm)

    @commands.command(name="fact")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def GetAFact(self, ctx):
        await ctx.message.channel.send(
            embed=discord.Embed(
                title="Random Fact", description=randfacts.getFact(), color=0x1F002A
            )
        )

    @commands.command(name="dadjoke")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def KillMe(self, ctx):
        rEqAla = requests.get(
            "https://icanhazdadjoke.com/", headers={"Accept": "application/json"}
        )
        TraTOjS = rEqAla.json()
        await ctx.message.channel.send(
            embed=discord.Embed(
                title="Random Dad Joke", description=TraTOjS["joke"], color=0x11D999
            )
        )

    @commands.command(aliases=["color", "colour"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ColorRandom(self, ctx):
        CrMakImG = numpy.zeros((360, 360, 3), numpy.uint8)
        R = random.randint(0, 255)
        G = random.randint(0, 255)
        B = random.randint(0, 255)
        CrMakImG[:, 0:360] = (B, G, R)
        RGhEC = "%02x%02x%02x" % (R, G, B)
        cv2.imwrite("Color.png", CrMakImG)
        LiImCo = Imgur.upload_from_path("Color.png")["link"]
        os.remove("Color.png")
        ColTEm = discord.Color(value=int(RGhEC, 16))
        CEm = discord.Embed(
            title="Random Color",
            description=f"```-Hex: #{RGhEC}\n-RGB: ({R},{G},{B})```",
            color=ColTEm,
        )
        CEm.set_thumbnail(url=LiImCo)
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