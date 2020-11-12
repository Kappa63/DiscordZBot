import discord
import praw
import random
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import FuncMon
import ItemFind
import os  
import deeppyer
from PIL import Image
import requests
from prawcore import NotFound, Forbidden
from hentai import Utils, Sort, Hentai, Format
import asyncio
import giphy_client
import twitter
import mal
import malclient

Mdb = "mongodb+srv://Kappa:85699658@cbotdb.exsit.mongodb.net/CBot?retryWrites=true&w=majority"
Cls = MongoClient(Mdb)
DbM = Cls["CBot"]
Col = DbM["Ser"]
TraEco = DbM["Ind"]

REqInt = discord.Intents.default()
REqInt.members = True

DClient = commands.Bot(case_insensitive = True, command_prefix = ["z","Z"], help_command = None, intents = REqInt)

Twitter = twitter.Api(consumer_key = "2lv4MgQDREClbQxjeWOQU5aGf", consumer_secret = "4vq5UjqJetyLm37YhQtpc6htb0WPimFJVV088TL0LDMXHUdYTA", access_token_key = "1297802233841623040-rYG0sXCKz0PSDUNAhUPx9hecf507LY", access_token_secret = "02dNbliU0EJOfUzGx8UVmrbaqZTlYOmwwKAWqnkecWzgd")

Reddit = praw.Reddit(client_id = "ntnBVsoqGHtoNw", client_secret = "ZklNqu4BQK4jWRp9dYXb4ApoQ10", user_agent = "CBot by u/Kamlin333")

GClient = "ZH1xoGH0XUffrtqFKdj3kD4YrVoZvb8i"
GApi = giphy_client.DefaultApi()

Doing = ["Calculations", "Flipping", "Cry away the pain at night, so I can fake a smile next day", "Griffin", "Getting Tortured", "Crying", "Still Counting", "Telescopes", "In Pain", "Aerodynamics", "Not A Robot", "Astrology", "Quantum Physics"]

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

def StrCool(ErrorCoolSec):
    Day = 0
    Hour = 0
    Min = 0
    while ErrorCoolSec >= 60:
        Min += 1
        if Min == 60:
            Hour += 1
            Min -= 60
        if Hour == 24:
            Day += 1
            Hour -= 24
        ErrorCoolSec -= 60
    if Day != 0:
        return str(Day)+"Day(s) "+str(Hour)+"Hour(s) "+str(Min)+"Min(s) "+str(ErrorCoolSec)+"Sec(s)"
    elif Hour != 0:
        return str(Hour)+"Hour(s) "+str(Min)+"Min(s) "+str(ErrorCoolSec)+"Sec(s)"
    elif Min != 0:
        return str(Min)+"Min(s) "+str(ErrorCoolSec)+"Sec(s)"
    else:
        return str(ErrorCoolSec)+"Sec(s)"

class IsBot(commands.CheckFailure):
    pass
