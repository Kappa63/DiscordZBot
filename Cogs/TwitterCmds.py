import discord
from discord.ext import commands
import requests
import tweepy
from Setup import Twitter
from Setup import ChVote, ChVoteUser, SendWait
from Setup import ErrorEmbeds
import asyncio


def TwitterbedMaker(TWprofile, IsVerified, TwTtype, TWtimeline, TwTNum, TwTtotal):
    TEmE = discord.Embed(
        title=f"@{TWprofile.screen_name} / {TWprofile.name} {IsVerified}",
        description=TwTtype,
        color=0x0384FC,
    )
    TEmE.set_thumbnail(url=TWprofile.profile_image_url_https)
    TEmE.add_field(name=f"{TwTtype} on: ", value=TWtimeline.created_at, inline=False)
    TEmE.add_field(name=f"`{TwTNum+1}/{TwTtotal}`", value="\u200b", inline=False)
    TEmE.add_field(
        name="Retweets: ", value=f"{TWtimeline.retweet_count:,}", inline=True
    )
    TEmE.add_field(name="Likes: ", value=f"{TWtimeline.favorite_count:,}", inline=True)
    if TwTtype == "Retweet":
        try:
            if hasattr(TWtimeline.retweeted_status, "extended_entities"):
                TEmE.set_image(
                    url=TWtimeline.retweeted_status.extended_entities["media"][0][
                        "media_url_https"
                    ]
                )
            TEmE.add_field(
                name=f"Retweeted Body (By: {Twitter.get_user(user_id = TWtimeline.retweeted_status.user.id).screen_name}): ",
                value=TWtimeline.retweeted_status.full_text,
                inline=False,
            )
        except tweepy.error.TweepError:
            TEmE.add_field(
                name="On (By: --Deleted--): ", value="--Deleted--", inline=False
            )
    elif TwTtype == "Quote":
        try:
            if hasattr(TWtimeline.quoted_status, "extended_entities"):
                TEmE.set_image(
                    url=TWtimeline.quoted_status.extended_entities["media"][0][
                        "media_url_https"
                    ]
                )
            TEmE.add_field(name="Main Body: ", value=TWtimeline.full_text, inline=False)
            TEmE.add_field(
                name=f"Quoted Body (By: {Twitter.get_user(user_id = TWtimeline.quoted_status.user.id).screen_name}): ",
                value=TWtimeline.quoted_status.full_text,
                inline=False,
            )
        except tweepy.error.TweepError:
            TEmE.add_field(
                name="On (By: --Deleted--): ", value="--Deleted--", inline=False
            )
    elif TwTtype == "Tweet":
        if hasattr(TWtimeline, "extended_entities"):
            TEmE.set_image(
                url=TWtimeline.extended_entities["media"][0]["media_url_https"]
            )
        TEmE.add_field(name="Tweet Body: ", value=TWtimeline.full_text, inline=False)
    elif TwTtype == "Comment":
        TEmE.add_field(name="Comment Body: ", value=TWtimeline.full_text, inline=False)
        try:
            TwCO = Twitter.get_status(
                id=TWtimeline.in_reply_to_status_id,
                trim_user=True,
                tweet_mode="extended",
            )
            if hasattr(TwCO, "extended_entities"):
                TEmE.set_image(
                    url=TwCO.extended_entities["media"][0]["media_url_https"]
                )
            TEmE.add_field(
                name=f"On (By: {TWtimeline.in_reply_to_screen_name}): ",
                value=TwCO.full_text,
                inline=False,
            )
        except tweepy.error.TweepError:
            TEmE.add_field(
                name="On (By: --Deleted--): ", value="--Deleted--", inline=False
            )

    TEmE.set_footer(text="Need help navigating? zhelp navigation")
    return TEmE


def ChTwTp(TWtimeline):
    if hasattr(TWtimeline, "retweeted_status") and TWtimeline.retweeted_status:
        return "Retweet"
    elif hasattr(TWtimeline, "quoted_status") and TWtimeline.quoted_status:
        return "Quote"
    elif (
        hasattr(TWtimeline, "in_reply_to_status_id")
        and TWtimeline.in_reply_to_status_id
    ):
        return "Comment"
    else:
        return "Tweet"


