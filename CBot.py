import discord
from discord.ext import commands
import praw
import random
import pymongo
from pymongo import MongoClient
import dbl
import giphy_client
import tweepy
import malclient
import COVID19Py
import imgurpython
# import asyncio
# from PIL import Image
# import requests
# import datetime
# from pdf2image import convert_from_path
# import FuncMon
# import os  
# import numpy
# import cv2
# from prawcore import NotFound, Forbidden
# from hentai import Utils, Sort, Hentai, Format
# import mal

Mdb = "mongodb+srv://Kappa:85699658@cbotdb.exsit.mongodb.net/CBot?retryWrites=true&w=majority"
Cls = MongoClient(Mdb)
DbM = Cls["CBot"]
Col = DbM["Ser"]
Colvt = DbM["Vts"]

GClient = "ZH1xoGH0XUffrtqFKdj3kD4YrVoZvb8i"
GApi = giphy_client.DefaultApi()

MClient = malclient.Client()
MClient.init(access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImY5OWNmNDExZjY5NDMwMGY0ZjcwMDAyM2JlOTYyYTkyYjQxYzUwNGQ0NzA0MzQyOWYxMjEyZmNkOTBmNWNiZjlkNmFmZWNkYWRmMTViMzdjIn0.eyJhdWQiOiIyYjcwMWQzNjY5NzFmYTFmMTgyYmZkNTBkMTUxNzJhZSIsImp0aSI6ImY5OWNmNDExZjY5NDMwMGY0ZjcwMDAyM2JlOTYyYTkyYjQxYzUwNGQ0NzA0MzQyOWYxMjEyZmNkOTBmNWNiZjlkNmFmZWNkYWRmMTViMzdjIiwiaWF0IjoxNjA1MTc4ODM5LCJuYmYiOjE2MDUxNzg4MzksImV4cCI6MTYwNzc3MDgzOSwic3ViIjoiNzQ5Njc5MSIsInNjb3BlcyI6W119.B8X86ggNC43bZwzKF6993WSnY1AUGQ2wgdxbL2kRhGPJAm4M3epzbTixTxxs3RmWOsUfypoU3U2vnlYs69enzwsdGxzpoLh-hO_Mav4kSTxeXqrvPk23_7fSyC1Q8AOFE_EszhI6DG67BcFAZWVdgFia8th6vZ_7HTugWd9dDrf1PIBDfNrpWrsTs1tUImTbsZ41Y_19uT2p3-oTpmQY_YwSbLxgzkdVZmASWdDkXyFjTNnYW5y_fCDYQrDJrNrId5Dvm1N02d66TNaJgyDn86L0Dr-lYqjU9qM45agHff4T8MpkIzqzA3pKT874QUOW5QXks46-9JaCCpSB-nIrfQ")
MClient.refresh_bearer_token(client_id = "2b701d366971fa1f182bfd50d15172ae", client_secret = "e01505a84d5e611e2e59b66f0dc245888656104b1529e1a25954d8ff51780f5c", refresh_token = "def50200b66cd79fef2e2b550556891e5d1a4c7774d4db62ff64a49900570a29f94680d1a93ba950d8af2f3b98a4b8af587e2fd939cb94f5a8ce5fc4498a26469da1973224c916e11ed3fbb73d7cfca981c865c3cd9d611674d113159746a6759cfcf4a646132332007b3228f7c83a761ef1226693a7b9e27c6d6b621602943c690ce1351f993088872976c25fa680f1622e7bbf38000fdc00a0e7557f4ef70e3cc4af93ea213ef090c155a9deb37a7c3db56fcabaef4a13783bb5d2a22cf100e5928292df6cb468b63497ad74b4a93fe3d2d086043bf51c9a58fd5341f519fa3a6946cd8ada2c554fffce8d59e35380ddbfb341d7777056e4c0da0a87a1e2cd5d0944ccc54f6593f2ccb5345cb827e0587cb07e66ae931d0e74d14f1a295110f5a4b402ab9a53b244168d629bc21925fb4aefc9aa201d48ccdff77d36557fb49bd5e89ce979aeb0c22972f6cdc5bc1dc2dcceb38b137a305b647bc1ccd3c18eac108cb5159e1c64ef17dd4059d64dd1b53c2000a74f8b4013a90e9325be2cc30ded29d8b72907c7")

twitter = tweepy.OAuthHandler("2lv4MgQDREClbQxjeWOQU5aGf", "4vq5UjqJetyLm37YhQtpc6htb0WPimFJVV088TL0LDMXHUdYTA")
twitter.set_access_token("1297802233841623040-rYG0sXCKz0PSDUNAhUPx9hecf507LY", "02dNbliU0EJOfUzGx8UVmrbaqZTlYOmwwKAWqnkecWzgd")
Twitter = tweepy.API(twitter)

Reddit = praw.Reddit(client_id = "ntnBVsoqGHtoNw", client_secret = "ZklNqu4BQK4jWRp9dYXb4ApoQ10", user_agent = "ZBot by u/Kamlin333")

REqInt = discord.Intents.default()
REqInt.members = True

DClient = commands.Bot(case_insensitive = True, command_prefix = ["z","Z"], help_command = None, intents = REqInt)

TClient = dbl.client.DBLClient(bot = DClient, token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc2ODM5NzY0MDE0MDA2MjcyMSIsImJvdCI6dHJ1ZSwiaWF0IjoxNjA2NjU3OTMwfQ.kdocPKBJMXoyKXnroUrb0KaP0lRFfxDRqLNLe3H_FXA", autopost = True)

Covid = COVID19Py.COVID19(data_source = "jhu")

Imgur = imgurpython.ImgurClient(client_id = "272a225589de547", client_secret = "421db91b32fe790c71a710f8bb48e6035f4fd365")

def RemoveExtra(listRm, val):
   return [value for value in listRm if value != val]

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
        return f'{Day}Day(s) {Hour}Hour(s) {Min}Min(s) {SecondsFormat}Sec(s)'
    elif Hour != 0:
        return f'{Hour}Hour(s) {Min}Min(s) {SecondsFormat}Sec(s)'
    elif Min != 0:
        return f'{Min}Min(s) {SecondsFormat}Sec(s)'
    else:
        return f'{SecondsFormat}Sec(s)'
    
class IsBot(commands.CheckFailure):
    pass
@DClient.check
async def ChBot(ctx):
    if ctx.author.bot:
        raise IsBot("Bot")
    return True

class IsSetup(commands.CheckFailure):
    pass
def ChSer(ctx):
    if (Col.count_documents({"IDd":"GuildInfo","IDg":str(ctx.guild.id),"Setup":"Done"}) != 0):
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
    if await TClient.get_user_vote(ctx.author.id):
        return True 
    else:
        MemGuild = DClient.get_guild(783250489843384341)
        Mem = MemGuild.get_member(ctx.author.id)
        Roles = []
        Roles.append(discord.utils.get(MemGuild.roles, id = 783250729686532126))
        Roles.append(discord.utils.get(MemGuild.roles, id = 783256987655340043))
        Roles.append(discord.utils.get(MemGuild.roles, id = 784123230372757515))
        Roles.append(discord.utils.get(MemGuild.roles, id = 784124034559377409))
        for Role in Roles:
            if Role in Mem.roles:
                return True
        raise IsVote("No Vote")

class IsPatreon(commands.CheckFailure):
    pass
def ChPatreon(ctx):
    MemGuild = DClient.get_guild(783250489843384341)
    Mem = MemGuild.get_member(ctx.author.id)
    Roles = []
    Roles.append(discord.utils.get(MemGuild.roles, id = 783250729686532126))
    Roles.append(discord.utils.get(MemGuild.roles, id = 783256987655340043))
    Roles.append(discord.utils.get(MemGuild.roles, id = 784123230372757515))
    Roles.append(discord.utils.get(MemGuild.roles, id = 784124034559377409))
    for Role in Roles:
        if Role in Mem.roles:
            return True
    raise IsPatreon("Not Patreon")

class Ignore(commands.CheckFailure):
    pass
def ChDev(ctx):
    if ctx.author.id == 443986051371892746:
        return True
    raise Ignore("Ignore")
@DClient.check
async def ChModDown(ctx):
    if ("".join(open("OpenState.txt").read().splitlines()) == "Down") and ctx.author.id not in [507212584634548254,443986051371892746,224809178793771009]:
        raise Ignore("Ignore")
    return True 

Cogs = ["Cogs.Misc","Cogs.MongoDB","Cogs.Covid","Cogs.Nasa","Cogs.RedditCmds","Cogs.TwitterCmds","Cogs.AnimeManga","Cogs.HelpInfo","Cogs.Randomizers","Cogs.OnlyMods","Cogs.MainEvents"]

if __name__ == "__main__":
    for Cog in Cogs:
        DClient.load_extension(Cog)

DClient.run("NzY4Mzk3NjQwMTQwMDYyNzIx.X4_4EQ.mpWIl074jvRs0X-ceDoKdwv4H_E")