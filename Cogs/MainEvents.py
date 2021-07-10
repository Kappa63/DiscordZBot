from discord.ext import commands, tasks
import discord
from Setup import (IsBot, IsVote, IsPatreon, IsPatreonT2, IsPatreonT3, IsPatreonT4, Ignore, IsAdmin,
                   IsSetup, IsNSFW, IsMultiredditLimit, FormatTime, TimeTillMidnight, GetPatreonTier,
                   ErrorEmbeds, ChPatreonUserT2, SendWait, AQd)
import random
import requests
import asyncio

Doing = ["Playing With The Laws Of Physics", "Getting Tortured", "Just Vibin'", "Playing With My Toes",
         "Playing Chess With God", "Playing With Leona", "Yeeting People"]


def MakeAPODEmbed():
    NASAapod = requests.get("https://api.nasa.gov/planetary/apod?api_key=0dsw3SiQmYCeNnwKZROSQIyrcZqjoDzMBo4ggCwS", headers={"Accept": "application/json"}).json()
    Explanation = NASAapod["explanation"][:1021]
    DEm = discord.Embed(title=NASAapod["title"], description=f'Date {NASAapod["date"]}', color=0xA9775A)
    DEm.add_field(name="Explanation:", value=Explanation, inline=False)
    if "hdurl" in NASAapod: DEm.set_image(url=NASAapod["hdurl"])
    else: DEm.add_field(name="\u200b", value=f'[Video Url]({NASAapod["url"]})', inline=False)
    if "copyright" in NASAapod: DEm.set_footer(text=f'Copyright: {NASAapod["copyright"]}')
    return DEm

#? def MakeQOTDEmbed():
#?     TodayQuote = requests.get(
#?         "https://favqs.com/api/qotd", headers={"Accept": "application/json"}
#?     ).json()
#?     QEm = discord.Embed(
#?         title="Quote Of The Day",
#?         description=TodayQuote["quote"]["body"],
#?         color=0x8D42EE,
#?     )
#?     QEm.set_footer(text=f'By: {TodayQuote["quote"]["author"]}')
#?     return QEm

def MakeCPTDEmbed():
    GetCPTD = requests.get("https://api.chess.com/pub/puzzle", headers={"Accept": "application/json"}).json()
    CEm = discord.Embed(title=GetCPTD["title"], description=f'[Daily Puzzle]({GetCPTD["url"]}) from [Chess.com](https://www.chess.com/)', color=0x6C9D41)
    CEm.set_image(url=GetCPTD["image"])
    return CEm


