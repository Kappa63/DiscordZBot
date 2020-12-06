import discord
import praw
import random
from discord.ext import commands
# import pymongo
# from pymongo import MongoClient
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
# import giphy_client
import tweepy
# import mal
# import malclient
import COVID19Py
import datetime
import time
import randfacts
from pdf2image import convert_from_path
import imgurpython

# Mdb = "mongodb+srv://Kappa:85699658@cbotdb.exsit.mongodb.net/CBot?retryWrites=true&w=majority"
# Cls = MongoClient(Mdb)
# DbM = Cls["CBot"]
# Col = DbM["Ser"]
# Colvt = DbM["Vts"]

REqInt = discord.Intents.default()
REqInt.members = True

DClient = commands.Bot(case_insensitive = True, command_prefix = ["z","Z"], help_command = None, intents = REqInt)

TClient = dbl.client.DBLClient(bot = DClient, token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc2ODM5NzY0MDE0MDA2MjcyMSIsImJvdCI6dHJ1ZSwiaWF0IjoxNjA2NjU3OTMwfQ.kdocPKBJMXoyKXnroUrb0KaP0lRFfxDRqLNLe3H_FXA", autopost = True)

Cov = COVID19Py.COVID19(data_source = "jhu")

Imgur = imgurpython.ImgurClient(client_id = "272a225589de547", client_secret = "421db91b32fe790c71a710f8bb48e6035f4fd365")

BoDowNFn = False

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
        raise IsVote("No Vote")

async def ChVoteFu(ctx):
    if await TClient.get_user_vote(ctx.author.id):
        return True 
    else:
        return False

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

def ChPatreonFu(ctx):
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
    return False

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

@DClient.command(name = "twitter")
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
        return RuS.bot == False and RcM.message == TwTsL and str(RcM.emoji) in ["⬅️","❌","➡️","#️⃣"]

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
            
        TEmE.set_footer(text = f'{"-"*10}\n\n"Make sure to close the tweet (with :x:) once you are done.\n\nReact with :hash: then type in a page number to instantly navigate to it (voters only).\n\n*Tweet closes automatically after 20sec of inactivity.*"')
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
            STEm.set_footer(text = 'Choose a number to open Twitter User Profile. "c" or "cancel" to exit search.\n\n*The Search closes automatically after 20sec of inactivity.*')
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
            await TwTsL.add_reaction("#️⃣")
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
                    elif ReaEm[0].emoji == "#️⃣":
                        if ChPatreonFu(ctx) or (await TClient.get_user_vote(ctx.author.id)):
                            TemTw = await ctx.message.channel.send('Choose a number to open navigate to page. "c" or "cancel" to exit navigation.\n\n*The Navigation closes automatically after 10sec of inactivity.*')
                            try:
                                ResE = await DClient.wait_for("message", check = ChCHEmFN, timeout = 10)
                                await ResE.delete()
                                await TemTw.delete()
                                try:
                                    try:
                                        pG = int(ResE.content)
                                        if 0 < pG <= len(TwExt)-1:
                                            TwTNum = pG-1
                                        elif pG < 1:
                                            TwTNum = 0
                                            pass
                                        else:
                                            TwTNum = len(TwExt)-1 
                                    except TypeError:
                                        pass
                                except ValueError:
                                    pass
                                await TwTsL.edit(embed = MakEmTwt(TwTp, VrMa, ChTwTp(TwExt[TwTNum]), TwExt[TwTNum], TwTNum, len(TwExt)))
                            except asyncio.TimeoutError:
                                await TemTw.edit("Request Timeout")
                                await asyncio.sleep(5)
                                await TemTw.delete()
                        else:
                            TemS = await ctx.message.channel.send("Instant navigation to tweet is only for voters or Patreon Supporters. \n:robot: zvote or zpatreon to learn more. :robot:")
                            await asyncio.sleep(5)
                            await TemS.delete()

                    elif ReaEm[0].emoji == "➡️" and len(TwExt) == TwTNum+1:
                        await TwTsL.remove_reaction("⬅️", DClient.user)
                        await TwTsL.remove_reaction("❌", DClient.user)
                        await TwTsL.remove_reaction("➡️", DClient.user)
                        await TwTsL.remove_reaction("#️⃣", DClient.user)
                        break
                    elif ReaEm[0].emoji == "❌":
                        await TwTsL.remove_reaction("⬅️", DClient.user)
                        await TwTsL.remove_reaction("❌", DClient.user)
                        await TwTsL.remove_reaction("➡️", DClient.user)
                        await TwTsL.remove_reaction("#️⃣", DClient.user)
                        break
                except asyncio.TimeoutError:
                    await TwTsL.remove_reaction("⬅️", DClient.user)
                    await TwTsL.remove_reaction("❌", DClient.user)
                    await TwTsL.remove_reaction("➡️", DClient.user)
                    await TwTsL.remove_reaction("#️⃣", DClient.user)
                    break
        except tweepy.error.TweepError:
            await ctx.message.channel.send("Not Found :expressionless:")
    except UnboundLocalError:
        pass

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

@DClient.command(name = "reddit")
@commands.cooldown(1, 3, commands.BucketType.user)
async def SrSub(ctx, *args):
    def EmbOri(REm, Type, SubCpoS):
        REm.add_field(name = "\u200b", value = f'The original post is a {Type} [click here]({SubCpoS.url}) to view the original', inline = False)
        REm.set_image(url = SubCpoS.preview["images"][-1]["source"]["url"])
        return REm

    def GetMaSPos(SubCpoS, ConTtE, Type = "R", CRposNum = 0, CPosTo = 0):
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
                if Type == "S":
                    REm.add_field(name = f'`Page: {CRposNum+1}/{CPosTo}`', value = "\u200b", inline = True)
                NSfw = True
            else:
                REm = discord.Embed(title = FtiTle, description = f'Upvote Ratio: {SubCpoS.upvote_ratio} // Post is Clean', color = 0x8b0000)
                if Type == "S":
                    REm.add_field(name = f'`Page: {CRposNum+1}/{CPosTo}`', value = "\u200b", inline = True)
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
                if Type == "S":
                    REm.add_field(name = f'`Post: {CRposNum+1}/{CPosTo}`', value = "\u200b", inline = True)
            else:
                REm = discord.Embed(title = FtiTle, description = f'Upvote Ratio: {SubCpoS.upvote_ratio} // Post is Clean', color = 0x8b0000)
                if Type == "S":
                    REm.add_field(name = f'`Post: {CRposNum+1}/{CPosTo}`', value = "\u200b", inline = True)
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
        REm.set_footer(text = f'From r/{ConTtE}{"-"*10}\n{"-"*10}\n"Make sure to close the tweet (with :x:) once you are done.\n\nReact with :hash: then type in a page number to instantly navigate to it (voters only).\n\n*Tweet closes automatically after 20sec of inactivity.*')
        REm.set_author(name = f'*By u/{SubCpoS.author}*')
        return REm

    def ChCHEmCH(RcM, RuS):
        return RuS.bot == False and RcM.message == KraPosS and str(RcM.emoji) in ["🔝","📈","🔥","📝","❌"]

    def ChCHEmCHT(RcM, RuS):
        return RuS.bot == False and RcM.message == KraPosS and str(RcM.emoji) in ["🗓️","🌍","📅","❌"]

    def ChCHEm(RcM, RuS):
        return RuS.bot == False and RcM.message == KraPosS and str(RcM.emoji) in ["⬅️","❌","➡️","#️⃣"]

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

    if len(args) == 1:
        if CheckSub("".join(args)): 
            try:                   
                Post = Reddit.subreddit("".join(args)).hot()             
                CPosTo = 0
                for _ in Post:
                    CPosTo += 1
                Post = Reddit.subreddit("".join(args)).hot()
                if CPosTo == 0:
                    await ctx.message.channel.send("No posts on that subreddit :no_mouth:")
                    return
                ChoicePosts = random.randint(1, CPosTo)
                for _ in range(0, ChoicePosts):
                    SubCpoS = next(Sub for Sub in Post if not Sub.stickied)                
            except StopIteration:
                await ctx.message.channel.send("No posts on that subreddit :no_mouth:")
                return
            await ctx.message.channel.send(embed = GetMaSPos(SubCpoS, "".join(args)))
        else:
            await ctx.message.channel.send("Sub doesn't exist or private :expressionless: (Make sure the argument doesnt include the r/)")

    elif len(args) == 2:
        ContT = (" ".join(args)).split(" ")
        if ContT[0].lower() == "surf":
            if ChPatreonFu(ctx) or (await TClient.get_user_vote(ctx.author.id)):
                if CheckSub(ContT[1]): 
                    KraPosS = await ctx.message.channel.send(embed = discord.Embed(title = "How would you like to sort the subreddit?", description = "🔝 to sort by top.\n📈 to sort by rising.\n🔥 to sort by hot.\n📝 to sort by new.\n❌ to cancel", footer = "This timesout in 10s"))
                    await KraPosS.add_reaction("🔝")
                    await KraPosS.add_reaction("📈")
                    await KraPosS.add_reaction("🔥")
                    await KraPosS.add_reaction("📝")
                    await KraPosS.add_reaction("❌")
                    try:
                        ResIni = await DClient.wait_for("reaction_add", check = ChCHEmCH, timeout = 10)
                        if ResIni[0].emoji != "🔝":
                            await KraPosS.edit(embed = discord.Embed(title = "Getting Posts"))
                            await KraPosS.remove_reaction("❌", DClient.user)
                        await KraPosS.remove_reaction(ResIni[0].emoji, ResIni[1])
                        await KraPosS.remove_reaction("🔝", DClient.user)
                        await KraPosS.remove_reaction("📝", DClient.user)
                        await KraPosS.remove_reaction("📈", DClient.user)
                        await KraPosS.remove_reaction("🔥", DClient.user)
                        
                        if ResIni[0].emoji == "❌":
                            await KraPosS.delete()
                            return
                        elif ResIni[0].emoji == "📝":
                            Post = Reddit.subreddit(ContT[1]).new()
                        elif ResIni[0].emoji == "🔥":
                            Post = Reddit.subreddit(ContT[1]).hot()
                        elif ResIni[0].emoji == "📈":
                            Post = Reddit.subreddit(ContT[1]).rising()
                        elif ResIni[0].emoji == "🔝":
                            await KraPosS.edit(embed = discord.Embed(title = "How would you like to sort by top?", description = "🌍 to sort by top all time.\n📅 to sort by top this month.\n🗓️ to sort by top today.\n❌ to cancel", footer = "This timesout in 10s"))
                            await KraPosS.add_reaction("🌍")
                            await KraPosS.add_reaction("📅")
                            await KraPosS.add_reaction("🗓️")
                            ResIniT = await DClient.wait_for("reaction_add", check = ChCHEmCHT, timeout = 10)
                            await KraPosS.remove_reaction(ResIniT[0].emoji, ResIniT[1])
                            await KraPosS.edit(embed = discord.Embed(title = "Getting Posts"))
                            await KraPosS.remove_reaction("❌", DClient.user)
                            await KraPosS.remove_reaction("🌍", DClient.user)
                            await KraPosS.remove_reaction("📅", DClient.user)
                            await KraPosS.remove_reaction("🗓️", DClient.user)
                            if ResIniT[0].emoji == "❌":
                                await KraPosS.delete()
                                return
                            elif ResIniT[0].emoji == "🌍":
                                Post = Reddit.subreddit(ContT[1]).top("all")
                            elif ResIniT[0].emoji == "📅":
                                Post = Reddit.subreddit(ContT[1]).top("month")
                            elif ResIniT[0].emoji == "🗓️":
                                Post = Reddit.subreddit(ContT[1]).top("day")
                    except asyncio.TimeoutError:
                        await KraPosS.edit(embed = discord.Embed(title = "Timeout"))
                        await asyncio.sleep(5)
                        await KraPosS.delete()
                        return
                                    
                    SubCpoS = []
                    CPosTo = 0
                    for SuTPos in Post:
                        CPosTo += 1
                        if not SuTPos.stickied:
                            SubCpoS.append(SuTPos)
                    if CPosTo == 0:
                        await ctx.message.channel.send("No posts on that subreddit :no_mouth:")
                        return              
                    KraPosS = await ctx.message.channel.send(embed = GetMaSPos(SubCpoS[0], ContT[1], "S", 0, CPosTo))
                    CRposNum = 0
                    await KraPosS.add_reaction("⬅️")
                    await KraPosS.add_reaction("❌")
                    await KraPosS.add_reaction("➡️")
                    await KraPosS.add_reaction("#️⃣")
                    while True:
                        try:
                            Res = await DClient.wait_for("reaction_add", check = ChCHEm, timeout = 120) 
                            await KraPosS.remove_reaction(Res[0].emoji, Res[1])
                            if Res[0].emoji == "⬅️" and CRposNum != 0:
                                CRposNum -= 1
                                await KraPosS.edit(embed = GetMaSPos(SubCpoS[CRposNum], ContT[1], "S", CRposNum, CPosTo))
                            elif Res[0].emoji == "➡️":
                                if CRposNum < CPosTo-1:
                                    CRposNum += 1
                                    await KraPosS.edit(embed = GetMaSPos(SubCpoS[CRposNum], ContT[1], "S", CRposNum, CPosTo))
                                else:
                                    await KraPosS.edit(embed = GetMaSPos(SubCpoS[CRposNum], ContT[1], "S", CRposNum, CPosTo))
                                    await KraPosS.remove_reaction("⬅️", DClient.user)
                                    await KraPosS.remove_reaction("❌", DClient.user)
                                    await KraPosS.remove_reaction("➡️", DClient.user)
                                    await KraPosS.remove_reaction("#️⃣", DClient.user)
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
                                                if 0 < pG <= CPosTo-1:
                                                    CRposNum = pG-1
                                                elif pG < 1:
                                                    CRposNum = 0
                                                    pass
                                                else:
                                                    CRposNum = CPosTo-1 
                                            except TypeError:
                                                pass
                                        except ValueError:
                                            pass
                                        await KraPosS.edit(embed = GetMaSPos(SubCpoS[CRposNum], ContT[1], "S", CRposNum, CPosTo))
                                    except asyncio.exceptions.TimeoutError:
                                        await TemTw.edit("Request Timeout")
                                        await asyncio.sleep(5)
                                        await TemTw.delete()
                                else:
                                    TemS = await ctx.message.channel.send("Instant navigation to post is only for voters or Patreon Supporters. \n:robot: zvote or zpatreon to learn more. :robot:")
                                    await asyncio.sleep(5)
                                    await TemS.delete()
                            elif Res[0].emoji == "❌":
                                await KraPosS.edit(embed = GetMaSPos(SubCpoS[CRposNum], ContT[1], "S", CRposNum, CPosTo))
                                await KraPosS.remove_reaction("⬅️", DClient.user)
                                await KraPosS.remove_reaction("❌", DClient.user)
                                await KraPosS.remove_reaction("➡️", DClient.user)
                                await KraPosS.remove_reaction("#️⃣", DClient.user)
                                break
                        except asyncio.TimeoutError:
                            await KraPosS.edit(embed = GetMaSPos(SubCpoS[CRposNum], ContT[1], "S", CRposNum, CPosTo))
                            await KraPosS.remove_reaction("⬅️", DClient.user)
                            await KraPosS.remove_reaction("❌", DClient.user)
                            await KraPosS.remove_reaction("➡️", DClient.user)
                            await KraPosS.remove_reaction("#️⃣", DClient.user)
                            break
                else:
                    await ctx.message.channel.send("Sub doesn't exist or private :expressionless: (Make sure the argument doesnt include the r/)")
            else:
                TemS = await ctx.message.channel.send("This command is reserved for voters or Patreon Supporters. \n:robot: zvote or zpatreon to learn more. :robot:")
                await asyncio.sleep(5)
                await TemS.delete()
        else:
            await ctx.message.channel.send("Too many arguments or not surf command :no_mouth:")
    elif len(args) == 0:
        await ctx.message.channel.send("No arguments :no_mouth:")
    
    else:
        await ctx.message.channel.send("Too many arguments :no_mouth:")

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