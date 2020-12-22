import discord
from discord.ext import commands
import requests

class Image(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.command(aliases=["kitten","kitty","cat"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RandomCat(self, ctx):
        CatGot = requests.get(
            "https://aws.random.cat/meow", headers={"Accept": "application/json"}
        )
        CatJSON = CatGot.json()
        CEm = discord.Embed(title="Meow", color=0xA3D7C1)
        CEm.set_image(url=CatJSON["file"])
        await ctx.message.channel.send(embed=CEm)

    @commands.command(aliases=["doggo","dog","pupper","puppy"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RandomDoggo(self, ctx):
        DoggoGot = requests.get(
            "https://random.dog/woof.json", headers={"Accept": "application/json"}
        )
        DoggoJSON = DoggoGot.json()
        DEm = discord.Embed(title="Woof Woof", color=0xFF3326)
        DEm.set_image(url=DoggoJSON["url"])
        await ctx.message.channel.send(embed=DEm)

    @commands.command(name="fox")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RandomFox(self, ctx):
        FoxGot = requests.get(
            "https://randomfox.ca/floof/", headers={"Accept": "application/json"}
        )
        FoxJSON = FoxGot.json()
        FEm = discord.Embed(title="What does the fox say?", color=0x9DAA45)
        FEm.set_image(url=FoxJSON["image"])
        await ctx.message.channel.send(embed=FEm)

    @commands.command(aliases=["food","dishes","dish"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RandomDishes(self, ctx):
        Hungry = requests.get("https://foodish-api.herokuapp.com/api/", headers = {"Accept": "application/json"}).json()
        FEm = discord.Embed(title="Hungry?", color=0xA3D7C1)
        FEm.set_image(url=Hungry["image"])
        await ctx.message.channel.send(embed=FEm)

def setup(DClient):
    DClient.add_cog(Image(DClient))