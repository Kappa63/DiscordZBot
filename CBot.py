import discord
import praw
import random
from discord.ext import commands
import pymongo
from pymongo import MongoClient
# import FuncMon
# import os  
# import numpy
# import cv2
# from prawcore import NotFound, Forbidden
# from hentai import Utils, Sort, Hentai, Format
# import mal
import deeppyer
from PIL import Image
import dbl
import requests
import asyncio
import giphy_client
import tweepy
import malclient
import COVID19Py
import datetime
from pdf2image import convert_from_path
import imgurpython

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

Cov = COVID19Py.COVID19(data_source = "jhu")

Imgur = imgurpython.ImgurClient(client_id = "272a225589de547", client_secret = "421db91b32fe790c71a710f8bb48e6035f4fd365")

def RemoveExtra(listRm, val):
   return [value for value in listRm if value != val]

def ChAdmin(ctx):
    if ctx.author.guild_permissions.administrator:
        return True
    raise IsAdmin("Normie")

def ChSer(ctx):
    if (Col.count_documents({"IDd":"GuildInfo","IDg":str(ctx.guild.id),"Setup":"Done"}) != 0):
        return True
    raise IsSetup("Unready")

def ChDev(ctx):
    if ctx.author.id == 443986051371892746:
        return True
    raise Ignore("Ignore")

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

class IsAdmin(commands.CheckFailure):
    pass

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
@DClient.check
async def ChModDown(ctx):
    if ("".join(open("OpenState.txt").read().splitlines()) == "Down") and ctx.author.id not in [507212584634548254,443986051371892746,224809178793771009]:
        raise Ignore("Ignore")
    return True 

@DClient.command(aliases = ["calculate","calc"])
@commands.cooldown(1, 1, commands.BucketType.user)
async def Calculate(ctx, *args):
    ToCalc = "".join(args)
    def Calc(Nums):
        ChSafe = True
        for Num in Nums:
            try:
                int(Num)
            except ValueError:
                if Num not in ["(",")","*","/","+","-","**"]:
                    ChSafe = False 
                    break
        if ChSafe:
            return f'Answer is: {round(eval(Nums),4)}'
        else:
            return "Failed to calculate :confused:"
    Calculated = Calc(ToCalc)
    await ctx.message.channel.send(Calculated)

@DClient.command(name = "covid")
@commands.cooldown(1, 3, commands.BucketType.guild)
async def Covid19(ctx, *args):
    if args:
        CovidLocs = Cov.getLocations()
        LocConfirmed = 0
        LocDeaths = 0
        LocRecovered = 0
        LocDiscovered = False
        for Loc in CovidLocs:
            if Loc["country"].lower() == " ".join(args).lower() or Loc["country_code"].lower() == " ".join(args).lower():
                LocDiscovered = True
                LocF = Loc["country"]
                LocPop = Loc["country_population"]
                LocConfirmed += Loc["latest"]["confirmed"]
                LocDeaths += Loc["latest"]["deaths"]
                LocRecovered += Loc["latest"]["recovered"]
        if LocDiscovered:
            CEm = discord.Embed(title = f'{ConT} Covid-19 Status', description = f'This data was requested on {datetime.date.today()}', color = 0xbd9400)
            CEm.add_field(name = "Population: ", value = f'{LocPop:,}', inline = False)
            CEm.add_field(name = "Confirmed: ", value = f'{LocConfirmed:,}', inline = False)
            CEm.add_field(name = "Deaths: ", value = f'{LocDeaths:,}', inline = False)
            CEm.add_field(name = "Recovered: ", value = f'{LocRecovered:,}', inline = False)
            CEm.set_footer(text = "Note: Data may not be completely accurate")
        else:
            await ctx.message.channel.send("Country not found :pensive:")
    else: 
        CovidWorld = Cov.getLatest()
        CEm = discord.Embed(title = "Worldwide Covid-19 Status", description = f'This data was requested on {datetime.date.today()}', color = 0xbd9400)
        CEm.add_field(name = "Confirmed: ", value = f'{CovidWorld["confirmed"]:,}', inline = False)
        CEm.add_field(name = "Deaths: ", value = f'{CovidWorld["deaths"]:,}', inline = False)
        CEm.add_field(name = "Recovered: ", value = f'{CovidWorld["recovered"]:,}', inline = False)
        CEm.set_footer(text = "Note: Data may not be completely accurate")
    await ctx.message.channel.send(embed = CEm)

