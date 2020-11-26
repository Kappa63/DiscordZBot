import discord
import praw
import random
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import FuncMon
import os  
import deeppyer
from PIL import Image
import requests
from prawcore import NotFound, Forbidden
from hentai import Utils, Sort, Hentai, Format
import asyncio
import giphy_client
import tweepy
import mal
import malclient
import COVID19Py
import datetime
from pdf2image import convert_from_path
import imgurpython

Mdb = "mongodb+srv://Kappa:85699658@cbotdb.exsit.mongodb.net/CBot?retryWrites=true&w=majority"
Cls = MongoClient(Mdb)
DbM = Cls["CBot"]
Col = DbM["Ser"]
TraEco = DbM["Ind"]

REqInt = discord.Intents.default()
REqInt.members = True

DClient = commands.Bot(case_insensitive = True, command_prefix = ["z","Z"], help_command = None, intents = REqInt)

twitter = tweepy.OAuthHandler("2lv4MgQDREClbQxjeWOQU5aGf", "4vq5UjqJetyLm37YhQtpc6htb0WPimFJVV088TL0LDMXHUdYTA")
twitter.set_access_token("1297802233841623040-rYG0sXCKz0PSDUNAhUPx9hecf507LY", "02dNbliU0EJOfUzGx8UVmrbaqZTlYOmwwKAWqnkecWzgd")
Twitter = tweepy.API(twitter)

Reddit = praw.Reddit(client_id = "ntnBVsoqGHtoNw", client_secret = "ZklNqu4BQK4jWRp9dYXb4ApoQ10", user_agent = "CBot by u/Kamlin333")

