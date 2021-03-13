from dotenv import load_dotenv
import os
from discord.ext import commands
import discord
import giphy_client
import tweepy
import malclient
import COVID19Py
#- import imgurpython
import praw
import pymongo
import CBot
from pymongo import MongoClient
from google_images_search import GoogleImagesSearch
import pyyoutube
import imdb
import pafy
import datetime
import osuapi
import concurrent.futures as Cf

load_dotenv()

Cls = MongoClient(os.getenv("MONGODB_URL"))
DbM = Cls["CBot"]
Col = DbM["Ser"]
ColT = DbM["SerTwo"]
AQd = DbM["Daily"]
Rdt = DbM["Reddit"]

GClient = os.getenv("GIPHY_KEY")
GApi = giphy_client.DefaultApi()

CClient = {"X-CMC_PRO_API_KEY": os.getenv("COINBASE_KEY")}

GiClient = GoogleImagesSearch(os.getenv("GCS_KEY"), os.getenv("CX_ID"))

MClient = malclient.Client()
MClient.init(access_token=os.getenv("MAL_ACCESS_TOKEN"))
MClient.refresh_bearer_token(
    client_id=os.getenv("MAL_ID"),
    client_secret=os.getenv("MAL_SECRET"),
    refresh_token=os.getenv("MAL_REFRESH_TOKEN"),
)

PClient = {"Authorization": os.getenv("PUBG_KEY"), "accept": "application/vnd.api+json"}

twitter = tweepy.OAuthHandler(os.getenv("TWITTER_KEY"), os.getenv("TWITTER_SECRET"))
twitter.set_access_token(
    os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_SECRET")
)
Twitter = tweepy.API(twitter)

Reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_ID"),
    client_secret=os.getenv("REDDIT_SECRET"),
    user_agent="ZBot by u/Kamlin333",
    check_for_async=False,
)

Covid = COVID19Py.COVID19(data_source="jhu")

#- Imgur = imgurpython.ImgurClient(
#-     client_id=os.getenv("IMGUR_ID"), client_secret=os.getenv("IMGUR_SECRET")
#- )

YClient = pyyoutube.Api(api_key=os.getenv("YOUTUBE_KEY"))

IMClient = imdb.IMDb()

OClient = osuapi.OsuApi(os.getenv("OSU_KEY"), connector=osuapi.ReqConnector())


async def SendWait(ctx, Notice):
    await ctx.message.channel.send(embed=discord.Embed(title=Notice))


def RemoveExtra(listRm, val):
    return [value for value in listRm if value != val]


def GetVidDuration(VidId):
    Vid = pafy.new(f"https://www.youtube.com/watch?v={VidId}")
    return Vid.duration


def TimeTillMidnight():
    Now = datetime.datetime.now()
    Time = (
        10
        + ((24 - Now.hour - 1) * 60 * 60)
        + ((60 - Now.minute - 1) * 60)
        + (60 - Now.second)
    )
    return Time


def FormatTime(SecondsFormat):
    Day = 0
    Hour = 0
    Min = 0
    while SecondsFormat >= 60:
        Min += 1
        if Min == 60:
            Hour += 1
            Min -= 60
        if Hour == 24:
            Day += 1
            Hour -= 24
        SecondsFormat -= 60
    if Day != 0:
        return f"{Day}Day(s) {Hour}Hour(s) {Min}Min(s) {SecondsFormat}Sec(s)"
    elif Hour != 0:
        return f"{Hour}Hour(s) {Min}Min(s) {SecondsFormat}Sec(s)"
    elif Min != 0:
        return f"{Min}Min(s) {SecondsFormat}Sec(s)"
    else:
        return f"{SecondsFormat}Sec(s)"


def Threader(FunctionList, ParameterList):
    with Cf.ThreadPoolExecutor() as Execute:
        Pool = [
            Execute.submit(Func, *Param)
            for Func, Param in zip(FunctionList, ParameterList)
        ]
        Results = [Execution.result() for Execution in Pool]
    return Results


class IsSetup(commands.CheckFailure):
    pass


def ChSer(ctx):
    if ColT.count_documents({"IDg": str(ctx.guild.id)}):
        return True
    raise IsSetup("Unready")

    #!! DEPRECATED Server Check
    #! if (
    #!     Col.count_documents(
    #!         {"IDd": "GuildInfo", "IDg": str(ctx.guild.id), "Setup": "Done"}
    #!     )
    #!     != 0
    #! ):
    #!     return True
    #! raise IsSetup("Unready")

def ChSerGuild(guild):
    if ColT.count_documents({"IDg": str(guild.id)}):
        return True
    return False

class IsMultiredditLimit(commands.CheckFailure):
    pass