def ChBot(ctx):
    if ctx.author.bot:
        raise IsBot("Bot")
    return True

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
        HEm.add_field(name = "zsetup: ", value = "Sets up the bot for the first time for counting/tracking", inline = False)
        HEm.add_field(name = "zhelp server: ", value = "Provides all the server commands (including word track commands)", inline = False) 
        HEm.add_field(name = "zhelp misc: ", value = "Miscellaneous commands", inline = False)   
        await ctx.message.channel.send(embed = HEm)
    elif "".join(args).lower()  == "server":
        HEm = discord.Embed(title = "**ZBot Server Help**", description = "\u200b", color = 0x0af531)
        HEm.add_field(name = "zadd: ", value = "Adds a word/phrase to keep track of", inline = False)
        HEm.add_field(name = "zremove: ", value = "Removes an existing word/phrase being tracked", inline = False)
        HEm.add_field(name = "zlist: ", value = "Returns all added words/phrases", inline = False)
        HEm.add_field(name = "zstats (@): ", value = "Returns stats for ALL words/phrases", inline = False)
        HEm.add_field(name = "zstats (@)(Word): ", value = "Returns stats for a SPECIFIC word/phrase", inline = False)
        HEm.add_field(name = "ztotal: ", value = "Returns the total number of times ALL words/phrases have been said in the server", inline = False)
        HEm.add_field(name = "ztotal (Word): ", value = "Returns the total number of times a SPECIFIC word/phrase has been said in the server", inline = False)
        HEm.set_footer(text = "Note: Counting is limited to 10 per Message to reduce spam incentives")
        await ctx.message.channel.send(embed = HEm)
    elif "".join(args).lower() == "misc" or "".join(args).lower() == "miscellaneous":
        HEm = discord.Embed(title = "**ZBot Misc. Help**", description = "\u200b", color = 0x0af531)
        HEm.add_field(name = "zfry (Image Attachment/Image Url): ", value = "Deep fries the image", inline = False)
        HEm.add_field(name = "zfry profile (@): ", value = "Deep fries the avatar", inline = False)
        HEm.add_field(name = "zreddit (Subreddit Name): ", value = "Returns a post from the top 50 posts in hot from any subreddit", inline = False)
        HEm.add_field(name = "ztwitter (User @): ", value = "Returns the user profile", inline = False)
        HEm.add_field(name = "ztwitter search (Username): ", value = "Searches for 10 users related to search argument", inline = False)
        HEm.add_field(name = "zanime (Anime Name): ", value = "Searches for anime and returns all the info about chosen anime", inline = False)
        HEm.add_field(name = "zhentai (Magic Numbers): ", value = "Gets doujin from nhentai using magic numbers", inline = False)
        HEm.add_field(name = "zhentai random: ", value = "Gets a random doujin from nhentai", inline = False)
        HEm.add_field(name = "zhentai search (Doujin Name): ", value = "Searches for the 10 most popular doujin", inline = False)
        HEm.add_field(name = "zgiphy (Phrase/Word to search for): ", value = "Returns a random gif from top 50 results on giphy", inline = False)
        HEm.set_footer(text = "Note: Some hentai are not available. This is to abide by the discord TOS")
        await ctx.message.channel.send(embed = HEm)
    else:
        await ctx.message.channel.send("That help category doesn't exist.")

@DClient.command(aliases = ["ver","version"])
@commands.check(ChBot)
@commands.cooldown(1, 1, commands.BucketType.user)
async def RetVer(ctx):
    VEm = discord.Embed(title = "Active Version", description = "ZBot build version and info", color = 0xf59542)
    VEm.add_field(name = "Dev: ", value = "Kappa", inline = True)
    VEm.add_field(name = "Version: ", value = "0.4b", inline = True)
    VEm.add_field(name = "Release: ", value = "Null", inline = True)
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
        await ctx.message.channel.send(":partying_face: Setup complete, you can now use tracking commands:partying_face:")
    else:
        await ctx.message.channel.send(":partying_face: This server is already setup :partying_face:")