MClient = malclient.Client()
MClient.init(access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImY5OWNmNDExZjY5NDMwMGY0ZjcwMDAyM2JlOTYyYTkyYjQxYzUwNGQ0NzA0MzQyOWYxMjEyZmNkOTBmNWNiZjlkNmFmZWNkYWRmMTViMzdjIn0.eyJhdWQiOiIyYjcwMWQzNjY5NzFmYTFmMTgyYmZkNTBkMTUxNzJhZSIsImp0aSI6ImY5OWNmNDExZjY5NDMwMGY0ZjcwMDAyM2JlOTYyYTkyYjQxYzUwNGQ0NzA0MzQyOWYxMjEyZmNkOTBmNWNiZjlkNmFmZWNkYWRmMTViMzdjIiwiaWF0IjoxNjA1MTc4ODM5LCJuYmYiOjE2MDUxNzg4MzksImV4cCI6MTYwNzc3MDgzOSwic3ViIjoiNzQ5Njc5MSIsInNjb3BlcyI6W119.B8X86ggNC43bZwzKF6993WSnY1AUGQ2wgdxbL2kRhGPJAm4M3epzbTixTxxs3RmWOsUfypoU3U2vnlYs69enzwsdGxzpoLh-hO_Mav4kSTxeXqrvPk23_7fSyC1Q8AOFE_EszhI6DG67BcFAZWVdgFia8th6vZ_7HTugWd9dDrf1PIBDfNrpWrsTs1tUImTbsZ41Y_19uT2p3-oTpmQY_YwSbLxgzkdVZmASWdDkXyFjTNnYW5y_fCDYQrDJrNrId5Dvm1N02d66TNaJgyDn86L0Dr-lYqjU9qM45agHff4T8MpkIzqzA3pKT874QUOW5QXks46-9JaCCpSB-nIrfQ")
MClient.refresh_bearer_token(client_id = "2b701d366971fa1f182bfd50d15172ae", client_secret = "e01505a84d5e611e2e59b66f0dc245888656104b1529e1a25954d8ff51780f5c", refresh_token = "def50200b66cd79fef2e2b550556891e5d1a4c7774d4db62ff64a49900570a29f94680d1a93ba950d8af2f3b98a4b8af587e2fd939cb94f5a8ce5fc4498a26469da1973224c916e11ed3fbb73d7cfca981c865c3cd9d611674d113159746a6759cfcf4a646132332007b3228f7c83a761ef1226693a7b9e27c6d6b621602943c690ce1351f993088872976c25fa680f1622e7bbf38000fdc00a0e7557f4ef70e3cc4af93ea213ef090c155a9deb37a7c3db56fcabaef4a13783bb5d2a22cf100e5928292df6cb468b63497ad74b4a93fe3d2d086043bf51c9a58fd5341f519fa3a6946cd8ada2c554fffce8d59e35380ddbfb341d7777056e4c0da0a87a1e2cd5d0944ccc54f6593f2ccb5345cb827e0587cb07e66ae931d0e74d14f1a295110f5a4b402ab9a53b244168d629bc21925fb4aefc9aa201d48ccdff77d36557fb49bd5e89ce979aeb0c22972f6cdc5bc1dc2dcceb38b137a305b647bc1ccd3c18eac108cb5159e1c64ef17dd4059d64dd1b53c2000a74f8b4013a90e9325be2cc30ded29d8b72907c7")

Cov = COVID19Py.COVID19(data_source = "jhu")

Imgur = imgurpython.ImgurClient(client_id = "272a225589de547", client_secret = "421db91b32fe790c71a710f8bb48e6035f4fd365")

GClient = "ZH1xoGH0XUffrtqFKdj3kD4YrVoZvb8i"
GApi = giphy_client.DefaultApi()

Doing = ["Playing with the laws of physics", "Torture", "Just Vibin'", "With my toes", "Chess with god", "With Leona"]

PrMUsI = []

def removeExtraS(listRm, val):
   return [value for value in listRm if value != val]

def CheckSub(Sub):
    Valid = True
    try:
        Reddit.subreddits.search_by_name(Sub, exact = True)
        Reddit.subreddit(Sub).subreddit_type
    except (NotFound, Forbidden):
        Valid = False
    return Valid
    
def PosType(Pty):
    TextB = False
    if Pty.is_self:
        TextB = True
    return TextB

def StrTSTM(SecGiN):
    Day = 0
    Hour = 0
    Min = 0
    while SecGiN >= 60:
        Min += 1
        if Min == 60:
            Hour += 1
            Min -= 60
        if Hour == 24:
            Day += 1
            Hour -= 24
        SecGiN -= 60
    if Day != 0:
        return f'{Day}Day(s) {Hour}Hour(s) {Min}Min(s) {SecGiN}Sec(s)'
    elif Hour != 0:
        return f'{Hour}Hour(s) {Min}Min(s) {SecGiN}Sec(s)'
    elif Min != 0:
        return f'{Min}Min(s) {SecGiN}Sec(s)'
    else:
        return f'{SecGiN}Sec(s)'

class IsBot(commands.CheckFailure):
    pass
def ChBot(ctx):
    if ctx.author.bot:
        raise IsBot("Bot")
    return True

class IsVote(commands.CheckFailure):
    pass
def ChVote(ctx):
    if ctx.author.id in PrMUsI:
        raise IsVote("No Vote")
    return True

def ChAdMo(ctx):
    if ctx.author.id == 443986051371892746:
        return True
    return False

class IsAdmin(commands.CheckFailure):
    pass
def ChAdmin(ctx):
    if ctx.author.guild_permissions.administrator:
        return True
    raise IsAdmin("Normie")

class ProfSer(commands.CheckFailure):
    pass
def ChSer(ctx):
    if (Col.count_documents({"IDd":"GuildInfo","IDg":str(ctx.guild.id),"Setup":"Done"}) != 0):
        return True
    raise ProfSer("Unready")

@DClient.command(name = "help")
@commands.check(ChBot)
@commands.cooldown(1, 1, commands.BucketType.user)
async def SendH(ctx, *args):
    if "".join(args) == "" or "".join(args) == " ":
        HEm = discord.Embed(title = "**ZBot Help**", description = "\u200b", color = 0x0af531)
        HEm.add_field(name = "zversion: ", value = "Checks the current running version of CBot", inline = False)
        HEm.add_field(name = "zvote: ", value = "To vote for ZBot", inline = False)
        HEm.add_field(name = "zhelp server: ", value = "Provides all the server commands (including word track commands)", inline = False) 
        HEm.add_field(name = "zhelp misc: ", value = "Miscellaneous commands", inline = False)   
        await ctx.message.channel.send(embed = HEm)
    elif "".join(args).lower()  == "server":
        HEm = discord.Embed(title = "**ZBot Server Help**", description = "\u200b", color = 0x0af531)
        HEm.add_field(name = "zsetup: ", value = "Sets up the bot for the first time for counting/tracking", inline = False)
        HEm.add_field(name = "zupdate: ", value = "This is used to add members that join when the bot is down.", inline = False)
        HEm.add_field(name = "zadd: ", value = "Adds a word/phrase to keep track of", inline = False)
        HEm.add_field(name = "zremove: ", value = "Removes an existing word/phrase being tracked", inline = False)
        HEm.add_field(name = "zlist: ", value = "Returns all added words/phrases", inline = False)
        HEm.add_field(name = "zstats (@) (Word): ", value = "Returns stats for word(s)/phrase(s)", inline = False)
        HEm.add_field(name = "ztotal (Word): ", value = "Returns the total number of times word(s)/phrase(s) have been said on server", inline = False)
        HEm.add_field(name = "ztop (Word): ", value = "Returns the top 3 number of times word(s)/phrase(s) have been said on server", inline = False)
        HEm.add_field(name = "zreset: ", value = "Reset everything (this is irreversable)", inline = False)
        HEm.set_footer(text = "Note: Counting is limited to 10 per Message to reduce spam incentives")
        await ctx.message.channel.send(embed = HEm)
    elif "".join(args).lower() == "misc" or "".join(args).lower() == "misc." or "".join(args).lower() == "miscellaneous":
        HEm = discord.Embed(title = "**ZBot Misc. Help**", description = "\u200b", color = 0x0af531)
        HEm.add_field(name = "zremind (Arguments): ", value = 'Pings you after time is over. Arguments are a number followed by d, h, m, or s for days, hours, minutes, seconds respectively.(Ex. "zremind 2d 3h 52m 14s" is a remind after 2days 3hours 52minutes and 14seconds)', inline = False)
        HEm.add_field(name = "zfry (Image Attachment/Image Url): ", value = "Deep fries the image", inline = False)
        HEm.add_field(name = "zfry profile (@): ", value = "Deep fries the avatar", inline = False)
        HEm.add_field(name = "zpdf (PDF Attachment/PDF Url): ", value = "Views the PDF's first 40 pages", inline = False)
        HEm.add_field(name = "zcalc (Input): ", value = "Calculates and returns", inline = False)
        HEm.add_field(name = "zcovid: ", value = "Returns the worldwide status of Covid-19", inline = False)
        HEm.add_field(name = "zcovid (Country): ", value = "Returns the status of Covid-19 in country", inline = False)
        HEm.add_field(name = "zreddit (Subreddit Name): ", value = "Returns a RANDOM post from the top 100 posts in hot from any subreddit", inline = False)
        HEm.add_field(name = "ztwitter (User @): ", value = "Returns the user profile and 20 of their latest tweets", inline = False)
        HEm.add_field(name = "ztwitter search (Username): ", value = "Searches for 10 users related to search argument", inline = False)
        HEm.add_field(name = "zanime (Anime Name): ", value = "Searches for anime and returns all the info about chosen one", inline = False)
        HEm.add_field(name = "zmanga (Manga Name): ", value = "Searches for manga and returns all the info about chosen one", inline = False)
        HEm.add_field(name = "zhentai (Magic Numbers): ", value = "Gets doujin from nhentai using magic numbers", inline = False)
        HEm.add_field(name = "zhentai random: ", value = "Gets a random doujin from nhentai", inline = False)
        HEm.add_field(name = "zhentai search (Doujin Name): ", value = "Searches for the 10 most popular doujin", inline = False)
        HEm.add_field(name = "zgiphy (Phrase/Word to search for): ", value = "Returns a RANDOM gif from top 50 results on giphy", inline = False)
        HEm.set_footer(text = "Notes: -During testing recovered data from zcovid was extremely inaccurate\n-Some hentai are not available. This is to abide by the discord TOS")
        await ctx.message.channel.send(embed = HEm)
    else:
        await ctx.message.channel.send("That help category doesn't exist.")

@DClient.command(name = "checkzbot")
@commands.check(ChAdMo)
async def BotSttSF(ctx):
    SEm = discord.Embed(title = "Current ZBot Status", color = 0x000000)
    SEm.add_field(name = "Guilds in: ", value = len(DClient.guilds), inline = False)
    SEm.add_field(name = "Latency: ", value = DClient.latency * 100, inline = False)
    SEm.add_field(name = "ShardCount: ", value = DClient.shard_count, inline = False)
    await ctx.message.channel.send(embed = SEm)

@DClient.command(name = "vote")
@commands.check(ChBot)
@commands.cooldown(1, 1, commands.BucketType.user)
async def BotVotF(ctx):
    SEm = discord.Embed(title = "Voting for ZBot", url = "https://top.gg/bot/768397640140062721/vote", description = "**You can vote once every 12 hours for the following perks**", color = 0x000000)
    SEm.add_field(name = "\u200b", value = "*Using instant navigation to page*\n\n", inline = False)
    SEm.set_footer(text = "These perks will remain active for 12hrs after voting\n\n***`More perks will be added soon`***")
    await ctx.message.channel.send(embed = SEm)

@DClient.command(aliases = ["ver","version"])
@commands.check(ChBot)
@commands.cooldown(1, 1, commands.BucketType.user)
async def RetVer(ctx):
    VEm = discord.Embed(title = "Active Version", description = "ZBot build version and info", color = 0xf59542)
    VEm.add_field(name = "Dev: ", value = "Kappa", inline = False)
    VEm.add_field(name = "Version: ", value = "1.1a", inline = False)
    VEm.add_field(name = "Release: ", value = "21/11/2020", inline = True)
    await ctx.message.channel.send(embed = VEm)

@DClient.command(name = "setup")
@commands.check(ChBot)
@commands.check(ChAdmin)
@commands.cooldown(1, 1, commands.BucketType.user)
async def SMsg(ctx):
    if Col.count_documents({"IDd":"GuildInfo","IDg":str(ctx.guild.id),"Setup":"Done"}) == 0:
        Col.insert_one({"IDd":"GuildInfo","IDg":str(ctx.guild.id),"Setup":"Done"})
        for Pid in ctx.guild.members:
            if Pid.bot == False:
                if Col.count_documents({"IDd":str(Pid.id),"IDg":str(ctx.guild.id)}) == 0:
                    Col.insert_one({"IDd":str(Pid.id),"IDg":str(ctx.guild.id)})
                    DbB = Col.find({"IDd":"GuildInfo","IDg":str(ctx.guild.id)})
                    for i in DbB:
                        Kyes = i.keys()    
                    for Wp in Kyes:
                        FuncMon.DbAdd(Col, {"IDd":str(Pid.id),"IDg":str(ctx.guild.id)}, Wp, 0)
        await ctx.message.channel.send(":partying_face: Setup complete, you can now use tracking commands :partying_face:")
    else:
        await ctx.message.channel.send(":partying_face: This server is already setup :partying_face:")

@DClient.command(name = "update")
@commands.check(ChBot)
@commands.check(ChSer)
@commands.check(ChAdmin)
@commands.cooldown(1, 1, commands.BucketType.user)
async def SUmsg(ctx):
    xNumP = 0
    for i in ctx.guild.members:
        if not i.bot:
            xNumP += 1
    NumAdD = 0
    if xNumP+1 != Col.count_documents({"IDg":str(ctx.guild.id)}):
        for Pid in ctx.guild.members:
            if Pid.bot == False:
                if Col.count_documents({"IDd":str(Pid.id),"IDg":str(ctx.guild.id)}) == 0:
                    Col.insert_one({"IDd":str(Pid.id),"IDg":str(ctx.guild.id)})
                    NumAdD += 1
                    DbB = Col.find({"IDd":"GuildInfo","IDg":str(ctx.guild.id)})
                    for i in DbB:
                        Kyes = i.keys()    
                    for Wp in Kyes:
                        FuncMon.DbAdd(Col, {"IDd":str(Pid.id),"IDg":str(ctx.guild.id)}, Wp, 0)
        await ctx.message.channel.send(f':partying_face: The server info has been updated (added {NumAdD} members) :partying_face:')
    else:
        await ctx.message.channel.send(":partying_face: This server is already up to date :partying_face:")

@DClient.command(aliases = ["calculate","calc"])
@commands.check(ChBot)
@commands.cooldown(1, 1, commands.BucketType.user)
async def CalCeR(ctx, *args):
    ToCalO = "".join(args)
    def CalcST(NumE):
        SaFTSen = True
        for i in NumE:
            try:
                int(i)
            except ValueError:
                if i not in ["(",")","*","/","+","-","**"]:
                    SaFTSen = False 
                    break
        if SaFTSen:
            return f'Answer is: {round(eval(NumE),4)}'
        else:
            return "Failed to calculate :confused:"
    AnSrsOErAl = CalcST(ToCalO)
    await ctx.message.channel.send(AnSrsOErAl)

@DClient.command(name = "manga")
@commands.check(ChBot)
@commands.cooldown(1, 10, commands.BucketType.guild)
async def MagMa(ctx, *args):
    def ChCHanS(MSg):
        MesS = MSg.content.lower()
        RsT = False
        try:
            if int(MSg.content) <= 10:
                RsT = True
        except ValueError:
            if (MesS == "cancel") or (MesS == "c"):
                RsT = True
        return MSg.guild.id == ctx.guild.id and MSg.channel.id == ctx.channel.id and RsT
    if args:
        try:
            Srks = " ".join(args)
            C = 0
            SrchMag = []
            MnSrS = await ctx.message.channel.send(embed = discord.Embed(title = ":mag: Searching...",  description = "\u200b", color = 0xa49cff))
            SAEm = discord.Embed(title = f":mag: Results for '{Srks}'",  description = "\u200b", color = 0xa49cff)
            for MagRes in mal.MangaSearch(Srks).results:
                C += 1
                SAEm.add_field(name = "\u200b", value = f'{C}. `{MagRes.title}` **({MagRes.type})**', inline = False)
                SrchMag.append(MagRes)
                if C == 10:
                    print(MagRes)
                    break
            SAEm.set_footer(text = 'Choose a number to view MAL entry. "c" or "cancel" to exit search.\n\n*The Search closes automatically after 20sec of inactivity.*')
            await MnSrS.edit(embed = SAEm)
            try:
                ResS = await DClient.wait_for('message', check = ChCHanS, timeout = 20)
                LResS = ResS.content.lower()
                try:
                    if int(ResS.content) <= 10:
                        MagI = SrchMag[int(ResS.content)-1].mal_id
                        await MnSrS.edit(embed = discord.Embed(title = ":calling: Finding...",  description = f'{SrchMag[int(ResS.content)-1].title} **({SrchMag[int(ResS.content)-1].type})**', color = 0xa49cff)) 
                except ValueError:
                    if (LResS == "cancel") or (LResS == "c"):
                        await MnSrS.edit(embed = discord.Embed(title = ":x: Search Cancelled",  description = "\u200b", color = 0xa49cff))
            except asyncio.TimeoutError:
                await MnSrS.edit(embed = discord.Embed(title = ":hourglass: Search Timeout...",  description = "\u200b", color = 0xa49cff))
        except UnboundLocalError:
            SAEm = discord.Embed(title = f':mag: Search for "{Srks}"',  description = "\u200b", color = 0xa49cff)
            SAEm.add_field(name = "\u200b", value = "No Results found :woozy_face:", inline = False)
            await MnSrS.edit(embed = SAEm)

        try:
            MagF = MClient.get_manga_details(MagI)
            MagFmal = mal.Manga(MagI)
            MagG = []
            for TMagG in MagF.genres:
                MagG.append(TMagG.name)
            AEm = discord.Embed(title = f'{MagF.title} / {MagF.alternative_titles.ja} **({MagFmal.type})**',  description = f'{", ".join(MagG)}\n[Mal Page]({MagFmal.url})', color = 0xa49cff)
            AEm.set_thumbnail(url = MagF.main_picture.large)
            if len(MagF.synopsis) > 1021:
                MagSyn = MagF.synopsis[0:1021]
                MagSyn = MagSyn + "..."
            else:
                MagSyn = MagF.synopsis
            AEm.add_field(name = f'By: {", ".join(MagFmal.authors)}', value = "\u200b", inline = False)
            AEm.add_field(name = "Synopsis:", value = MagSyn, inline = False)
            try:
                AEm.add_field(name = "Start Airing on:", value = MagF.start_date, inline = True)
            except AttributeError:
                pass
            try:
                AEm.add_field(name = "Finish Airing on:", value = MagF.end_date, inline = True)
            except AttributeError:
                pass
            AEm.add_field(name = "Status:", value = MagFmal.status, inline = True)
            AEm.add_field(name = "Score:", value = MagFmal.score, inline = True)
            AEm.add_field(name = "Rank:", value = MagFmal.rank, inline = True)
            AEm.add_field(name = "Popularity:", value = MagFmal.popularity, inline = True)
            AEm.add_field(name = "No# Volumes:", value = MagFmal.volumes, inline = True)
            AEm.add_field(name = "No# Chapters:", value = MagFmal.chapters, inline = True)
            MagAdp = []
            MagAlt = []
            MagSum = []
            MagSeq = []
            MagSiSt = []
            MagSpO = []
            for TMagAdp in MagF.related_manga:
                if TMagAdp.relation_type_formatted == "Adaptation":
                    MagAdp.append(TMagAdp.node.title)
                elif TMagAdp.relation_type_formatted == "Summary":
                    MagSum.append(TMagAdp.node.title)
                elif TMagAdp.relation_type_formatted == "Sequel":
                    MagSeq.append(TMagAdp.node.title)
                elif TMagAdp.relation_type_formatted == "Spin-off":
                    MagSpO.append(TMagAdp.node.title)
                elif TMagAdp.relation_type_formatted == "Alternative version":
                    MagAlt.append(TMagAdp.node.title)
                elif TMagAdp.relation_type_formatted == "Side story":
                    MagSiSt.append(TMagAdp.node.title)

            if len("\n".join(MagSeq)) > 950:
                MagSeqF = "\n".join(MagSeq)[0:950]
                MagSeqF = MagSeqF + "..."
            else:
                MagSeqF = "\n".join(MagSeq)

            if len("\n".join(MagAdp)) > 950:
                MagAdpF = "\n".join(MagAdp)[0:950]
                MagAdpF = MagAdpF + "..."
            else:
                MagAdpF = "\n".join(MagAdp)

            if len("\n".join(MagSum)) > 950:
                MagSumF = "\n".join(MagSum)[0:950]
                MagSumF = MagSumF + "..."
            else:
                MagSumF = "\n".join(MagSum)

            if len("\n".join(MagAlt)) > 950:
                MagAltF = "\n".join(MagAlt)[0:950]
                MagAltF = MagAltF + "..."
            else:
                MagAltF = "\n".join(MagAlt)

            if len("\n".join(MagSpO)) > 950:
                MagSpOF = "\n".join(MagSpO)[0:950]
                MagSpOF = MagSpOF + "..."
            else:
                MagSpOF = "\n".join(MagSpO)

            if len("\n".join(MagSiSt)) > 950:
                MagSiStF = "\n".join(MagSiSt)[0:950]
                MagSiStF = MagSiStF + "..."
            else:
                MagSiStF = "\n".join(MagSiSt)
            if MagSeqF or MagAltF or MagAdpF or MagSiStF or MagSumF or MagSpOF:
                AEm.add_field(name = "\u200b", value = "\u200b", inline = False)
            if MagSeqF:
                AEm.add_field(name = "Sequel:", value = MagSeqF, inline = False)
            if MagAltF:
                AEm.add_field(name = "Alternate Version:", value = MagAltF, inline = False)
            if MagAdpF:
                AEm.add_field(name = "Adaptation:", value = MagAdpF, inline = False)
            if MagSiStF:
                AEm.add_field(name = "Side Story:", value = MagSiStF, inline = False)
            if MagSumF:
                AEm.add_field(name = "Summary:", value = MagSumF, inline = False)
            if MagSpOF:
                AEm.add_field(name = "Spin Off:", value = MagSpOF, inline = False)
            await ctx.message.channel.send(embed = AEm)
        except UnboundLocalError:
            pass
    else:
        await ctx.message.channel.send("No Arguments :no_mouth:")

@DClient.command(name = "anime")
@commands.check(ChBot)
@commands.cooldown(1, 10, commands.BucketType.guild)
async def AniMa(ctx, *args):
    def ChCHanS(MSg):
        MesS = MSg.content.lower()
        RsT = False
        try:
            if int(MSg.content) <= 10:
                RsT = True
        except ValueError:
            if (MesS == "cancel") or (MesS == "c"):
                RsT = True
        return MSg.guild.id == ctx.guild.id and MSg.channel.id == ctx.channel.id and RsT
    if args:
        try:
            Srks = " ".join(args)
            C = 0
            SrchAni = []
            AnSrS = await ctx.message.channel.send(embed = discord.Embed(title = ":mag: Searching...",  description = "\u200b", color = 0xa49cff))
            SAEm = discord.Embed(title = f':mag: Results for "{Srks}"',  description = "\u200b", color = 0xa49cff)
            for AniRes in mal.AnimeSearch(Srks).results:
                C += 1
                SAEm.add_field(name = "\u200b", value = f"{C}. `{AniRes.title}` **({AniRes.type})**", inline = False)
                SrchAni.append(AniRes)
                if C == 10:
                    break
            SAEm.set_footer(text = 'Choose a number to view MAL entry. "c" or "cancel" to exit search.\n\n*The Search closes automatically after 20sec of inactivity.*')
            await AnSrS.edit(embed = SAEm)
            try:
                ResS = await DClient.wait_for('message', check = ChCHanS, timeout = 20)
                LResS = ResS.content.lower()
                try:
                    if int(ResS.content) <= 10:
                        AniI = SrchAni[int(ResS.content)-1].mal_id
                        await AnSrS.edit(embed = discord.Embed(title = ":calling: Finding...",  description = f'{SrchAni[int(ResS.content)-1].title} **({SrchAni[int(ResS.content)-1].type})**', color = 0xa49cff)) 
                except ValueError:
                    if (LResS == "cancel") or (LResS == "c"):
                        await AnSrS.edit(embed = discord.Embed(title = ":x: Search Cancelled",  description = "\u200b", color = 0xa49cff))
            except asyncio.TimeoutError:
                await AnSrS.edit(embed = discord.Embed(title = ":hourglass: Search Timeout...",  description = "\u200b", color = 0xa49cff))
        except UnboundLocalError:
            SAEm = discord.Embed(title = f':mag: Search for "{Srks}"',  description = "\u200b", color = 0xa49cff)
            SAEm.add_field(name = "\u200b", value = "No Results found :woozy_face:", inline = False)
            await AnSrS.edit(embed = SAEm)

        try:
            AniF = MClient.get_anime_details(AniI)
            AniFmal = mal.Anime(AniI)
            AniG = []
            for TAniG in AniF.genres:
                AniG.append(TAniG.name)
            AEm = discord.Embed(title = f'{AniF.title} / {AniF.alternative_titles.ja} **({AniFmal.type})**',  description = f'{", ".join(AniG)}\n[Mal Page]({AniFmal.url})', color = 0xa49cff)
            AEm.set_thumbnail(url = AniF.main_picture.large)
            if len(AniF.synopsis) > 1021:
                AniSyn = AniF.synopsis[0:1021]
                AniSyn = AniSyn + "..."
            else:
                AniSyn = AniF.synopsis
            AEm.add_field(name = f'Studios: {", ".join(AniFmal.studios)}', value = "\u200b", inline = False)
            AEm.add_field(name = "Synopsis:", value = AniSyn, inline = False)
            try:
                AEm.add_field(name = "Start Airing on:", value = AniF.start_date, inline = True)
            except AttributeError:
                pass
            try:
                AEm.add_field(name = "Finish Airing on:", value = AniF.end_date, inline = True)
            except AttributeError:
                pass
            AEm.add_field(name = "Status:", value = AniFmal.status, inline = True)
            AEm.add_field(name = "Rating:", value = AniFmal.rating, inline = False)
            AEm.add_field(name = "Score:", value = AniFmal.score, inline = True)
            AEm.add_field(name = "Rank:", value = AniFmal.rank, inline = True)
            AEm.add_field(name = "Popularity:", value = AniFmal.popularity, inline = True)
            AEm.add_field(name = "No# Episodes:", value = AniFmal.episodes, inline = True)
            AEm.add_field(name = "Episode Duration:", value = AniFmal.duration, inline = True)
            AniAdp = []
            AniAlt = []
            AniSum = []
            AniSeq = []
            AniSiSt = []
            AniSpO = []
            for TAniAdp in AniF.related_anime:
                if TAniAdp.relation_type_formatted == "Adaptation":
                    AniAdp.append(TAniAdp.node.title)
                elif TAniAdp.relation_type_formatted == "Summary":
                    AniSum.append(TAniAdp.node.title)
                elif TAniAdp.relation_type_formatted == "Sequel":
                    AniSeq.append(TAniAdp.node.title)
                elif TAniAdp.relation_type_formatted == "Spin-off":
                    AniSpO.append(TAniAdp.node.title)
                elif TAniAdp.relation_type_formatted == "Alternative version":
                    AniAlt.append(TAniAdp.node.title)
                elif TAniAdp.relation_type_formatted == "Side story":
                    AniSiSt.append(TAniAdp.node.title)
            if len("\n".join(AniSeq)) > 950:
                AniSeqF = "\n".join(AniSeq)[0:950]
                AniSeqF = AniSeqF + "..."
            else:
                AniSeqF = "\n".join(AniSeq)

            if len("\n".join(AniAdp)) > 950:
                AniAdpF = "\n".join(AniAdp)[0:950]
                AniAdpF = AniAdpF + "..."
            else:
                AniAdpF = "\n".join(AniAdp)

            if len("\n".join(AniSum)) > 950:
                AniSumF = "\n".join(AniSum)[0:950]
                AniSumF = AniSumF + "..."
            else:
                AniSumF = "\n".join(AniSum)

            if len("\n".join(AniAlt)) > 950:
                AniAltF = "\n".join(AniAlt)[0:950]
                AniAltF = AniAltF + "..."
            else:
                AniAltF = "\n".join(AniAlt)

            if len("\n".join(AniSpO)) > 950:
                AniSpOF = "\n".join(AniSpO)[0:950]
                AniSpOF = AniSpOF + "..."
            else:
                AniSpOF = "\n".join(AniSpO)

            if len("\n".join(AniSiSt)) > 950:
                AniSiStF = "\n".join(AniSiSt)[0:950]
                AniSiStF = AniSiStF + "..."
            else:
                AniSiStF = "\n".join(AniSiSt)
            if AniSeqF or AniAltF or AniAdpF or AniSiStF or AniSumF or AniSpOF:
                AEm.add_field(name = "\u200b", value = "\u200b", inline = False)
            if AniSeqF:
                AEm.add_field(name = "Sequel:", value = AniSeqF, inline = False)
            if AniAltF:
                AEm.add_field(name = "Alternate Version:", value = AniAltF, inline = False)
            if AniAdpF:
                AEm.add_field(name = "Adaptation:", value = AniAdpF, inline = False)
            if AniSiStF:
                AEm.add_field(name = "Side Story:", value = AniSiStF, inline = False)
            if AniSumF:
                AEm.add_field(name = "Summary:", value = AniSumF, inline = False)
            if AniSpOF:
                AEm.add_field(name = "Spin Off:", value = AniSpOF, inline = False)
            AEm.add_field(name = "\u200b", value = "\u200b", inline = False)
            try:
                if len("\n".join(AniFmal.opening_themes)) > 950:
                    AniOT = ("\n".join(AniFmal.opening_themes))[0:950]
                    AniOT = AniOT + "..."
                else:
                    AniOT = "\n".join(AniFmal.opening_themes)
                AEm.add_field(name = "Opening Theme(s):", value = AniOT, inline = False)
            except TypeError:
                pass

            try:
                if len("\n".join(AniFmal.ending_themes)) > 950:
                    AniET = ("\n".join(AniFmal.ending_themes))[0:950]
                    AniET = AniET + "..."
                else:
                    AniET = "\n".join(AniFmal.ending_themes)
                AEm.add_field(name = "Ending Theme(s):", value = AniET, inline = True)
            except TypeError:
                pass
            await ctx.message.channel.send(embed = AEm)
        except UnboundLocalError:
            pass
    else:
        await ctx.message.channel.send("No Arguments :no_mouth:")

@DClient.command(name = "twitter")
@commands.check(ChBot)
@commands.cooldown(1, 5, commands.BucketType.user)
async def TwttMsSur(ctx, *args):
    def ChCHanS(MSg):
        MesS = MSg.content.lower()
        RsT = False
        try:
            if int(MSg.content) <= 10:
                RsT = True
        except ValueError:
            if (MesS == "cancel") or (MesS == "c"):
                RsT = True
        return MSg.guild.id == ctx.guild.id and MSg.channel.id == ctx.channel.id and RsT

    def ChCHEm(RcM, RuS):
        return RuS.bot == False and RcM.message == TwTsL and str(RcM.emoji) in ["⬅️","❌","➡️"]

    def MakEmTwt(TwTp, VrMa, TwTYPE, TwExt, TwTNum, TwTtot):
        TEmE = discord.Embed(title = f'@{TwTp.screen_name} / {TwTp.name} {VrMa}',  description = TwTYPE, color = 0x0384fc)
        TEmE.set_thumbnail(url = TwTp.profile_image_url_https)
        TEmE.add_field(name = f'{TwTYPE} on: ', value = TwExt.created_at, inline = False)
        TEmE.add_field(name = f'`{TwTNum+1}/{TwTtot}`', value = "\u200b", inline = False)
        TEmE.add_field(name = "Retweets: ", value = f'{TwExt.retweet_count:,}', inline = True)
        TEmE.add_field(name = "Likes: ", value = f'{TwExt.favorite_count:,}', inline = True)
        if TwTYPE == "Retweet":
            try:
                if hasattr(TwExt.retweeted_status, "extended_entities"):
                    TEmE.set_image(url = TwExt.retweeted_status.extended_entities["media"][0]["media_url_https"])
                TEmE.add_field(name = f'Retweeted Body (By: {Twitter.get_user(user_id = TwExt.retweeted_status.user.id).screen_name}): ', value = TwExt.retweeted_status.full_text, inline = False)
            except tweepy.error.TweepError:
                TEmE.add_field(name = "On (By: --Deleted--): ", value = "--Deleted--", inline = False)
        elif TwTYPE == "Quote":
            try:
                if hasattr(TwExt.quoted_status, "extended_entities"):
                    TEmE.set_image(url = TwExt.quoted_status.extended_entities["media"][0]["media_url_https"])
                TEmE.add_field(name = "Main Body: ", value = TwExt.full_text, inline = False)
                TEmE.add_field(name = f'Quoted Body (By: {Twitter.get_user(user_id = TwExt.quoted_status.user.id).screen_name}): ', value = TwExt.quoted_status.full_text, inline = False)
            except tweepy.error.TweepError:
                TEmE.add_field(name = "On (By: --Deleted--): ", value = "--Deleted--", inline = False)
        elif TwTYPE == "Tweet":
            if hasattr(TwExt, "extended_entities"):
                TEmE.set_image(url = TwExt.extended_entities["media"][0]["media_url_https"])
            TEmE.add_field(name = "Tweet Body: ", value = TwExt.full_text, inline = False)
        elif TwTYPE == "Comment":
            TEmE.add_field(name = "Comment Body: ", value = TwExt.full_text, inline = False)
            try:
                TwCO = Twitter.get_status(id = TwExt.in_reply_to_status_id, trim_user=True, tweet_mode="extended")
                if hasattr(TwCO, "extended_entities"):
                    TEmE.set_image(url = TwCO.extended_entities["media"][0]["media_url_https"])
                TEmE.add_field(name = f'On (By: {TwExt.in_reply_to_screen_name}): ', value = TwCO.full_text, inline = False)
            except tweepy.error.TweepError:
                TEmE.add_field(name = "On (By: --Deleted--): ", value = "--Deleted--", inline = False)
            
        TEmE.set_footer(text = f'{"-"*10}\n\nMake sure to close the tweet once you are done .\n\n*Tweet closes automatically after 20sec of inactivity.*')
        return TEmE

    def ChTwTp(TwExt):
        if hasattr(TwExt, "retweeted_status") and TwExt.retweeted_status:
            return "Retweet"
        elif hasattr(TwExt, "quoted_status") and TwExt.quoted_status:
            return "Quote"
        elif hasattr(TwExt, "in_reply_to_status_id") and TwExt.in_reply_to_status_id:
            return "Comment"
        else:
            return "Tweet"

    TwCS = " ".join(args).split(" ")
    if TwCS[0].lower() == "search" and args:
        TwCS.pop(0)
        if " ".join(TwCS):
            C = 0
            SrchTw = []
            for TwU in Twitter.search_users(TwCS, count = 10):
                C += 1
                if C == 1:
                    STEm = discord.Embed(title = f':mag: Search for "{" ".join(TwCS)}"',  description = "\u200b", color = 0x0384fc)
                VrMa = ""
                if TwU.verified:
                    VrMa = ":ballot_box_with_check: "
                STEm.add_field(name = "\u200b", value = f'{C}. `@{TwU.screen_name} / {TwU.name}` {VrMa}', inline = False)
                SrchTw.append(TwU)
            STEm.set_footer(text = 'Choose a number to open doujin. "c" or "cancel" to exit search.\n\n*The Search closes automatically after 20sec of inactivity.*')
            TwSent = await ctx.message.channel.send(embed = STEm)
            try:
                ResS = await DClient.wait_for('message', check = ChCHanS, timeout = 20)
                LResS = ResS.content.lower()
                try:
                    if int(ResS.content) <= 10:
                        ProT = SrchTw[int(ResS.content)-1]
                        VrMa = ""
                        if ProT.verified:
                            VrMa = ":ballot_box_with_check: "
                        TwS = SrchTw[int(ResS.content)-1].screen_name
                        await TwSent.edit(embed = discord.Embed(title = ":calling: Finding...",  description = f'@{ProT.screen_name} / {ProT.name} {VrMa}', color = 0x0384fc)) 
                except ValueError:
                    if (LResS == "cancel") or (LResS == "c"):
                        await TwSent.edit(embed = discord.Embed(title = ":x: Search Cancelled",  description = "\u200b", color = 0x0384fc))
            except asyncio.TimeoutError:
                await TwSent.edit(embed = discord.Embed(title = ":hourglass: Search Timeout...",  description = "\u200b", color = 0x0384fc))
        else:
            await ctx.message.channel.send("No search argument :woozy_face:")
    elif args:
        TwS = " ".join(args)
    else:
        await ctx.message.channel.send("No Arguments :no_mouth:")
    try:
        try:
            TwTp = Twitter.get_user(TwS)
            VrMa = ""
            TwDes = "\u200b"
            if TwTp.verified:
                VrMa = ":ballot_box_with_check: "
            if TwTp.description:
                TwDes = TwTp.description
            TEm = discord.Embed(title = f'@{TwTp.screen_name} / {TwTp.name} {VrMa}',  description = TwDes, color = 0x0384fc)
            TEm.set_thumbnail(url = TwTp.profile_image_url_https)
            if TwTp.location:
                TEm.add_field(name = "Location: ", value = TwTp.location, inline = True)
            if TwTp.url:
                TEm.add_field(name = "Website: ", value = (requests.head(TwTp.url)).headers['Location'], inline = True)
            TEm.add_field(name = "Created: ", value = (str(TwTp.created_at).split(" "))[0], inline = False)
            TEm.add_field(name = "Following: ", value = f'{TwTp.friends_count:,}', inline = True) 
            TEm.add_field(name = "Followers: ", value = f'{TwTp.followers_count:,}', inline = True)
            TEm.set_footer(text = "Make sure to close the tweet once you are done .\n\n*Tweet closes automatically after 20sec of inactivity.*")
            TwExt = Twitter.user_timeline(TwS, trim_user=True, tweet_mode="extended")
            TwTsL = await ctx.message.channel.send(embed = TEm)
            TwTNum = 0
            OnPrF = True
            await TwTsL.add_reaction("⬅️")
            await TwTsL.add_reaction("❌")
            await TwTsL.add_reaction("➡️")
            while True:
                try:
                    ReaEm = await DClient.wait_for("reaction_add", check = ChCHEm, timeout = 20) 
                    await TwTsL.remove_reaction(ReaEm[0].emoji, ReaEm[1])
                    if ReaEm[0].emoji == "⬅️" and TwTNum == 0:
                        OnPrF = True
                        await TwTsL.edit(embed = TEm)
                    elif ReaEm[0].emoji == "⬅️" and TwTNum > 0:
                        TwTNum -= 1
                        await TwTsL.edit(embed = MakEmTwt(TwTp, VrMa, ChTwTp(TwExt[TwTNum]), TwExt[TwTNum], TwTNum, len(TwExt)))
                    elif ReaEm[0].emoji == "➡️" and OnPrF:
                        OnPrF = False    
                        TwTNum = 0
                        await TwTsL.edit(embed = MakEmTwt(TwTp, VrMa, ChTwTp(TwExt[TwTNum]), TwExt[TwTNum], TwTNum, len(TwExt)))
                    elif ReaEm[0].emoji == "➡️" and len(TwExt) > TwTNum+1 and TwTNum >= 0:
                        TwTNum += 1
                        await TwTsL.edit(embed = MakEmTwt(TwTp, VrMa, ChTwTp(TwExt[TwTNum]), TwExt[TwTNum], TwTNum, len(TwExt)))
                    elif ReaEm[0].emoji == "➡️" and len(TwExt) == TwTNum+1:
                        await TwTsL.remove_reaction("⬅️", DClient.user)
                        await TwTsL.remove_reaction("❌", DClient.user)
                        await TwTsL.remove_reaction("➡️", DClient.user)
                        break
                    elif ReaEm[0].emoji == "❌":
                        await TwTsL.remove_reaction("⬅️", DClient.user)
                        await TwTsL.remove_reaction("❌", DClient.user)
                        await TwTsL.remove_reaction("➡️", DClient.user)
                        break
                except asyncio.TimeoutError:
                    await TwTsL.remove_reaction("⬅️", DClient.user)
                    await TwTsL.remove_reaction("❌", DClient.user)
                    await TwTsL.remove_reaction("➡️", DClient.user)
                    break
        except tweepy.error.TweepError:
            await ctx.message.channel.send("Not Found :expressionless:")
    except UnboundLocalError:
        pass

@DClient.command(name = "hentai")
@commands.check(ChBot)
@commands.cooldown(1, 3, commands.BucketType.user)
async def nHen(ctx, *args):  
    def ChCHanS(MSg):
        MesS = MSg.content.lower()
        MeseS = (MSg.content.lower()).split(" ")
        RsT = False
        try:
            if int(MSg.content) <= 10:
                RsT = True
        except ValueError:
            if (MesS == "cancel") or (MesS == "c") or (MesS == "zhentai") or (MeseS[0] == "zhentai"):
                RsT = True
        return MSg.guild.id == ctx.guild.id and MSg.channel.id == ctx.channel.id and RsT

    def ChCHEm(RcM, RuS):
        return RuS.bot == False and RcM.message == DmSent and str(RcM.emoji) in ["⬅️","❌","➡️","#️⃣"]

    def ChCHEmFN(MSg):
        MesS = MSg.content.lower()
        RsT = False
        try:
            if int(MSg.content):
                RsT = True
        except ValueError:
            if (MesS == "cancel") or (MesS == "c"):
                RsT = True
        return MSg.guild.id == ctx.guild.id and MSg.channel.id == ctx.channel.id and RsT

    def EmbedMaker(DentAi,Page, State):
        DEmE = discord.Embed(title = DentAi.title(Format.Pretty),  description = FdesCtI, color = 0x000000)
        DEmE.set_thumbnail(url = DentAi.image_urls[0])
        DEmE.set_footer(text = f'Released on {DentAi.upload_date}\n\n"n" or "next" for next page. "b"" or "back" for previous page. "go (page n#)" for a specific page. "c" or "close" to end reading.\n\n*The Doujin closes automatically after 2mins of inactivity.*')
        DEmE.set_image(url = DentAi.image_urls[Page])
        DEmE.add_field(name = "Doujin ID", value = DentAi.id, inline = False)
        DEmE.add_field(name = "\u200b", value = f'**Doujin {State}**\n\n`Page: {(Page+1)}/{len(DentAi.image_urls)}`', inline = False)
        return DEmE

    def EmbedMakerfORNum(DentAi,Page, State):
        DEmE = discord.Embed(title = DentAi.title(Format.Pretty),  description = FdesCtI, color = 0x000000)
        DEmE.set_thumbnail(url = DentAi.image_urls[0])
        DEmE.set_image(url = DentAi.image_urls[Page])
        DEmE.add_field(name = "Doujin ID", value = str(DentAi.id), inline = False)
        DEmE.add_field(name = "\u200b", value = "**Doujin " + State +"** \n\n `Page: " + str(Page+1) + "/" + str(len(DentAi.image_urls)) + "`", inline = False)
        DEmE.set_footer(text = 'Choose a number to open navigate to page. "c" or "cancel" to exit navigation.\n\n*The Navigation closes automatically after 10sec of inactivity.*')
        return DEmE

    if args:
        Chlks = " ".join(args).split(" ")
        if Chlks[0].lower() == "search":
            Chlks.pop(0)
            C = 0
            SrchDen = []
            if " ".join(Chlks):
                try:
                    for DeOujin in Utils.search_by_query(query =  f'{" ".join(Chlks)} -tag:"lolicon" -tag:"shotacon"', sort = Sort.Popular):
                        C += 1
                        if C == 1:
                            SEm = discord.Embed(title = f':mag: Search for "{" ".join(Chlks)}"',  description = "\u200b", color = 0x000000)
                        SEm.add_field(name = "\u200b", value = f'{C}. `{DeOujin["title"]["english"]}`', inline = False)
                        SrchDen.append(DeOujin)
                        if C == 10:
                            break
                    SEm.set_footer(text = 'Choose a number to open doujin. "c" or "cancel" to exit search. \n\n*The Search closes automatically after 20sec of inactivity.*' )
                    DmSent = await ctx.message.channel.send(embed = SEm)
                    try:
                        ResS = await DClient.wait_for("message", check = ChCHanS, timeout = 20)
                        LResS = ResS.content.lower()
                        ReseS = (ResS.content.lower()).split(" ")

                        try:
                            if int(ResS.content) <= 10:
                                Srch = SrchDen[int(ResS.content)-1]["id"]
                                DentAi = Hentai(Srch)
                                await DmSent.edit(embed = discord.Embed(title = ":newspaper: Opening...",  description = DentAi.title(Format.Pretty), color = 0x000000)) 
                        except ValueError:
                            if (LResS == "cancel") or (LResS == "c") or (LResS == "zhentai") or (ReseS[0] == "zhentai"):
                                await DmSent.edit(embed = discord.Embed(title = ":newspaper2: Search Cancelled",  description = "\u200b", color = 0x000000))
                    except asyncio.TimeoutError:
                        await DmSent.edit(embed = discord.Embed(title = ":hourglass: Search Timeout...",  description = "\u200b", color = 0x000000))
                except UnboundLocalError:
                    SEm = discord.Embed(title = f':mag: Search for "{" ".join(Chlks)}"',  description = "\u200b", color = 0x000000)
                    SEm.add_field(name = "\u200b", value = "No Results found :woozy_face:", inline = False)
                    await ctx.message.channel.send(embed = SEm)    
            else:
                await ctx.message.channel.send("No search argument :woozy_face:")     
        elif len(Chlks) >= 1:
            try:
                Srch = int(" ".join(args))
            except ValueError:
                if " ".join(args).lower() == "random":
                    while True:
                        Srch = Utils.get_random_id()
                        DentAi = Hentai(Srch)
                        if ("lolicon" not in [tag.name for tag in DentAi.tag]) and ("shotacon" not in [tag.name for tag in DentAi.tag]):
                            break
                else:
                    await ctx.message.channel.send("The argument contained non-numeral characters and wasn't a random request. :no_mouth:")
        try:
            if (Hentai.exists(Srch)):
                DentAi = Hentai(Srch)
                if ("lolicon" not in [tag.name for tag in DentAi.tag]) and ("shotacon" not in [tag.name for tag in DentAi.tag]):
                    if ctx.channel.is_nsfw(): 
                        Tags = ", ".join([tag.name for tag in DentAi.tag])
                        if len(Tags) > 253:
                            FdesCtI = Tags[0:253]
                            FdesCtI = FdesCtI + "..."
                        else:
                            FdesCtI = Tags
                        Page = 0
                        DEm = discord.Embed(title = DentAi.title(Format.Pretty),  description = FdesCtI, color = 0x000000)
                        DEm.set_thumbnail(url = DentAi.image_urls[0])
                        DEm.set_footer(text = f'Released on {DentAi.upload_date}\n\n"n" or "next" for next page. "b"" or "back" for previous page. "go (page n#)" for a specific page. "c" or "close" to end reading.\n\n*The Doujin closes automatically after 2mins of inactivity.*')
                        DEm.set_image(url = DentAi.image_urls[0])
                        DEm.add_field(name = "Doujin ID", value = str(DentAi.id), inline = False)
                        DEm.add_field(name = "\u200b", value = f'**Doujin OPEN**\n\n`Page: {(Page+1)}/{len(DentAi.image_urls)}`', inline = False)
                        await ctx.message.channel.send("**WARNING:** ALL messages sent after the embed will be deleted until doujin is closed. This is to ensure a proper reading experience.")
                        DmSent = await ctx.message.channel.send(embed = DEm)
                await DmSent.add_reaction("⬅️")
                await DmSent.add_reaction("❌")
                await DmSent.add_reaction("➡️")
                await DmSent.add_reaction("#️⃣")
                while True:
                    try:
                        Res = await DClient.wait_for("reaction_add", check = ChCHEm, timeout = 120) 
                        await DmSent.remove_reaction(Res[0].emoji, Res[1])
                        if Res[0].emoji == "⬅️" and Page != 0:
                            Page -= 1
                            await DmSent.edit(embed = EmbedMaker(DentAi, Page, "OPEN"))
                        elif Res[0].emoji == "➡️":
                            if Page < len(DentAi.image_urls)-1:
                                Page += 1
                                await DmSent.edit(embed = EmbedMaker(DentAi, Page, "OPEN"))
                            else:
                                await DmSent.edit(embed = EmbedMaker(DentAi, Page, "CLOSED"))
                                await DmSent.remove_reaction("⬅️", DClient.user)
                                await DmSent.remove_reaction("❌", DClient.user)
                                await DmSent.remove_reaction("➡️", DClient.user)
                                await DmSent.remove_reaction("#️⃣", DClient.user)
                                break
                        elif Res[0].emoji == "#️⃣":
                            if Res[1].id in PrMUsI:
                                await DmSent.edit(embed = EmbedMakerfORNum(DentAi, Page, "CHOOSE A PAGE"))
                                ResE = await DClient.wait_for("message", check = ChCHEmFN, timeout = 10)
                                await ResE.delete()
                                try:
                                    try:
                                        pG = int(ResE.content)
                                        if 0 < pG <= len(DentAi.image_urls)-1:
                                            Page = pG-1
                                        elif pG < 1:
                                            Page = 0
                                            pass
                                        else:
                                            Page = len(DentAi.image_urls)-1 
                                    except TypeError:
                                        pass
                                except ValueError:
                                    pass
                                await DmSent.edit(embed = EmbedMaker(DentAi, Page, "OPEN"))
                            else:
                                TemS = await ctx.message.channel.send("Instant navigation to page is only for voters. Vote [here](https://top.gg/bot/768397640140062721/vote).\n:robot: zvote to learn more. :robot:")
                                await asyncio.sleep(5)
                                await TemS.delete()
                        elif Res[0].emoji == "❌":
                            await DmSent.edit(embed = EmbedMaker(DentAi, Page, "CLOSED"))
                            await DmSent.remove_reaction("⬅️", DClient.user)
                            await DmSent.remove_reaction("❌", DClient.user)
                            await DmSent.remove_reaction("➡️", DClient.user)
                            await DmSent.remove_reaction("#️⃣", DClient.user)
                            break
                    except asyncio.TimeoutError:
                        await DmSent.edit(embed = EmbedMaker(DentAi, Page, "CLOSED"))
                        break
                await ctx.message.channel.send(":newspaper2: Doujin Closed :newspaper2:")
            else:
                await ctx.message.channel.send("That Doujin doesn't exist :expressionless:")
        except UnboundLocalError:
            pass
    else:
        await ctx.message.channel.send("No arguments :no_mouth:")

@DClient.command(name = "covid")
@commands.check(ChBot)
@commands.cooldown(1, 3, commands.BucketType.guild)
async def CovSt(ctx, *args):
    if args:
        CovDLoc = Cov.getLocations()
        ConFC = 0
        DeaFC = 0
        RecFC = 0
        FounCon = False
        for TCov in CovDLoc:
            if TCov["country"].lower() == " ".join(args).lower() or TCov["country_code"].lower() == " ".join(args).lower():
                FounCon = True
                ConT = TCov["country"]
                PopT = TCov["country_population"]
                ConFC += TCov["latest"]["confirmed"]
                DeaFC += TCov["latest"]["deaths"]
                RecFC += TCov["latest"]["recovered"]
        if FounCon:
            CEm = discord.Embed(title = f'{ConT} Covid-19 Status', description = f'This data was requested on {datetime.date.today()}', color = 0xbd9400)
            CEm.add_field(name = "Population: ", value = f'{PopT:,}', inline = False)
            CEm.add_field(name = "Confirmed: ", value = f'{ConFC:,}', inline = False)
            CEm.add_field(name = "Deaths: ", value = f'{DeaFC:,}', inline = False)
            CEm.add_field(name = "Recovered: ", value = f'{RecFC:,}', inline = False)
            CEm.set_footer(text = "Note: Data may not be completely accurate")
        else:
            await ctx.message.channel.send("Country not found :pensive:")
    else: 
        CovDWW = Cov.getLatest()
        CEm = discord.Embed(title = "Worldwide Covid-19 Status", description = f'This data was requested on {datetime.date.today()}', color = 0xbd9400)
        CEm.add_field(name = "Confirmed: ", value = f'{CovDWW["confirmed"]:,}', inline = False)
        CEm.add_field(name = "Deaths: ", value = f'{CovDWW["deaths"]:,}', inline = False)
        CEm.add_field(name = "Recovered: ", value = f'{CovDWW["recovered"]:,}', inline = False)
        CEm.set_footer(text = "Note: Data may not be completely accurate")
    await ctx.message.channel.send(embed = CEm)

@DClient.command(name = "reddit")
@commands.check(ChBot)
@commands.cooldown(1, 3, commands.BucketType.user)
async def SrSub(ctx, *args):
    def EmbOri(REm, Type, SubCpoS):
        REm.add_field(name = "\u200b", value = f'The original post is a {Type} [click here]({SubCpoS.url}) to view the original', inline = False)
        REm.set_image(url = SubCpoS.preview["images"][-1]["source"]["url"])
        return REm

    if len(args) == 1:
        Tries = 0
        if CheckSub("".join(args)):
            while True:
                if Tries >= 100:
                    break
                try:
                    Post = Reddit.subreddit("".join(args)).hot()
                    ChoicePosts = random.randint(1, 100)
                    for _ in range(0, ChoicePosts):
                        SubCpoS = next(Sub for Sub in Post if not Sub.stickied)
                    break
                except StopIteration:
                    print("Again")
                    Tries += 1
                    continue

            if len(SubCpoS.title) > 253:
                FtiTle = SubCpoS.title[0:253]
                FtiTle = FtiTle + "..."
            else:
                FtiTle = SubCpoS.title

            if len(SubCpoS.selftext) > 1021:
                FteXt = SubCpoS.selftext[0:1021]
                FteXt = FteXt + "..."
            else:
                FteXt = SubCpoS.selftext

            if PosType(SubCpoS):
                NSfw = False
                if SubCpoS.over_18 and ctx.channel.is_nsfw():
                    REm = discord.Embed(title = FtiTle,  description = f'Upvote Ratio: {SubCpoS.upvote_ratio} // Post is NSFW', color = 0x8b0000)
                    NSfw = True
                else:
                    REm = discord.Embed(title = FtiTle, description = f'Upvote Ratio: {SubCpoS.upvote_ratio} // Post is Clean', color = 0x8b0000)
                if (NSfw and ctx.channel.is_nsfw()) or (NSfw == False):
                    if SubCpoS.selftext != "":
                        REm.add_field(name = "Body", value = FteXt, inline = False)
                    REm.add_field(name = "Post: ", value = SubCpoS.url, inline = True)
                else:
                    REm.add_field(name = "NSFW: ", value = "This channel isn't NSFW. No NSFW here", inline = False)
            else:
                NSfw = False
                if SubCpoS.over_18:
                    if ctx.channel.is_nsfw():
                        REm = discord.Embed(title = FtiTle,  description = f'Upvote Ratio: {SubCpoS.upvote_ratio} // Post is NSFW', color = 0x8b0000)
                    else:
                        REm = discord.Embed(title = "***NOT NSFW CHANNEL***",  description = "Post is NSFW", color = 0x8b0000)
                    NSfw = True
                else:
                    REm = discord.Embed(title = FtiTle, description = f'Upvote Ratio: {SubCpoS.upvote_ratio} // Post is Clean', color = 0x8b0000)
                C = 0
                if (NSfw and ctx.channel.is_nsfw()) or (NSfw == False):
                    try:
                        GaLpos = SubCpoS.gallery_data["items"]
                        for ImgPoGa in GaLpos:
                            FiPoS = SubCpoS.media_metadata[ImgPoGa["media_id"]]
                            if FiPoS["e"] == "Image":
                                REm.add_field(name = "\u200b", value = f'The original post is a gallery [click here]({SubCpoS.url}) to view the rest of the post', inline = False)
                                pstR = FiPoS["p"][-1]["u"]
                                REm.set_image(url = pstR)
                                break
                    except AttributeError:
                        for ExT in [".png",".jpg",".jpeg",".gif",".gifv"]:
                            C += 1
                            if (SubCpoS.url).endswith(ExT):
                                pstR = SubCpoS.url
                                if ExT == ".gifv":
                                    REm.add_field(name = "\u200b", value = f'The original post is a video(imgur) [click here]({SubCpoS.url}) to view the original', inline = False)
                                    pstR = SubCpoS.url[:-1]
                                REm.set_image(url = pstR)
                                break
                            elif C == 5: 
                                try:
                                    if "v.redd.it" in SubCpoS.url:
                                        EmbOri(REm, "video (reddit)", SubCpoS)
                                    elif "youtu.be" in SubCpoS.url  or "youtube.com" in SubCpoS.url:
                                        EmbOri(REm, "video (youtube)", SubCpoS)
                                    elif "gfycat" in SubCpoS.url:
                                        EmbOri(REm, "video (gfycat)", SubCpoS)
                                    elif "redgifs" in SubCpoS.url:
                                        EmbOri(REm, "video (redgifs)", SubCpoS)
                                    else:
                                        EmbOri(REm, "webpage", SubCpoS)
                                except AttributeError:
                                    REm.add_field(name = "Post: ", value = SubCpoS.url, inline = False)
                                    REm.add_field(name = "Media Preview Unavailable. Sorry!!", value = '\u200b')
                else:
                    REm.add_field(name = "NSFW: ", value = "This isn't an NSFW channel. No NSFW allowed here.", inline = False)
            REm.set_footer(text = f'From r/{"".join(args)}')
            REm.set_author(name = f'*By u/{SubCpoS.author}*')
            await ctx.message.channel.send(embed = REm)
        else:
            await ctx.message.channel.send("Sub doesn't exist or private :expressionless: (Make sure the argument doesnt include the r/)")
    elif len(args) == 0:
        await ctx.message.channel.send("No arguments :no_mouth:")
    
    else:
        await ctx.message.channel.send("Too many arguments :no_mouth:")

@DClient.command(name = "add")
@commands.check(ChBot)
@commands.check(ChAdmin)
@commands.check(ChSer)
@commands.cooldown(1, 1, commands.BucketType.user)
async def AWord(ctx, *args): 
    WorA = " ".join(args)
    if FuncMon.DbAdd(Col, {"IDd":"GuildInfo","IDg":str(ctx.guild.id)}, WorA, 0):
        Msg = f'"{WorA}" ADDED :thumbsup:' 
        FuncMon.DbAppendRest(Col, {"IDg":str(ctx.guild.id)}, {"IDd":"GuildInfo","IDg":str(ctx.guild.id)}, WorA, 0, "a")
    else:
        Msg = f'"{WorA}" ALREADY EXIST :confused:'
    await ctx.message.channel.send(Msg)

@DClient.command(aliases = ["rem","remove"])
@commands.check(ChBot)
@commands.check(ChAdmin)
@commands.check(ChSer)
@commands.cooldown(1, 1, commands.BucketType.user)
async def RWord(ctx, *args):
    WorA = " ".join(args)
    if FuncMon.DbRem(Col, {"IDd":"GuildInfo", "IDg":str(ctx.guild.id)}, WorA):
        Msg = f'"{WorA}" REMOVED :thumbsup:'
        FuncMon.DbAppendRest(Col, {"IDg":str(ctx.guild.id)}, {"IDd":"GuildInfo","IDg":str(ctx.guild.id)}, WorA, 0, "r")
    else:
        Msg = f'"{WorA}" DOESNT EXIST :confused:'
    await ctx.message.channel.send(Msg)  

@DClient.command(name = "list")
@commands.check(ChBot)
@commands.check(ChSer)
@commands.cooldown(1, 1, commands.BucketType.user)
async def LWord(ctx):
    LEm = discord.Embed(title = "Server List", description = "Words/Phrases being tracked", color = 0xf59542) 

    DbB = Col.find({"IDd":"GuildInfo","IDg":str(ctx.guild.id)})
    for i in DbB:
        Kyes = i.keys()

    for Wp in Kyes:
        if Wp == "_id" or Wp == "IDd" or Wp == "IDg" or Wp == "Setup":
            pass
        else:
            LEm.add_field(name = Wp, value =  "\u200b", inline = True)
    await ctx.message.channel.send(embed = LEm)     

@DClient.command(name = "remind")
@commands.check(ChBot)
@commands.cooldown(1, 1, commands.BucketType.user)
async def RmdAtDMY(ctx, *args):
    def TtWaT(Day, Hour, Min, Sec):
        return (Day*86400) + (Hour*3600) + (Min*60) + (Sec)
    def ChCHEm(RcM, RuS):
        return RuS.bot == False and RcM.message == RemTmm and str(RcM.emoji) in ["✅","❌"]
    if args:
        try:
            EnPerT = (" ".join(args)).split(" ")
            D = 0
            H = 0
            M = 0
            S = 0
            for TimSE in EnPerT:
                if TimSE[-1].lower() == "d":
                    D += int(TimSE[:-1])
                elif TimSE[-1].lower() == "h":
                    H += int(TimSE[:-1])
                elif TimSE[-1].lower() == "m":
                    M += int(TimSE[:-1])
                elif TimSE[-1].lower() == "s":
                    S += int(TimSE[:-1])
                else:
                    raise ValueError
            TToTm = TtWaT(D,H,M,S)
            if TToTm <= 518400:
                RemTmm = await ctx.message.channel.send(f':timer: Are you sure you want to me reminded in {StrTSTM(TToTm)}? :timer:')
                await RemTmm.add_reaction("❌")
                await RemTmm.add_reaction("✅")
                try:
                    ReaEm = await DClient.wait_for("reaction_add", check = ChCHEm, timeout = 10)
                    if ReaEm[0].emoji == "✅":
                        await RemTmm.edit(content = f'You will be pinged in {StrTSTM(TToTm)} :thumbsup:')
                        await asyncio.sleep(2)
                        await RemTmm.delete()
                        await asyncio.sleep(TToTm)
                        await ctx.message.channel.send(f':timer: Its been {StrTSTM(TToTm)} {ctx.message.author.mention} :timer:') 
                    elif  ReaEm[0].emoji == "❌":
                        await RemTmm.edit(content = "Request Cancelled :thumbsup:")
                        await asyncio.sleep(2)
                        await RemTmm.delete()
                except asyncio.TimeoutError:
                    await RemTmm.edit(content = "Request Timeout :alarm_clock:")
                    await asyncio.sleep(2)
                    await RemTmm.delete()
            else:
                await ctx.message.channel.send("zremind is limited to waiting for 6days. :cry:")      
        except ValueError:
            await ctx.message.channel.send('Argument was improper. Check "zhelp misc" to check how to use it. :no_mouth:')    
    else:
        await ctx.message.channel.send("No arguments given :no_mouth:")

@DClient.command(name = "reset")
@commands.check(ChBot)
@commands.check(ChAdmin)
@commands.check(ChSer)
@commands.cooldown(1, 1, commands.BucketType.user)
async def ReAll(ctx):
    def ChCHEm(RcM, RuS):
        return RuS.bot == False and RcM.message == ReSConF and str(RcM.emoji) in ["✅","❌"]
        
    ResEmF = discord.Embed(title = "Delete ALL server data?", description = "This is ```IRREVERSIBLE```", color = 0xf59542)
    ResEmF.set_footer(text = "*The reset request timesout in 10secs.*")
    ReSConF = await ctx.message.channel.send(embed = ResEmF)
    await ReSConF.add_reaction("❌")
    await ReSConF.add_reaction("✅")
    try:
        ReaEm = await DClient.wait_for("reaction_add", check = ChCHEm, timeout = 10) 
        await ReSConF.remove_reaction("❌", DClient.user)
        await ReSConF.remove_reaction("✅", DClient.user)
        if ReaEm[0].emoji == "❌":
            await ReSConF.edit(embed = discord.Embed(title = "Cancelled :thumbsup:", description = "Nothing was removed", color = 0xf59542))
        elif ReaEm[0].emoji == "✅":
            if Col.count_documents({"IDd":"GuildInfo","IDg":str(ctx.guild.id),"Setup":"Done"}) > 0:
                DbB = Col.find({"IDg":str(ctx.guild.id)})
                for DbG in DbB:
                    Col.delete_one(DbG)
                await ReSConF.edit(embed = discord.Embed(title = "Success :thumbsup:", description = "All info was cleared", color = 0xf59542))
    except asyncio.TimeoutError:
        await ReSConF.remove_reaction("❌", DClient.user)
        await ReSConF.remove_reaction("✅", DClient.user)
        await ReSConF.edit(embed = discord.Embed(title = "Timeout :alarm_clock:", description = "Nothing was removed", color = 0xf59542))

@DClient.command(name = "top")
@commands.check(ChBot)
@commands.check(ChSer)
@commands.cooldown(1, 1, commands.BucketType.user)
async def ToTMsg(ctx, *args):
    def GetNVa(DiDIV, WtRt = 0):
        for Mks in DiDIV:
            for MjsD in DiDIV[Mks]:
                if WtRt == 1:
                    return MjsD
                else:
                    return DiDIV[Mks][MjsD]
    Top = []
    Enput = " ".join(args)
    DbB = Col.find({"IDd":"GuildInfo","IDg":str(ctx.guild.id)})
    SrtI = await ctx.message.channel.send(embed = discord.Embed(title = ":mag: Fetching...",  description = "\u200b", color = 0x3252a8))
    for i in DbB:
        Kyes = i.keys()
    if not args:
        IEm = discord.Embed(title = ctx.guild.name, description = "Leaderboard", color = 0x3252a8)
        for Wp in Kyes:
            OSfDb = Col.find({"IDg":str(ctx.guild.id)})
            if Wp == "_id" or Wp == "IDd" or Wp == "IDg" or Wp == "Setup":
                pass
            else:
                for j in OSfDb:
                    if j["IDd"] != "GuildInfo":
                        Top.append({j["IDd"]:{Wp:j[Wp]}})
        Top = sorted(Top,key = GetNVa)
        for i in range(1,4):
            x = int(list(Top[-i].keys())[0])
            IEm.add_field(name = f'**`{i}. {(ctx.guild.get_member(x)).nick}:`** {GetNVa(Top[-i], 1)} = {GetNVa(Top[-i]):,}', value = "\u200b", inline = False)
        await SrtI.edit(embed = IEm)
    elif Enput in Kyes:
        IEm = discord.Embed(title = ctx.guild.name, description = f'Leaderboard for {Enput}', color = 0x3252a8)
        OSfDb = Col.find({"IDg":str(ctx.guild.id)})
        for j in OSfDb:
            if j["IDd"] != "GuildInfo":
                Top.append({j["IDd"]:{Enput:j[Enput]}})
        Top = sorted(Top,key = GetNVa)
        for i in range(1,4):
            x = int(list(Top[-i].keys())[0])
            IEm.add_field(name = f'**`{i}. {(ctx.guild.get_member(x)).nick}:`** {GetNVa(Top[-i], 1)} = {GetNVa(Top[-i]):,}', value = "\u200b", inline = False)
        await SrtI.edit(embed = IEm)
    else:
        await SrtI.edit(embed = discord.Embed(title = "That word doesnt exist yet :confused:",  description = "\u200b", color = 0x3252a8))

@DClient.command(name = "total")
@commands.check(ChBot)
@commands.check(ChSer)
@commands.cooldown(1, 1, commands.BucketType.user)
async def TMsg(ctx, *args):
    Num = 0
    Enput = " ".join(args)
    DbB = Col.find({"IDd":"GuildInfo","IDg":str(ctx.guild.id)})
    OSfDb = Col.find({"IDg":str(ctx.guild.id)})
    for i in DbB:
        Kyes = i.keys()

    if (Enput == "") or (Enput == " "):
        IEm = discord.Embed(title = ctx.guild.name, description = "Total times repeated", color = 0x3252a8)
        for Wp in Kyes:
            Num = 0
            OSfDb = Col.find({"IDg":str(ctx.guild.id)})
            if Wp == "_id" or Wp == "IDd" or Wp == "IDg" or Wp == "Setup":
                pass
            else:
                for j in OSfDb:
                    Num += j[Wp]
                    
                IEm.add_field(name = Wp, value = Num, inline = True)
        await ctx.message.channel.send(embed = IEm)

    elif Enput in Kyes:
        IEm = discord.Embed(title = ctx.guild.name, description = f'Total times {Enput} was repeated', color = 0x3252a8)
        for j in OSfDb:
            Num += j[Enput]

        IEm.add_field(name = Enput, value = Num, inline = True)
        await ctx.message.channel.send(embed = IEm)
    
    else:
        await ctx.message.channel.send("That word doesnt exist yet :confused:")

@DClient.command(name = "pdf")
@commands.check(ChBot)
@commands.cooldown(1, 5, commands.BucketType.user)
async def PdSwtOI(ctx, *args):
    def EmbTI(NfIRa, ImGCns, NpIMg, SImAUp):
        try:
            ImFA = SImAUp[NpIMg]
            print("Cached...")
            SEco = False
        except IndexError:
            print("Uploading...")
            ImGCns[NpIMg].save(f'{NfIRa}.jpg', "JPEG")
            ImFA = Imgur.upload_from_path(f'{NfIRa}.jpg')["link"]
            SEco = True
        PcEmE = discord.Embed(title = "PDF Viewer")
        PcEmE.set_image(url = ImFA)
        PcEmE.add_field(name = f'```{NpIMg+1}/{len(ImGCns)}```', value = "\u200b")
        PcEmE.set_footer(text = "Make sure to close the PDF once you are done .\n\n*PDF closes automatically after 2mins of inactivity.*")
        return SEco, ImFA, PcEmE

    def ChCHEm(RcM, RuS):
        return RuS.bot == False and RcM.message == PcEm and str(RcM.emoji) in ["⬅️","❌","➡️"]
    if (len(ctx.message.attachments) == 1 and len(args) == 0) or (len(ctx.message.attachments) == 0 and len(args) == 1):
        AttLi = []
        ArC = " ".join(args).split(" ")
        if len(ctx.message.attachments) == 1:
            for AtT in ctx.message.attachments:
                AttLi.append(AtT.url)
        else:
            try:
                for Lin in ArC:
                    AttLi.append(Lin)
            except TypeError:
                pass

        for DoPdRd in AttLi:
            try:
                TyPaT = requests.head(DoPdRd).headers.get("content-type").split("/")[1]
                if TyPaT == "pdf":
                    ChLeT = "ioewsahkzcldnpq"
                    NfIRa = "".join((random.choice(ChLeT) for i in range(10)))
                    rETyP = requests.get(DoPdRd, allow_redirects = True)
                    open(f'{NfIRa}.pdf', "wb").write(rETyP.content)
                    ImGCns = convert_from_path(f'{NfIRa}.pdf', 500, last_page = 40) 
                    print(ImGCns)
                    NpIMg = 0   
                    SImAUp = [] 
                    PcEm = await ctx.message.channel.send(embed = discord.Embed(title = "Uploading Page...", description = "After upload a page will no longer be uploaded again (Faster navigation to page)"))
                    SEco, ImFA, PcEmE = EmbTI(NfIRa, ImGCns, NpIMg, SImAUp)
                    if SEco:
                        SImAUp.append(ImFA)
                    await PcEm.edit(embed = PcEmE)
                    await PcEm.add_reaction("⬅️")
                    await PcEm.add_reaction("❌")
                    await PcEm.add_reaction("➡️")
                    while True:
                        try:
                            ReaEm = await DClient.wait_for("reaction_add", check = ChCHEm, timeout = 120) 
                            await PcEm.remove_reaction(ReaEm[0].emoji, ReaEm[1])
                            if ReaEm[0].emoji == "⬅️" and NpIMg != 0:
                                NpIMg -= 1     
                                SEco, ImFA, PcEmE = EmbTI(NfIRa, ImGCns, NpIMg, SImAUp)
                                if SEco:
                                    SImAUp.append(ImFA)
                                await PcEm.edit(embed = PcEmE)

                            elif ReaEm[0].emoji == "➡️":
                                if NpIMg < len(ImGCns)-1:
                                    NpIMg += 1
                                    SEco, ImFA, PcEmE = EmbTI(NfIRa, ImGCns, NpIMg, SImAUp)
                                    if SEco:
                                        SImAUp.append(ImFA)
                                    await PcEm.edit(embed = PcEmE)
                                else:
                                    await PcEm.remove_reaction("⬅️", DClient.user)
                                    await PcEm.remove_reaction("❌", DClient.user)
                                    await PcEm.remove_reaction("➡️", DClient.user)
                                    os.remove(f'{NfIRa}.jpg')
                                    os.remove(f'{NfIRa}.pdf')
                                    break

                            elif ReaEm[0].emoji == "❌":
                                await PcEm.remove_reaction("⬅️", DClient.user)
                                await PcEm.remove_reaction("❌", DClient.user)
                                await PcEm.remove_reaction("➡️", DClient.user)
                                os.remove(f'{NfIRa}.jpg')
                                os.remove(f'{NfIRa}.pdf')
                                break
                        except asyncio.TimeoutError:
                            await PcEm.remove_reaction("⬅️", DClient.user)
                            await PcEm.remove_reaction("❌", DClient.user)
                            await PcEm.remove_reaction("➡️", DClient.user)
                            os.remove(f'{NfIRa}.jpg')
                            os.remove(f'{NfIRa}.pdf')
                            break
            except requests.exceptions.MissingSchema:
                await ctx.message.channel.send("Not a PDF :woozy_face:")
    else:
        await ctx.message.channel.send("No or too many attachments :woozy_face:")

@DClient.command(name = "stats")
@commands.check(ChBot)
@commands.check(ChSer)
@commands.cooldown(1, 1, commands.BucketType.user)
async def IMsg(ctx, *args): 
    isBot = False
    if len(ctx.message.mentions) > 0:
        if ctx.message.mentions[0].bot == False and (f'<@!{ctx.message.mentions[0].id}>') == args[0]:
            AUmN = ctx.message.mentions[0]
            aRGu = list(args)
            aRGu.pop(0)
        elif ctx.message.mentions[0].bot == True:
            isBot = True
        else:
            pass
    else:
        AUmN = ctx.author
        aRGu = list(args)

    if isBot == False:
        Num = 0
        Enput = " ".join(aRGu)
        DbB = Col.find({"IDd":"GuildInfo","IDg":str(ctx.guild.id)})
        OSfDb = Col.find({"IDd":str(AUmN.id),"IDg":str(ctx.guild.id)})
        for i in DbB:
            Kyes = i.keys()

        if (Enput == "") or (Enput == " "):
            IEm = discord.Embed(title = AUmN.display_name, description = "All stats", color = 0x3252a8)
            for Wp in Kyes:
                OSfDb = Col.find({"IDd":str(AUmN.id),"IDg":str(ctx.guild.id)})
                if Wp == "_id" or Wp == "IDd" or Wp == "IDg" or Wp == "Setup":
                    pass
                else:
                    for j in OSfDb:
                        Num = j[Wp]
                    IEm.add_field(name = Wp, value = Num, inline = True)
            await ctx.message.channel.send(embed = IEm)

        elif Enput in Kyes:
            IEm = discord.Embed(title = AUmN.display_name, description = "Word stats", color = 0x3252a8)
            for j in OSfDb:
                Num = j[Enput]
            IEm.add_field(name = Enput, value = Num, inline = True)
            await ctx.message.channel.send(embed = IEm)    
        else:
            await ctx.message.channel.send("That word doesnt exist yet! :confused:")
    elif isBot == True:
        await ctx.message.channel.send("Cannot check a bot's stats :confused:")

@DClient.command(name = "giphy")
async def Gfin(ctx, *args):
    if args:
        try:
            QRGifs = GApi.gifs_search_get(GClient, " ".join(args), limit = 50)
            GifSAl = list(QRGifs.data)
            GifF = random.choices(GifSAl)
            await ctx.message.channel.send(GifF[0].url)
        except IndexError:
            await ctx.message.channel.send("No gifs found :expressionless:")
    else:
        await ctx.message.channel.send("No search term given :confused:")

@DClient.command(name = "fry")
@commands.check(ChBot)
@commands.cooldown(1, 1, commands.BucketType.user)
async def CMsend(ctx, *args):
    if len(ctx.message.attachments) > 0 or args:
        ArC = " ".join(args).split(" ")
        AttLi = []
        if ArC[0] == "profile":
            ArC.pop(0)
            if len(ctx.message.mentions) > 0 and (f'<@!{ctx.message.mentions[0].id}>') == ArC[0]:
                AttLi.append(str((ctx.message.mentions[0]).avatar_url))
                ArC.pop(0)
            else:
                AttLi.append(str(ctx.author.avatar_url))
        try:
            for Lin in ArC:
                AttLi.append(Lin)
        except TypeError:
            pass
        for AtT in ctx.message.attachments:
            AttLi.append(AtT.url)
        files = []
        C = 0
        for file in AttLi:
            try:
                if requests.head(file).headers.get("content-type").split("/")[0] == "image":
                    C += 1
                    r = requests.get(file, allow_redirects = True)
                    open("NsRndo.jpg", "wb").write(r.content)
                    img = Image.open("NsRndo.jpg")
                    img = await deeppyer.deepfry(img, flares = False)
                    img.save("NsRndo.jpg")
                    files.append(discord.File("NsRndo.jpg"))
                    await ctx.message.channel.send(files = files)
                    files.pop(0)
                    os.remove("NsRndo.jpg")
                else:
                    await ctx.message.channel.send(f'file({C}) isnt a valid image type :sweat:')
            except requests.exceptions.MissingSchema:
                pass
    else:
        await ctx.message.channel.send("No image(s) or link(s) were attached :woozy_face:")

@DClient.event
async def on_message(message):
    CmSLim = 0
    if Col.count_documents({"IDd":"GuildInfo","IDg":str(message.guild.id),"Setup":"Done"}) != 0:
        DbB = Col.find({"IDd":"GuildInfo","IDg":str(message.guild.id),"Setup":"Done"})
        for i in DbB:
            KMeys = i.keys()
        Remove = '*_'
        PhMsRase = ((message.content.lower()).strip(Remove)).split(" ")
        PhMsRase = removeExtraS(PhMsRase, "")
        LoKmeys = 1
        for Ph in KMeys:
            if len(Ph.split(" ")) > LoKmeys:
                LoKmeys = len(Ph.split(" "))        
        if message.author.bot == False:
            for _ in range(len(PhMsRase)):
                if CmSLim >= 10:
                    print("Broke count")
                    break
                Temp = []
                for MMmsg in PhMsRase:
                    if CmSLim >= 10:
                        break
                    Temp.append(MMmsg)
                    CTemp = " ".join(Temp)
                    if LoKmeys >= len(Temp) > 0:
                        if FuncMon.AddTo(Col, {"IDd":str(message.author.id),"IDg":str(message.guild.id)}, CTemp, 1):
                            print("Added")
                            CmSLim += 1
                    else:
                        break
                try:
                    PhMsRase.pop(0)
                except IndexError:
                    pass
    else:
        pass
    await DClient.process_commands(message)

@DClient.event
async def on_ready():
    await DClient.change_presence(activity = discord.Game(random.choice(Doing)))
    print(f'Online in {len(DClient.guilds)}...')

@DClient.event
async def on_member_join(member):
    Pid = member
    if Pid.bot == False:
        if Col.count_documents({"IDd":str(Pid.id),"IDg":str(member.guild.id)}) == 0 and Col.count_documents({"IDd":"GuildInfo","IDg":str(member.guild.id),"Setup":"Done"}) == 1:
            Col.insert_one({"IDd":str(Pid.id),"IDg":str(member.guild.id)})
            DbB = Col.find({"IDd":"GuildInfo","IDg":str(member.guild.id),"Setup":"Done"})
            print("Adding (join)")
            for i in DbB:
                Kyes = i.keys()
            for Wp in Kyes:
                FuncMon.DbAdd(Col, {"IDd":str(Pid.id),"IDg":str(member.guild.id)}, Wp, 0)

@DClient.event
async def on_dbl_vote(Dt):
    print(f'{Dt.user.id} voted')
    try:
        PrMUsI.remove(Dt.user.id)
    except ValueError:
        pass
    PrMUsI.append(Dt.user.id)
    print(PrMUsI)
    await asyncio.sleep(60*60*12)
    print("gone")
    PrMUsI.remove(Dt.user.id)

@DClient.event
async def on_member_remove(member):
    Pid = member
    if Pid.bot == False:
        if (Col.count_documents({"IDd":str(Pid.id),"IDg":str(member.guild.id)}) != 0):
            Col.delete_one({"IDd":str(Pid.id),"IDg":str(member.guild.id)})

@DClient.event
async def on_guild_remove(guild):
    if Col.count_documents({"IDd":"GuildInfo","IDg":str(guild.id),"Setup":"Done"}) > 0:
        DbB = Col.find({"IDg":str(guild.id)})
        for DbG in DbB:
            Col.delete_one(DbG)

@CalCeR.error
async def eCalCeRror(ctx, error):
    if isinstance(error, commands.UnexpectedQuoteError):
        await ctx.message.channel.send("Failed to calculate :confused:")
    raise error

@DClient.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.channel.send(f'Hold the spam. Wait atleast {StrTSTM(round(error.retry_after, 2))}')
    elif isinstance(error, IsBot):
        await ctx.message.channel.send("Bots can't use commands :pensive:")
    elif isinstance(error, IsAdmin):
        await ctx.message.channel.send("Non-admins are not allowed to use this command :face_with_raised_eyebrow:")
    elif isinstance(error, IsVote):
        await ctx.message.channel.send("This command is only for voters! You can vote [here](https://top.gg/bot/768397640140062721/vote) :no_mouth:")
    elif isinstance(error, ProfSer):
        await ctx.message.channel.send(":point_right: Please setup your server first (with 'zsetup')! Check all server commands with 'zhelp server' :point_left:")   
    elif isinstance(error, commands.CommandNotFound):
        pass 
    else:
        raise error

DClient.run("NzY4Mzk3NjQwMTQwMDYyNzIx.X4_4EQ.mpWIl074jvRs0X-ceDoKdwv4H_E")