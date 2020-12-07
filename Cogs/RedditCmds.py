import discord
from discord.ext import commands
from prawcore import NotFound, Forbidden
import requests
import os 
from CBot import Reddit
from CBot import ChVote
import asyncio

def EmbedMaker(SubCpoS, Subname, Type = "R", PostNum = 0, TotalPosts = 0):
    if len(SubCpoS.title) > 253:
        PostTitle = SubCpoS.title[0:253]
        PostTitle = PostTitle + "..."
    else:
        PostTitle = SubCpoS.title

    if len(SubCpoS.selftext) > 1021:
        PostText = SubCpoS.selftext[0:1021]
        PostText = PostText + "..."
    else:
        PostText = SubCpoS.selftext

    if PosType(SubCpoS):
        if SubCpoS.over_18:
            if ctx.channel.is_nsfw():
                REm = discord.Embed(title = PostTitle,  description = f'Upvote Ratio: {SubCpoS.upvote_ratio} // Post is NSFW', color = 0x8b0000)
                if Type == "S":
                    REm.add_field(name = f'`Page: {PostNum+1}/{TotalPosts}`', value = "\u200b", inline = True)
                if SubCpoS.selftext != "":
                    REm.add_field(name = "Body", value = PostText, inline = False)
                REm.add_field(name = "Post: ", value = SubCpoS.url, inline = True)
            else:
                REm = discord.Embed(title = "***NOT NSFW CHANNEL***",  description = "Post is NSFW", color = 0x8b0000)
                REm.add_field(name = "NSFW: ", value = "This channel isn't NSFW. No NSFW here", inline = False)
        else:
            REm = discord.Embed(title = PostTitle, description = f'Upvote Ratio: {SubCpoS.upvote_ratio} // Post is Clean', color = 0x8b0000)
            if Type == "S":
                REm.add_field(name = f'`Page: {PostNum+1}/{TotalPosts}`', value = "\u200b", inline = True)
            if SubCpoS.selftext != "":
                REm.add_field(name = "Body", value = PostText, inline = False)
            REm.add_field(name = "Post: ", value = SubCpoS.url, inline = True)
    else:
        NSfw = False
        if SubCpoS.over_18:
            if ctx.channel.is_nsfw():
                REm = discord.Embed(title = PostTitle,  description = f'Upvote Ratio: {SubCpoS.upvote_ratio} // Post is NSFW', color = 0x8b0000)
            else:
                REm = discord.Embed(title = "***NOT NSFW CHANNEL***",  description = "Post is NSFW", color = 0x8b0000)
            NSfw = True
            if Type == "S":
                REm.add_field(name = f'`Post: {PostNum+1}/{TotalPosts}`', value = "\u200b", inline = True)
        else:
            REm = discord.Embed(title = PostTitle, description = f'Upvote Ratio: {SubCpoS.upvote_ratio} // Post is Clean', color = 0x8b0000)
            if Type == "S":
                REm.add_field(name = f'`Post: {PostNum+1}/{TotalPosts}`', value = "\u200b", inline = True)
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
    REm.set_footer(text = f'From r/{Subname}')
    REm.set_author(name = f'*By u/{SubCpoS.author}*')
    return REm

def EmbOri(REm, Type, SubCpoS):
    REm.add_field(name = "\u200b", value = f'The original post is a {Type} [click here]({SubCpoS.url}) to view the original', inline = False)
    REm.set_image(url = SubCpoS.preview["images"][-1]["source"]["url"])
    return REm

def CheckSub(Sub):
    Valid = True
    try:
        Reddit.subreddits.search_by_name(Sub, exact = True)
        Reddit.subreddit(Sub).subreddit_type
    except (NotFound, Forbidden):
        Valid = False
    return Valid
    
