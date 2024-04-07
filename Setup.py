from dotenv import load_dotenv
import os
from discord.ext import commands
import discord
# import giphy_client
# import tweepy
# import malclient
# import COVID19Py
# import twitch
import asyncio
import praw
# import pymongo
# from pymongo import MongoClient
import CBot
# from google_images_search import GoogleImagesSearch
# import pyyoutube
from imdby.imdb import imdb as IMClient
# import pafy
import datetime
# import osuapi
import concurrent.futures as Cf
# from ro_py import Client as Roblox

load_dotenv()
Cogs = ["Cogs.Randomizers", "Cogs.MainEvents", "Cogs.Rule34", "Cogs.AnimeManga", 
        #  "Cogs.HelpInfo", 
        "Cogs.Socials", "Cogs.OnlyMods", "Cogs.Nasa", "Cogs.Movies", "Cogs.Misc", "Cogs.Images"]

# Cls = MongoClient(os.getenv("MONGODB_URL"))
# DbM = Cls["CBot"]
# ColT = DbM["SerTwo"]
# AQd = DbM["Daily"]
# Rdt = DbM["Reddit"]

# GClient = os.getenv("GIPHY_KEY")
# GApi = giphy_client.DefaultApi()

CClient = {"X-CMC_PRO_API_KEY": os.getenv("COINBASE_KEY")}

# NClient = {"country": "us", "apiKey": os.getenv("NEWS_KEY")}

# GiClient = GoogleImagesSearch(os.getenv("GCS_KEY"), os.getenv("CX_ID"))

# MClient = malclient.Client()
# MClient.init(access_token=os.getenv("MAL_ACCESS_TOKEN"))
# MClient.refresh_bearer_token(client_id=os.getenv("MAL_ID"), client_secret=os.getenv("MAL_SECRET"), refresh_token=os.getenv("MAL_REFRESH_TOKEN"))

# PClient = {"Authorization": os.getenv("PUBG_KEY"), "accept": "application/vnd.api+json"}

# twitter = tweepy.OAuthHandler(os.getenv("TWITTER_KEY"), os.getenv("TWITTER_SECRET"))
# twitter.set_access_token(os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_SECRET"))
# Twitter = tweepy.API(twitter)

Reddit = praw.Reddit(client_id=os.getenv("REDDIT_ID"), client_secret=os.getenv("REDDIT_SECRET"), user_agent="ZBot by u/Kamlin333", check_for_async=False)

# Covid = COVID19Py.COVID19()

# YClient = pyyoutube.Api(api_key=os.getenv("YOUTUBE_KEY"))

# THelix = twitch.Helix(os.getenv("TWITCH_ID"), os.getenv("TWITCH_SECRET"), use_cache=True, cache_duration=datetime.timedelta(minutes=3))

# IMClient = imdb

# OClient = osuapi.OsuApi(os.getenv("OSU_KEY"), connector=osuapi.ReqConnector())

# RLox = Roblox(os.getenv("ROBLOX_SECRET"))

PatreonTiers = {
    783250729686532126: "Tier 1 Casual",
    783256987655340043: "Tier 2 Super",
    784123230372757515: "Tier 3 Legend",
    784124034559377409: "Tier 4 Ultimate",
}

RemoveExtra = lambda listRm, val: [value for value in listRm if value != val]

# GetVidDuration = lambda VidId: pafy.new(f"https://www.youtube.com/watch?v={VidId}").duration

async def SendWait(ctx, Notice): await ctx.message.channel.send(embed=discord.Embed(title=Notice))

def TimeTillMidnight():
    Now = datetime.datetime.now()
    return (10 + ((24 - Now.hour - 1) * 60 * 60) + ((60 - Now.minute - 1) * 60) + (60 - Now.second))

def Threader(FunctionList, ParameterList):
    with Cf.ThreadPoolExecutor() as Execute:
        Pool = [Execute.submit(Func, *Param) for Func, Param in zip(FunctionList, ParameterList)]
        Results = [Execution.result() for Execution in Pool]
    return Results

# def RefreshGISClient():
#     global GiClient
#     del GiClient
#     GiClient = GoogleImagesSearch(os.getenv("GCS_KEY"), os.getenv("CX_ID"))

