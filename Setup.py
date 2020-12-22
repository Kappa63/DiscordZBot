from dotenv import load_dotenv
import os
from discord.ext import commands
import discord
import giphy_client
import tweepy
import malclient
import COVID19Py
import imgurpython
import praw
import pymongo
import CBot
from pymongo import MongoClient
import pyyoutube
import imdb
import pafy

load_dotenv()

Mdb = os.getenv("MONGODB_URL")
Cls = MongoClient(Mdb)
DbM = Cls["CBot"]   
Col = DbM["Ser"]
Colvt = DbM["Vts"]

GClient = os.getenv("GIPHY_KEY")
GApi = giphy_client.DefaultApi()

MClient = malclient.Client()
MClient.init(access_token=os.getenv("MAL_ACCESS_TOKEN"))
MClient.refresh_bearer_token(
    client_id=os.getenv("MAL_ID"),
    client_secret=os.getenv("MAL_SECRET"),
    refresh_token=os.getenv("MAL_REFRESH_TOKEN"),
)

twitter = tweepy.OAuthHandler(os.getenv("TWITTER_KEY"), os.getenv("TWITTER_SECRET"))
twitter.set_access_token(
    os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_SECRET")
)
Twitter = tweepy.API(twitter)

Reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_ID"),
    client_secret=os.getenv("REDDIT_SECRET"),
    user_agent="ZBot by u/Kamlin333",
)

Covid = COVID19Py.COVID19(data_source="jhu")

Imgur = imgurpython.ImgurClient(
    client_id=os.getenv("IMGUR_ID"), client_secret=os.getenv("IMGUR_SECRET")
)

YClient = pyyoutube.Api(api_key=os.getenv("YOUTUBE_KEY"))

IMClient = imdb.IMDb()

def RemoveExtra(listRm, val):
    return [value for value in listRm if value != val]


def GetVidDuration(VidId):
    Vid = pafy.new(f"https://www.youtube.com/watch?v={VidId}")
    return Vid.duration


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


class IsSetup(commands.CheckFailure):
    pass


def ChSer(ctx):
    if (
        Col.count_documents(
            {"IDd": "GuildInfo", "IDg": str(ctx.guild.id), "Setup": "Done"}
        )
        != 0
    ):
        return True
    raise IsSetup("Unready")


class IsAdmin(commands.CheckFailure):
    pass


def ChAdmin(ctx):
    if ctx.author.guild_permissions.administrator:
        return True
    raise IsAdmin("Normie")


class IsVote(commands.CheckFailure):
    pass


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


class IsPatreon(commands.CheckFailure):
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