def ChMaxMultireddits(ctx):
    TierApplicable = {"Tier 2 Super": 1, "Tier 3 Legend": 2, "Tier 4 Ultimate": 4}
    TierLimit = TierApplicable[GetPatreonTier(ctx.author.id)]
    if Rdt.count_documents({"IDd": ctx.author.id}) > 0:
        User = Rdt.find({"IDd": ctx.author.id})[0]
        Multireddits = User.keys()
        if len(Multireddits) > TierLimit:
            raise IsMultiredditLimit("Too much")
    return True


class IsAdmin(commands.CheckFailure):
    pass


def ChAdmin(ctx):
    if ctx.author.guild_permissions.administrator:
        return True
    raise IsAdmin("Normie")


class IsVote(commands.CheckFailure):
    pass


def ErrorEmbeds(Type):
    if Type == "Vote":
        return discord.Embed(
            title="Oops",
            description="This command is only for voters or patreon! [Official Server](https://discord.gg/V6E6prUBPv) / [Patreon](https://www.patreon.com/join/ZBotDiscord) / [Vote](https://top.gg/bot/768397640140062721/vote)",
        )
    elif Type == "Patreon":
        return discord.Embed(
            title="Oops",
            description="This command is only for patreons supporters! [Official Server](https://discord.gg/V6E6prUBPv) / [Patreon](https://www.patreon.com/join/ZBotDiscord)",
        )
    elif Type == "PatreonT2":
        return discord.Embed(
            title="Oops",
            description="This command is only for Tier 2 patreons (Super) supporters or above! [Official Server](https://discord.gg/V6E6prUBPv) / [Patreon](https://www.patreon.com/join/ZBotDiscord)",
        )
    elif Type == "PatreonT3":
        return discord.Embed(
            title="Oops",
            description="This command is only for Tier 3 patreons (Legend) supporters or above! [Official Server](https://discord.gg/V6E6prUBPv) / [Patreon](https://www.patreon.com/join/ZBotDiscord)",
        )
    elif Type == "PatreonT4":
        return discord.Embed(
            title="Oops",
            description="This command is only for Tier 4 patreons (Ultimate) supporters or above! [Official Server](https://discord.gg/V6E6prUBPv) / [Patreon](https://www.patreon.com/join/ZBotDiscord)",
        )


async def ChVote(ctx):
    if await CBot.TClient.get_user_vote(ctx.author.id):
        return True
    else:
        try:
            MemGuild = CBot.DClient.get_guild(783250489843384341)
            Mem = MemGuild.get_member(ctx.author.id)
            Roles = []
            Roles.append(discord.utils.get(MemGuild.roles, id=783250729686532126))
            Roles.append(discord.utils.get(MemGuild.roles, id=783256987655340043))
            Roles.append(discord.utils.get(MemGuild.roles, id=784123230372757515))
            Roles.append(discord.utils.get(MemGuild.roles, id=784124034559377409))
            for Role in Roles:
                if Role in Mem.roles:
                    return True
        except AttributeError:
            pass
        raise IsVote("No Vote")


async def ChVoteUser(UserID):
    if await CBot.TClient.get_user_vote(UserID):
        return True
    else:
        try:
            MemGuild = CBot.DClient.get_guild(783250489843384341)
            Mem = MemGuild.get_member(UserID)
            Roles = []
            Roles.append(discord.utils.get(MemGuild.roles, id=783250729686532126))
            Roles.append(discord.utils.get(MemGuild.roles, id=783256987655340043))
            Roles.append(discord.utils.get(MemGuild.roles, id=784123230372757515))
            Roles.append(discord.utils.get(MemGuild.roles, id=784124034559377409))
            for Role in Roles:
                if Role in Mem.roles:
                    return True
        except AttributeError:
            pass
        raise IsVote("No Vote")


class IsPatreon(commands.CheckFailure):
    pass


class IsPatreonT2(commands.CheckFailure):
    pass


class IsPatreonT3(commands.CheckFailure):
    pass


class IsPatreonT4(commands.CheckFailure):
    pass


PatreonTiers = {
    783250729686532126: "Tier 1 Casual",
    783256987655340043: "Tier 2 Super",
    784123230372757515: "Tier 3 Legend",
    784124034559377409: "Tier 4 Ultimate",
}


def GetPatreonTier(UserID):
    try:
        MemGuild = CBot.DClient.get_guild(783250489843384341)
        Mem = MemGuild.get_member(UserID)
        Roles = []
        Roles.append(discord.utils.get(MemGuild.roles, id=783250729686532126))
        Roles.append(discord.utils.get(MemGuild.roles, id=783256987655340043))
        Roles.append(discord.utils.get(MemGuild.roles, id=784123230372757515))
        Roles.append(discord.utils.get(MemGuild.roles, id=784124034559377409))
        for Role in Roles:
            if Role in Mem.roles:
                return PatreonTiers[Role.id]
    except AttributeError:
        pass