# def ErrorEmbeds(Type):
#     Descs = {"Vote": "This command is only for voters or patreon! [Official Server](https://discord.gg/V6E6prUBPv) / [Patreon](https://www.patreon.com/join/ZBotDiscord) / [Vote](https://top.gg/bot/768397640140062721/vote)",
#              "Patreon": "This command is only for patreons supporters! [Official Server](https://discord.gg/V6E6prUBPv) / [Patreon](https://www.patreon.com/join/ZBotDiscord)",
#              "PatreonT2": "This command is only for Tier 2 patreons (Super) supporters or above! [Official Server](https://discord.gg/V6E6prUBPv) / [Patreon](https://www.patreon.com/join/ZBotDiscord)",
#              "PatreonT3": "This command is only for Tier 3 patreons (Legend) supporters or above! [Official Server](https://discord.gg/V6E6prUBPv) / [Patreon](https://www.patreon.com/join/ZBotDiscord)",
#              "PatreonT4": "This command is only for Tier 4 patreons (Ultimate) supporters or above! [Official Server](https://discord.gg/V6E6prUBPv) / [Patreon](https://www.patreon.com/join/ZBotDiscord)"}
#     return discord.Embed(title="Oops",description= Descs[Type])

# def GetPatreonTier(UserID):
#     try:
#         MemGuild = CBot.DClient.get_guild(783250489843384341)
#         Mem = MemGuild.get_member(UserID)
#         Roles = [discord.utils.get(MemGuild.roles, id=783250729686532126), discord.utils.get(MemGuild.roles, id=783256987655340043),
#                  discord.utils.get(MemGuild.roles, id=784123230372757515), discord.utils.get(MemGuild.roles, id=784124034559377409)]
#         for Role in Roles:
#             if Role in Mem.roles: return PatreonTiers[Role.id]
#     except AttributeError: pass

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
    if Day != 0: return f"{Day}d {Hour}h {Min}m {SecondsFormat}s"
    elif Hour != 0: return f"{Hour}h {Min}m {SecondsFormat}s"
    elif Min != 0: return f"{Min}m {SecondsFormat}s"
    else: return f"{SecondsFormat}s"

async def Navigator(ctx, Items, Type="#", EmbedAndContent=False, ContItems=None, Main=False, MainBed=None):
    # ChCHEm = lambda RcM, RuS: (not RuS.bot) and RcM.message == Nav and str(RcM.emoji) in ["⬅️", "❌", "➡️", "#️⃣"]

    def ChCHEmFN(MSg):
        MesS = MSg.content.lower()
        RsT = False
        try:
            if int(MSg.content): RsT = True
        except ValueError:
            if MesS in ["cancel", "c"]: RsT = True
        return MSg.guild.id == ctx.guild.id and MSg.channel.id == ctx.channel.id and RsT

    ItemNum = 0
    if not Main: Nav = await ctx.message.channel.send(embed=Items[ItemNum])
    else: Nav = await ctx.message.channel.send(embed=MainBed)
    if EmbedAndContent: Cont = await ctx.message.channel.send(content=ContItems[ItemNum])
    TotalItems = len(Items)
    await Nav.add_reaction("⬅️")
    await Nav.add_reaction("❌")
    await Nav.add_reaction("➡️")
    if Type == "#": await Nav.add_reaction("#️⃣")
    while True:
        try:
            Res = await CBot.BotClient.wait_for("reaction_add", timeout=120)
            await Nav.remove_reaction(Res[0].emoji, Res[1])
            if Res[0].emoji == "⬅️":
                if ItemNum:
                    ItemNum -= 1
                    await Nav.edit(embed=Items[ItemNum])
                    if EmbedAndContent: await Cont.edit(content=ContItems[ItemNum])
                elif MainBed: await Nav.edit(embed=MainBed); Main = True

            elif Res[0].emoji == "➡️":
                if ItemNum < TotalItems - 1:
                    if Main: await Nav.edit(embed=Items[ItemNum]); Main = False
                    else:
                        ItemNum += 1
                        await Nav.edit(embed=Items[ItemNum])
                        if EmbedAndContent: await Cont.edit(content=ContItems[ItemNum])
                else:
                    await Nav.remove_reaction("⬅️", CBot.BotClient.user)
                    await Nav.remove_reaction("❌", CBot.BotClient.user)
                    await Nav.remove_reaction("➡️", CBot.BotClient.user)
                    if Type == "#": await Nav.remove_reaction("#️⃣", CBot.BotClient.user)
                    break
            elif Res[0].emoji == "#️⃣" and Type == "#":
                # if await ChVoteUser(Res[1].id):
                TempNG = await ctx.message.channel.send('Choose a number to open navigate to ItemNum. "c" or "cancel" to exit navigation.')
                try:
                    ResE = await CBot.BotClient.wait_for("message", check=ChCHEmFN, timeout=10)
                    await TempNG.delete()
                    await ResE.delete()
                    try:
                        pG = int(ResE.content)
                        if 0 < pG <= TotalItems - 1: ItemNum = pG - 1
                        elif pG < 1:
                            ItemNum = 0
                            pass
                        else: ItemNum = TotalItems - 1
                    except: pass
                    await Nav.edit(embed=Items[ItemNum])
                    if EmbedAndContent: await Cont.edit(content=ContItems[ItemNum])
                except asyncio.TimeoutError:
                    await TempNG.edit("Request Timeout")
                    await asyncio.sleep(5)
                    await TempNG.delete()
                # else: await ctx.message.channel.send(embed=ErrorEmbeds("Vote"))
            elif Res[0].emoji == "❌":
                await Nav.remove_reaction("⬅️", CBot.BotClient.user)
                await Nav.remove_reaction("❌", CBot.BotClient.user)
                await Nav.remove_reaction("➡️", CBot.BotClient.user)
                if Type == "#": await Nav.remove_reaction("#️⃣", CBot.BotClient.user)
                break
        except asyncio.TimeoutError:
            await Nav.remove_reaction("⬅️", CBot.BotClient.user)
            await Nav.remove_reaction("❌", CBot.BotClient.user)
            await Nav.remove_reaction("➡️", CBot.BotClient.user)
            if Type == "#": await Nav.remove_reaction("#️⃣", CBot.BotClient.user)
            break