@DClient.command(name = "remind")
@commands.cooldown(1, 1, commands.BucketType.user)
async def RemindAfter(ctx, *args):
    def TotalWait(Day, Hour, Min, Sec):
        return (Day*86400) + (Hour*3600) + (Min*60) + (Sec)
    def ChCHEm(RcM, RuS):
        return RuS.bot == False and RcM.message == ConfirmAwait and str(RcM.emoji) in ["✅","❌"]
    if args:
        try:
            TimeInputs = (" ".join(args)).split(" ")
            D = 0
            H = 0
            M = 0
            S = 0
            for Times in TimeInputs:
                if Times[-1].lower() == "d":
                    D += int(Times[:-1])
                elif Times[-1].lower() == "h":
                    H += int(Times[:-1])
                elif Times[-1].lower() == "m":
                    M += int(Times[:-1])
                elif Times[-1].lower() == "s":
                    S += int(Times[:-1])
                else:
                    raise ValueError
            AwaitTime = TotalWait(D,H,M,S)
            if AwaitTime <= 86400:
                ConfirmAwait = await ctx.message.channel.send(f':timer: Are you sure you want to be reminded in {FormatTime(AwaitTime)}? :timer:')
                await ConfirmAwait.add_reaction("❌")
                await ConfirmAwait.add_reaction("✅")
                try:
                    ReaEm = await DClient.wait_for("reaction_add", check = ChCHEm, timeout = 10)
                    if ReaEm[0].emoji == "✅":
                        await ConfirmAwait.edit(content = f'You will be pinged in {FormatTime(AwaitTime)} :thumbsup:')
                        await asyncio.sleep(2)
                        await ConfirmAwait.delete()
                        await asyncio.sleep(AwaitTime)
                        await ctx.message.channel.send(f':timer: Its been {FormatTime(AwaitTime)} {ctx.message.author.mention} :timer:') 
                    elif  ReaEm[0].emoji == "❌":
                        await ConfirmAwait.edit(content = "Request Cancelled :thumbsup:")
                        await asyncio.sleep(2)
                        await ConfirmAwait.delete()
                except asyncio.TimeoutError:
                    await ConfirmAwait.edit(content = "Request Timeout :alarm_clock:")
                    await asyncio.sleep(2)
                    await ConfirmAwait.delete()
            else:
                await ctx.message.channel.send("zremind is limited to waiting for 1day max. :cry:")      
        except ValueError:
            await ctx.message.channel.send('Argument was improper. Check "zhelp misc" to check how to use it. :no_mouth:')    
    else:
        await ctx.message.channel.send("No arguments given :no_mouth:")