def ChPatreon(ctx):
    try:
        MemGuild = CBot.DClient.get_guild(783250489843384341)
        Mem = MemGuild.get_member(ctx.author.id)
        Roles = []
        Roles.append(discord.utils.get(MemGuild.roles, id=783250729686532126))
        Roles.append(discord.utils.get(MemGuild.roles, id=783256987655340043))
        Roles.append(discord.utils.get(MemGuild.roles, id=784123230372757515))
        Roles.append(discord.utils.get(MemGuild.roles, id=784124034559377409))
        for Role in Roles:
            if Role in Mem.roles:
                return True
    except AttributeError:
        pass
    raise IsPatreon("Not Patreon")


def ChPatreonUser(UserID):
    try:
        MemGuild = CBot.DClient.get_guild(783250489843384341)
        Mem = MemGuild.get_member(UserID)
        Roles = []
        Roles.append(discord.utils.get(MemGuild.roles, id=783250729686532126))
        Roles.append(discord.utils.get(MemGuild.roles, id=783256987655340043))
        Roles.append(discord.utils.get(MemGuild.roles, id=784123230372757515))
        Roles.append(discord.utils.get(MemGuild.roles, id=784124034559377409))
        for Role in Roles:
            if Role in Mem.roles:
                return True
    except AttributeError:
        pass
    return False


def ChPatreonT2(ctx):
    try:
        MemGuild = CBot.DClient.get_guild(783250489843384341)
        Mem = MemGuild.get_member(ctx.author.id)
        Roles = []
        Roles.append(discord.utils.get(MemGuild.roles, id=783256987655340043))
        Roles.append(discord.utils.get(MemGuild.roles, id=784123230372757515))
        Roles.append(discord.utils.get(MemGuild.roles, id=784124034559377409))
        for Role in Roles:
            if Role in Mem.roles:
                return True
    except AttributeError:
        pass
    raise IsPatreonT2("Not Patreon")


def ChPatreonUserT2(UserID):
    try:
        MemGuild = CBot.DClient.get_guild(783250489843384341)
        Mem = MemGuild.get_member(UserID)
        Roles = []
        Roles.append(discord.utils.get(MemGuild.roles, id=783256987655340043))
        Roles.append(discord.utils.get(MemGuild.roles, id=784123230372757515))
        Roles.append(discord.utils.get(MemGuild.roles, id=784124034559377409))
        for Role in Roles:
            if Role in Mem.roles:
                return True
    except AttributeError:
        pass
    return False


def ChPatreonT3(ctx):
    try:
        MemGuild = CBot.DClient.get_guild(783250489843384341)
        Mem = MemGuild.get_member(ctx.author.id)
        Roles = []
        Roles.append(discord.utils.get(MemGuild.roles, id=784123230372757515))
        Roles.append(discord.utils.get(MemGuild.roles, id=784124034559377409))
        for Role in Roles:
            if Role in Mem.roles:
                return True
    except AttributeError:
        pass
    raise IsPatreonT3("Not Patreon")


def ChPatreonUserT3(UserID):
    try:
        MemGuild = CBot.DClient.get_guild(783250489843384341)
        Mem = MemGuild.get_member(UserID)
        Roles = []
        Roles.append(discord.utils.get(MemGuild.roles, id=784123230372757515))
        Roles.append(discord.utils.get(MemGuild.roles, id=784124034559377409))
        for Role in Roles:
            if Role in Mem.roles:
                return True
    except AttributeError:
        pass
    return False


def ChPatreonT4(ctx):
    try:
        MemGuild = CBot.DClient.get_guild(783250489843384341)
        Mem = MemGuild.get_member(ctx.author.id)
        Roles = []
        Roles.append(discord.utils.get(MemGuild.roles, id=784124034559377409))
        for Role in Roles:
            if Role in Mem.roles:
                return True
    except AttributeError:
        pass
    raise IsPatreonT4("Not Patreon")


def ChPatreonUserT4(UserID):
    try:
        MemGuild = CBot.DClient.get_guild(783250489843384341)
        Mem = MemGuild.get_member(UserID)
        Roles = []
        Roles.append(discord.utils.get(MemGuild.roles, id=784124034559377409))
        for Role in Roles:
            if Role in Mem.roles:
                return True
    except AttributeError:
        pass
    return False


class IsBot(commands.CheckFailure):
    pass


class Ignore(commands.CheckFailure):
    pass


def ChDev(ctx):
    if ctx.author.id == 443986051371892746:
        return True
    raise Ignore("Ignore")


class IsNSFW(commands.CheckFailure):
    pass


def ChNSFW(ctx):
    if ctx.channel.is_nsfw():
        return True
    raise IsNSFW("Not Safe")