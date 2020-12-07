import discord
import praw
import random
from discord.ext import commands
import pymongo
from pymongo import MongoClient
# import FuncMon
# import os  
import deeppyer
from PIL import Image
# import numpy
# import cv2
import dbl
# import requests
# from prawcore import NotFound, Forbidden
# from hentai import Utils, Sort, Hentai, Format
import asyncio
import giphy_client
import tweepy
# import mal
import malclient
import COVID19Py
import datetime
import time
import randfacts
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

BoDowNFn = False

def removeExtraS(listRm, val):
   return [value for value in listRm if value != val]

def ChAdmin(ctx):
    if ctx.author.guild_permissions.administrator:
        return True
    raise IsAdmin("Normie")

def ChSer(ctx):
    if (Col.count_documents({"IDd":"GuildInfo","IDg":str(ctx.guild.id),"Setup":"Done"}) != 0):
        return True
    raise ProfSer("Unready")

def ChAdMo(ctx):
    if ctx.author.id == 443986051371892746:
        return True
    raise Ignore("Ignore")

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

def GeRoP(user):
    SuPServ = DClient.get_guild(783250489843384341)
    
class IsBot(commands.CheckFailure):
    pass
@DClient.check
async def ChBot(ctx):
    if ctx.author.bot:
        raise IsBot("Bot")
    return True

class ProfSer(commands.CheckFailure):
    pass

class IsAdmin(commands.CheckFailure):
    pass

class IsVote(commands.CheckFailure):
    pass
async def ChVote(ctx):
    if await TClient.get_user_vote(ctx.author.id):
        return True 
    else:
        SuPServ = DClient.get_guild(783250489843384341)
        SuPuS = SuPServ.get_member(ctx.author.id)
        SuRo = []
        SuRo.append(discord.utils.get(SuPServ.roles, id = 783250729686532126))
        SuRo.append(discord.utils.get(SuPServ.roles, id = 783256987655340043))
        SuRo.append(discord.utils.get(SuPServ.roles, id = 784123230372757515))
        SuRo.append(discord.utils.get(SuPServ.roles, id = 784124034559377409))
        for i in SuRo:
            if i in SuPuS.roles:
                return True
        raise IsVote("No Vote")

class IsPatreon(commands.CheckFailure):
    pass
def ChPatreon(ctx):
    SuPServ = DClient.get_guild(783250489843384341)
    SuPuS = SuPServ.get_member(ctx.author.id)
    SuRo = []
    SuRo.append(discord.utils.get(SuPServ.roles, id = 783250729686532126))
    SuRo.append(discord.utils.get(SuPServ.roles, id = 783256987655340043))
    SuRo.append(discord.utils.get(SuPServ.roles, id = 784123230372757515))
    SuRo.append(discord.utils.get(SuPServ.roles, id = 784124034559377409))
    for i in SuRo:
        if i in SuPuS.roles:
            return True
    raise IsPatreon("Not Patreon")

class Ignore(commands.CheckFailure):
    pass
@DClient.check
async def ChAdMonD(ctx):
    if BoDowNFn and ctx.guild.id != 586940644153622550:
        raise Ignore("Ignore")
    return True 

@DClient.command(name = "apod")
@commands.cooldown(1, 1, commands.BucketType.user)
async def GeNAapod(ctx):
    if ChPatreonFu(ctx) or (await TClient.get_user_vote(ctx.author.id)):
        NaSapod = requests.get("https://api.nasa.gov/planetary/apod?api_key=0dsw3SiQmYCeNnwKZROSQIyrcZqjoDzMBo4ggCwS", headers = {"Accept": "application/json"})
        MaNaSapodJ = NaSapod.json()
        if len(MaNaSapodJ["explanation"]) > 1021:
            NapodteXt = MaNaSapodJ["explanation"][0:1021]
            NapodteXt = NapodteXt + "..."
        else:
            NapodteXt = MaNaSapodJ["explanation"]
        DEm = discord.Embed(title = MaNaSapodJ["title"], description = f'Date {MaNaSapodJ["date"]}', color = 0xa9775a)
        DEm.add_field(name = "Explanation:", value = NapodteXt, inline = False)
        DEm.set_image(url = MaNaSapodJ["hdurl"])
        await ctx.message.channel.send(embed = DEm)
    else:
        TemS = await ctx.message.channel.send("This command is reserved for voters or Patreon Supporters. \n:robot: zvote or zpatreon to learn more. :robot:")

