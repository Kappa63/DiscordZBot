import discord
from discord.ext import commands
from Setup import YClient
from Setup import ChVoteUser
from Setup import ErrorEmbeds
from Setup import GetVidDuration
import asyncio


def EmbedMaker(VidID, Channel, VidNum, VidsTotal):
    Vid = YClient.get_video_by_id(video_id=VidID).items[0]
    YLEm = discord.Embed(
        title=Vid.snippet.title,
        description=Vid.snippet.description.split("\n")[0],
        url=f"https://www.youtube.com/watch?v={VidID}",
        color=0xFF0000,
    )
    YLEm.set_thumbnail(url=Vid.snippet.thumbnails.high.url)
    YLEm.add_field(
        name=f"`Video: {VidNum+1}/{VidsTotal}`", value="\u200b", inline=False
    )
    if Vid.snippet.liveBroadcastContent == "live":
        YLEm.add_field(name="**CURRENTLY LIVE**", value="\u200b", inline=True)
    else:
        YLEm.add_field(
            name=f"Upload Date: {Vid.snippet.publishedAt[0:10]}",
            value="\u200b",
            inline=False,
        )
        YLEm.add_field(
            name=f"Duration: {GetVidDuration(VidID)}", value="\u200b", inline=False
        )
    try:
        YLEm.add_field(
            name="Views :eye:", value=f"{int(Vid.statistics.viewCount):,}", inline=True
        )
    except AttributeError:
        YLEm.add_field(name="Views :eye:", value="Disabled", inline=True)
    YLEm.add_field(name="\u200b", value="\u200b", inline=True)
    try:
        YLEm.add_field(
            name="Comments :speech_balloon:",
            value=f"{int(Vid.statistics.commentCount):,}",
            inline=True,
        )
    except AttributeError:
        YLEm.add_field(name="Comments :speech_balloon:", value="Disabled", inline=True)
    try:
        YLEm.add_field(
            name="Likes :thumbsup:",
            value=f"{int(Vid.statistics.likeCount):,}",
            inline=True,
        )
    except AttributeError:
        YLEm.add_field(name="Likes :thumbsup:", value="Disabled", inline=True)
    YLEm.add_field(name="\u200b", value="\u200b", inline=True)
    try:
        YLEm.add_field(
            name="Dislikes :thumbsdown:",
            value=f"{int(Vid.statistics.dislikeCount):,}",
            inline=True,
        )
    except AttributeError:
        YLEm.add_field(name="Dislikes :thumbsdown:", value="Disabled", inline=True)
    YLEm.add_field(name="\u200b", value="\u200b", inline=False)
    if Channel.statistics.hiddenSubscriberCount == False:
        YLEm.set_footer(
            text=f"{Channel.snippet.title} / Subs: {int(Channel.statistics.subscriberCount):,} / Videos: {int(Channel.statistics.videoCount):,}",
            icon_url=Channel.snippet.thumbnails.high.url,
        )
    else:
        YLEm.set_footer(
            text=f"{Channel.snippet.title} / Videos: {int(Channel.statistics.videoCount):,}\n\nNeed help navigating? zhelp navigation",
            icon_url=Channel.snippet.thumbnails.high.url,
        )
    return YLEm


