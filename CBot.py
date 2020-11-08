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

Mdb = "mongodb+srv://Kappa:85699658@cbotdb.exsit.mongodb.net/CBot?retryWrites=true&w=majority"
Cls = MongoClient(Mdb)
DbM = Cls["CBot"]
Col = DbM["Ser"]
TraEco = DbM["Ind"]

REqInt = discord.Intents.default()
REqInt.members = True

DClient = commands.Bot(case_insensitive = True, command_prefix = ["z","Z"], help_command = None, intents = REqInt)

Reddit = praw.Reddit(client_id = "ntnBVsoqGHtoNw", client_secret = "ZklNqu4BQK4jWRp9dYXb4ApoQ10", user_agent = "CBot by u/Kamlin333")

Doing = ["Calculations", "Flipping", "Griffin", "Getting Tortured", "Crying", "Still Counting", "Telescopes", "In Pain", "Aerodynamics", "Not A Robot", "Astrology", "Quantum Physics"]

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

class ProfEco(commands.CheckFailure):
    pass
def ChEco(ctx):
    if TraEco.count_documents({"IDd":str(ctx.author.id)}) != 0:
        return True
    raise ProfEco("Unready")

@DClient.command(name = "help")
@commands.check(ChBot)
@commands.cooldown(1, 2, commands.BucketType.user)
async def SendH(ctx, *args):
    if "".join(args) == "" or "".join(args) == " ":
        HEm = discord.Embed(title = "**CBot Help**", description = "\u200b", color = 0x0af531)
        HEm.add_field(name = "zversion: ", value = "Checks the current running version of CBot", inline = False)
        HEm.add_field(name = "zsetupserver: ", value = "Sets up the bot for the first time for counting/tracking", inline = False)
        HEm.add_field(name = "zhelp server: ", value = "Provides all the server commands (including word track commands)", inline = False) 
        HEm.add_field(name = "zhelp misc: ", value = "Miscellaneous commands", inline = False)   
        await ctx.message.channel.send(embed = HEm)
    elif "".join(args).lower()  == "server":
        HEm = discord.Embed(title = "**CBot Server Help**", description = "\u200b", color = 0x0af531)
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
        HEm = discord.Embed(title = "**CBot Misc. Help**", description = "\u200b", color = 0x0af531)
        HEm.add_field(name = "zfry (Image Attachment): ", value = "Deep fries the attached image", inline = False)
        HEm.add_field(name = "zreddit (Subreddit Name): ", value = "Returns a post from the top 50 posts in hot from any subreddit", inline = False)
        HEm.add_field(name = "zhentai (Magic Numbers): ", value = "Gets doujin from nhentai using magic numbers", inline = False)
        HEm.add_field(name = "zhentai random: ", value = "Gets a random doujin from nhentai", inline = False)
        HEm.set_footer(text = "Note: Some hentai are not available. This is to abide by the discord TOS")
        await ctx.message.channel.send(embed = HEm)
    else:
        await ctx.message.channel.send("That help category doesn't exist.")

@DClient.command(aliases = ["ver","version"])
@commands.check(ChBot)
@commands.cooldown(1, 2, commands.BucketType.user)
async def RetVer(ctx):
    VEm = discord.Embed(title = "Active Version", description = "CBot build version and info", color = 0xf59542)
    VEm.add_field(name = "Dev: ", value = "Kappa", inline = True)
    VEm.add_field(name = "Version: ", value = "0.4b", inline = True)
    VEm.add_field(name = "Release: ", value = "Null", inline = True)
    await ctx.message.channel.send(embed = VEm)

@DClient.command(aliases = ["setupserver","setupser"])
@commands.check(ChBot)
@commands.check(ChAdmin)
@commands.cooldown(1, 2, commands.BucketType.user)
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

@DClient.command(name = "hentai")
@commands.check(ChBot)
@commands.cooldown(1, 2, commands.BucketType.user)
async def nHen(ctx, args):  
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

    if args != "" and args != " ":
        try:
            Srch = int(args)
        except ValueError:
            if args.lower() == "random":
                while True:
                    Srch = Utils.get_random_id()
                    DentAi = Hentai(Srch)
                    if ("lolicon" not in [tag.name for tag in DentAi.tag]) and ("shotacon" not in [tag.name for tag in DentAi.tag]):
                        break
            else:
                await ctx.message.channel.send("The argument contained non-numeral characters and wasn't a random request. :no_mouth:")
        if(Hentai.exists(Srch)):
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
    else:
        await ctx.message.channel.send("No arguments :no_mouth:")