@DClient.command(name = "pdf")
@commands.cooldown(1, 5, commands.BucketType.user)
async def PDFreader(ctx, *args):
    def EmbTI(PDFname, PDFimages, PDFpage, PDFcache, Extra = "Make sure to close the PDF once you are done .\n\n*PDF closes automatically after 2mins of inactivity.*"):
        try:
            ImgurLink = PDFcache[PDFpage]
            print("Cached...")
            CHcache = False
        except IndexError:
            print("Uploading...")
            PDFimages[PDFpage].save(f'{PDFname}.jpg', "JPEG")
            ImgurLink = Imgur.upload_from_path(f'{PDFname}.jpg')["link"]
            CHcache = True
        PEm = discord.Embed(title = "PDF Viewer")
        PEm.set_image(url = ImgurLink)
        PEm.add_field(name = f'```{PDFpage+1}/{len(PDFimages)}```', value = "\u200b")
        PEm.set_footer(text = "")
        return CHcache, ImgurLink, PEm

    def ChCHEm(RcM, RuS):
        return RuS.bot == False and RcM.message == PTEm and str(RcM.emoji) in ["⬅️","❌","➡️","#️⃣"]

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

    if (len(ctx.message.attachments) == 1 and len(args) == 0) or (len(ctx.message.attachments) == 0 and len(args) == 1):
        PDFattach = []
        URLargs = " ".join(args).split(" ")
        if len(ctx.message.attachments) == 1:
            for AtT in ctx.message.attachments:
                PDFattach.append(AtT.url)
        else:
            try:
                for Lin in URLargs:
                    PDFattach.append(Lin)
            except TypeError:
                pass

        for GetPDF in PDFattach:
            try:
                ChPDF = requests.head(GetPDF).headers.get("content-type").split("/")[1]
                if ChPDF == "pdf":
                    RanLetters = "ioewsahkzcldnpq"
                    PDFname = "".join((random.choice(RanLetters) for i in range(10)))
                    PDFcontent = requests.get(GetPDF, allow_redirects = True)
                    open(f'{PDFname}.pdf', "wb").write(PDFcontent.content)
                    PDFimages = convert_from_path(f'{PDFname}.pdf', 500, last_page = 40) 
                    print(PDFimages)
                    PDFpage = 0   
                    PDFcache = [] 
                    PTEm = await ctx.message.channel.send(embed = discord.Embed(title = "Uploading Page...", description = "After upload a page will no longer be uploaded again (Faster navigation to page)"))
                    CHcache, ImgurLink, PEm = EmbTI(PDFname, PDFimages, PDFpage, PDFcache)
                    if CHcache:
                        PDFcache.append(ImgurLink)
                    await PTEm.edit(embed = PEm)
                    await PTEm.add_reaction("⬅️")
                    await PTEm.add_reaction("❌")
                    await PTEm.add_reaction("➡️")
                    await PTEm.add_reaction("#️⃣")
                    while True:
                        try:
                            ReaEm = await DClient.wait_for("reaction_add", check = ChCHEm, timeout = 120) 
                            await PTEm.remove_reaction(ReaEm[0].emoji, ReaEm[1])
                            if ReaEm[0].emoji == "⬅️" and PDFpage != 0:
                                PDFpage -= 1     
                                CHcache, ImgurLink, PEm = EmbTI(PDFname, PDFimages, PDFpage, PDFcache)
                                if CHcache:
                                    PDFcache.append(ImgurLink)
                                await PTEm.edit(embed = PEm)
                            elif ReaEm[0].emoji == "➡️":
                                if PDFpage < len(PDFimages)-1:
                                    PDFpage += 1
                                    CHcache, ImgurLink, PEm = EmbTI(PDFname, PDFimages, PDFpage, PDFcache)
                                    if CHcache:
                                        PDFcache.append(ImgurLink)
                                    await PTEm.edit(embed = PEm)
                                else:
                                    await PTEm.remove_reaction("⬅️", DClient.user)
                                    await PTEm.remove_reaction("❌", DClient.user)
                                    await PTEm.remove_reaction("➡️", DClient.user)
                                    await PTEm.remove_reaction("#️⃣", DClient.user)
                                    os.remove(f'{PDFname}.jpg')
                                    os.remove(f'{PDFname}.pdf')
                                    break
                            elif ReaEm[0].emoji == "#️⃣":
                                if ChVote(ctx):
                                    CHcache, ImgurLink, PEm = EmbTI(PDFname, PDFimages, PDFpage, PDFcache,"**CHOOSE A NUMBER** or type anything else to cancel")
                                    await PTEm.edit(embed = PEm)
                                    ResE = await DClient.wait_for("message", check = ChCHEmFN, timeout = 10)
                                    await ResE.delete()
                                    try:
                                        try:
                                            pG = int(ResE.content)
                                            if 0 < pG <= len(PDFimages)-1:
                                                PDFpage = pG-1
                                            elif pG < 1:
                                                PDFpage = 0
                                                pass
                                            else:
                                                PDFpage = len(PDFimages)-1 
                                        except TypeError:
                                            pass
                                    except ValueError:
                                        pass
                                    CHcache, ImgurLink, PEm = EmbTI(PDFname, PDFimages, PDFpage, PDFcache)
                                    if CHcache:
                                        PDFcache.append(ImgurLink)
                                    await PTEm.edit(embed = PEm)
                            elif ReaEm[0].emoji == "❌":
                                await PTEm.remove_reaction("⬅️", DClient.user)
                                await PTEm.remove_reaction("❌", DClient.user)
                                await PTEm.remove_reaction("➡️", DClient.user)
                                await PTEm.remove_reaction("#️⃣", DClient.user)
                                os.remove(f'{PDFname}.jpg')
                                os.remove(f'{PDFname}.pdf')
                                break
                        except asyncio.TimeoutError:
                            await PTEm.remove_reaction("⬅️", DClient.user)
                            await PTEm.remove_reaction("❌", DClient.user)
                            await PTEm.remove_reaction("➡️", DClient.user)
                            await PTEm.remove_reaction("#️⃣", DClient.user)
                            os.remove(f'{PDFname}.jpg')
                            os.remove(f'{PDFname}.pdf')
                            break
            except requests.exceptions.MissingSchema:
                await ctx.message.channel.send("Not a PDF :woozy_face:")
    else:
        await ctx.message.channel.send("No or too many attachments :woozy_face:")

