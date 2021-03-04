import discord
from discord.ext import commands
import requests
import randfacts
from Setup import (
    ChVote,
    ChPatreonT2,
    GetPatreonTier,
    ChAdmin,
    FormatTime,
    TimeTillMidnight,
    SendWait,
)
from Setup import AQd


class WrittenStuff(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.command(name="advice")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RandomAdvice(self, ctx):
        Advice = requests.get(
            "https://api.adviceslip.com/advice", headers={"Accept": "application/json"}
        ).json()
        await ctx.message.channel.send(
            embed=discord.Embed(
                title="Some Advice",
                description=Advice["slip"]["advice"],
                color=0x7DD7D8,
            )
        )

    @commands.command(aliases=["funfact", "fact"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def GetAFact(self, ctx):
        await ctx.message.channel.send(
            embed=discord.Embed(
                title="Fact", description=randfacts.getFact(), color=0x1F002A
            )
        )

    @commands.command(aliases=["kanye", "kanyewest"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ShitByKanye(self, ctx):
        KanyeSays = requests.get(
            "https://api.kanye.rest", headers={"Accept": "application/json"}
        ).json()
        await ctx.message.channel.send(
            embed=discord.Embed(
                title="Kanye Says Alot, Here's One",
                description=KanyeSays["quote"],
                color=0x53099B,
            )
        )

    # @commands.command(name="qotd")
    # @commands.check(ChVote)
    # @commands.cooldown(1, 1, commands.BucketType.user)
    # async def QuoteOfTheDay(self, ctx):
    #     TodayQuote = requests.get(
    #         "https://favqs.com/api/qotd", headers={"Accept": "application/json"}
    #     ).json()
    #     QEm = discord.Embed(
    #         title="Quote Of The Day",
    #         description=TodayQuote["quote"]["body"],
    #         color=0x8D42EE,
    #     )
    #     QEm.set_footer(text=f'By: {TodayQuote["quote"]["author"]}')
    #     await ctx.message.channel.send(embed=QEm)

    # @commands.group(name="qotddaily", invoke_without_command=True)
    # @commands.cooldown(1, 1, commands.BucketType.user)
    # async def QotdDAILY(self, ctx):
    #     TimeLeft = FormatTime(TimeTillMidnight())
    #     await SendWait(
    #         ctx,
    #         f'The next Daily QOTD is in {TimeLeft}.\n You can be added to QOTD Daily with "zqotddaily start" (If patreon tier 2+).\n Check "zhelp qotd" for more info',
    #     )

    # @QotdDAILY.command(name="start")
    # @commands.check(ChPatreonT2)
    # @commands.check(ChAdmin)
    # @commands.cooldown(1, 1, commands.BucketType.user)
    # async def StartQotdDAILY(self, ctx):
    #     TierApplicable = {"Tier 2 Super": 1, "Tier 3 Legend": 2, "Tier 4 Ultimate": 4}
    #     TierLimit = TierApplicable[GetPatreonTier(ctx.author.id)]
    #     if AQd.count_documents({"Type": "QOTD", "IDd": ctx.author.id}) >= TierLimit:
    #         await SendWait(
    #             ctx,
    #             "You already added the max amount of channels to QOTD daily.\nDifferent patreon levels get more channels\nCheck 'zpatreon'",
    #         )
    #         return
    #     QOTDUsers = AQd.find({"Type": "QOTD"})
    #     UserToCheckAdd = {
    #         "Type": "QOTD",
    #         "IDd": ctx.author.id,
    #         "IDg": ctx.guild.id,
    #         "Channel": ctx.message.channel.id,
    #     }
    #     if AQd.count_documents(UserToCheckAdd) == 1:
    #         await SendWait(ctx, "This channel is already added to QOTD daily")
    #         return
    #     AQd.insert_one(UserToCheckAdd)
    #     await SendWait(ctx, "Added to QOTD daily successfully")

    # @QotdDAILY.command(aliases=["stop", "end"])
    # @commands.check(ChPatreonT2)
    # @commands.check(ChAdmin)
    # @commands.cooldown(1, 1, commands.BucketType.user)
    # async def RemoveQotddDAILY(self, ctx):
    #     UserToCheckRemove = {
    #         "Type": "QOTD",
    #         "IDd": ctx.author.id,
    #         "IDg": ctx.guild.id,
    #         "Channel": ctx.message.channel.id,
    #     }
    #     if AQd.count_documents(UserToCheckRemove) == 1:
    #         Users = AQd.find(UserToCheckRemove)
    #         for User in Users:
    #             AQd.delete_one(User)
    #             await SendWait(ctx, "Removed from QOTD daily successfully")
    #             return
    #     await SendWait(ctx, "You are already not in QOTD daily")

    @commands.command(name="insult")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RandomInsult(self, ctx):
        InsultGot = requests.get(
            "https://evilinsult.com/generate_insult.php?lang=en&type=json",
            headers={"Accept": "application/json"},
        )
        InsultJSON = InsultGot.json()
        await ctx.message.channel.send(
            embed=discord.Embed(
                title="Insult", description=InsultJSON["insult"], color=0xBD2DB8
            )
        )

    @commands.command(name="dadjoke")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def KillMe(self, ctx):
        DadJoke = requests.get(
            "https://icanhazdadjoke.com/", headers={"Accept": "application/json"}
        ).json()
        await ctx.message.channel.send(
            embed=discord.Embed(
                title="Dad Joke", description=DadJoke["joke"], color=0x99807E
            )
        )

    @commands.command(name="joke")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def Joke(self, ctx):
        Joke = requests.get(
            "https://sv443.net/jokeapi/v2/joke/Programming,Miscellaneous,Spooky,Christmas?blacklistFlags=nsfw,religious,political,racist,sexist",
            headers={"Accept": "application/json"},
        ).json()
        if Joke["type"] == "twopart":
            await ctx.message.channel.send(
                embed=discord.Embed(
                    title=f'Joke ({Joke["category"]})',
                    description=f'{Joke["setup"]}\n\n||{Joke["delivery"]}||',
                    color=0xEB88DA,
                )
            )
        else:
            await ctx.message.channel.send(
                embed=discord.Embed(
                    title=f'Joke ({Joke["category"]})',
                    description=Joke["joke"],
                    color=0xEB88DA,
                )
            )

    @commands.command(name="darkjoke")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def DarkJoke(self, ctx):
        DarkJoke = requests.get(
            "https://sv443.net/jokeapi/v2/joke/Dark",
            headers={"Accept": "application/json"},
        ).json()
        if DarkJoke["type"] == "twopart":
            await ctx.message.channel.send(
                embed=discord.Embed(
                    title=f'Joke ({DarkJoke["category"]})',
                    description=f'{DarkJoke["setup"]}\n\n||{DarkJoke["delivery"]}||',
                    color=0xD8DCCD,
                )
            )
        else:
            await ctx.message.channel.send(
                embed=discord.Embed(
                    title=f'Joke ({DarkJoke["category"]})',
                    description=DarkJoke["joke"],
                    color=0xD8DCCD,
                )
            )

    @commands.command(name="pun")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def Pun(self, ctx):
        Pun = requests.get(
            "https://sv443.net/jokeapi/v2/joke/Pun",
            headers={"Accept": "application/json"},
        ).json()
        if Pun["type"] == "twopart":
            await ctx.message.channel.send(
                embed=discord.Embed(
                    title="Pun",
                    description=f'{Pun["setup"]}\n\n||{Pun["delivery"]}||',
                    color=0x05D111,
                )
            )
        else:
            await ctx.message.channel.send(
                embed=discord.Embed(
                    title="Pun", description=Pun["joke"], color=0x05D111
                )
            )


def setup(DClient):
    DClient.add_cog(WrittenStuff(DClient))