def PosType(Sub):
    TextB = False
    if Sub.is_self:
        TextB = True
    return TextB

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
                    TotalPosts = 0
                    for _ in Post:
                        TotalPosts += 1
                    Post = Reddit.subreddit("".join(args)).hot()
                    if TotalPosts == 0:
                        await ctx.message.channel.send("No posts on that subreddit :no_mouth:")
                        return
                    ChoicePosts = random.randint(1, TotalPosts)
                    for _ in range(0, ChoicePosts):
                        SubCpoS = next(Sub for Sub in Post if not Sub.stickied)                
                except StopIteration:
                    await ctx.message.channel.send("No posts on that subreddit :no_mouth:")
                    return
                await ctx.message.channel.send(embed = EmbedMaker(SubCpoS, "".join(args)))
            else:
                await ctx.message.channel.send("Sub doesn't exist or private :expressionless: (Make sure the argument doesnt include the r/)")
        else:
            await ctx.message.channel.send("No arguments :no_mouth:")

    @SrSub.command(name = "surf")
    @commands.check(ChVote)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def SrSub(self, ctx, *args):
        if args:
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
                TotalPosts = 0
                for SuTPos in Post:
                    TotalPosts += 1
                    if not SuTPos.stickied:
                        SubCpoS.append(SuTPos)
                if TotalPosts == 0:
                    await ctx.message.channel.send("No posts on that subreddit :no_mouth:")
                    return              
                KraPosS = await ctx.message.channel.send(embed = EmbedMaker(SubCpoS[0], ContT[1], "S", 0, TotalPosts))
                PostNum = 0
                await KraPosS.add_reaction("⬅️")
                await KraPosS.add_reaction("❌")
                await KraPosS.add_reaction("➡️")
                await KraPosS.add_reaction("#️⃣")
                while True:
                    try:
                        Res = await self.DClient.wait_for("reaction_add", check = ChCHEm, timeout = 120) 
                        await KraPosS.remove_reaction(Res[0].emoji, Res[1])
                        if Res[0].emoji == "⬅️" and PostNum != 0:
                            PostNum -= 1
                            await KraPosS.edit(embed = EmbedMaker(SubCpoS[PostNum], ContT[1], "S", PostNum, TotalPosts))
                        elif Res[0].emoji == "➡️":
                            if PostNum < TotalPosts-1:
                                PostNum += 1
                                await KraPosS.edit(embed = EmbedMaker(SubCpoS[PostNum], ContT[1], "S", PostNum, TotalPosts))
                            else:
                                await KraPosS.edit(embed = EmbedMaker(SubCpoS[PostNum], ContT[1], "S", PostNum, TotalPosts))
                                await KraPosS.remove_reaction("⬅️", self.DClient.user)
                                await KraPosS.remove_reaction("❌", self.DClient.user)
                                await KraPosS.remove_reaction("➡️", self.DClient.user)
                                await KraPosS.remove_reaction("#️⃣", self.DClient.user)
                                break
                        elif Res[0].emoji == "#️⃣":
                            if await ChVote(ctx):
                                TemTw = await ctx.message.channel.send('Choose a number to open navigate to page. "c" or "cancel" to exit navigation.\n\n*The Navigation closes automatically after 10sec of inactivity.*')
                                try:
                                    ResE = await self.DClient.wait_for("message", check = ChCHEmFN, timeout = 10)
                                    await TemTw.delete()
                                    await ResE.delete()
                                    try:
                                        try:
                                            pG = int(ResE.content)
                                            if 0 < pG <= TotalPosts-1:
                                                PostNum = pG-1
                                            elif pG < 1:
                                                PostNum = 0
                                                pass
                                            else:
                                                PostNum = TotalPosts-1 
                                        except TypeError:
                                            pass
                                    except ValueError:
                                        pass
                                    await KraPosS.edit(embed = EmbedMaker(SubCpoS[PostNum], ContT[1], "S", PostNum, TotalPosts))
                                except asyncio.exceptions.TimeoutError:
                                    await TemTw.edit("Request Timeout")
                                    await asyncio.sleep(5)
                                    await TemTw.delete()
                        elif Res[0].emoji == "❌":
                            await KraPosS.edit(embed = EmbedMaker(SubCpoS[PostNum], ContT[1], "S", PostNum, TotalPosts))
                            await KraPosS.remove_reaction("⬅️", self.DClient.user)
                            await KraPosS.remove_reaction("❌", self.DClient.user)
                            await KraPosS.remove_reaction("➡️", self.DClient.user)
                            await KraPosS.remove_reaction("#️⃣", self.DClient.user)
                            break
                    except asyncio.TimeoutError:
                        await KraPosS.edit(embed = EmbedMaker(SubCpoS[PostNum], ContT[1], "S", PostNum, TotalPosts))
                        await KraPosS.remove_reaction("⬅️", self.DClient.user)
                        await KraPosS.remove_reaction("❌", self.DClient.user)
                        await KraPosS.remove_reaction("➡️", self.DClient.user)
                        await KraPosS.remove_reaction("#️⃣", self.DClient.user)
                        break
            else:
                await ctx.message.channel.send("Sub doesn't exist or private :expressionless: (Make sure the argument doesnt include the r/)")
        else:
            await ctx.message.channel.send("No arguments :no_mouth:")

def setup(DClient):
    DClient.add_cog(RedditCmds(DClient))