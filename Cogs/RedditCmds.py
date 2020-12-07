import discord
from discord.ext import commands
from prawcore import NotFound, Forbidden
import requests
import os 
from CBot import Reddit
import asyncio

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

def EmbOri(REm, Type, SubCpoS):
    REm.add_field(name = "\u200b", value = f'The original post is a {Type} [click here]({SubCpoS.url}) to view the original', inline = False)
    REm.set_image(url = SubCpoS.preview["images"][-1]["source"]["url"])
    return REm

class RedditCmds(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient
    
    @commands.group(name = "reddit", invoke_without_command = True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def SrSub(self, ctx, *args):
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
        if args:
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
        else:
            await ctx.message.channel.send("No arguments :no_mouth:")

    @SrSub.command(name = "surf")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def SrSub(self, ctx, *args):
        if args:
            if ChPatreonFu(ctx) or (await TClient.get_user_vote(ctx.author.id)):
                if CheckSub("".join(args)): 
                    KraPosS = await ctx.message.channel.send(embed = discord.Embed(title = "How would you like to sort the subreddit?", description = "🔝 to sort by top.\n📈 to sort by rising.\n🔥 to sort by hot.\n📝 to sort by new.\n❌ to cancel", footer = "This timesout in 10s"))
                    await KraPosS.add_reaction("🔝")
                    await KraPosS.add_reaction("📈")
                    await KraPosS.add_reaction("🔥")
                    await KraPosS.add_reaction("📝")
                    await KraPosS.add_reaction("❌")
                    try:
                        ResIni = await self.DClient.wait_for("reaction_add", check = ChCHEmCH, timeout = 10)
                        if ResIni[0].emoji != "🔝":
                            await KraPosS.edit(embed = discord.Embed(title = "Getting Posts"))
                            await KraPosS.remove_reaction("❌", self.DClient.user)
                        await KraPosS.remove_reaction(ResIni[0].emoji, ResIni[1])
                        await KraPosS.remove_reaction("🔝", self.DClient.user)
                        await KraPosS.remove_reaction("📝", self.DClient.user)
                        await KraPosS.remove_reaction("📈", self.DClient.user)
                        await KraPosS.remove_reaction("🔥", self.DClient.user)
                        
                        if ResIni[0].emoji == "❌":
                            await KraPosS.delete()
                            return
                        elif ResIni[0].emoji == "📝":
                            Post = Reddit.subreddit("".join(args)).new()
                        elif ResIni[0].emoji == "🔥":
                            Post = Reddit.subreddit("".join(args)).hot()
                        elif ResIni[0].emoji == "📈":
                            Post = Reddit.subreddit("".join(args)).rising()
                        elif ResIni[0].emoji == "🔝":
                            await KraPosS.edit(embed = discord.Embed(title = "How would you like to sort by top?", description = "🌍 to sort by top all time.\n📅 to sort by top this month.\n🗓️ to sort by top today.\n❌ to cancel", footer = "This timesout in 10s"))
                            await KraPosS.add_reaction("🌍")
                            await KraPosS.add_reaction("📅")
                            await KraPosS.add_reaction("🗓️")
                            ResIniT = await self.DClient.wait_for("reaction_add", check = ChCHEmCHT, timeout = 10)
                            await KraPosS.remove_reaction(ResIniT[0].emoji, ResIniT[1])
                            await KraPosS.edit(embed = discord.Embed(title = "Getting Posts"))
                            await KraPosS.remove_reaction("❌", self.DClient.user)
                            await KraPosS.remove_reaction("🌍", self.DClient.user)
                            await KraPosS.remove_reaction("📅", self.DClient.user)
                            await KraPosS.remove_reaction("🗓️", self.DClient.user)
                            if ResIniT[0].emoji == "❌":
                                await KraPosS.delete()
                                return
                            elif ResIniT[0].emoji == "🌍":
                                Post = Reddit.subreddit("".join(args)).top("all")
                            elif ResIniT[0].emoji == "📅":
                                Post = Reddit.subreddit("".join(args)).top("month")
                            elif ResIniT[0].emoji == "🗓️":
                                Post = Reddit.subreddit("".join(args)).top("day")
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
                            Res = await self.DClient.wait_for("reaction_add", check = ChCHEm, timeout = 120) 
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
                                    await KraPosS.remove_reaction("⬅️", self.DClient.user)
                                    await KraPosS.remove_reaction("❌", self.DClient.user)
                                    await KraPosS.remove_reaction("➡️", self.DClient.user)
                                    await KraPosS.remove_reaction("#️⃣", self.DClient.user)
                                    break
                            elif Res[0].emoji == "#️⃣":
                                if ChPatreonFu(ctx) or (await TClient.get_user_vote(ctx.author.id)):
                                    TemTw = await ctx.message.channel.send('Choose a number to open navigate to page. "c" or "cancel" to exit navigation.\n\n*The Navigation closes automatically after 10sec of inactivity.*')
                                    try:
                                        ResE = await self.DClient.wait_for("message", check = ChCHEmFN, timeout = 10)
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
                                await KraPosS.remove_reaction("⬅️", self.DClient.user)
                                await KraPosS.remove_reaction("❌", self.DClient.user)
                                await KraPosS.remove_reaction("➡️", self.DClient.user)
                                await KraPosS.remove_reaction("#️⃣", self.DClient.user)
                                break
                        except asyncio.TimeoutError:
                            await KraPosS.edit(embed = GetMaSPos(SubCpoS[CRposNum], ContT[1], "S", CRposNum, CPosTo))
                            await KraPosS.remove_reaction("⬅️", self.DClient.user)
                            await KraPosS.remove_reaction("❌", self.DClient.user)
                            await KraPosS.remove_reaction("➡️", self.DClient.user)
                            await KraPosS.remove_reaction("#️⃣", self.DClient.user)
                            break
                else:
                    await ctx.message.channel.send("Sub doesn't exist or private :expressionless: (Make sure the argument doesnt include the r/)")
            else:
                TemS = await ctx.message.channel.send("This command is reserved for voters or Patreon Supporters. \n:robot: zvote or zpatreon to learn more. :robot:")
                await asyncio.sleep(5)
                await TemS.delete()
        else:
            await ctx.message.channel.send("No arguments :no_mouth:")

def setup(DClient):
    DClient.add_cog(RedditCmds(DClient))