@DClient.group(name = "fry", invoke_without_command = True)
@commands.cooldown(1, 1, commands.BucketType.user)
async def ImageFrier(ctx, *args):
    if args:
        URLargs = " ".join(args).split(" ")
        Attached = []
        try:
            for url in URLargs:
                Attached.append(url)
        except TypeError:
            pass
        for AtT in ctx.message.attachments:
            Attached.append(AtT.url)
        Files = []
        C = 0
        for File in Attached:
            try:
                if requests.head(File).headers.get("content-type").split("/")[0] == "image":
                    C += 1
                    GetURLimg = requests.get(File, allow_redirects = True)
                    open("NsRndo.jpg", "wb").write(GetURLimg.content)
                    Img = Image.open("NsRndo.jpg")
                    Img = await deeppyer.deepfry(Img, flares = False)
                    Img.save("NsRndo.jpg")
                    Files.append(discord.File("NsRndo.jpg"))
                    await ctx.message.channel.send(files = Files)
                    Files.pop(0)
                    os.remove("NsRndo.jpg")
                else:
                    await ctx.message.channel.send(f'File({C}) isnt a valid image type :sweat:')
            except requests.exceptions.MissingSchema:
                pass
    else:
        await ctx.message.channel.send("No image(s) or link(s) were attached :woozy_face:")

@ImageFrier.command(name = "profile")
@commands.cooldown(1, 1, commands.BucketType.user)
async def ProfileFrier(ctx):
    if len(ctx.message.mentions) > 0:
        Profile = str((ctx.message.mentions[0]).avatar_url)
    else:
        Profile = str(ctx.author.avatar_url)
    try:
        Files = []
        C = 0
        if requests.head(Profile).headers.get("content-type").split("/")[0] == "image":
            C += 1
            GetURLimg = requests.get(Profile, allow_redirects = True)
            open("NsRndo.jpg", "wb").write(GetURLimg.content)
            Img = Image.open("NsRndo.jpg")
            Img = await deeppyer.deepfry(Img, flares = False)
            Img.save("NsRndo.jpg")
            Files.append(discord.File("NsRndo.jpg"))
            await ctx.message.channel.send(files = Files)
            Files.pop(0)
            os.remove("NsRndo.jpg")
        else:
            await ctx.message.channel.send(f'File({C}) isnt a valid image type :sweat:')
    except requests.exceptions.MissingSchema:
        pass

@Calculate.error
async def CalculateError(ctx, error):
    if isinstance(error, commands.UnexpectedQuoteError):
        await ctx.message.channel.send("Failed to calculate :confused:")
    raise error

DClient.run("NzY4Mzk3NjQwMTQwMDYyNzIx.X4_4EQ.mpWIl074jvRs0X-ceDoKdwv4H_E")