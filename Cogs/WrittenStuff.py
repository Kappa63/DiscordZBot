import discord
from discord.ext import commands
import requests
import randfacts
from Setup import ChVote, ChPatreonT2, GetPatreonTier, ChAdmin, FormatTime, TimeTillMidnight

class WrittenStuff(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.command(name="advice")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RandomAdvice(self, ctx):
        Advice = requests.get("https://api.adviceslip.com/advice", headers = {"Accept": "application/json"}).json()
        await ctx.message.channel.send(
            embed=discord.Embed(title="Some Advice", description = Advice["slip"]["advice"], color=0x7dd7d8)
        )

    @commands.command(aliases = ["funfact", "fact"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def GetAFact(self, ctx):
        await ctx.message.channel.send(
            embed=discord.Embed(
                title="Fact", description=randfacts.getFact(), color=0x1F002A
            )
        )

    @commands.command(aliases = ["kanye", "kanyewest"])
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
    
    @commands.group(name="qotddaily", invoke_without_command=True)
    @commands.check(ChPatreonT2)
    @commands.check(ChAdmin)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def QotdDAILY(self, ctx):
        TimeLeft = FormatTime(TimeTillMidnight())
        await ctx.message.channel.send(embed = discord.Embed(title = "APOD in...", description = f'The next Daily QOTD is in {TimeLeft}.\n You can be added to QOTD Daily with "zqotddaily start".\n Check "zhelp qotd" for more info'))
    
    @QotdDAILY.command(name="start")
    @commands.check(ChPatreonT2)
    @commands.check(ChAdmin)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def StartQotdDAILY(self, ctx):
        TierApplicable = {"Tier 2 Super":1, "Tier 3 Legend":2, "Tier 4 Ultimate":4}
        LineToCheckAdd = f'{ctx.author.id} {ctx.message.channel.id} {ctx.guild.id} \n'
        UserID = f'{ctx.author.id}'
        OpenQOTDChannelUserFile = open("QOTDDaily.txt")
        QOTDChannelUserFile = OpenQOTDChannelUserFile.readlines()
        OpenQOTDChannelUserFile.close()
        TierLimit = TierApplicable[GetPatreonTier(ctx.author.id)]
        for Line in QOTDChannelUserFile:
            if Line == LineToCheckAdd:
                await ctx.message.channel.send(embed = discord.Embed(title = "All Good", description = "This channel is already added to QOTD daily"))
                return
        Channels = 0
        for Line in QOTDChannelUserFile:
            if Line.split(" ")[0] == UserID:
                Channels += 1
                if Channels == TierLimit: 
                    await ctx.message.channel.send(embed = discord.Embed(title = "Oops", description = "You already added the max amount of channels to QOTD daily.\nDifferent patreon levels get more channels\nCheck 'zpatreon'"))
                    return
        AppendQOTDChannelUserFile = open("QOTDDaily.txt", "a")
        AppendQOTDChannelUserFile.write(f'{ctx.author.id} {ctx.message.channel.id} {ctx.guild.id} \n')
        AppendQOTDChannelUserFile.close()
        await ctx.message.channel.send(embed = discord.Embed(title = "Success", description = "Added to QOTD daily successfully"))

    @QotdDAILY.command(name="stop")
    @commands.check(ChPatreonT2)
    @commands.check(ChAdmin)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RemoveQotddDAILY(self, ctx):
        LineToCheckAdd = f'{ctx.author.id} {ctx.message.channel.id} {ctx.guild.id} \n'
        OpenQOTDChannelUserFile = open("QOTDDaily.txt")
        QOTDChannelUserFile = OpenQOTDChannelUserFile.readlines()
        OpenQOTDChannelUserFile.close()
        LineNum = 0
        Exist = False
        for Line in QOTDChannelUserFile:
            if Line == LineToCheckAdd:
                del QOTDChannelUserFile[LineNum]
                Exist = True
                return
            LineNum += 1
        if Exist:
            FixQOTDChannelUserFile = open("QOTDDaily.txt", "w+")
            for Line in QOTDChannelUserFile:
                FixQOTDChannelUserFile.write(Line)
            FixQOTDChannelUserFile.close()
            await ctx.message.channel.send(embed = discord.Embed(title = "Success", description = "Removed from QOTD daily successfully"))
            return
        await ctx.message.channel.send(embed = discord.Embed(title = "All Good", description = "You are already not in QOTD daily"))

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

    @commands.command(name="dadjoke")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def KillMe(self, ctx):
        DadJoke = requests.get(
            "https://icanhazdadjoke.com/", headers={"Accept": "application/json"}
        ).json()
        await ctx.message.channel.send(
            embed=discord.Embed(
                title="Dad Joke", description=DadJoke["joke"], color=0x99807e
            )
        )

    @commands.command(name = "joke")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def Joke(self, ctx):
        Joke = requests.get("https://sv443.net/jokeapi/v2/joke/Programming,Miscellaneous,Spooky,Christmas?blacklistFlags=nsfw,religious,political,racist,sexist", headers = {"Accept": "application/json"}).json()
        if Joke["type"] == "twopart":
            await ctx.message.channel.send(
                embed=discord.Embed(
                    title=f'Joke ({Joke["category"]})', description=f'{Joke["setup"]}\n\n||{Joke["delivery"]}||', color=0xeb88da
                )
            )
        else:
            await ctx.message.channel.send(
                embed=discord.Embed(
                    title=f'Joke ({Joke["category"]})', description=Joke["joke"], color=0xeb88da
                )
            )

    @commands.command(name = "darkjoke")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def DarkJoke(self, ctx):
        DarkJoke = requests.get("https://sv443.net/jokeapi/v2/joke/Dark", headers = {"Accept": "application/json"}).json()
        if DarkJoke["type"] == "twopart":
            await ctx.message.channel.send(
                embed=discord.Embed(
                    title=f'Joke ({DarkJoke["category"]})', description=f'{DarkJoke["setup"]}\n\n||{DarkJoke["delivery"]}||', color=0xd8dccd
                )
            )
        else:
            await ctx.message.channel.send(
                embed=discord.Embed(
                    title=f'Joke ({DarkJoke["category"]})', description=DarkJoke["joke"], color=0xd8dccd
                )
            )
    
    @commands.command(name = "pun")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def Pun(self, ctx):
        Pun = requests.get("https://sv443.net/jokeapi/v2/joke/Pun", headers = {"Accept": "application/json"}).json()
        if Pun["type"] == "twopart":
            await ctx.message.channel.send(
                embed=discord.Embed(
                    title="Pun", description=f'{Pun["setup"]}\n\n||{Pun["delivery"]}||', color=0x05d111
                )
            )
        else:
            await ctx.message.channel.send(
                embed=discord.Embed(
                    title="Pun", description=Pun["joke"], color=0x05d111
                )
            )

def setup(DClient):
    DClient.add_cog(WrittenStuff(DClient))