@DClient.command(name = "anime")
@commands.check(ChBot)
@commands.cooldown(1, 5, commands.BucketType.guild)
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
            SAEm = discord.Embed(title = ":mag: Search for '" + Srks + "'",  description = "\u200b", color = 0xa49cff)
            for AniRes in mal.AnimeSearch(Srks).results:
                C += 1
                if C == 1:
                    SAEm = discord.Embed(title = ":mag: Search for '" + Srks + "'",  description = "\u200b", color = 0xa49cff)
                SAEm.add_field(name = "\u200b", value = str(C) + ". `" + AniRes.title + "`", inline = False)
                SrchAni.append(AniRes)
                if C == 10:
                    break
            SAEm.set_footer(text = "Choose a number to view MAL entry. 'c' or 'cancel' to exit search. \n\n*The Search closes automatically after 20sec of inactivity.*" )
            AnSrS = await ctx.message.channel.send(embed = SAEm)
            try:
                ResS = await DClient.wait_for('message', check = ChCHanS, timeout = 20)
                LResS = ResS.content.lower()
                try:
                    if int(ResS.content) <= 10:
                        AniI = SrchAni[int(ResS.content)-1].mal_id
                        await AnSrS.edit(embed = discord.Embed(title = ":calling: Finding...",  description = SrchAni[int(ResS.content)-1].title, color = 0xa49cff)) 
                except ValueError:
                    if (LResS == "cancel") or (LResS == "c"):
                        await AnSrS.edit(embed = discord.Embed(title = ":x: Search Cancelled",  description = "\u200b", color = 0xa49cff))
            except asyncio.TimeoutError:
                await AnSrS.edit(embed = discord.Embed(title = ":hourglass: Search Timeout...",  description = "\u200b", color = 0xa49cff))
        except UnboundLocalError:
            SAEm = discord.Embed(title = ":mag: Search for '" + Srks + "'",  description = "\u200b", color = 0xa49cff)
            SAEm.add_field(name = "\u200b", value = "No Results found :woozy_face:", inline = False)
            await ctx.message.channel.send(embed = SAEm)

        try:
            AniF = MClient.get_anime_details(AniI)
            AniFmal = mal.Anime(AniI)
            AniG = []
            for TAniG in AniF.genres:
                AniG.append(TAniG.name)
            AEm = discord.Embed(title = AniF.title + " / " + AniF.alternative_titles.ja,  description = ", ".join(AniG) + f"\n [Mal Page]({AniFmal.url})", color = 0xa49cff)
            AEm.set_thumbnail(url = AniF.main_picture.large)
            if len(AniF.synopsis) > 1021:
                AniSyn = AniF.synopsis[0:1021]
                AniSyn = AniSyn + "..."
            else:
                AniSyn = AniF.synopsis
            AEm.add_field(name = "Synopsis:", value = AniSyn, inline = False)
            AEm.add_field(name = "Start Airing on:", value = AniF.start_date, inline = True)
            AEm.add_field(name = "Finish Airing on:", value = AniF.end_date, inline = True)
            AEm.add_field(name = "Status:", value = AniFmal.status, inline = True)
            AEm.add_field(name = "Rating:", value = AniFmal.rating, inline = False)
            AEm.add_field(name = "Score:", value = AniF.mean, inline = True)
            AEm.add_field(name = "Rank:", value = AniF.rank, inline = True)
            AEm.add_field(name = "Popularity:", value = AniF.popularity, inline = True)
            AEm.add_field(name = "No# Episodes:", value = AniF.num_episodes, inline = True)
            AEm.add_field(name = "Episode Duration:", value = AniFmal.duration, inline = True)
            AEm.add_field(name = "\u200b", value = "\u200b", inline = False)
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

            if AniSeqF:
                AEm.add_field(name = "Sequel:", value = AniSeqF, inline = False)
            if AniSumF:
                AEm.add_field(name = "Alternate Version:", value = AniAltF, inline = False)
            if AniAdpF:
                AEm.add_field(name = "Adaptation:", value = AniAdpF, inline = False)
            if AniSumF:
                AEm.add_field(name = "Side Story:", value = AniSiStF, inline = False)
            if AniSumF:
                AEm.add_field(name = "Summary:", value = AniSumF, inline = False)
            if AniSumF:
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
        await ctx.message.channel.send("No Arguments")