# class IsSetup(commands.CheckFailure): pass
# def ChSer(ctx):
#     if ColT.count_documents({"IDg": str(ctx.guild.id)}): return True
#     raise IsSetup("Unready")
# ChSerGuild = lambda guild: ColT.count_documents({"IDg": str(guild.id)})


# class IsMultiredditLimit(commands.CheckFailure): pass
# def ChMaxMultireddits(ctx):
#     TierApplicable = {"Tier 2 Super": 1, "Tier 3 Legend": 2, "Tier 4 Ultimate": 4}
#     TierLimit = TierApplicable[GetPatreonTier(ctx.author.id)]
#     if Rdt.count_documents({"IDd": ctx.author.id}):
#         User = Rdt.find({"IDd": ctx.author.id})[0]
#         if len(User)-2 > TierLimit: raise IsMultiredditLimit("Too much")
#     return True


# class IsAdmin(commands.CheckFailure): pass
# def ChAdmin(ctx):
#     if ctx.author.guild_permissions.administrator: return True
#     raise IsAdmin("Normie")


# class IsVote(commands.CheckFailure): pass
# async def ChVote(ctx):
#     if await CBot.TClient.get_user_vote(ctx.author.id): return True
#     else:
#         try:
#             MemGuild = CBot.DClient.get_guild(783250489843384341)
#             Mem = MemGuild.get_member(ctx.author.id)
#             Roles = [discord.utils.get(MemGuild.roles, id=783250729686532126), discord.utils.get(MemGuild.roles, id=783256987655340043),
#                      discord.utils.get(MemGuild.roles, id=784123230372757515), discord.utils.get(MemGuild.roles, id=784124034559377409)]
#             #- Roles.append(discord.utils.get(MemGuild.roles, id=783250729686532126))
#             #- Roles.append(discord.utils.get(MemGuild.roles, id=783256987655340043))
#             #- Roles.append(discord.utils.get(MemGuild.roles, id=784123230372757515))
#             #- Roles.append(discord.utils.get(MemGuild.roles, id=784124034559377409))
#             for Role in Roles:
#                 if Role in Mem.roles: return True
#         except AttributeError: pass
#         raise IsVote("No Vote")
# async def ChVoteUser(UserID):
#     if await CBot.TClient.get_user_vote(UserID): return True
#     else:
#         try:
#             MemGuild = CBot.DClient.get_guild(783250489843384341)
#             Mem = MemGuild.get_member(UserID)
#             Roles = [discord.utils.get(MemGuild.roles, id=783250729686532126), discord.utils.get(MemGuild.roles, id=783256987655340043),
#                      discord.utils.get(MemGuild.roles, id=784123230372757515), discord.utils.get(MemGuild.roles, id=784124034559377409)]
#             for Role in Roles:
#                 if Role in Mem.roles: return True
#         except AttributeError: pass
#         return False


