from discord.ext import commands, tasks
import discord
from Setup import (
    IsBot,
    IsVote,
    IsPatreon,
    IsPatreonT2,
    IsPatreonT3,
    IsPatreonT4,
    Ignore,
    IsAdmin,
    IsSetup,
    IsNSFW,
)
from Setup import FormatTime, TimeTillMidnight, GetPatreonTier, ErrorEmbeds
from Setup import ChPatreonUserT2
import random
import requests
import asyncio

Doing = [
    "Playing with the laws of physics",
    "Torture",
    "Just Vibin'",
    "With my toes",
    "Chess with god",
    "With Leona",
]


def MakeAPODEmbed():
    NASAapod = requests.get(
        "https://api.nasa.gov/planetary/apod?api_key=0dsw3SiQmYCeNnwKZROSQIyrcZqjoDzMBo4ggCwS",
        headers={"Accept": "application/json"},
    )
    JSONapod = NASAapod.json()
    if len(JSONapod["explanation"]) > 1021:
        Explanation = JSONapod["explanation"][0:1021]
        Explanation = Explanation + "..."
    else:
        Explanation = JSONapod["explanation"]
    DEm = discord.Embed(
        title=JSONapod["title"],
        description=f'Date {JSONapod["date"]}',
        color=0xA9775A,
    )
    DEm.add_field(name="Explanation:", value=Explanation, inline=False)
    try:
        DEm.set_image(url=JSONapod["hdurl"])
    except KeyError:
        DEm.add_field(
            name="\u200b", value=f'[Video Url]({JSONapod["url"]})', inline=False
        )
    try:
        DEm.set_footer(text=f'Copyright: {JSONapod["copyright"]}')
    except KeyError:
        pass
    return DEm


def MakeQOTDEmbed():
    TodayQuote = requests.get(
        "https://favqs.com/api/qotd", headers={"Accept": "application/json"}
    ).json()
    QEm = discord.Embed(
        title="Quote Of The Day",
        description=TodayQuote["quote"]["body"],
        color=0x8D42EE,
    )
    QEm.set_footer(text=f'By: {TodayQuote["quote"]["author"]}')
    return QEm


