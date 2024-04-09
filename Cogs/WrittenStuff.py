import discord
from discord import app_commands
from discord.ext import commands
import requests
import randfacts
from Setup import (
    #? ChVote,
    #? ChPatreonT2,
    #? GetPatreonTier,
    # ChAdmin,
    #? FormatTime,
    #? TimeTillMidnight,
    SendWait,
    NClient,
    #? AQd
)
import re


class WrittenStuff(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.hybrid_command(name="advice", description="Because a Discord Bot is Where you Should be Getting Advice From.")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RandomAdvice(self, ctx):
        Advice = requests.get("https://api.adviceslip.com/advice", headers={"Accept": "application/json"} ).json()
        await ctx.send(embed=discord.Embed(title="Some Advice", description=Advice["slip"]["advice"], color=0x7DD7D8))
    
    @commands.hybrid_command(name="news", description="Latest Headline News.")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def TheNews(self, ctx):
        News = requests.get("https://newsapi.org/v2/top-headlines", params=NClient).json()
        NEm = discord.Embed(title = "News", color = 0x0F49B2)
        for Num, Article in enumerate(News["articles"], start=1): 
            NEm.add_field(name = f'`{Num}.` {Article["title"]}. **Published On:** {re.sub("T", " ", Article["publishedAt"])[:-1]}', value=Article["url"])
        await ctx.send(embed = NEm)

    @commands.hybrid_command(name="fact",aliases=["funfact"], description="Did you Know this Command Sends Fun Facts?")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def GetAFact(self, ctx): await ctx.send(embed=discord.Embed(title="Fact", description=randfacts.getFact(), color=0x1F002A))

    @commands.hybrid_group(name="bin", aliases=["binary"], description="Deal with Binary Stuff.")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def Bins(self, ctx): pass
    
    @Bins.command(name="make", aliases=["create"], description="Text to Binary")
    @app_commands.rename(txt="text")
    @app_commands.describe(txt="Text to Convert to Binary")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def To(self, ctx, *, txt:str):
        Binary = " ".join([format(i,"b") for i in bytearray(txt,"utf-8")])
        await ctx.send(embed = discord.Embed(title = "Convert To Binary", description = Binary[:2048], color = 0x5ADF44))

    @Bins.command(name = "read", description="Binary to Text")
    @app_commands.rename(bin="binary")
    @app_commands.describe(bin="Text to Convert to Binary")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def From(self, ctx, *, bin:str):
        # print(bin)
        try:
            String = "".join([chr(int(Binary, 2)) for Binary in bin.split(" ")])
            try:
                requests.get(String)
                await ctx.send(String)
            except: await ctx.send(embed = discord.Embed(title = "Convert To Text", description = String[:2048], color = 0x5ADF44))
        except ValueError: await SendWait(ctx, "Something went wrong. Check if the binary has any errors.")

    @commands.hybrid_command(name="kanye", aliases=["kanyewest"], description="Kanye Yaps. Here are his Yaps.")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ShitByKanye(self, ctx):
        KanyeSays = requests.get("https://api.kanye.rest", headers={"Accept": "application/json"}).json()
        await ctx.send(embed=discord.Embed(title="Kanye Says Alot, Here's One", description=KanyeSays["quote"], color=0x53099B))

    @commands.hybrid_command(name="insult", description="Sometimes you Need to Curb your Ego,")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RandomInsult(self, ctx):
        InsultGot = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=json", headers={"Accept": "application/json"}).json()
        await ctx.send(embed=discord.Embed( title="Insult", description=InsultGot["insult"], color=0xBD2DB8))

    @commands.hybrid_command(name="dadjoke", description="Remember your Dad's Lame Jokes.")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def KillMe(self, ctx):
        DadJoke = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"}).json()
        await ctx.send(embed=discord.Embed(title="Dad Joke", description=DadJoke["joke"], color=0x99807E))

    @commands.hybrid_command(name="joke", description="Jokes for a Tamer Audience.")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def Joke(self, ctx):
        Joke = requests.get("https://sv443.net/jokeapi/v2/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit", #?blacklistFlags=
                            headers={"Accept": "application/json"}).json()
        if Joke["type"] == "twopart": 
            await ctx.send(embed=discord.Embed(title=f'Joke ({Joke["category"]})', description=f'{Joke["setup"]}\n\n||{Joke["delivery"]}||', color=0xEB88DA))
        else: await ctx.send(embed=discord.Embed(title=f'Joke ({Joke["category"]})', description=Joke["joke"], color=0xEB88DA))

    @commands.hybrid_command(name="darkjoke", description="A Joke so Dark it will Probably Make you Uncomfortable.")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def DarkJoke(self, ctx):
        DarkJoke = requests.get("https://sv443.net/jokeapi/v2/joke/Dark", headers={"Accept": "application/json"}).json()
        if DarkJoke["type"] == "twopart": 
            await ctx.send(embed=discord.Embed(title=f'Joke ({DarkJoke["category"]})', description=f'{DarkJoke["setup"]}\n\n||{DarkJoke["delivery"]}||',
                                                               color=0xD8DCCD))
        else: await ctx.send(embed=discord.Embed(title=f'Joke ({DarkJoke["category"]})', description=DarkJoke["joke"], color=0xD8DCCD))

    @commands.hybrid_command(name="pun", description="Ba Dumm Tiss.")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def Pun(self, ctx):
        Pun = requests.get("https://sv443.net/jokeapi/v2/joke/Pun", headers={"Accept": "application/json"}).json()
        if Pun["type"] == "twopart": await ctx.send(embed=discord.Embed(title="Pun", description=f'{Pun["setup"]}\n\n||{Pun["delivery"]}||', color=0x05D111))
        else: await ctx.send(embed=discord.Embed(title="Pun", description=Pun["joke"], color=0x05D111))

    @commands.hybrid_command(name="qotd", description="A Daily Quote.")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def QuoteOfTheDay(self, ctx):
        TodayQuote = requests.get(
            "https://favqs.com/api/qotd", headers={"Accept": "application/json"}
        ).json()
        QEm = discord.Embed(
            title="Quote Of The Day",
            description=TodayQuote["quote"]["body"],
            color=0x8D42EE,
        )
        QEm.set_footer(text=f'By: {TodayQuote["quote"]["author"]}')
        await ctx.send(embed=QEm)
    #? @commands.group(name="qotddaily", invoke_without_command=True)
    #? @commands.cooldown(1, 1, commands.BucketType.user)
    #? async def QotdDAILY(self, ctx):
    #?     TimeLeft = FormatTime(TimeTillMidnight())
    #?     await SendWait(
    #?         ctx,
    #?         f'The next Daily QOTD is in {TimeLeft}.\n You can be added to QOTD Daily with "zqotddaily start" (If patreon tier 2+).\n Check "zhelp qotd" for more info',
    #?     )
    #? @QotdDAILY.command(name="start")
    #? @commands.check(ChPatreonT2)
    #? @commands.check(ChAdmin)
    #? @commands.cooldown(1, 1, commands.BucketType.user)
    #? async def StartQotdDAILY(self, ctx):
    #?     TierApplicable = {"Tier 2 Super": 1, "Tier 3 Legend": 2, "Tier 4 Ultimate": 4}
    #?     TierLimit = TierApplicable[GetPatreonTier(ctx.author.id)]
    #?     if AQd.count_documents({"Type": "QOTD", "IDd": ctx.author.id}) >= TierLimit:
    #?         await SendWait(
    #?             ctx,
    #?             "You already added the max amount of channels to QOTD daily.\nDifferent patreon levels get more channels\nCheck 'zpatreon'",
    #?         )
    #?         return
    #?     QOTDUsers = AQd.find({"Type": "QOTD"})
    #?     UserToCheckAdd = {
    #?         "Type": "QOTD",
    #?         "IDd": ctx.author.id,
    #?         "IDg": ctx.guild.id,
    #?         "Channel": ctx.message.channel.id,
    #?     }
    #?     if AQd.count_documents(UserToCheckAdd) == 1:
    #?         await SendWait(ctx, "This channel is already added to QOTD daily")
    #?         return
    #?     AQd.insert_one(UserToCheckAdd)
    #?     await SendWait(ctx, "Added to QOTD daily successfully")
    #? @QotdDAILY.command(aliases=["stop", "end"])
    #? @commands.check(ChPatreonT2)
    #? @commands.check(ChAdmin)
    #? @commands.cooldown(1, 1, commands.BucketType.user)
    #? async def RemoveQotddDAILY(self, ctx):
    #?     UserToCheckRemove = {
    #?         "Type": "QOTD",
    #?         "IDd": ctx.author.id,
    #?         "IDg": ctx.guild.id,
    #?         "Channel": ctx.message.channel.id,
    #?     }
    #?     if AQd.count_documents(UserToCheckRemove) == 1:
    #?         Users = AQd.find(UserToCheckRemove)
    #?         for User in Users:
    #?             AQd.delete_one(User)
    #?             await SendWait(ctx, "Removed from QOTD daily successfully")
    #?             return
    #?     await SendWait(ctx, "You are already not in QOTD daily")
    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded!")

async def setup(DClient):
    await DClient.add_cog(WrittenStuff(DClient))