@DClient.command(name = "nasa")
@commands.cooldown(1, 1, commands.BucketType.user)
async def BGteNasCur(ctx):
    def MaANasEm(ChImNaCr, IMNuNa, IMgAllT):
        NEm = discord.Embed(title = "Mars", description = "By: Curiosity Rover (NASA)", color = 0xcd5d2e)
        NEm.set_thumbnail(url = "https://i.imgur.com/xmSmG0f.jpeg")
        NEm.add_field(name = "Camera:", value = ChImNaCr[IMNuNa]["camera"]["full_name"], inline = True)
        NEm.add_field(name = "Taken on:", value = ChImNaCr[IMNuNa]["earth_date"], inline = True)
        NEm.add_field(name = f'`Image: {IMNuNa+1}/{IMgAllT}`', value = "\u200b", inline = False)
        NEm.set_image(url = ChImNaCr[IMNuNa]["img_src"])
        return NEm

    def ChCHEm(RcM, RuS):
        return RuS.bot == False and RcM.message == NAimSu and str(RcM.emoji) in ["⬅️","❌","➡️","#️⃣"]

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

    NaSiCr = requests.get("https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key=0dsw3SiQmYCeNnwKZROSQIyrcZqjoDzMBo4ggCwS", headers = {"Accept": "application/json"})
    MaNasCrJ = NaSiCr.json()
    ChImNaCr = random.sample(MaNasCrJ["photos"], k = 25)
    IMgAllT = len(ChImNaCr)
    IMNuNa = 0
    NAimSu = await ctx.message.channel.send(embed = MaANasEm(ChImNaCr, IMNuNa, IMgAllT))
    await NAimSu.add_reaction("⬅️")
    await NAimSu.add_reaction("❌")
    await NAimSu.add_reaction("➡️")
    await NAimSu.add_reaction("#️⃣")
    while True:
        try:
            Res = await DClient.wait_for("reaction_add", check = ChCHEm, timeout = 120) 
            await NAimSu.remove_reaction(Res[0].emoji, Res[1])
            if Res[0].emoji == "⬅️" and IMNuNa != 0:
                IMNuNa -= 1
                await NAimSu.edit(embed = MaANasEm(ChImNaCr, IMNuNa, IMgAllT))
            elif Res[0].emoji == "➡️":
                if IMNuNa < IMgAllT-1:
                    IMNuNa += 1
                    await NAimSu.edit(embed = MaANasEm(ChImNaCr, IMNuNa, IMgAllT))
                else:
                    await NAimSu.edit(embed = MaANasEm(ChImNaCr, IMNuNa, IMgAllT))
                    await NAimSu.remove_reaction("⬅️", DClient.user)
                    await NAimSu.remove_reaction("❌", DClient.user)
                    await NAimSu.remove_reaction("➡️", DClient.user)
                    await NAimSu.remove_reaction("#️⃣", DClient.user)
                    break
            elif Res[0].emoji == "#️⃣":
                if ChPatreonFu(ctx) or (await TClient.get_user_vote(ctx.author.id)):
                    TemTw = await ctx.message.channel.send('Choose a number to open navigate to page. "c" or "cancel" to exit navigation.\n\n*The Navigation closes automatically after 10sec of inactivity.*')
                    try:
                        ResE = await DClient.wait_for("message", check = ChCHEmFN, timeout = 10)
                        await TemTw.delete()
                        await ResE.delete()
                        try:
                            try:
                                pG = int(ResE.content)
                                if 0 < pG <= IMgAllT-1:
                                    IMNuNa = pG-1
                                elif pG < 1:
                                    IMNuNa = 0
                                    pass
                                else:
                                    IMNuNa = IMgAllT-1 
                            except TypeError:
                                pass
                        except ValueError:
                            pass
                        await NAimSu.edit(embed = MaANasEm(ChImNaCr, IMNuNa, IMgAllT))
                    except asyncio.exceptions.TimeoutError:
                        await TemTw.edit("Request Timeout")
                        await asyncio.sleep(5)
                        await TemTw.delete()
                else:
                    TemS = await ctx.message.channel.send("Instant navigation to image is only for voters or Patreon Supporters. \n:robot: zvote or zpatreon to learn more. :robot:")
                    await asyncio.sleep(5)
                    await TemS.delete()
            elif Res[0].emoji == "❌":
                await NAimSu.edit(embed = MaANasEm(ChImNaCr, IMNuNa, IMgAllT))
                await NAimSu.remove_reaction("⬅️", DClient.user)
                await NAimSu.remove_reaction("❌", DClient.user)
                await NAimSu.remove_reaction("➡️", DClient.user)
                await NAimSu.remove_reaction("#️⃣", DClient.user)
                break
        except asyncio.TimeoutError:
            await NAimSu.edit(embed = MaANasEm(ChImNaCr, IMNuNa, IMgAllT))
            await NAimSu.remove_reaction("⬅️", DClient.user)
            await NAimSu.remove_reaction("❌", DClient.user)
            await NAimSu.remove_reaction("➡️", DClient.user)
            await NAimSu.remove_reaction("#️⃣", DClient.user)
            break