class Youtube(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.command(aliases=["youtube", "yt"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def YoutubeGetter(self, ctx, *args):
        def ChCHEm(RcM, RuS):
            return (
                RuS.bot == False
                and RcM.message == YTEm
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

        YTinput = " ".join(args).split(" ")
        if YTinput[0].lower() == "search" and args:
            IDorName = "ID"
            YTinput.pop(0)
            if " ".join(YTinput):
                C = 0
                SrchYT = []
                for YTchannel in YClient.search(
                    q=" ".join(YTinput), count=10, search_type="channel"
                ).items:
                    ChannelGetter = YClient.get_channel_info(
                        channel_id=YTchannel.snippet.channelId,
                    )
                    C += 1
                    if C == 1:
                        SYem = discord.Embed(
                            title=f':mag: Search for "{" ".join(YTinput)}"',
                            description="\u200b",
                            color=0xFF0000,
                        )
                    if ChannelGetter.items[0].statistics.hiddenSubscriberCount == False:
                        SYem.add_field(
                            name="\u200b",
                            value=f"{C}. `{ChannelGetter.items[0].snippet.title} / Subs: {int(ChannelGetter.items[0].statistics.subscriberCount):,} / Videos: {int(ChannelGetter.items[0].statistics.videoCount):,}`",
                            inline=False,
                        )
                    else:
                        SYem.add_field(
                            name="\u200b",
                            value=f"{C}. `{ChannelGetter.items[0].snippet.title} / Videos: {int(ChannelGetter.items[0].statistics.videoCount):,}`",
                            inline=False,
                        )
                    SrchYT.append(ChannelGetter)
                if C == 0:
                    await ctx.message.channel.send("Nothing Found :woozy_face:")
                    return
                SYem.set_footer(
                    text='Choose a number to open Youtube Channel. "c" or "cancel" to exit search.\n\n*The Search closes automatically after 20sec of inactivity.*'
                )
                YTSent = await ctx.message.channel.send(embed=SYem)
                try:
                    ResS = await self.DClient.wait_for(
                        "message", check=ChCHanS, timeout=20
                    )
                    LResS = ResS.content.lower()
                    try:
                        if int(ResS.content) <= 10:
                            YTchoice = SrchYT[int(ResS.content) - 1]
                            YTid = YTchoice.items[0].id
                            if (
                                YTchoice.items[0].statistics.hiddenSubscriberCount
                                == False
                            ):
                                await YTSent.edit(
                                    embed=discord.Embed(
                                        title=":calling: Finding...",
                                        description=f"{YTchoice.items[0].snippet.title} / Subs: {int(YTchoice.items[0].statistics.subscriberCount):,} / Videos: {int(YTchoice.items[0].statistics.videoCount):,}",
                                        color=0xFF0000,
                                    )
                                )
                            else:
                                await YTSent.edit(
                                    embed=discord.Embed(
                                        title=":calling: Finding...",
                                        description=f"{YTchoice.items[0].snippet.title} / Videos: {int(YTchoice.items[0].statistics.videoCount):,}",
                                        color=0xFF0000,
                                    )
                                )
                    except ValueError:
                        if (LResS == "cancel") or (LResS == "c"):
                            await YTSent.edit(
                                embed=discord.Embed(
                                    title=":x: Search Cancelled",
                                    description="\u200b",
                                    color=0xFF0000,
                                )
                            )
                            return
                except asyncio.TimeoutError:
                    await YTSent.edit(
                        embed=discord.Embed(
                            title=":hourglass: Search Timeout...",
                            description="\u200b",
                            color=0xFF0000,
                        )
                    )
                    return
            else:
                await ctx.message.channel.send("No search argument :woozy_face:")
                return

        elif args:
            YTname = " ".join(args)
            IDorName = "NAME"
        else:
            await ctx.message.channel.send("No Arguments :no_mouth:")
            return

        if IDorName == "NAME":
            try:
                YTtempID = (
                    YClient.search(q=" ".join(YTinput), count=1, search_type="channel")
                    .items[0]
                    .snippet.channelId
                )
                YTinfo = YClient.get_channel_info(channel_id=YTtempID)
                YTVids = YClient.get_activities_by_channel(
                    channel_id=YTtempID, count=20
                )
            except IndexError:
                await ctx.message.channel.send("Nothing Found :woozy_face:")
                return
        elif IDorName == "ID":
            YTinfo = YClient.get_channel_info(channel_id=YTid)
            YTVids = YClient.get_activities_by_channel(channel_id=YTid, count=20)

        YTdesc = YTinfo.items[0].snippet.description
        if len(YTdesc) > 253:
            YTcDesc = YTdesc[0:253]
            YTcDesc = YTcDesc + "..."
        else:
            YTcDesc = YTdesc

        YEm = discord.Embed(
            title=YTinfo.items[0].snippet.title,
            description=YTcDesc,
            url=f"https://www.youtube.com/channel/{YTinfo.items[0].id}",
            color=0xFF0000,
        )
        YEm.add_field(
            name="Created on:",
            value=YTinfo.items[0].snippet.publishedAt[0:10],
            inline=False,
        )
        if YTinfo.items[0].statistics.hiddenSubscriberCount == False:
            YEm.add_field(
                name="Subscribers:",
                value=f"{int(YTinfo.items[0].statistics.subscriberCount):,}",
                inline=False,
            )
        YEm.add_field(
            name="Videos:",
            value=f"{int(YTinfo.items[0].statistics.videoCount):,}",
            inline=True,
        )
        YEm.add_field(name="\u200b", value="\u200b", inline=True)
        YEm.add_field(
            name="Total Views:",
            value=f"{int(YTinfo.items[0].statistics.viewCount):,}",
            inline=True,
        )
        YEm.set_thumbnail(url=YTinfo.items[0].snippet.thumbnails.high.url)
        YTEm = await ctx.message.channel.send(embed=YEm)
        Vidnum = 0
        OnChannel = True
        await YTEm.add_reaction("⬅️")
        await YTEm.add_reaction("❌")
        await YTEm.add_reaction("➡️")
        await YTEm.add_reaction("#️⃣")
        while True:
            try:
                ReaEm = await self.DClient.wait_for(
                    "reaction_add", check=ChCHEm, timeout=120
                )
                await YTEm.remove_reaction(ReaEm[0].emoji, ReaEm[1])
                if ReaEm[0].emoji == "⬅️" and VidNum == 0:
                    OnChannel = True
                    await YTEm.edit(embed=YEm)
                elif ReaEm[0].emoji == "⬅️" and VidNum > 0:
                    VidNum -= 1
                    await YTEm.edit(
                        embed=EmbedMaker(
                            YTVids.items[VidNum].contentDetails.upload.videoId,
                            YTinfo.items[0],
                            VidNum,
                            len(YTVids.items),
                        )
                    )

                elif ReaEm[0].emoji == "➡️" and OnChannel:
                    OnChannel = False
                    VidNum = 0
                    await YTEm.edit(
                        embed=EmbedMaker(
                            YTVids.items[VidNum].contentDetails.upload.videoId,
                            YTinfo.items[0],
                            VidNum,
                            len(YTVids.items),
                        )
                    )
                elif (
                    ReaEm[0].emoji == "➡️"
                    and len(YTVids.items) > VidNum + 1
                    and VidNum >= 0
                ):
                    VidNum += 1
                    await YTEm.edit(
                        embed=EmbedMaker(
                            YTVids.items[VidNum].contentDetails.upload.videoId,
                            YTinfo.items[0],
                            VidNum,
                            len(YTVids.items),
                        )
                    )
                elif ReaEm[0].emoji == "#️⃣":
                    if await ChVoteUser(ReaEm[1].id):
                        TempYT = await ctx.message.channel.send(
                            'Choose a number to open navigate to page. "c" or "cancel" to exit navigation.'
                        )
                        try:
                            ResE = await self.DClient.wait_for(
                                "message", check=ChCHEmFN, timeout=10
                            )
                            await ResE.delete()
                            await TempYT.delete()
                            try:
                                try:
                                    pG = int(ResE.content)
                                    if 0 < pG <= len(YTVids.items) - 1:
                                        VidNum = pG - 1
                                    elif pG < 1:
                                        VidNum = 0
                                        pass
                                    else:
                                        VidNum = len(YTVids.items) - 1
                                except TypeError:
                                    pass
                            except ValueError:
                                pass
                            await YTEm.edit(
                                embed=EmbedMaker(
                                    YTVids.items[VidNum].contentDetails.upload.videoId,
                                    YTinfo.items[0],
                                    VidNum,
                                    len(YTVids.items),
                                )
                            )
                        except asyncio.TimeoutError:
                            await TempYT.edit("Request Timeout")
                            await asyncio.sleep(5)
                            await TempYT.delete()
                    else:
                        await ctx.message.channel.send(embed=ErrorEmbeds("Vote"))
                elif ReaEm[0].emoji == "➡️" and len(YTVids.items) == VidNum + 1:
                    await YTEm.remove_reaction("⬅️", self.DClient.user)
                    await YTEm.remove_reaction("❌", self.DClient.user)
                    await YTEm.remove_reaction("➡️", self.DClient.user)
                    await YTEm.remove_reaction("#️⃣", self.DClient.user)
                    break
                elif ReaEm[0].emoji == "❌":
                    await YTEm.remove_reaction("⬅️", self.DClient.user)
                    await YTEm.remove_reaction("❌", self.DClient.user)
                    await YTEm.remove_reaction("➡️", self.DClient.user)
                    await YTEm.remove_reaction("#️⃣", self.DClient.user)
                    break
            except asyncio.TimeoutError:
                await YTEm.remove_reaction("⬅️", self.DClient.user)
                await YTEm.remove_reaction("❌", self.DClient.user)
                await YTEm.remove_reaction("➡️", self.DClient.user)
                await YTEm.remove_reaction("#️⃣", self.DClient.user)
                break


def setup(DClient):
    DClient.add_cog(Youtube(DClient))