import discord
from discord.ext import commands
import requests

class Jokes(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.command(name="dadjoke")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def KillMe(self, ctx):
        DadJoke = requests.get(
            "https://icanhazdadjoke.com/", headers={"Accept": "application/json"}
        ).json()
        await ctx.message.channel.send(
            embed=discord.Embed(
                title="Dad Joke", description=DadJoke["joke"], color=0x11D999
            )
        )

    @commands.command(name = "joke")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def Joke(self, ctx):
        Joke = requests.get("https://sv443.net/jokeapi/v2/joke/Programming,Miscellaneous,Spooky,Christmas?blacklistFlags=nsfw,religious,political,racist,sexist", headers = {"Accept": "application/json"}).json()
        if Joke["type"] == "twopart":
            await ctx.message.channel.send(
                embed=discord.Embed(
                    title=f'Joke ({Joke["category"]})', description=f'{Joke["setup"]}\n\n||{Joke["delivery"]}||', color=0x11D999
                )
            )
        else:
            await ctx.message.channel.send(
                embed=discord.Embed(
                    title=f'Joke ({Joke["category"]})', description=Joke["joke"], color=0x11D999
                )
            )

    @commands.command(name = "darkjoke")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def DarkJoke(self, ctx):
        DarkJoke = requests.get("https://sv443.net/jokeapi/v2/joke/Dark", headers = {"Accept": "application/json"}).json()
        if DarkJoke["type"] == "twopart":
            await ctx.message.channel.send(
                embed=discord.Embed(
                    title=f'Joke ({DarkJoke["category"]})', description=f'{DarkJoke["setup"]}\n\n||{DarkJoke["delivery"]}||', color=0x11D999
                )
            )
        else:
            await ctx.message.channel.send(
                embed=discord.Embed(
                    title=f'Joke ({DarkJoke["category"]})', description=DarkJoke["joke"], color=0x11D999
                )
            )
    
    @commands.command(name = "pun")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def Pun(self, ctx):
        Pun = requests.get("https://sv443.net/jokeapi/v2/joke/Pun", headers = {"Accept": "application/json"}).json()
        if Pun["type"] == "twopart":
            await ctx.message.channel.send(
                embed=discord.Embed(
                    title="Pun", description=f'{Pun["setup"]}\n\n||{Pun["delivery"]}||', color=0x11D999
                )
            )
        else:
            await ctx.message.channel.send(
                embed=discord.Embed(
                    title="Pun", description=Pun["joke"], color=0x11D999
                )
            )

def setup(DClient):
    DClient.add_cog(Randomizers(DClient))