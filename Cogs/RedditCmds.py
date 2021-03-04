import discord
from discord.ext import commands
from prawcore import NotFound, Forbidden
import os
import random
from Setup import Reddit, Rdt, GetPatreonTier, SendWait
from Setup import ChVote, ChVoteUser, ChPatreonT2, ChMaxMultireddits
from Setup import ErrorEmbeds
import FuncMon
import inspect
import asyncio
import datetime


def EmbedMaker(ctx, SubCpoS, Subname, Type="R", PostNum=0, TotalPosts=0):
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
                REm = discord.Embed(
                    title=PostTitle,
                    description=f"Upvote Ratio: {SubCpoS.upvote_ratio} // Post is NSFW",
                    color=0x8B0000,
                )
                if Type == "S":
                    REm.add_field(
                        name=f"`Page: {PostNum+1}/{TotalPosts}`",
                        value="\u200b",
                        inline=True,
                    )
                if SubCpoS.selftext != "":
                    REm.add_field(name="Body", value=PostText, inline=False)
                REm.add_field(name="Post: ", value=SubCpoS.url, inline=True)
            else:
                REm = discord.Embed(
                    title="***NOT NSFW CHANNEL***",
                    description="Post is NSFW",
                    color=0x8B0000,
                )
                REm.add_field(
                    name="NSFW: ",
                    value="This channel isn't NSFW. No NSFW here",
                    inline=False,
                )
        else:
            REm = discord.Embed(
                title=PostTitle,
                description=f"Upvote Ratio: {SubCpoS.upvote_ratio} // Post is Clean",
                color=0x8B0000,
            )
            if Type == "S":
                REm.add_field(
                    name=f"`Page: {PostNum+1}/{TotalPosts}`",
                    value="\u200b",
                    inline=True,
                )
            if SubCpoS.selftext != "":
                REm.add_field(name="Body", value=PostText, inline=False)
            REm.add_field(name="Post: ", value=SubCpoS.url, inline=True)
    else:
        NSfw = False
        if SubCpoS.over_18:
            if ctx.channel.is_nsfw():
                REm = discord.Embed(
                    title=PostTitle,
                    description=f"Upvote Ratio: {SubCpoS.upvote_ratio} // Post is NSFW",
                    color=0x8B0000,
                )
            else:
                REm = discord.Embed(
                    title="***NOT NSFW CHANNEL***",
                    description="Post is NSFW",
                    color=0x8B0000,
                )
            NSfw = True
            if Type == "S":
                REm.add_field(
                    name=f"`Post: {PostNum+1}/{TotalPosts}`",
                    value="\u200b",
                    inline=True,
                )
        else:
            REm = discord.Embed(
                title=PostTitle,
                description=f"Upvote Ratio: {SubCpoS.upvote_ratio} // Post is Clean",
                color=0x8B0000,
            )
            if Type == "S":
                REm.add_field(
                    name=f"`Post: {PostNum+1}/{TotalPosts}`",
                    value="\u200b",
                    inline=True,
                )
        C = 0
        if (NSfw and ctx.channel.is_nsfw()) or (NSfw == False):
            try:
                GaLpos = SubCpoS.gallery_data["items"]
                for ImgPoGa in GaLpos:
                    FiPoS = SubCpoS.media_metadata[ImgPoGa["media_id"]]
                    if FiPoS["e"] == "Image":
                        REm.add_field(
                            name="\u200b",
                            value=f"The original post is a gallery [click here]({SubCpoS.url}) to view the rest of the post",
                            inline=False,
                        )
                        pstR = FiPoS["p"][-1]["u"]
                        REm.set_image(url=pstR)
                        break
            except AttributeError:
                for ExT in [".png", ".jpg", ".jpeg", ".gif", ".gifv"]:
                    C += 1
                    if (SubCpoS.url).endswith(ExT):
                        pstR = SubCpoS.url
                        if ExT == ".gifv":
                            REm.add_field(
                                name="\u200b",
                                value=f"The original post is a video(imgur) [click here]({SubCpoS.url}) to view the original",
                                inline=False,
                            )
                            pstR = SubCpoS.url[:-1]
                        REm.set_image(url=pstR)
                        break
                    elif C == 5:
                        try:
                            if "v.redd.it" in SubCpoS.url:
                                EmbOri(REm, "video (reddit)", SubCpoS)
                            elif (
                                "youtu.be" in SubCpoS.url
                                or "youtube.com" in SubCpoS.url
                            ):
                                EmbOri(REm, "video (youtube)", SubCpoS)
                            elif "gfycat" in SubCpoS.url:
                                EmbOri(REm, "video (gfycat)", SubCpoS)
                            elif "redgifs" in SubCpoS.url:
                                EmbOri(REm, "video (redgifs)", SubCpoS)
                            else:
                                EmbOri(REm, "webpage", SubCpoS)
                        except AttributeError:
                            REm.add_field(
                                name="Post: ", value=SubCpoS.url, inline=False
                            )
                            REm.add_field(
                                name="Media Preview Unavailable. Sorry!!",
                                value="\u200b",
                            )
        else:
            REm.add_field(
                name="NSFW: ",
                value="This isn't an NSFW channel. No NSFW allowed here.",
                inline=False,
            )
    if Type == "S":
        REm.set_footer(
            text=f"From r/{SubCpoS.subreddit.display_name}\n\nNeed help navigating? zhelp navigation"
        )
    else:
        REm.set_footer(text=f"From r/{SubCpoS.subreddit.display_name}")
    REm.set_author(name=f"*By u/{SubCpoS.author}*")
    return REm


