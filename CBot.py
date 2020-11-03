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

@DClient.command(name = "help")
async def SendH(ctx, *args):
    if "".join(args) == "" or "".join(args) == " ":
        HEm = discord.Embed(title = "CBot Help", description = "Commands", color = 0x0af531)
        HEm.add_field(name = "zversion: ", value = "Checks the current running version of CBot", inline = False)
        HEm.add_field(name = "zsetup (server/economy): ", value = "Setsup the bot for the first time (for counting/economy repectively)", inline = False)
        HEm.add_field(name = "zhelp economy: ", value = "Setsup the bot for the first time (for counting/economy repectively)", inline = False)
        HEm.add_field(name = "zhelp server: ", value = "Provides all the server commands (including word track commands)", inline = False) 
        HEm.add_field(name = "zhelp misc: ", value = "Miscellaneous commands", inline = False)   
        await ctx.message.channel.send(embed = HEm)
    elif "".join(args).lower()  == "eco" or "".join(args).lower()  == "economy":
        HEm = discord.Embed(title = "CBot Economy Help", description = "Commands", color = 0x0af531)
        HEm.add_field(name = "zprofile: ", value = "Shows your economy profile", inline = False)
        HEm.add_field(name = "zdig: ", value = "Dig for treasure. Who knows? You might find some gold (or bones)", inline = False)
        await ctx.message.channel.send(embed = HEm)
    elif "".join(args).lower()  == "server":
        HEm = discord.Embed(title = "CBot Server Help", description = "Commands", color = 0x0af531)
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
        HEm = discord.Embed(title = "CBot Misc. Help", description = "Commands", color = 0x0af531)
        HEm.add_field(name = "zfry (Image Attachment): ", value = "Deep fries the attached image", inline = False)
        HEm.add_field(name = "zreddit (Subreddit Name): ", value = "Returns a post from the top 50 posts in hot from any subreddit", inline = False)
        await ctx.message.channel.send(embed = HEm)
    else:
        await ctx.message.channel.send("That help category doesn't exist.")

@DClient.command(name = "version")
async def RetVer(ctx):
    VEm = discord.Embed(title = "Active Version", description = "CBot build version and info", color = 0xf59542)
    VEm.add_field(name = "Dev: ", value = "Kappa", inline = True)
    VEm.add_field(name = "Version: ", value = "1.7.2", inline = True)
    VEm.add_field(name = "Release: ", value = "10/20/20", inline = True)
    await ctx.message.channel.send(embed = VEm)

@DClient.command(name = "setup")
async def SMsg(ctx, *args):
    if ("".join(args)).lower() == "server":
        if (Col.count_documents({"IDd":"GuildInfo","IDg":str(ctx.guild.id),"Setup":"Done"}) == 0) or Col.count_documents({}) == 0:
            if ctx.author.guild_permissions.administrator:
                DbB = Col.find({"IDd":"GuildInfo","IDg":str(ctx.guild.id)})
                for i in DbB:
                    Kyes = i.keys()

                if (Col.count_documents({"IDd":"GuildInfo","IDg":str(ctx.guild.id),"Setup":"Done"}) == 0):
                    info = {"IDd":"GuildInfo","IDg":str(ctx.guild.id),"Setup":"Done"}
                    Col.insert_one(info)

                for Pid in ctx.guild.members:
                    if Pid.bot == False:
                        if (Col.count_documents({}) == 0) or (Col.count_documents({"IDd":str(Pid.id),"IDg":str(ctx.guild.id)}) == 0):
                            info = {"IDd":str(Pid.id),"IDg":str(ctx.guild.id)}
                            Col.insert_one(info)
                            DbB = Col.find({"IDd":"GuildInfo","IDg":str(ctx.guild.id)})
                            for i in DbB:
                                Kyes = i.keys()
                            
                            for Wp in Kyes:
                                if Wp == "_id" or Wp == "IDd" or Wp == "IDg" or Wp == "Setup":
                                    pass
                                else:
                                    Col.update_one({"IDd":str(Pid.id),"IDg":str(ctx.guild.id)},{"$set":{Wp:0}})
                await ctx.message.channel.send(":partying_face: Setup complete, you can now use tracking commands:partying_face:")
            else:
                await ctx.message.channel.send("Non-admins are not allowed to setup :face_with_raised_eyebrow:")
        else:
            await ctx.message.channel.send(":partying_face: This server is already setup :partying_face:")
    
    elif ("".join(args)).lower() == "economy":
        if (TraEco.count_documents({"IDd":str(ctx.author.id)}) == 0) or TraEco.count_documents({}) == 0:
            DbB = TraEco.find({"IDd":"Setup"})
            for i in DbB:
                Kyes = i.keys()

            if ctx.author.bot == False:
                if (TraEco.count_documents({}) == 0) or (TraEco.count_documents({"IDd":str(ctx.author.id)}) == 0):
                    info = {"IDd":str(ctx.author.id)}
                    TraEco.insert_one(info)
                    for Wp in Kyes:
                        if Wp == "_id" or Wp == "IDd" or Wp == "Setup":
                            pass
                        elif Wp == "ReqXp":
                            TraEco.update_one({"IDd":str(ctx.author.id)},{"$set":{Wp:500}})
                        else:
                            TraEco.update_one({"IDd":str(ctx.author.id)},{"$set":{Wp:0}})
                await ctx.message.channel.send(":partying_face: Setup complete, you can now use economy commands :partying_face:")
            else:
                await ctx.message.channel.send("Silly Bot. You can't setup a profile :pensive:")
        else:
            await ctx.message.channel.send(":partying_face: You are already setup :partying_face:")
    else:
        await ctx.message.channel.send("Missing argument. Check zhelp for proper way to use it :confused:")