# class IsPatreon(commands.CheckFailure): pass
# def ChPatreon(ctx):
#     try:
#         MemGuild = CBot.DClient.get_guild(783250489843384341)
#         Mem = MemGuild.get_member(ctx.author.id)
#         Roles = [discord.utils.get(MemGuild.roles, id=783250729686532126), discord.utils.get(MemGuild.roles, id=783256987655340043),
#                  discord.utils.get(MemGuild.roles, id=784123230372757515), discord.utils.get(MemGuild.roles, id=784124034559377409)]
#         for Role in Roles:
#             if Role in Mem.roles: return True
#     except AttributeError: pass
#     raise IsPatreon("Not Patreon")
# def ChPatreonUser(UserID):
#     try:
#         MemGuild = CBot.DClient.get_guild(783250489843384341)
#         Mem = MemGuild.get_member(UserID)
#         Roles = [discord.utils.get(MemGuild.roles, id=783250729686532126), discord.utils.get(MemGuild.roles, id=783256987655340043),
#                  discord.utils.get(MemGuild.roles, id=784123230372757515), discord.utils.get(MemGuild.roles, id=784124034559377409)]
#         for Role in Roles:
#             if Role in Mem.roles: return True
#     except AttributeError: pass
#     return False


# class IsPatreonT2(commands.CheckFailure): pass
# def ChPatreonT2(ctx):
#     try:
#         MemGuild = CBot.DClient.get_guild(783250489843384341)
#         Mem = MemGuild.get_member(ctx.author.id)
#         Roles = [discord.utils.get(MemGuild.roles, id=783256987655340043), discord.utils.get(MemGuild.roles, id=784123230372757515), 
#                  discord.utils.get(MemGuild.roles, id=784124034559377409)]
#         for Role in Roles:
#             if Role in Mem.roles: return True
#     except AttributeError: pass
#     raise IsPatreonT2("Not Patreon")
# def ChPatreonUserT2(UserID):
#     try:
#         MemGuild = CBot.DClient.get_guild(783250489843384341)
#         Mem = MemGuild.get_member(UserID)
#         Roles = [discord.utils.get(MemGuild.roles, id=783256987655340043), discord.utils.get(MemGuild.roles, id=784123230372757515), 
#                  discord.utils.get(MemGuild.roles, id=784124034559377409)]
#         for Role in Roles:
#             if Role in Mem.roles: return True
#     except AttributeError: pass
#     return False


# class IsPatreonT3(commands.CheckFailure): pass
# def ChPatreonT3(ctx):
#     try:
#         MemGuild = CBot.DClient.get_guild(783250489843384341)
#         Mem = MemGuild.get_member(ctx.author.id)
#         Roles = [discord.utils.get(MemGuild.roles, id=784123230372757515), discord.utils.get(MemGuild.roles, id=784124034559377409)]
#         for Role in Roles:
#             if Role in Mem.roles: return True
#     except AttributeError: pass
#     raise IsPatreonT3("Not Patreon")
# def ChPatreonUserT3(UserID):
#     try:
#         MemGuild = CBot.DClient.get_guild(783250489843384341)
#         Mem = MemGuild.get_member(UserID)
#         Roles = [discord.utils.get(MemGuild.roles, id=784123230372757515), discord.utils.get(MemGuild.roles, id=784124034559377409)]
#         for Role in Roles:
#             if Role in Mem.roles: return True
#     except AttributeError: pass
#     return False


# class IsPatreonT4(commands.CheckFailure): pass
# def ChPatreonT4(ctx):
#     try:
#         MemGuild = CBot.DClient.get_guild(783250489843384341)
#         Mem = MemGuild.get_member(ctx.author.id)
#         Role = discord.utils.get(MemGuild.roles, id=784124034559377409)
#         if Role in Mem.roles: return True
#     except AttributeError: pass
#     raise IsPatreonT4("Not Patreon")
# def ChPatreonUserT4(UserID):
#     try:
#         MemGuild = CBot.DClient.get_guild(783250489843384341)
#         Mem = MemGuild.get_member(UserID)
#         Role = discord.utils.get(MemGuild.roles, id=784124034559377409)
#         if Role in Mem.roles: return True
#     except AttributeError: pass
#     return False


# class Ignore(commands.CheckFailure): pass
# def ChDev(ctx):
#     if ctx.author.id == 443986051371892746: return True
#     raise Ignore("Ignore")


# class IsNSFW(commands.CheckFailure): pass
# def ChNSFW(ctx):
#     if ctx.channel.is_nsfw(): return True
#     raise IsNSFW("Not Safe")


# class IsBot(commands.CheckFailure): pass