def EmbOri(REm, Type, SubCpoS):
    REm.add_field(
        name="\u200b",
        value=f"The original post is a {Type} [click here]({SubCpoS.url}) to view the original",
        inline=False,
    )
    REm.set_image(url=SubCpoS.preview["images"][-1]["source"]["url"])
    return REm


def CheckSub(Sub):
    Valid = True
    try:
        Reddit.subreddits.search_by_name(Sub, exact=True)
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

    @commands.group(name="reddit", invoke_without_command=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def RedditRand(self, ctx, *args):
        if args:
            if CheckSub("".join(args)):
                await SendWait(ctx, ":mobile_phone: Finding Post...")
                try:
                    Post = list(Reddit.subreddit("".join(args)).hot())
                    TotalPosts = len(Post)
                    if TotalPosts == 0:
                        await ctx.message.channel.send(
                            "No posts on that subreddit :no_mouth:"
                        )
                        return
                    ChoicePosts = random.randint(1, TotalPosts)
                    for _ in range(0, ChoicePosts):
                        SubCpoS = next(Sub for Sub in Post if not Sub.stickied)
                except StopIteration:
                    await ctx.message.channel.send(
                        "No posts on that subreddit :no_mouth:"
                    )
                    return
                await ctx.message.channel.send(
                    embed=EmbedMaker(ctx, SubCpoS, "".join(args))
                )
            else:
                await ctx.message.channel.send(
                    "Sub doesn't exist or private :expressionless: (Make sure the argument doesnt include the r/)"
                )
        else:
            await ctx.message.channel.send("No arguments :no_mouth:")

    @RedditRand.command(name="surf")
    @commands.check(ChVote)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def RedditNav(self, ctx, *args):
        def ChCHEmCH(RcM, RuS):
            return (
                RuS.bot == False
                and RcM.message == KraPosS
                and str(RcM.emoji) in ["🔝", "📈", "🔥", "📝", "❌"]
            )

        def ChCHEmCHT(RcM, RuS):
            return (
                RuS.bot == False
                and RcM.message == KraPosS
                and str(RcM.emoji) in ["🗓️", "🌍", "📅", "❌"]
            )

        def ChCHEm(RcM, RuS):
            return (
                RuS.bot == False
                and RcM.message == KraPosS
                and str(RcM.emoji) in ["⬅️", "❌", "➡️", "#️⃣"]
            )

        def ChCHEmFN(MSg):
            MesS = MSg.content.lower()
            RsT = False
            try:
                if int(MSg.content):
                    RsT = True
            except ValueError:
                if (MesS == "cancel") or (MesS == "c"):
                    RsT = True
            return (
                MSg.guild.id == ctx.guild.id
                and MSg.channel.id == ctx.channel.id
                and RsT
            )

        if args:
            if CheckSub("".join(args)) or inspect.stack()[1].function == "__call__":
                KraPosS = await ctx.message.channel.send(
                    embed=discord.Embed(
                        title="How would you like to sort the subreddit?",
                        description="🔝 to sort by top.\n📈 to sort by rising.\n🔥 to sort by hot.\n📝 to sort by new.\n❌ to cancel",
                        footer="This timesout in 10s",
                    )
                )
                await KraPosS.add_reaction("🔝")
                await KraPosS.add_reaction("📈")
                await KraPosS.add_reaction("🔥")
                await KraPosS.add_reaction("📝")
                await KraPosS.add_reaction("❌")
                try:
                    ResIni = await self.DClient.wait_for(
                        "reaction_add", check=ChCHEmCH, timeout=10
                    )
                    if ResIni[0].emoji != "🔝":
                        await KraPosS.edit(
                            embed=discord.Embed(title=":mobile_phone: Finding Posts...")
                        )
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
                        await KraPosS.edit(
                            embed=discord.Embed(
                                title="How would you like to sort by top?",
                                description="🌍 to sort by top all time.\n🗓️ to sort by top this month.\n📅 to sort by top today.\n❌ to cancel",
                                footer="This timesout in 10s",
                            )
                        )
                        await KraPosS.add_reaction("🌍")
                        await KraPosS.add_reaction("🗓️")
                        await KraPosS.add_reaction("📅")
                        ResIniT = await self.DClient.wait_for(
                            "reaction_add", check=ChCHEmCHT, timeout=10
                        )
                        await KraPosS.remove_reaction(ResIniT[0].emoji, ResIniT[1])
                        await KraPosS.edit(
                            embed=discord.Embed(title=":mobile_phone: Finding Posts...")
                        )
                        await KraPosS.remove_reaction("❌", self.DClient.user)
                        await KraPosS.remove_reaction("🌍", self.DClient.user)
                        await KraPosS.remove_reaction("🗓️", self.DClient.user)
                        await KraPosS.remove_reaction("📅", self.DClient.user)
                        if ResIniT[0].emoji == "❌":
                            await KraPosS.delete()
                            return
                        elif ResIniT[0].emoji == "🌍":
                            Post = Reddit.subreddit("".join(args)).top("all")
                        elif ResIniT[0].emoji == "🗓️":
                            Post = Reddit.subreddit("".join(args)).top("month")
                        elif ResIniT[0].emoji == "📅":
                            Post = Reddit.subreddit("".join(args)).top("day")
                except asyncio.TimeoutError:
                    await KraPosS.edit(embed=discord.Embed(title="Timeout"))
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
                    await SendWait(ctx, "No posts on that subreddit :no_mouth:")
                    return
                KraPosS = await ctx.message.channel.send(
                    embed=EmbedMaker(ctx, SubCpoS[0], "".join(args), "S", 0, TotalPosts)
                )
                PostNum = 0
                await KraPosS.add_reaction("⬅️")
                await KraPosS.add_reaction("❌")
                await KraPosS.add_reaction("➡️")
                await KraPosS.add_reaction("#️⃣")
                while True:
                    try:
                        Res = await self.DClient.wait_for(
                            "reaction_add", check=ChCHEm, timeout=120
                        )
                        await KraPosS.remove_reaction(Res[0].emoji, Res[1])
                        if Res[0].emoji == "⬅️" and PostNum != 0:
                            PostNum -= 1
                            await KraPosS.edit(
                                embed=EmbedMaker(
                                    ctx,
                                    SubCpoS[PostNum],
                                    "".join(args),
                                    "S",
                                    PostNum,
                                    TotalPosts,
                                )
                            )
                        elif Res[0].emoji == "➡️":
                            if PostNum < TotalPosts - 1:
                                PostNum += 1
                                await KraPosS.edit(
                                    embed=EmbedMaker(
                                        ctx,
                                        SubCpoS[PostNum],
                                        "".join(args),
                                        "S",
                                        PostNum,
                                        TotalPosts,
                                    )
                                )
                            else:
                                await KraPosS.edit(
                                    embed=EmbedMaker(
                                        ctx,
                                        SubCpoS[PostNum],
                                        "".join(args),
                                        "S",
                                        PostNum,
                                        TotalPosts,
                                    )
                                )
                                await KraPosS.remove_reaction("⬅️", self.DClient.user)
                                await KraPosS.remove_reaction("❌", self.DClient.user)
                                await KraPosS.remove_reaction("➡️", self.DClient.user)
                                await KraPosS.remove_reaction("#️⃣", self.DClient.user)
                                break
                        elif Res[0].emoji == "#️⃣":
                            if await ChVoteUser(Res[1].id):
                                TemTw = await ctx.message.channel.send(
                                    'Choose a number to open navigate to page. "c" or "cancel" to exit navigation.'
                                )
                                try:
                                    ResE = await self.DClient.wait_for(
                                        "message", check=ChCHEmFN, timeout=10
                                    )
                                    await TemTw.delete()
                                    await ResE.delete()
                                    try:
                                        try:
                                            pG = int(ResE.content)
                                            if 0 < pG <= TotalPosts - 1:
                                                PostNum = pG - 1
                                            elif pG < 1:
                                                PostNum = 0
                                                pass
                                            else:
                                                PostNum = TotalPosts - 1
                                        except TypeError:
                                            pass
                                    except ValueError:
                                        pass
                                    await KraPosS.edit(
                                        embed=EmbedMaker(
                                            ctx,
                                            SubCpoS[PostNum],
                                            "".join(args),
                                            "S",
                                            PostNum,
                                            TotalPosts,
                                        )
                                    )
                                except asyncio.exceptions.TimeoutError:
                                    await TemTw.edit("Request Timeout")
                                    await asyncio.sleep(5)
                                    await TemTw.delete()
                            else:
                                await ctx.message.channel.send(
                                    embed=ErrorEmbeds("Vote")
                                )
                        elif Res[0].emoji == "❌":
                            await KraPosS.edit(
                                embed=EmbedMaker(
                                    ctx,
                                    SubCpoS[PostNum],
                                    "".join(args),
                                    "S",
                                    PostNum,
                                    TotalPosts,
                                )
                            )
                            await KraPosS.remove_reaction("⬅️", self.DClient.user)
                            await KraPosS.remove_reaction("❌", self.DClient.user)
                            await KraPosS.remove_reaction("➡️", self.DClient.user)
                            await KraPosS.remove_reaction("#️⃣", self.DClient.user)
                            break
                    except asyncio.TimeoutError:
                        await KraPosS.edit(
                            embed=EmbedMaker(
                                ctx,
                                SubCpoS[PostNum],
                                "".join(args),
                                "S",
                                PostNum,
                                TotalPosts,
                            )
                        )
                        await KraPosS.remove_reaction("⬅️", self.DClient.user)
                        await KraPosS.remove_reaction("❌", self.DClient.user)
                        await KraPosS.remove_reaction("➡️", self.DClient.user)
                        await KraPosS.remove_reaction("#️⃣", self.DClient.user)
                        break
            else:
                await SendWait(
                    ctx,
                    "Sub doesn't exist or private :expressionless: (Make sure the argument doesnt include the r/)",
                )
        else:
            await SendWait(ctx, "No arguments :no_mouth:")

    @commands.command(name="redditor")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def GetRedditor(self, ctx, *args):
        def ChCHEm(RcM, RuS):
            return (
                RuS.bot == False
                and RcM.message == RTEm
                and str(RcM.emoji) in ["⬅️", "❌", "➡️", "#️⃣"]
            )

        def ChCHEmFN(MSg):
            MesS = MSg.content.lower()
            RsT = False
            try:
                if int(MSg.content):
                    RsT = True
            except ValueError:
                if (MesS == "cancel") or (MesS == "c"):
                    RsT = True
            return (
                MSg.guild.id == ctx.guild.id
                and MSg.channel.id == ctx.channel.id
                and RsT
            )

        if args:
            try:
                User = Reddit.redditor("".join(args))
                UEm = discord.Embed(
                    title=f"u/{User.name}",
                    description=User.subreddit["public_description"],
                    color=0x8B0000,
                )
                UEm.add_field(
                    name=f"{(User.link_karma + User.awarder_karma + User.awardee_karma + User.comment_karma):,} karma **·** {(datetime.datetime.now() - datetime.datetime.fromtimestamp(User.created_utc)).days} days",
                    value="\u200b",
                    inline=False,
                )
                UEm.add_field(
                    name=f'Trophies: `{", ".join([trophy.name for trophy in User.trophies()])}`',
                    value="\u200b",
                    inline=False,
                )
                UEm.set_thumbnail(url=User.icon_img)
                RTEm = await ctx.message.channel.send(embed=UEm)
                PostNum = 0
                OnRedditor = True
                SubCpoS = []
                TotalPosts = 0
                for SuTPos in User.submissions.new():
                    TotalPosts += 1
                    if not SuTPos.stickied:
                        SubCpoS.append(SuTPos)
                if TotalPosts == 0:
                    await SendWait(ctx, "No posts :no_mouth:")
                    return
                await RTEm.add_reaction("⬅️")
                await RTEm.add_reaction("❌")
                await RTEm.add_reaction("➡️")
                await RTEm.add_reaction("#️⃣")
                while True:
                    try:
                        ReaEm = await DClient.wait_for(
                            "reaction_add", check=ChCHEm, timeout=120
                        )
                        await RTEm.remove_reaction(ReaEm[0].emoji, ReaEm[1])
                        if ReaEm[0].emoji == "⬅️" and PostNum == 0:
                            OnRedditor = True
                            await RTEm.edit(embed=UEm)
                        elif ReaEm[0].emoji == "⬅️" and PostNum > 0:
                            PostNum -= 1
                            await RTEm.edit(
                                embed=EmbedMaker(
                                    ctx,
                                    SubCpoS[PostNum],
                                    "".join(args),
                                    "S",
                                    PostNum,
                                    TotalPosts,
                                )
                            )

                        elif ReaEm[0].emoji == "➡️" and OnRedditor:
                            OnRedditor = False
                            PostNum = 0
                            await RTEm.edit(
                                embed=EmbedMaker(
                                    ctx,
                                    SubCpoS[PostNum],
                                    "".join(args),
                                    "S",
                                    PostNum,
                                    TotalPosts,
                                )
                            )
                        elif (
                            ReaEm[0].emoji == "➡️"
                            and TotalPosts > PostNum + 1
                            and PostNum >= 0
                        ):
                            PostNum += 1
                            await RTEm.edit(
                                embed=EmbedMaker(
                                    ctx,
                                    SubCpoS[PostNum],
                                    "".join(args),
                                    "S",
                                    PostNum,
                                    TotalPosts,
                                )
                            )
                        elif ReaEm[0].emoji == "#️⃣":
                            if await ChVoteUser(ReaEm[1].id):
                                TempRdt = await ctx.message.channel.send(
                                    'Choose a number to open navigate to page. "c" or "cancel" to exit navigation.'
                                )
                                try:
                                    ResE = await DClient.wait_for(
                                        "message", check=ChCHEmFN, timeout=10
                                    )
                                    await ResE.delete()
                                    await TempRdt.delete()
                                    try:
                                        try:
                                            pG = int(ResE.content)
                                            if 0 < pG <= TotalPosts - 1:
                                                PostNum = pG - 1
                                            elif pG < 1:
                                                PostNum = 0
                                                pass
                                            else:
                                                PostNum = TotalPosts - 1
                                        except TypeError:
                                            pass
                                    except ValueError:
                                        pass
                                    await RTEm.edit(
                                        embed=EmbedMaker(
                                            ctx,
                                            SubCpoS[PostNum],
                                            "".join(args),
                                            "S",
                                            PostNum,
                                            TotalPosts,
                                        )
                                    )
                                except asyncio.TimeoutError:
                                    await TempRdt.edit("Request Timeout")
                                    await asyncio.sleep(5)
                                    await TempRdt.delete()
                            else:
                                await ctx.message.channel.send(
                                    embed=ErrorEmbeds("Vote")
                                )
                        elif ReaEm[0].emoji == "➡️" and TotalPosts == PostNum + 1:
                            await RTEm.remove_reaction("⬅️", self.DClient.user)
                            await RTEm.remove_reaction("❌", self.DClient.user)
                            await RTEm.remove_reaction("➡️", self.DClient.user)
                            await RTEm.remove_reaction("#️⃣", self.DClient.user)
                            break
                        elif ReaEm[0].emoji == "❌":
                            await RTEm.remove_reaction("⬅️", self.DClient.user)
                            await RTEm.remove_reaction("❌", self.DClient.user)
                            await RTEm.remove_reaction("➡️", self.DClient.user)
                            await RTEm.remove_reaction("#️⃣", self.DClient.user)
                            break
                    except asyncio.TimeoutError:
                        await RTEm.remove_reaction("⬅️", self.DClient.user)
                        await RTEm.remove_reaction("❌", self.DClient.user)
                        await RTEm.remove_reaction("➡️", self.DClient.user)
                        await RTEm.remove_reaction("#️⃣", self.DClient.user)
                        break
            except NotFound:
                await SendWait(ctx, "Redditor Not Found :no_mouth:")
        else:
            await SendWait(ctx, "No arguments :no_mouth:")

    @commands.group(name="multireddit", invoke_without_command=True)
    @commands.check(ChPatreonT2)
    @commands.check(ChMaxMultireddits)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def GetMultis(self, ctx, *args):
        if args:

            ArgumentHandle = " ".join(args).split(" ")
            if Rdt.count_documents({"IDd": ctx.author.id}) > 0:
                User = Rdt.find({"IDd": ctx.author.id})[0]
                Multireddits = User.keys()
                if ArgumentHandle[0] in Multireddits and ArgumentHandle[0] not in [
                    "IDd",
                    "_id",
                ]:
                    Subreddits = "+".join(User[ArgumentHandle[0]])
                    await self.RedditNav(ctx, Subreddits)
                else:
                    await SendWait(
                        ctx, f"That Multireddit ({ArgumentHandle[0]}) doesn't exist"
                    )
            else:
                await SendWait(ctx, "No Multireddits Found")
        else:
            await SendWait(ctx, "You forgot to add a Multireddit name")

    @GetMultis.command(name="list")
    @commands.check(ChPatreonT2)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ListMultis(self, ctx):
        if Rdt.count_documents({"IDd": ctx.author.id}) > 0:
            User = Rdt.find({"IDd": ctx.author.id})[0]
            Multireddits = User.keys()
            MEm = discord.Embed(
                title=f"{ctx.author.display_name}'s MultiReddits", color=0x8B0000
            )
            for Multireddit in Multireddits:
                if Multireddit not in ["IDd", "_id"]:
                    MEm.add_field(
                        name=Multireddit, value=f'`{", ".join(User[Multireddit])}`'
                    )
            await ctx.message.channel.send(embed=MEm)
        else:
            await SendWait(ctx, "No Multireddits Found")

    @GetMultis.command(name="create")
    @commands.check(ChPatreonT2)
    @commands.check(ChMaxMultireddits)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def CreateMulti(self, ctx, *args):
        ArgumentHandle = " ".join(args).split(" ")
        if args:
            TierApplicable = {
                "Tier 2 Super": 1,
                "Tier 3 Legend": 2,
                "Tier 4 Ultimate": 4,
            }
            TierLimit = TierApplicable[GetPatreonTier(ctx.author.id)]
            if Rdt.count_documents({"IDd": ctx.author.id}) > 0:
                User = Rdt.find({"IDd": ctx.author.id})[0]
                Multireddits = User.keys()
                if len(Multireddits) < TierLimit:
                    for Multireddit in Multireddits:
                        if Multireddit == ArgumentHandle[0]:
                            await SendWait(
                                ctx, f"Multireddit ({ArgumentHandle[0]}) Already Exists"
                            )
                            return
                    FuncMon.DbAdd(Rdt, {"IDd": ctx.author.id}, ArgumentHandle[0], [])
                    await SendWait(
                        ctx,
                        f"Added the Multireddit ({ArgumentHandle[0]}), you can now add and remove subreddits from it.",
                    )
                else:
                    await SendWait(
                        ctx,
                        "You already have the maximum amount of Multireddits. You can use 'zmultireddit' to see your multireddits or check 'zpatreon' to know more about limits",
                    )
            else:
                Rdt.insert_one({"IDd": ctx.author.id, ArgumentHandle[0]: []})
                await SendWait(
                    ctx,
                    f"Added the Multireddit ({ArgumentHandle[0]}), you can now add and remove subreddits from it.",
                )
        else:
            await SendWait(ctx, "No Arguments")

    @GetMultis.command(name="delete")
    @commands.check(ChPatreonT2)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def DeleteMulti(self, ctx, *args):
        if args:
            ArgumentHandle = " ".join(args).split(" ")
            if Rdt.count_documents({"IDd": ctx.author.id}) > 0:
                User = Rdt.find({"IDd": ctx.author.id})[0]
                Multireddits = User.keys()
                Multis = len(Multireddits) - 2
                for Multireddit in Multireddits:
                    if Multireddit == ArgumentHandle[0]:
                        if Multis == 1:
                            Rdt.delete_one({"IDd": ctx.author.id})
                        else:
                            FuncMon.DbRem(
                                Rdt, {"IDd": ctx.author.id}, ArgumentHandle[0]
                            )
                        await SendWait(
                            ctx, f"Deleted the Multireddit ({ArgumentHandle[0]})."
                        )
                        return
            else:
                await SendWait(ctx, "You don't have any Multireddits")
        else:
            await SendWait(ctx, "No Arguments")

    @GetMultis.command(name="add")
    @commands.check(ChPatreonT2)
    @commands.check(ChMaxMultireddits)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def AddMulti(self, ctx, *args):
        ArgumentHandle = " ".join(args).split(" ")
        if args:
            User = Rdt.find({"IDd": ctx.author.id})[0]
            Multireddits = User.keys()
            if ArgumentHandle[0] in Multireddits and ArgumentHandle[0] not in [
                "IDd",
                "_id",
            ]:
                if "".join(ArgumentHandle[1:]) not in User[ArgumentHandle[0]]:
                    if CheckSub("".join(ArgumentHandle[1:])):
                        User[ArgumentHandle[0]].append("".join(ArgumentHandle[1:]))
                        if FuncMon.ChangeTo(
                            Rdt,
                            {"IDd": ctx.author.id},
                            ArgumentHandle[0],
                            User[ArgumentHandle[0]],
                        ):
                            await SendWait(
                                ctx,
                                f'Added the Subreddit ({"".join(ArgumentHandle[1:])}) to Multireddit ({ArgumentHandle[0]})',
                            )
                        else:
                            await SendWait(ctx, "Something happened... Not sure")
                    else:
                        await SendWait(
                            ctx,
                            f'That Subreddit ({"".join(ArgumentHandle[1:])}) does not exist or is private',
                        )
                else:
                    await SendWait(
                        ctx,
                        f"Subreddit ({ArgumentHandle[0]}) Already Exists in that Multireddit ({ArgumentHandle[0]})",
                    )
            else:
                await SendWait(
                    ctx,
                    f"That Multireddit ({ArgumentHandle[0]}) does not exist. Check if the name is right or create it.",
                )
        else:
            await SendWait(ctx, "No Arguments")

    @GetMultis.command(aliases=["remove", "rem"])
    @commands.check(ChPatreonT2)
    @commands.check(ChMaxMultireddits)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def RemoveMulti(self, ctx, *args):
        ArgumentHandle = " ".join(args).split(" ")
        if args:
            if Rdt.count_documents({"IDd": ctx.author.id}) > 0:
                User = Rdt.find({"IDd": ctx.author.id})[0]
                Multireddits = User.keys()
                if ArgumentHandle[0] in Multireddits and ArgumentHandle[0] not in [
                    "IDd",
                    "_id",
                ]:
                    if "".join(ArgumentHandle[1:]) in User[ArgumentHandle[0]]:
                        User[ArgumentHandle[0]].remove("".join(ArgumentHandle[1:]))
                        if FuncMon.ChangeTo(
                            Rdt,
                            {"IDd": ctx.author.id},
                            ArgumentHandle[0],
                            User[ArgumentHandle[0]],
                        ):
                            await SendWait(
                                ctx,
                                f'Removed the Subreddit ({"".join(ArgumentHandle[1:])}) from Multireddit ({ArgumentHandle[0]})',
                            )
                        else:
                            await SendWait(ctx, "Something happened... Not sure")
                    else:
                        await SendWait(
                            ctx,
                            f"Subreddit ({ArgumentHandle[0]}) does not exist in that Multireddit ({ArgumentHandle[0]})",
                        )
                else:
                    await SendWait(
                        ctx,
                        f"That Multireddit ({ArgumentHandle[0]}) does not exist. Check if the name is right or create it.",
                    )
            else:
                await SendWait(ctx, "You don't have any Multireddits")
        else:
            await SendWait(ctx, "No Arguments")


def setup(DClient):
    DClient.add_cog(RedditCmds(DClient))