@DClient.command(aliases = ["p","profile"])
async def PecoS(ctx, *args):
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

    if not isBot:
        if TraEco.count_documents({"IDd":str(AUmN.id)}) != 0:
            OSfDb = TraEco.find({"IDd":str(AUmN.id)})
            for i in OSfDb:
                Kyes = i.keys()
            PeEm = discord.Embed(title = AUmN.display_name, description = "Newbie", color = 0x42e0f5) 
            PeEm.set_thumbnail(url = AUmN.avatar_url)
            PeEm.add_field(name = "\u200b", value = "\u200b", inline = False)
            Num = ""
            for Wp in Kyes:
                OSfDb = TraEco.find({"IDd":str(AUmN.id)})
                if Wp == "_id" or Wp == "IDd" or Wp == "IDg" or Wp == "Setup":
                    pass
                elif Wp == "ReqXp":
                    for j in OSfDb:
                        Num += "**Xp for level up:** " + str(j[Wp]-j["XP"]) + "\n"  
                else:
                    for j in OSfDb:
                        Num += "**" + Wp + ":** " + str(j[Wp]) + "\n"     
            PeEm.add_field(name = "GENERAL: ", value = Num, inline = False)
            await ctx.message.channel.send(embed = PeEm)
        else:
            await ctx.message.channel.send(":point_right: That profile doesnt exist yet. Please setup your economy profile first (with 'zsetup eco')! Check all economy commands with 'zhelp eco' :point_left:")
    else:
        await ctx.message.channel.send("Cannot check a bot's profile :confused:")

@DClient.command(name = "dig")
async def DEco(ctx):
    if ctx.author.bot == False:
        if TraEco.count_documents({"IDd":str(ctx.author.id)}) != 0:
            PosDigs = ["Bones","Pure Gold","Dirt","Copper","Landmine","Plumbing"]
            Ch = {"IDd":str(ctx.author.id)}
            CDug = random.choice(PosDigs)
            FuncMon.DbAdd(Ch,CDug)   
            Numo = ItemFind.Item(CDug)
            FuncMon.AddTo(Ch, CDug, Numo)
            await ctx.message.channel.send("You found " + str(Numo) + " " + CDug +"!!")
        else:
            await ctx.message.channel.send(":point_right: Please setup your economy profile first (with 'zsetup eco')! Check all economy commands with 'zhelp eco' :point_left:")
    else:   
       await ctx.message.channel.send("Silly Bot. You can't use commands :pensive:")
    