@DClient.command(name = "twitter")
@commands.check(ChBot)
@commands.cooldown(1, 1, commands.BucketType.user)
async def TestiNNGone(ctx, *args):
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

    TwCS = " ".join(args).split(" ")
    if TwCS[0].lower() == "search" and args:
        TwCS.pop(0)
        if " ".join(TwCS):
            C = 0
            SrchTw = []
            for TwU in Twitter.GetUsersSearch(term = TwCS, count = 10):
                C += 1
                if C == 1:
                    STEm = discord.Embed(title = ":mag: Search for '" + " ".join(TwCS) + "'",  description = "\u200b", color = 0x0384fc)
                VrMa = ""
                if TwU.verified:
                    VrMa = ":ballot_box_with_check: "
                STEm.add_field(name = "\u200b", value = str(C) + ". `" + "@" + TwU.screen_name + " / " + TwU.name + "` " + VrMa, inline = False)
                SrchTw.append(TwU)
            STEm.set_footer(text = "Choose a number to open doujin. 'c' or 'cancel' to exit search. \n\n*The Search closes automatically after 20sec of inactivity.*" )
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
                        await TwSent.edit(embed = discord.Embed(title = ":calling: Finding...",  description = "@" + ProT.screen_name + " / " + ProT.name + "` " + VrMa, color = 0x0384fc)) 
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
        await ctx.message.channel.send("No Arguments")

    try:
        try:
            TwTp = Twitter.GetUser(screen_name = TwS)
            VrMa = ""
            TwDes = "\u200b"
            if TwTp.verified:
                VrMa = ":ballot_box_with_check: "
            if TwTp.description:
                TwDes = TwTp.description
            TEm = discord.Embed(title = "@" + TwTp.screen_name + " / " + TwTp.name + " " + VrMa,  description = TwDes, color = 0x0384fc)
            TEm.set_thumbnail(url = TwTp.profile_image_url_https)
            if TwTp.location:
                TEm.add_field(name = "Location: ", value = TwTp.location, inline = True)
            if TwTp.url:
                TEm.add_field(name = "Website: ", value = (requests.head(TwTp.url)).headers['Location'], inline = True)
            TEm.add_field(name = "Created: ", value = "-".join(TwTp.created_at.split(" ")[1:3]) + "-" + str(TwTp.created_at.split(" ")[-1]), inline = False)
            TEm.add_field(name = "Following: ", value = f"{TwTp.friends_count:,}", inline = True) 
            TEm.add_field(name = "Followers: ", value = f"{TwTp.followers_count:,}", inline = True)
            await ctx.message.channel.send(embed = TEm)
        except twitter.error.TwitterError:
            await ctx.message.channel.send("Not Found")
    except UnboundLocalError:
        pass