class MainEvents(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient
        self.SendAPODDaily.start()
        self.SendQOTDDaily.start()

    @commands.Cog.listener()
    async def on_ready(self):
        StateFile = open("OpenState.txt")
        State = StateFile.readlines()
        StateFile.close()
        if "".join(State) == "Up":
            await self.DClient.change_presence(
                activity=discord.Game(f"zhelp || {random.choice(Doing)}")
            )
        else:
            await self.DClient.change_presence(status=discord.Status.invisible)
        print(f"Online in {len(self.DClient.guilds)}...")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.message.channel.send(
                embed=discord.Embed(
                    title="Oops",
                    description=f"Hold the spam. Wait atleast {FormatTime(round(error.retry_after, 2))}",
                )
            )
        elif isinstance(error, IsBot):
            await ctx.message.channel.send(
                embed=discord.Embed(
                    title="Oops", description="Bots can't use commands :pensive:"
                )
            )
        elif isinstance(error, IsAdmin):
            await ctx.message.channel.send(
                embed=discord.Embed(
                    title="Oops",
                    description="Non-admins are not allowed to use this command",
                )
            )
        elif isinstance(error, IsVote):
            await ctx.message.channel.send(embed=ErrorEmbeds("Vote"))
        elif isinstance(error, IsPatreon):
            await ctx.message.channel.send(embed=ErrorEmbeds("Patreon"))
        elif isinstance(error, IsPatreonT2):
            await ctx.message.channel.send(embed=ErrorEmbeds("PatreonT2"))
        elif isinstance(error, IsPatreonT3):
            await ctx.message.channel.send(embed=ErrorEmbeds("PatreonT3"))
        elif isinstance(error, IsPatreonT4):
            await ctx.message.channel.send(embed=ErrorEmbeds("PatreonT4"))
        elif isinstance(error, IsSetup):
            await ctx.message.channel.send(
                embed=discord.Embed(
                    title="Oops",
                    description='Please setup your server first (with "zsetup")! Check all server commands (with "zhelp server")',
                )
            )
        elif isinstance(error, IsNSFW):
            await ctx.message.channel.send(
                embed=discord.Embed(
                    title="Oops", description="This can only be used in NSFW channels."
                )
            )
        elif isinstance(error, commands.CommandNotFound) or isinstance(error, Ignore):
            pass
        else:
            raise error

    @tasks.loop(hours=24)
    async def SendAPODDaily(self):
        print("Sending APOD...")
        TierApplicable = {"Tier 2 Super": 1, "Tier 3 Legend": 2, "Tier 4 Ultimate": 4}
        OpenAPODChannelUserList = open("APODDaily.txt")
        APODChannelUserList = OpenAPODChannelUserList.readlines()
        OpenAPODChannelUserList.close()
        APODEm = MakeAPODEmbed()
        Line = 0
        UserChannelCount = {}
        for APODChannelUser in APODChannelUserList:
            UserID = APODChannelUser.split(" ")[0]
            ChannelID = APODChannelUser.split(" ")[1]
            Channel = self.DClient.get_channel(int(ChannelID))
            if ChPatreonUserT2(int(UserID)):
                TierLimit = TierApplicable[GetPatreonTier(UserID)]
                if UserID in UserChannelCount:
                    UserChannelCount[UserID] += 1
                else:
                    UserChannelCount[UserID] = 1
                if Channel is None:
                    del APODChannelUserList[Line]
                else:
                    if UserChannelCount <= TierLimit:
                        await Channel.send(embed=APODEm)
                    else:
                        await Channel.send(
                            "NO LONGER APPLICABLE FOR THIS MANY CHANNELS. Daily APOD stopped in this channel. :pensive: You can resign up for patreon, check zpatreon"
                        )
                        del APODChannelUserList[Line]
            else:
                await Channel.send(
                    "NO LONGER A PATREON. Daily APOD stopped. :pensive: You can re-sign up for patreon, check zpatreon"
                )
                del APODChannelUserList[Line]
            Line += 1
        FixAPODChannelUserFile = open("APODDaily.txt", "w+")
        for Line in APODChannelUserList:
            FixAPODChannelUserFile.write(Line)
        FixAPODChannelUserFile.close()

    @SendAPODDaily.before_loop
    async def RegulateBeforeAPODLoop(self):
        TimeToWait = TimeTillMidnight()
        print(f"{TimeToWait}s to start 24 hour APOD loop...")
        for _ in range(TimeToWait):
            await asyncio.sleep(1)
        print("Start 24 hour APOD loop")
        print("Sending APOD...")
        TierApplicable = {"Tier 2 Super": 1, "Tier 3 Legend": 2, "Tier 4 Ultimate": 4}
        OpenAPODChannelUserList = open("APODDaily.txt")
        APODChannelUserList = OpenAPODChannelUserList.readlines()
        OpenAPODChannelUserList.close()
        APODEm = MakeAPODEmbed()
        Line = 0
        UserChannelCount = {}
        for APODChannelUser in APODChannelUserList:
            UserID = APODChannelUser.split(" ")[0]
            ChannelID = APODChannelUser.split(" ")[1]
            Channel = self.DClient.get_channel(int(ChannelID))
            if ChPatreonUserT2(int(UserID)):
                TierLimit = TierApplicable[GetPatreonTier(UserID)]
                if UserID in UserChannelCount:
                    UserChannelCount[UserID] += 1
                else:
                    UserChannelCount[UserID] = 1
                if Channel is None:
                    del APODChannelUserList[Line]
                else:
                    if UserChannelCount <= TierLimit:
                        await Channel.send(embed=APODEm)
                    else:
                        await Channel.send(
                            "NO LONGER APPLICABLE FOR THIS MANY CHANNELS. Daily APOD stopped in this channel. :pensive: You can resign up for patreon, check zpatreon"
                        )
                        del APODChannelUserList[Line]
            else:
                await Channel.send(
                    "NO LONGER A PATREON. Daily APOD stopped. :pensive: You can re-sign up for patreon, check zpatreon"
                )
                del APODChannelUserList[Line]
            Line += 1
        FixAPODChannelUserFile = open("APODDaily.txt", "w+")
        for Line in APODChannelUserList:
            FixAPODChannelUserFile.write(Line)
        FixAPODChannelUserFile.close()

    @tasks.loop(hours=24)
    async def SendQOTDDaily(self):
        print("Sending QOTD...")
        TierApplicable = {"Tier 2 Super": 1, "Tier 3 Legend": 2, "Tier 4 Ultimate": 4}
        OpenQOTDChannelUserList = open("QOTDDaily.txt")
        QOTDChannelUserList = OpenQOTDChannelUserList.readlines()
        OpenQOTDChannelUserList.close()
        QOTDEm = MakeQOTDEmbed()
        Line = 0
        UserChannelCount = {}
        for QOTDChannelUser in QOTDChannelUserList:
            UserID = QOTDChannelUser.split(" ")[0]
            ChannelID = QOTDChannelUser.split(" ")[1]
            Channel = self.DClient.get_channel(int(ChannelID))
            if ChPatreonUserT2(UserID):
                TierLimit = TierApplicable[GetPatreonTier(UserID)]
                if UserID in UserChannelCount:
                    UserChannelCount[UserID] += 1
                else:
                    UserChannelCount[UserID] = 1
                if Channel is None:
                    del QOTDChannelUserList[Line]
                else:
                    if UserChannelCount <= TierLimit:
                        await Channel.send(embed=QOTDEm)
                    else:
                        await Channel.send(
                            "NO LONGER APPLICABLE FOR THIS MANY CHANNELS. Daily APOD stopped in this channel. :pensive: You can resign up for patreon, check zpatreon"
                        )
                        del QOTDChannelUserList[Line]
            else:
                await Channel.send(
                    "NO LONGER A PATREON or NO LONGER APPLICABLE TO THIS MANY CHANNELS. Daily QOTD stopped. :pensive: You can resign up for patreon, check zpatreon"
                )
                del QOTDChannelUserList[Line]
            Line += 1
        FixQOTDChannelUserFile = open("QOTDDaily.txt", "w+")
        for Line in QOTDChannelUserList:
            FixQOTDChannelUserFile.write(Line)
        FixQOTDChannelUserFile.close()

    @SendQOTDDaily.before_loop
    async def RegulateBeforeQOTDLoop(self):
        TimeToWait = TimeTillMidnight()
        print(f"{TimeToWait}s to start 24 hour QOTD loop...")
        for _ in range():
            await asyncio.sleep(1)
        print("Start 24 hour QOTD loop")
        print("Sending QOTD...")
        TierApplicable = {"Tier 2 Super": 1, "Tier 3 Legend": 2, "Tier 4 Ultimate": 4}
        OpenQOTDChannelUserList = open("QOTDDaily.txt")
        QOTDChannelUserList = OpenQOTDChannelUserList.readlines()
        OpenQOTDChannelUserList.close()
        QOTDEm = MakeQOTDEmbed()
        Line = 0
        UserChannelCount = {}
        for QOTDChannelUser in QOTDChannelUserList:
            UserID = QOTDChannelUser.split(" ")[0]
            ChannelID = QOTDChannelUser.split(" ")[1]
            Channel = self.DClient.get_channel(int(ChannelID))
            if ChPatreonUserT2(UserID):
                TierLimit = TierApplicable[GetPatreonTier(UserID)]
                if UserID in UserChannelCount:
                    UserChannelCount[UserID] += 1
                else:
                    UserChannelCount[UserID] = 1
                if Channel is None:
                    del QOTDChannelUserList[Line]
                else:
                    if UserChannelCount <= TierLimit:
                        await Channel.send(embed=QOTDEm)
                    else:
                        await Channel.send(
                            "NO LONGER APPLICABLE FOR THIS MANY CHANNELS. Daily APOD stopped in this channel. :pensive: You can resign up for patreon, check zpatreon"
                        )
                        del QOTDChannelUserList[Line]
            else:
                await Channel.send(
                    "NO LONGER A PATREON or NO LONGER APPLICABLE TO THIS MANY CHANNELS. Daily QOTD stopped. :pensive: You can resign up for patreon, check zpatreon"
                )
                del QOTDChannelUserList[Line]
            Line += 1
        FixQOTDChannelUserFile = open("QOTDDaily.txt", "w+")
        for Line in QOTDChannelUserList:
            FixQOTDChannelUserFile.write(Line)
        FixQOTDChannelUserFile.close()


def setup(DClient):
    DClient.add_cog(MainEvents(DClient))