@DClient.command(name = "hentai")
async def nHen(ctx, args):
    try:
        if(Hentai.exists(int(args))):
            DentAi = Hentai(int(args))
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
                DEm.set_footer(text = "Released on " + str(DentAi.upload_date) + "\n\n 'n' or 'next' for next page. 'b' or 'back' for previous page. 'c' or 'close' to end reading")
                DEm.set_image(url = DentAi.image_urls[0])
                DEm.add_field(name = "\u200b", value = "`Page: " + str(Page+1) + "`", inline = False)
                await ctx.message.channel.send("**WARNING:** ALL messages sent after the embed will be deleted until doujin is closed. This is to ensure a proper reading experience.")
                DmSent = await ctx.message.channel.send(embed = DEm)
                while True:
                    Res = await DClient.wait_for('message')
                    Rese = Res.content.split(" ")
                    if len(Rese) == 1:
                        if (Res.content).lower() == "n" or (Res.content).lower() == "next":
                            await Res.delete()
                            if Page < len(DentAi.image_urls)-1:
                                Page += 1
                                DEmE = discord.Embed(title = DentAi.title(Format.Pretty),  description = FdesCtI, color = 0x000000)
                                DEmE.set_thumbnail(url = DentAi.image_urls[0])
                                DEmE.set_footer(text = "Released on " + str(DentAi.upload_date) + "\n\n 'n' or 'next' for next page. 'b' or 'back' for previous page. 'c' or 'close' to end reading")
                                DEmE.set_image(url = DentAi.image_urls[Page])
                                DEmE.add_field(name = "\u200b", value = "`Page: " + str(Page+1) + "`", inline = False)
                                await DmSent.edit(embed = DEmE)
                            else:
                                break
                        elif (Res.content).lower() == "b" or (Res.content).lower() == "back":
                            await Res.delete()
                            if Page != 0:
                                Page -= 1
                                DEmE = discord.Embed(title = DentAi.title(Format.Pretty),  description = FdesCtI, color = 0x000000)
                                DEmE.set_thumbnail(url = DentAi.image_urls[0])
                                DEmE.set_footer(text = "Released on " + str(DentAi.upload_date) + "\n\n 'n' or 'next' for next page. 'b' or 'back' for previous page. 'c' or 'close' to end reading")
                                DEmE.set_image(url = DentAi.image_urls[Page])
                                DEmE.add_field(name = "\u200b", value = "`Page: " + str(Page+1) + "`", inline = False)
                                await DmSent.edit(embed = DEmE)
                            else:
                                pass
                        elif (Res.content).lower() == "c" or (Res.content).lower() == "close":
                            break
                        else:
                            await Res.delete()
                    elif len(Rese) == 2:
                        if Rese[0] == "go":
                            await Res.delete()
                            try:
                                pG = int(Rese[1])
                                Page = pG
                                DEmE = discord.Embed(title = DentAi.title(Format.Pretty),  description = FdesCtI, color = 0x000000)
                                DEmE.set_thumbnail(url = DentAi.image_urls[0])
                                DEmE.set_footer(text = "Released on " + str(DentAi.upload_date) + "\n\n 'n' or 'next' for next page. ''")
                                DEmE.set_image(url = DentAi.image_urls[Page])
                                DEmE.add_field(name = "\u200b", value = "Page: " + str(Page), inline = False)
                                await DmSent.edit(embed = DEmE)
                            except ValueError:
                                pass
                        else:
                            await Res.delete()
                    else:
                        await Res.delete()
                await ctx.message.channel.send(":newspaper2: Doujin Closed :newspaper2:")
            else:
                await ctx.message.channel.send("This isn't an NSFW channel. No NSFW allowed here. :confused:")
        else:
            await ctx.message.channel.send("That Doujin doesn't exist :expressionless:")
    except ValueError:
        await ctx.message.channel.send("The argument contained non-numeral characters. :no_mouth:")