class TwitterCmds(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.group(name="twitter", invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def TwitterNav(self, ctx, *args):
        def ChCHanS(MSg):
            MesS = MSg.content.lower()
            RsT = False
            try:
                if int(MSg.content) <= 10:
                    RsT = True
            except ValueError:
                if (MesS == "cancel") or (MesS == "c"):
                    RsT = True
            return (
                MSg.guild.id == ctx.guild.id
                and MSg.channel.id == ctx.channel.id
                and RsT
            )

        def ChCHEm(RcM, RuS):
            return (
                RuS.bot == False
                and RcM.message == TwTsL
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

        TWinput = " ".join(args).split(" ")
        if TWinput[0].lower() == "search" and args:
            TWinput.pop(0)
            if " ".join(TWinput):
                C = 0
                SrchTw = []
                for TWuser in Twitter.search_users(TWinput, count=10):
                    C += 1
                    if C == 1:
                        STEm = discord.Embed(
                            title=f':mag: Search for "{" ".join(TWinput)}"',
                            description="\u200b",
                            color=0x0384FC,
                        )
                    IsVerified = ""
                    if TWuser.verified:
                        IsVerified = ":ballot_box_with_check: "
                    STEm.add_field(
                        name="\u200b",
                        value=f"{C}. `@{TWuser.screen_name} / {TWuser.name}` {IsVerified}",
                        inline=False,
                    )
                    SrchTw.append(TWuser)
                if C == 0:
                    await SendWait(ctx, "Not Found :expressionless:")
                    return
                STEm.set_footer(
                    text='Choose a number to open Twitter User Profile. "c" or "cancel" to exit search.\n\n*The Search closes automatically after 20sec of inactivity.*'
                )
                TwSent = await ctx.message.channel.send(embed=STEm)
                try:
                    ResS = await self.DClient.wait_for(
                        "message", check=ChCHanS, timeout=20
                    )
                    LResS = ResS.content.lower()
                    try:
                        if int(ResS.content) <= 10:
                            TWchoice = SrchTw[int(ResS.content) - 1]
                            IsVerified = ""
                            if TWchoice.verified:
                                IsVerified = ":ballot_box_with_check: "
                            TWname = SrchTw[int(ResS.content) - 1].screen_name
                            await TwSent.edit(
                                embed=discord.Embed(
                                    title=":calling: Finding...",
                                    description=f"@{TWchoice.screen_name} / {TWchoice.name} {IsVerified}",
                                    color=0x0384FC,
                                )
                            )
                    except ValueError:
                        if (LResS == "cancel") or (LResS == "c"):
                            await TwSent.edit(
                                embed=discord.Embed(
                                    title=":x: Search Cancelled",
                                    description="\u200b",
                                    color=0x0384FC,
                                )
                            )
                except asyncio.TimeoutError:
                    await TwSent.edit(
                        embed=discord.Embed(
                            title=":hourglass: Search Timeout...",
                            description="\u200b",
                            color=0x0384FC,
                        )
                    )
            else:
                await SendWait(ctx, "No search argument :woozy_face:")

        elif args:
            TWname = " ".join(args)
        else:
            await SendWait(ctx, "No Arguments :no_mouth:")
        try:
            try:
                TWprofile = Twitter.get_user(TWname)
                IsVerified = ""
                TWdesc = "\u200b"
                if TWprofile.verified:
                    IsVerified = ":ballot_box_with_check: "
                if TWprofile.description:
                    TWdesc = TWprofile.description
                TEm = discord.Embed(
                    title=f"@{TWprofile.screen_name} / {TWprofile.name} {IsVerified}",
                    description=TWdesc,
                    color=0x0384FC,
                )
                TEm.set_thumbnail(url=TWprofile.profile_image_url_https)
                if TWprofile.location:
                    TEm.add_field(
                        name="Location: ", value=TWprofile.location, inline=True
                    )
                if TWprofile.url:
                    TEm.add_field(
                        name="Website: ",
                        value=(requests.head(TWprofile.url)).headers["Location"],
                        inline=True,
                    )
                TEm.add_field(
                    name="Created: ",
                    value=(str(TWprofile.created_at).split(" "))[0],
                    inline=False,
                )
                TEm.add_field(
                    name="Following: ",
                    value=f"{TWprofile.friends_count:,}",
                    inline=True,
                )
                TEm.add_field(
                    name="Followers: ",
                    value=f"{TWprofile.followers_count:,}",
                    inline=True,
                )
                TEm.set_footer(text="Need help navigating? zhelp navigation")
                TWtimeline = Twitter.user_timeline(
                    TWname, trim_user=True, tweet_mode="extended"
                )
                TwTsL = await ctx.message.channel.send(embed=TEm)
                TwTNum = 0
                OnMain = True
                await TwTsL.add_reaction("⬅️")
                await TwTsL.add_reaction("❌")
                await TwTsL.add_reaction("➡️")
                await TwTsL.add_reaction("#️⃣")
                while True:
                    try:
                        ReaEm = await self.DClient.wait_for(
                            "reaction_add", check=ChCHEm, timeout=120
                        )
                        await TwTsL.remove_reaction(ReaEm[0].emoji, ReaEm[1])
                        if ReaEm[0].emoji == "⬅️" and TwTNum == 0:
                            OnMain = True
                            await TwTsL.edit(embed=TEm)
                        elif ReaEm[0].emoji == "⬅️" and TwTNum > 0:
                            TwTNum -= 1
                            await TwTsL.edit(
                                embed=TwitterbedMaker(
                                    TWprofile,
                                    IsVerified,
                                    ChTwTp(TWtimeline[TwTNum]),
                                    TWtimeline[TwTNum],
                                    TwTNum,
                                    len(TWtimeline),
                                )
                            )
                        elif ReaEm[0].emoji == "➡️" and OnMain:
                            OnMain = False
                            TwTNum = 0
                            await TwTsL.edit(
                                embed=TwitterbedMaker(
                                    TWprofile,
                                    IsVerified,
                                    ChTwTp(TWtimeline[TwTNum]),
                                    TWtimeline[TwTNum],
                                    TwTNum,
                                    len(TWtimeline),
                                )
                            )
                        elif (
                            ReaEm[0].emoji == "➡️"
                            and len(TWtimeline) > TwTNum + 1
                            and TwTNum >= 0
                        ):
                            TwTNum += 1
                            await TwTsL.edit(
                                embed=TwitterbedMaker(
                                    TWprofile,
                                    IsVerified,
                                    ChTwTp(TWtimeline[TwTNum]),
                                    TWtimeline[TwTNum],
                                    TwTNum,
                                    len(TWtimeline),
                                )
                            )
                        elif ReaEm[0].emoji == "#️⃣":
                            if await ChVoteUser(ReaEm[1].id):
                                TemTw = await ctx.message.channel.send(
                                    'Choose a number to open navigate to page. "c" or "cancel" to exit navigation.'
                                )
                                try:
                                    ResE = await self.DClient.wait_for(
                                        "message", check=ChCHEmFN, timeout=10
                                    )
                                    await ResE.delete()
                                    await TemTw.delete()
                                    try:
                                        try:
                                            pG = int(ResE.content)
                                            if 0 < pG <= len(TWtimeline) - 1:
                                                TwTNum = pG - 1
                                            elif pG < 1:
                                                TwTNum = 0
                                                pass
                                            else:
                                                TwTNum = len(TWtimeline) - 1
                                        except TypeError:
                                            pass
                                    except ValueError:
                                        pass
                                    await TwTsL.edit(
                                        embed=TwitterbedMaker(
                                            TWprofile,
                                            IsVerified,
                                            ChTwTp(TWtimeline[TwTNum]),
                                            TWtimeline[TwTNum],
                                            TwTNum,
                                            len(TWtimeline),
                                        )
                                    )
                                except asyncio.TimeoutError:
                                    await TemTw.edit("Request Timeout")
                                    await asyncio.sleep(5)
                                    await TemTw.delete()
                            else:
                                await ctx.message.channel.send(
                                    embed=ErrorEmbeds("Vote")
                                )
                        elif ReaEm[0].emoji == "➡️" and len(TWtimeline) == TwTNum + 1:
                            await TwTsL.remove_reaction("⬅️", self.DClient.user)
                            await TwTsL.remove_reaction("❌", self.DClient.user)
                            await TwTsL.remove_reaction("➡️", self.DClient.user)
                            await TwTsL.remove_reaction("#️⃣", self.DClient.user)
                            break
                        elif ReaEm[0].emoji == "❌":
                            await TwTsL.remove_reaction("⬅️", self.DClient.user)
                            await TwTsL.remove_reaction("❌", self.DClient.user)
                            await TwTsL.remove_reaction("➡️", self.DClient.user)
                            await TwTsL.remove_reaction("#️⃣", self.DClient.user)
                            break
                    except asyncio.TimeoutError:
                        await TwTsL.remove_reaction("⬅️", self.DClient.user)
                        await TwTsL.remove_reaction("❌", self.DClient.user)
                        await TwTsL.remove_reaction("➡️", self.DClient.user)
                        await TwTsL.remove_reaction("#️⃣", self.DClient.user)
                        break
            except tweepy.error.TweepError:
                await SendWait(ctx, "Not Found :expressionless:")
        except UnboundLocalError:
            pass

    @TwitterNav.command(name="trending")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def TwitterTrends(self, ctx, *args):
        Trends = Twitter.trends_place(id=23424977)
        TEm = discord.Embed(
            title=f'Currently Trending (USA) ({Trends[0]["as_of"][:10]} {Trends[0]["as_of"][12:16]})',
            color=0x0384FC,
        )
        for Trend in Trends[0]["trends"]:
            if Trend["tweet_volume"]:
                TEm.add_field(
                    name=Trend["name"],
                    value=f'{Trend["tweet_volume"]:,} Tweets',
                    inline=False,
                )
            else:
                TEm.add_field(name=Trend["name"], value=f"\u200b", inline=False)
        await ctx.message.channel.send(embed=TEm)


def setup(DClient):
    DClient.add_cog(TwitterCmds(DClient))