@DClient.command(name = "hentai")
@commands.check(ChBot)
@commands.cooldown(1, 1, commands.BucketType.user)
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

    def ChCHan(MSg):
        return MSg.guild.id == ctx.guild.id and MSg.channel.id == ctx.channel.id

    def EmbedMaker(DentAi,Page, State):
        DEmE = discord.Embed(title = DentAi.title(Format.Pretty),  description = FdesCtI, color = 0x000000)
        DEmE.set_thumbnail(url = DentAi.image_urls[0])
        DEmE.set_footer(text = "Released on " + str(DentAi.upload_date) + "\n\n 'n' or 'next' for next page. 'b' or 'back' for previous page. 'go (page n#)' for a specific page. 'c' or 'close' to end reading. \n\n*The Doujin closes automatically after 2mins of inactivity.*")
        DEmE.set_image(url = DentAi.image_urls[Page])
        DEmE.add_field(name = "Doujin ID", value = str(DentAi.id), inline = False)
        DEmE.add_field(name = "\u200b", value = "**Doujin " + State +"** \n\n `Page: " + str(Page+1) + "/" + str(len(DentAi.image_urls)) + "`", inline = False)
        return DEmE

    if args:
        Chlks = " ".join(args).split(" ")
        if Chlks[0].lower() == "search":
            Chlks.pop(0)
            C = 0
            SrchDen = []
            if " ".join(Chlks):
                try:
                    for DeOujin in Utils.search_by_query(query =  " ".join(Chlks) + ' -tag:"lolicon" -tag:"shotacon"', sort = Sort.Popular):
                        C += 1
                        if C == 1:
                            SEm = discord.Embed(title = ":mag: Search for '" + " ".join(Chlks) + "'",  description = "\u200b", color = 0x000000)
                        SEm.add_field(name = "\u200b", value = str(C) + ". `" + DeOujin['title']['english'] + "`", inline = False)
                        SrchDen.append(DeOujin)
                        if C == 10:
                            break
                    SEm.set_footer(text = "Choose a number to open doujin. 'c' or 'cancel' to exit search. \n\n*The Search closes automatically after 20sec of inactivity.*" )
                    DmSent = await ctx.message.channel.send(embed = SEm)
                    try:
                        ResS = await DClient.wait_for('message', check = ChCHanS, timeout = 20)
                        LResS = ResS.content.lower()
                        ReseS = (ResS.content.lower()).split(" ")

                        try:
                            if int(ResS.content) <= 10:
                                Srch = SrchDen[int(ResS.content)-1]['id']
                                DentAi = Hentai(Srch)
                                await DmSent.edit(embed = discord.Embed(title = ":newspaper: Opening...",  description = DentAi.title(Format.Pretty), color = 0x000000)) 
                        except ValueError:
                            if (LResS == "cancel") or (LResS == "c") or (LResS == "zhentai") or (ReseS[0] == "zhentai"):
                                await DmSent.edit(embed = discord.Embed(title = ":newspaper2: Search Cancelled",  description = "\u200b", color = 0x000000))
                    except asyncio.TimeoutError:
                        await DmSent.edit(embed = discord.Embed(title = ":hourglass: Search Timeout...",  description = "\u200b", color = 0x000000))
                except UnboundLocalError:
                    SEm = discord.Embed(title = ":mag: Search for '" + " ".join(Chlks) + "'",  description = "\u200b", color = 0x000000)
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
                        DEm.set_footer(text = "Released on " + str(DentAi.upload_date) + "\n\n'n' or 'next' for next page. 'b' or 'back' for previous page. 'go (page n#)' for a specific page. 'c' or 'close' to end reading. \n\n*The Doujin closes automatically after 2mins of inactivity.*")
                        DEm.set_image(url = DentAi.image_urls[0])
                        DEm.add_field(name = "Doujin ID", value = str(DentAi.id), inline = False)
                        DEm.add_field(name = "\u200b", value = "**Doujin OPEN** \n\n `Page: " + str(Page+1) + "/" + str(len(DentAi.image_urls)) + "`", inline = False)
                        await ctx.message.channel.send("**WARNING:** ALL messages sent after the embed will be deleted until doujin is closed. This is to ensure a proper reading experience.")
                        DmSent = await ctx.message.channel.send(embed = DEm)
                        while True:
                            try:
                                Res = await DClient.wait_for('message', check = ChCHan, timeout = 120)
                                LRes = (Res.content).lower()
                                Rese = (Res.content.lower()).split(" ")
                                if (LRes != "close") and (LRes != "c") and (LRes != "zhentai") and (Rese[0] != "zhentai"):
                                    await Res.delete()
                                if len(Rese) == 1:
                                    if LRes == "n" or LRes == "next":
                                        if Page < len(DentAi.image_urls)-1:
                                            Page += 1
                                            await DmSent.edit(embed = EmbedMaker(DentAi, Page, "OPEN"))
                                        else:
                                            await DmSent.edit(embed = EmbedMaker(DentAi, Page, "CLOSED"))
                                            break
                                    elif LRes == "b" or LRes == "back":
                                        if Page != 0:
                                            Page -= 1
                                            await DmSent.edit(embed = EmbedMaker(DentAi, Page, "OPEN"))
                                        else:
                                            pass
                                    elif LRes == "c" or LRes == "close" or LRes == "zhentai":
                                        await DmSent.edit(embed = EmbedMaker(DentAi, Page, "CLOSED"))
                                        break
                                elif len(Rese) == 2:
                                    if Rese[0] == "go":
                                        try:
                                            pG = int(Rese[1])
                                            if 0 < pG <= len(DentAi.image_urls)-1:
                                                Page = pG-1
                                                await DmSent.edit(embed = EmbedMaker(DentAi, Page, "OPEN"))
                                            elif pG < 1:
                                                Page = 0
                                                await DmSent.edit(embed = EmbedMaker(DentAi, Page, "OPEN"))
                                                pass
                                            else:
                                                Page = len(DentAi.image_urls)-1
                                                await DmSent.edit(embed = EmbedMaker(DentAi, Page, "OPEN"))
                                        except ValueError:
                                            pass
                                    elif Rese[0] == "zhentai":
                                        await DmSent.edit(embed = EmbedMaker(DentAi, Page, "CLOSED"))
                                        break
                            except asyncio.TimeoutError:
                                await DmSent.edit(embed = EmbedMaker(DentAi, Page, "CLOSED"))
                                break
                        await ctx.message.channel.send(":newspaper2: Doujin Closed :newspaper2:")
                    else:
                        await ctx.message.channel.send("This isn't an NSFW channel. No NSFW allowed here. :confused:")
                else:
                    await ctx.message.channel.send("Doujin contains prohibited terms. :zipper_mouth:")
            else:
                await ctx.message.channel.send("That Doujin doesn't exist :expressionless:")
        except UnboundLocalError:
            pass
    else:
        await ctx.message.channel.send("No arguments :no_mouth:")