@DClient.command(name = "reddit")
async def SrSub(ctx, *args):
    if len(args) == 1:
        if CheckSub("".join(args)):
            try:
                Post = Reddit.subreddit("".join(args)).hot()
                ChoicePosts = random.randint(1, 50)
                for _ in range(0, ChoicePosts):
                    SubCpoS = next(Sub for Sub in Post if not Sub.stickied)

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
                    REm.set_footer(text = "From " + "r/" + "".join(args))
                    REm.set_author(name = "By: u/" + str(SubCpoS.author))
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
                        for ExT in [".png",".jpg",".jpeg"]:
                            C += 1
                            if (SubCpoS.url).endswith(ExT):
                                REm.set_image(url = SubCpoS.url)
                                break
                            elif C == 3:
                                REm.add_field(name = "Couldnt get media. Probably a video, gallery, or external webpage. Sorry!!", value = '\u200b')
                                REm.add_field(name = "Post: ", value = SubCpoS.url, inline = False)
                    else:
                        REm.add_field(name = "NSFW: ", value = "This isn't an NSFW channel. No NSFW allowed here.", inline = False)
                    REm.set_footer(text = "From " + "r/" + "".join(args))
                    REm.set_author(name = "By: u/" + str(SubCpoS.author))
                await ctx.message.channel.send(embed = REm)
            except StopIteration:
                await ctx.message.channel.send("Sub has less than 50 posts :no_mouth:")
        else:
            await ctx.message.channel.send("Sub doesn't exist or private :expressionless: (Make sure the argument doesnt include the r/)")
    elif len(args) == 0:
        await ctx.message.channel.send("No arguments :no_mouth:")
    
    else:
        await ctx.message.channel.send("Too many arguments :no_mouth:")

@DClient.command(name = "add")
async def AWord(ctx, *args): 
    if ctx.author.bot == False:
        if ctx.author.guild_permissions.administrator:
            if Col.count_documents({"IDd":"GuildInfo","IDg":str(ctx.guild.id),"Setup":"Done"}) != 0:
                DbB = Col.find({"IDd":"GuildInfo","IDg":str(ctx.guild.id)})
                for i in DbB:
                    KMeys = i.keys()
                if " ".join(args) not in KMeys:
                    Col.update_one({"IDd":"GuildInfo","IDg":str(ctx.guild.id)},{"$set":{" ".join(args):0}})
                    Msg = "'" + (" ".join(args)) + "' ADDED :thumbsup:" 
                    DbA = Col.find({"IDg":str(ctx.guild.id)})
                    for j in DbA:
                        if j == i:
                            pass
                        else:
                            Col.update_one(j,{"$set":{" ".join(args):0}})
                else:
                    Msg = "'" + (" ".join(args)) + "' ALREADY EXIST :confused:"
                await ctx.message.channel.send(Msg)
            else:
                await ctx.message.channel.send(":point_right: Please setup your server first (with 'zsetup server')! Check all server commands with 'zhelpserver' :point_left:")
        else:
            await ctx.message.channel.send("Non-admins are not allowed to add words :face_with_raised_eyebrow:")
    else:
       await ctx.message.channel.send("Silly Bot. You can't use commands :pensive:")

@DClient.command(aliases = ["rem","remove"])
async def RWord(ctx, *args):
    if ctx.authot.bot == False:
        if ctx.author.guild_permissions.administrator:
            if Col.count_documents({"IDd":"GuildInfo","IDg":str(ctx.guild.id),"Setup":"Done"}) != 0:
                DbB = Col.find({"IDd":"GuildInfo","IDg":str(ctx.guild.id)})
                
                for i in DbB:
                    Kyes = i.keys()

                if " ".join(args) in Kyes:
                    Col.update_one({"IDd":"GuildInfo","IDg":str(ctx.guild.id)},{"$unset":{" ".join(args): ""}})
                    Msg = "'" + (" ".join(args)) + "' REMOVED :thumbsup:"
                else:
                    Msg = "'" + (" ".join(args)) + "' DOESNT EXISTS :confused:"

                DbA = Col.find({"IDg":str(ctx.guild.id)})
                for j in DbA:
                    if j == i:
                        pass
                    else:
                        Col.update_one(j,{"$unset":{" ".join(args): ""}})

                await ctx.message.channel.send(Msg)  
            else:
                    await ctx.message.channel.send(":point_right: Please setup your server first (with 'zsetup server')! Check all server commands with 'zhelpserver' :point_left:")
        else:
            await ctx.message.channel.send("Non-admins are not allowed to remove words :face_with_raised_eyebrow:")
    else:
       await ctx.message.channel.send("Silly Bot. You can't use commands :pensive:")