@DClient.command(name = "reddit")
@commands.check(ChBot)
@commands.cooldown(1, 2, commands.BucketType.user)
async def SrSub(ctx, *args):
    def EmbOri(REm, Type, SubCpoS):
        REm.add_field(name = "\u200b", value = "The original post is a " + Type + " [click here](" + SubCpoS.url + ") to view the original", inline = False)
        REm.set_image(url = SubCpoS.preview['images'][-1]['source']['url'])
        return REm

    if len(args) == 1:
        Tries = 0
        if CheckSub("".join(args)):
            while True:
                if Tries >= 50:
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
                                    REm.add_field(name = "Media Unavailable. Sorry!!", value = '\u200b')
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
@commands.cooldown(1, 2, commands.BucketType.user)
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
@commands.cooldown(1, 2, commands.BucketType.user)
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
@commands.cooldown(1, 2, commands.BucketType.user)
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
@commands.cooldown(1, 2, commands.BucketType.user)
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
@commands.cooldown(1, 2, commands.BucketType.user)
async def IMsg(ctx, *args): 
    isBot = False
    if len(ctx.message.mentions) > 0:
        if ctx.message.mentions[0].bot == False:
            AUmN = ctx.message.mentions[0]
            aRGu = list(args)
            aRGu.pop(0)
        else:
            isBot = True
    else:
        AUmN = ctx.author
        aRGu = list(args)

    if isBot == False:
        print("kk")
        Num = 0
        Enput = " ".join(aRGu)
        DbB = Col.find({"IDd":"GuildInfo","IDg":str(ctx.guild.id)})
        OSfDb = Col.find({"IDd":str(AUmN.id),"IDg":str(ctx.guild.id)})
        for i in DbB:
            Kyes = i.keys()

        if (Enput == "") or (Enput == " "):
            print("kk")
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
            print("kk")
            IEm = discord.Embed(title = AUmN.name, description = "Word stats", color = 0x3252a8)
            for j in OSfDb:
                Num = j[Enput]
            IEm.add_field(name = Enput, value = Num, inline = True)
            await ctx.message.channel.send(embed = IEm)    
        else:
            await ctx.message.channel.send("That word doesnt exist yet! :confused:")
    elif isBot == True:
        await ctx.message.channel.send("Cannot check a bot's stats :confused:")
    
@DClient.command(name = "fry")
@commands.check(ChBot)
@commands.cooldown(1, 2, commands.BucketType.user)
async def CMsend(ctx):
    if len(ctx.message.attachments) > 0:
        files = []
        C = 0
        for file in ctx.message.attachments:
            C += 1
            for ExT in [".png",".jpg",".jpeg"]:
                if (file.url).endswith(ExT):
                    r = requests.get(file.url, allow_redirects = True)
                    open("resend.jpg", "wb").write(r.content)
                    img = Image.open("resend.jpg")
                    img = await deeppyer.deepfry(img, flares = False)
                    img.save("resend.jpg")
                    files.append(discord.File("resend.jpg", filename = file.filename, spoiler = file.is_spoiler()))
                    await ctx.message.channel.send(files = files)
                    files.pop(0)
                    os.remove("resend.jpg")
                    break
            else:
                await ctx.message.channel.send("file(" + str(C) + ") isnt a valid image type :sweat:")
    else:
        await ctx.message.channel.send("No image(s) were attached :woozy_face:")

@DClient.event
async def on_message(message):
    CmSLim = 0
    if Col.count_documents({"IDd":"GuildInfo","IDg":str(message.guild.id),"Setup":"Done"}) != 0:
        Remove = '*_'
        PhMsRase = ((message.content.lower()).strip(Remove)).split(" ")
        R = len(PhMsRase)
        PhMsRase = removeExtraS(PhMsRase, "")
        if message.author.bot == False:
            for _ in range(R):
                if CmSLim >= 10:
                    break
                Temp = []
                for MMmsg in PhMsRase:
                    Temp.append(MMmsg)
                    CTemp = " ".join(Temp)
                    if len(Temp) > 0:
                        if FuncMon.AddTo(Col, {"IDd":str(message.author.id),"IDg":str(message.guild.id)}, CTemp, 1):
                            CmSLim += 1
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
    elif isinstance(error, ProfEco):
        await ctx.message.channel.send(":point_right: Please setup your economy profile first (with 'zsetupeco')! Check all economy commands with 'zhelp eco' :point_left:")
    raise error

DClient.run("NzY4Mzk3NjQwMTQwMDYyNzIx.X4_4EQ.mpWIl074jvRs0X-ceDoKdwv4H_E")