@DClient.command(name = "reddit")
@commands.check(ChBot)
@commands.cooldown(1, 1, commands.BucketType.user)
async def SrSub(ctx, *args):
    def EmbOri(REm, Type, SubCpoS):
        REm.add_field(name = "\u200b", value = "The original post is a " + Type + " [click here](" + SubCpoS.url + ") to view the original", inline = False)
        REm.set_image(url = SubCpoS.preview['images'][-1]['source']['url'])
        return REm

    if len(args) == 1:
        Tries = 0
        if CheckSub("".join(args)):
            while True:
                if Tries >= 100:
                    break
                try:
                    Post = Reddit.subreddit("".join(args)).hot()
                    ChoicePosts = random.randint(1, 50)
                    for _ in range(0, ChoicePosts):
                        SubCpoS = next(Sub for Sub in Post if not Sub.stickied)
                    break
                except StopIteration:
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
                    REm = discord.Embed(title = FtiTle,  description = "Upvote Ratio: " + str(SubCpoS.upvote_ratio) + " // Post is NSFW", color = 0x8b0000)
                    NSfw = True
                else:
                    REm = discord.Embed(title = FtiTle, description = "Upvote Ratio: " + str(SubCpoS.upvote_ratio) + " // Post is Clean", color = 0x8b0000)
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
                        REm = discord.Embed(title = FtiTle,  description = "Upvote Ratio: " + str(SubCpoS.upvote_ratio) + " // Post is NSFW", color = 0x8b0000)
                    else:
                        REm = discord.Embed(title = "***NOT NSFW CHANNEL***",  description = "Post is NSFW", color = 0x8b0000)
                    NSfw = True
                else:
                    REm = discord.Embed(title = FtiTle, description = "Upvote Ratio: " + str(SubCpoS.upvote_ratio) + " // Post is Clean", color = 0x8b0000)
                C = 0
                if (NSfw and ctx.channel.is_nsfw()) or (NSfw == False):
                    try:
                        GaLpos = SubCpoS.gallery_data['items']
                        for ImgPoGa in GaLpos:
                            FiPoS = SubCpoS.media_metadata[ImgPoGa['media_id']]
                            if FiPoS['e'] == 'Image':
                                REm.add_field(name = "\u200b", value = "The original post is a gallery [click here](" + SubCpoS.url + ") to view the rest of the post", inline = False)
                                pstR = FiPoS['p'][-1]['u']
                                REm.set_image(url = pstR)
                                break
                    except AttributeError:
                        for ExT in [".png",".jpg",".jpeg",".gif",".gifv"]:
                            C += 1
                            if (SubCpoS.url).endswith(ExT):
                                pstR = SubCpoS.url
                                if ExT == ".gifv":
                                    REm.add_field(name = "\u200b", value = "The original post is a video(imgur) [click here](" + SubCpoS.url + ") to view the original", inline = False)
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
            REm.set_footer(text = "From " + "r/" + "".join(args))
            REm.set_author(name = "*By: u/" + str(SubCpoS.author) + "*")
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
        Msg = "'" + (WorA) + "' ADDED :thumbsup:" 
        FuncMon.DbAppendRest(Col, {"IDg":str(ctx.guild.id)}, {"IDd":"GuildInfo","IDg":str(ctx.guild.id)}, WorA, 0, "a")
    else:
        Msg = "'" + (WorA) + "' ALREADY EXIST :confused:"
    await ctx.message.channel.send(Msg)