@DClient.command(name = "list")
async def LWord(ctx):
    if ctx.authot.bot == False:
        if Col.count_documents({"IDd":"GuildInfo","IDg":str(ctx.guild.id),"Setup":"Done"}) != 0:
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
        else:
            await ctx.message.channel.send(":point_right: Please setup your server first (with 'zsetup server')! Check all server commands with 'zhelpserver' :point_left:")    
    else:
       await ctx.message.channel.send("Silly Bot. You can't use commands :pensive:")

@DClient.command(name = "total")
async def TMsg(ctx, *args):
    if Col.count_documents({"IDd":"GuildInfo","IDg":str(ctx.guild.id),"Setup":"Done"}) != 0 and ctx.author.bot == False:
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
    elif Col.count_documents({"IDd":"GuildInfo","IDg":str(ctx.guild.id),"Setup":"Done"}) == 0 and ctx.author.bot == False:
            await ctx.message.channel.send(":point_right: Please setup your server first (with 'zsetup server')! Check all server commands with 'zhelpserver' :point_left:")
    else:
        await ctx.message.channel.send("Silly Bot. You can't use commands :pensive:")

@DClient.command(name = "stats")
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

    if Col.count_documents({"IDd":"GuildInfo","IDg":str(ctx.guild.id),"Setup":"Done"}) != 0 and (isBot == False):
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

    elif Col.count_documents({"IDd":"GuildInfo","IDg":str(ctx.guild.id),"Setup":"Done"}) != 0 and (isBot == True):
        await ctx.message.channel.send("Cannot check a bot's stats :confused:")

    else:
        await ctx.message.channel.send(":point_right: Please setup your server first (with 'zsetup server')! Check all server commands with 'zhelpserver' :point_left:")
    
@DClient.command(name = "fry")
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
        DbB = Col.find({"IDd":str(message.author.id),"IDg":str(message.guild.id)})
        for i in DbB:
            Kyes = i.keys()
        PhMsRase = ((message.content.lower()).strip(Remove)).split(" ")
        R = len(PhMsRase)
        PhMsRase = removeExtraS(PhMsRase, "")
        if message.author.bot == False:
            for i in range(R):
                if CmSLim >= 10:
                    break
                DbB = Col.find({"IDd":str(message.author.id),"IDg":str(message.guild.id)})
                for i in DbB:
                    Kyes = i.keys()
                Temp = []
                for MMmsg in PhMsRase:
                    Temp.append(MMmsg)
                    CTemp = " ".join(Temp)
                    if len(Temp) > 0:
                        if (CTemp in Kyes) and (CTemp != "IDd") and (CTemp != "IDg") and (CTemp != "Setup") and (CTemp != "_id"):      
                            Col.update_one(i,{"$set":{CTemp:i[CTemp]+1}}) 
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
            info = {"IDd":str(Pid.id),"IDg":str(member.guild.id)}
            Col.insert_one(info)
            DbB = Col.find({"IDd":"GuildInfo","IDg":str(member.guild.id)})
            for i in DbB:
                Kyes = i.keys()
            
            for Wp in Kyes:
                if Wp == "_id" or Wp == "IDd" or Wp == "IDg" or Wp == "Setup":
                    pass
                else:
                    Col.update_one({"IDd":str(Pid.id),"IDg":str(member.guild.id)},{"$set":{Wp:0}})

@DClient.event
async def on_member_remove(member):
    Pid = member
    if Pid.bot == False:
        if (Col.count_documents({"IDd":str(Pid.id),"IDg":str(member.guild.id)}) != 0):
            info = {"IDd":str(Pid.id),"IDg":str(member.guild.id)}
            Col.delete_one(info)

@DClient.event
async def on_guild_remove(guild):
    DbB = Col.find({"IDg":str(guild.id)})
    for DbG in DbB:
        Col.delete_one(DbG)

DClient.run("NzY4Mzk3NjQwMTQwMDYyNzIx.X4_4EQ.mpWIl074jvRs0X-ceDoKdwv4H_E")