class MainEvents(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient
        self.SendAPODDaily.start()
        #? self.SendQOTDDaily.start()
        self.SendCPTDDaily.start()

    @commands.Cog.listener()
    async def on_ready(self):
        StateFile = open("OpenState.txt")
        State = StateFile.readlines()
        StateFile.close()
        if "".join(State) == "Up": await self.DClient.change_presence(activity=discord.Game(f"zhelp || {random.choice(Doing)}"))
        else: await self.DClient.change_presence(status=discord.Status.invisible)
        self.StaffChannel = self.DClient.get_channel(795080325020909598)
        self.Me = self.DClient.get_user(443986051371892746)
        print(f"Online in {len(self.DClient.guilds)}...")
        await self.StaffChannel.send(f"Back Online In {len(self.DClient.guilds)}...")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown): await SendWait(ctx, f'Hold the spam. Wait atleast {FormatTime(round(error.retry_after, 2))}')
        elif isinstance(error, IsAdmin): await SendWait(ctx, "Non-admins are not allowed to use this command")
        elif isinstance(error, IsVote): await ctx.message.channel.send(embed=ErrorEmbeds("Vote"))
        elif isinstance(error, IsPatreon): await ctx.message.channel.send(embed=ErrorEmbeds("Patreon"))
        elif isinstance(error, IsPatreonT2): await ctx.message.channel.send(embed=ErrorEmbeds("PatreonT2"))
        elif isinstance(error, IsPatreonT3): await ctx.message.channel.send(embed=ErrorEmbeds("PatreonT3"))
        elif isinstance(error, IsPatreonT4): await ctx.message.channel.send(embed=ErrorEmbeds("PatreonT4"))
        elif isinstance(error, IsSetup): await SendWait(ctx, 'Please setup your server first (with "zsetup")! Check all server commands (with "zhelp server")')
        elif isinstance(error, IsNSFW): await SendWait(ctx, "This can only be used in NSFW channels.")
        elif isinstance(error, IsMultiredditLimit): await SendWait(ctx, "You can no longer have this many Multireddits. Remove some to comply with your limit. Until then you cannot use your Multireddits.")
        elif isinstance(error, (commands.CommandNotFound, Ignore, IsBot, commands.MessageNotFound)): return
        else:
            # StaffChannel = self.DClient.get_channel(795080325020909598)
            # Me = self.DClient.get_user(443986051371892746)
            await self.StaffChannel.send(self.Me.mention)
            await self.StaffChannel.send(f'In {ctx.command} ({ctx.message.content}): {error}')
            raise error

    @tasks.loop(seconds=TimeTillMidnight())
    async def SendAPODDaily(self):
        print("Sending APOD...")
        # StaffChannel = self.DClient.get_channel(795080325020909598)
        await self.StaffChannel.send("Sending APOD...")
        TierApplicable = {"Tier 2 Super": 1, "Tier 3 Legend": 2, "Tier 4 Ultimate": 4}
        APODEm = MakeAPODEmbed()
        APODUsers = AQd.find({"Type": "APOD"})
        ToBeRemoved = []
        for User in APODUsers:
            UserID = User["IDd"]
            ChannelID = User["Channel"]
            if ChPatreonUserT2(UserID):
                TierLimit = TierApplicable[GetPatreonTier(UserID)]
                if AQd.count_documents({"Type": "APOD", "IDd": UserID}) > TierLimit:
                    APODTempUsers = AQd.find({"Type": "APOD", "IDd": UserID})
                    Num = 0
                    for TempUser in APODTempUsers:
                        Num += 1
                        if Num > TierLimit and TempUser not in ToBeRemoved: ToBeRemoved.append(TempUser) 
                Channel = self.DClient.get_channel(ChannelID)
                if User not in ToBeRemoved:
                    if Channel is None: AQd.delete_one(User)
                    else: await Channel.send(embed=APODEm)
                else:
                    await Channel.send("NO LONGER APPLICABLE TO THIS MANY CHANNELS. Daily APOD stopped. :pensive: You can sign up for donator, check zdonate")
                    AQd.delete_one(User)
            else: await Channel.send("NO LONGER A Donator. Daily APOD stopped. :pensive: You can sign up for donator, check zdonate")
        await self.StaffChannel.send(f"Next APOD in {TimeTillMidnight()}s...")
        raise ValueError
        # self.SendAPODDaily.change_interval(seconds=TimeTillMidnight())

    @SendAPODDaily.before_loop
    async def RegulateBeforeAPODLoop(self):
        await self.DClient.wait_until_ready()
        print("APOD Regulating...")
        # StaffChannel = self.DClient.get_channel(795080325020909598)
        # await self.StaffChannel.send(f"APOD Regulating for {TimeTillMidnight()}s...")
        await asyncio.sleep(TimeTillMidnight())

    @tasks.loop(seconds=TimeTillMidnight())
    async def SendCPTDDaily(self):
        print("Sending CPTD...")
        # StaffChannel = self.DClient.get_channel(795080325020909598)
        await self.StaffChannel.send("Sending CPTD...")
        TierApplicable = {"Tier 2 Super": 1, "Tier 3 Legend": 2, "Tier 4 Ultimate": 4}
        CPTDEm = MakeCPTDEmbed()
        CPTDUsers = AQd.find({"Type": "CPTD"})
        ToBeRemoved = []
        for User in CPTDUsers:
            UserID = User["IDd"]
            ChannelID = User["Channel"]
            if ChPatreonUserT2(UserID):
                TierLimit = TierApplicable[GetPatreonTier(UserID)]
                if AQd.count_documents({"Type": "CPTD", "IDd": UserID}) > TierLimit:
                    CPTDTempUsers = AQd.find({"Type": "CPTD", "IDd": UserID})
                    Num = 0
                    for TempUser in CPTDTempUsers:
                        Num += 1
                        if Num > TierLimit and TempUser not in ToBeRemoved: ToBeRemoved.append(TempUser) 
                Channel = self.DClient.get_channel(ChannelID)
                if User not in ToBeRemoved:
                    if Channel is None: AQd.delete_one(User)
                    else: await Channel.send(embed=CPTDEm)
                else:
                    await Channel.send("NO LONGER APPLICABLE TO THIS MANY CHANNELS. Daily CPTD stopped. :pensive: You can sign up for donator, check zdonate")
                    AQd.delete_one(User)
            else: await Channel.send("NO LONGER A Donator. Daily CPTD stopped. :pensive: You can sign up for donator, check zdonate")
        await self.StaffChannel.send(f"Next CPTD in {TimeTillMidnight()}s...")
        raise ValueError
        # self.SendCPTDDaily.change_interval(seconds=TimeTillMidnight())

    @SendCPTDDaily.before_loop
    async def RegulateBeforeCPTDLoop(self):
        await self.DClient.wait_until_ready()
        print("CPTD Regulating...")
        # StaffChannel = self.DClient.get_channel(795080325020909598)
        # await self.StaffChannel.send(f"CPTD Regulating for {TimeTillMidnight()}s...")
        await asyncio.sleep(TimeTillMidnight())

    #? @tasks.loop(seconds=TimeTillMidnight())
    #? async def SendQOTDDaily(self):
    #?     print("Sending QOTD...")
    #?     # StaffChannel = self.DClient.get_channel(795080325020909598)
    #?     await self.StaffChannel.send("Sending QOTD...")
    #?     TierApplicable = {"Tier 2 Super": 1, "Tier 3 Legend": 2, "Tier 4 Ultimate": 4}
    #?     QOTDEm = MakeQOTDEmbed()
    #?     QOTDUsers = AQd.find({"Type": "QOTD"})
    #?     ToBeRemoved = []
    #?     for User in QOTDUsers:
    #?         UserID = User["IDd"]
    #?         ChannelID = User["Channel"]
    #?         if ChPatreonUserT2(UserID):
    #?             TierLimit = TierApplicable[GetPatreonTier(UserID)]
    #?             if AQd.count_documents({"Type": "QOTD", "IDd": UserID}) > TierLimit:
    #?                 QOTDTempUsers = AQd.find({"Type": "QOTD", "IDd": UserID})
    #?                 Num = 0
    #?                 for TempUser in QOTDTempUsers:
    #?                     Num += 1
    #?                     if Num > TierLimit:
    #?                         ToBeRemoved.append(
    #?                             TempUser
    #?                         ) if TempUser not in ToBeRemoved else ToBeRemoved
    #?             Channel = self.DClient.get_channel(ChannelID)
    #?             if User not in ToBeRemoved:
    #?                 if Channel is None:
    #?                     AQd.delete_one(User)
    #?                 else:
    #?                     await Channel.send(embed=QOTDEm)
    #?             else:
    #?                 await Channel.send(
    #?                     "NO LONGER APPLICABLE TO THIS MANY CHANNELS. Daily QOTD stopped. :pensive: You can resign up for patreon, check zpatreon"
    #?                 )
    #?                 AQd.delete_one(User)
    #?         else:
    #?             await Channel.send(
    #?                 "NO LONGER A PATREON. Daily QOTD stopped. :pensive: You can resign up for patreon, check zpatreon"
    #?             )
    #?     await self.StaffChannel.send(f"Next QOTD in {TimeTillMidnight()}s...")
    #?     raise ValueError
    #?     self.SendQOTDDaily.change_interval(seconds=TimeTillMidnight())

    #? @SendQOTDDaily.before_loop
    #? async def RegulateBeforeQOTDLoop(self):
    #?     await self.DClient.wait_until_ready()
    #?     print("QOTD Regulating...")
    #?     # StaffChannel = self.DClient.get_channel(795080325020909598)
    #?     await self.StaffChannel.send(f"QOTD Regulating for {TimeTillMidnight()}s...")
    #?     await asyncio.sleep(TimeTillMidnight())


def setup(DClient):
    DClient.add_cog(MainEvents(DClient))