@DClient.command(aliases = ["rem","remove"])
@commands.check(ChBot)
@commands.check(ChAdmin)
@commands.check(ChSer)
@commands.cooldown(1, 1, commands.BucketType.user)
async def RWord(ctx, *args):
    WorA = " ".join(args)
    if FuncMon.DbRem(Col, {"IDd":"GuildInfo", "IDg":str(ctx.guild.id)}, WorA):
        Msg = "'" + WorA + "' REMOVED :thumbsup:"
        FuncMon.DbAppendRest(Col, {"IDg":str(ctx.guild.id)}, {"IDd":"GuildInfo","IDg":str(ctx.guild.id)}, WorA, 0, "r")
    else:
        Msg = "'" + WorA + "' DOESNT EXIST :confused:"
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
        IEm = discord.Embed(title = ctx.guild.name, description = "Total times word/phrase was repeated", color = 0x3252a8)
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
        IEm = discord.Embed(title = ctx.guild.name, description = "Total times word/phrase was repeated", color = 0x3252a8)
        for j in OSfDb:
            Num += j[Enput]

        IEm.add_field(name = Enput, value = Num, inline = True)
        await ctx.message.channel.send(embed = IEm)
    
    else:
        await ctx.message.channel.send("That word doesnt exist yet :confused:")

@DClient.command(name = "stats")
@commands.check(ChBot)
@commands.check(ChSer)
@commands.cooldown(1, 1, commands.BucketType.user)
async def IMsg(ctx, *args): 
    isBot = False
    if len(ctx.message.mentions) > 0:
        if ctx.message.mentions[0].bot == False and ("<@!"+str(ctx.message.mentions[0].id)+">") == args[0]:
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
            IEm = discord.Embed(title = AUmN.name, description = "All stats", color = 0x3252a8)
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
            IEm = discord.Embed(title = AUmN.name, description = "Word stats", color = 0x3252a8)
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
            if len(ctx.message.mentions) > 0 and ("<@!"+str(ctx.message.mentions[0].id)+">") == ArC[0]:
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
                if requests.head(file).headers.get('content-type').split("/")[0] == "image":
                    C += 1
                    r = requests.get(file, allow_redirects = True)
                    open("resend.jpg", "wb").write(r.content)
                    img = Image.open("resend.jpg")
                    img = await deeppyer.deepfry(img, flares = False)
                    img.save("resend.jpg")
                    files.append(discord.File("resend.jpg"))
                    await ctx.message.channel.send(files = files)
                    files.pop(0)
                    os.remove("resend.jpg")
                else:
                    await ctx.message.channel.send("file(" + str(C) + ") isnt a valid image type :sweat:")
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
    print("Online...")

@DClient.event
async def on_member_join(member):
    Pid = member
    if Pid.bot == False:
        if (Col.count_documents({}) == 0) or (Col.count_documents({"IDd":str(Pid.id),"IDg":str(member.guild.id)}) == 0):
            Col.insert_one({"IDd":str(Pid.id),"IDg":str(member.guild.id)})
            DbB = Col.find({"IDd":"GuildInfo","IDg":str(member.guild.id)})
            for i in DbB:
                Kyes = i.keys()
            for Wp in Kyes:
                FuncMon.DbAdd(Col, {"IDd":str(Pid.id),"IDg":str(member.guild.id)}, Wp, 0)

@DClient.event
async def on_member_remove(member):
    Pid = member
    if Pid.bot == False:
        if (Col.count_documents({"IDd":str(Pid.id),"IDg":str(member.guild.id)}) != 0):
            Col.delete_one({"IDd":str(Pid.id),"IDg":str(member.guild.id)})

@DClient.event
async def on_guild_remove(guild):
    DbB = Col.find({"IDg":str(guild.id)})
    for DbG in DbB:
        Col.delete_one(DbG)

@DClient.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.channel.send("Hold the spam. Wait atleast " + StrCool(round(error.retry_after,2)))
    elif isinstance(error, IsBot):
        await ctx.message.channel.send("Bots can't use commands :pensive:")
    elif isinstance(error, IsAdmin):
        await ctx.message.channel.send("Non-admins are not allowed to use this command :face_with_raised_eyebrow:")
    elif isinstance(error, ProfSer):
        await ctx.message.channel.send(":point_right: Please setup your server first (with 'zsetupserver')! Check all server commands with 'zhelp server' :point_left:")   
    else:
        raise error

DClient.run("NzY4Mzk3NjQwMTQwMDYyNzIx.X4_4EQ.mpWIl074jvRs0X-ceDoKdwv4H_E")