@DClient.command(aliases = ["calculate","calc"])
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

@DClient.command(name = "covid")
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

@DClient.command(name = "remind")
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
            if TToTm <= 86400:
                RemTmm = await ctx.message.channel.send(f':timer: Are you sure you want to be reminded in {StrTSTM(TToTm)}? :timer:')
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
                await ctx.message.channel.send("zremind is limited to waiting for 1day max. :cry:")      
        except ValueError:
            await ctx.message.channel.send('Argument was improper. Check "zhelp misc" to check how to use it. :no_mouth:')    
    else:
        await ctx.message.channel.send("No arguments given :no_mouth:")

@DClient.command(name = "pdf")
@commands.cooldown(1, 5, commands.BucketType.user)
async def PdSwtOI(ctx, *args):
    def EmbTI(NfIRa, ImGCns, NpIMg, SImAUp, Extra = "Make sure to close the PDF once you are done .\n\n*PDF closes automatically after 2mins of inactivity.*"):
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
        PcEmE.set_footer(text = "")
        return SEco, ImFA, PcEmE

    def ChCHEm(RcM, RuS):
        return RuS.bot == False and RcM.message == PcEm and str(RcM.emoji) in ["⬅️","❌","➡️","#️⃣"]

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
                    await PcEm.add_reaction("#️⃣")
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
                                    await PcEm.remove_reaction("#️⃣", DClient.user)
                                    os.remove(f'{NfIRa}.jpg')
                                    os.remove(f'{NfIRa}.pdf')
                                    break
                            elif ReaEm[0].emoji == "#️⃣":
                                if ChPatreonFu(ctx) or (await TClient.get_user_vote(ctx.author.id)):
                                    SEco, ImFA, PcEmE = EmbTI(NfIRa, ImGCns, NpIMg, SImAUp,"**CHOOSE A NUMBER** or type anything else to cancel")
                                    await PcEm.edit(embed = PcEmE)
                                    ResE = await DClient.wait_for("message", check = ChCHEmFN, timeout = 10)
                                    await ResE.delete()
                                    try:
                                        try:
                                            pG = int(ResE.content)
                                            if 0 < pG <= len(ImGCns)-1:
                                                NpIMg = pG-1
                                            elif pG < 1:
                                                NpIMg = 0
                                                pass
                                            else:
                                                NpIMg = len(ImGCns)-1 
                                        except TypeError:
                                            pass
                                    except ValueError:
                                        pass
                                    SEco, ImFA, PcEmE = EmbTI(NfIRa, ImGCns, NpIMg, SImAUp)
                                    if SEco:
                                        SImAUp.append(ImFA)
                                    await PcEm.edit(embed = PcEmE)
                                else:
                                    TemS = await ctx.message.channel.send("Instant navigation to page is only for voters or Patreon Supporters. \n:robot: zvote or zpatreon to learn more. :robot:")
                                    await asyncio.sleep(5)
                                    await TemS.delete()
                            elif ReaEm[0].emoji == "❌":
                                await PcEm.remove_reaction("⬅️", DClient.user)
                                await PcEm.remove_reaction("❌", DClient.user)
                                await PcEm.remove_reaction("➡️", DClient.user)
                                await PcEm.remove_reaction("#️⃣", DClient.user)
                                os.remove(f'{NfIRa}.jpg')
                                os.remove(f'{NfIRa}.pdf')
                                break
                        except asyncio.TimeoutError:
                            await PcEm.remove_reaction("⬅️", DClient.user)
                            await PcEm.remove_reaction("❌", DClient.user)
                            await PcEm.remove_reaction("➡️", DClient.user)
                            await PcEm.remove_reaction("#️⃣", DClient.user)
                            os.remove(f'{NfIRa}.jpg')
                            os.remove(f'{NfIRa}.pdf')
                            break
            except requests.exceptions.MissingSchema:
                await ctx.message.channel.send("Not a PDF :woozy_face:")
    else:
        await ctx.message.channel.send("No or too many attachments :woozy_face:")

@DClient.command(name = "fry")
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

@CalCeR.error
async def eCalCeRror(ctx, error):
    if isinstance(error, commands.UnexpectedQuoteError):
        await ctx.message.channel.send("Failed to calculate :confused:")
    raise error

DClient.run("NzY4Mzk3NjQwMTQwMDYyNzIx.X4_4EQ.mpWIl074jvRs0X-ceDoKdwv4H_E")