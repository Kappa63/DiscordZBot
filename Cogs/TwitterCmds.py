import discord
from discord.ext import commands
import requests
import os 
import tweepy
from TestBot import Twitter
import asyncio

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

class TwitterCmds(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.command(name = "twitter")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def TwttMsSur(self, ctx, *args):
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
                    ResS = await self.DClient.wait_for('message', check = ChCHanS, timeout = 20)
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
                        ReaEm = await self.DClient.wait_for("reaction_add", check = ChCHEm, timeout = 20) 
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
                            if await ChVote(ctx):
                                TemTw = await ctx.message.channel.send('Choose a number to open navigate to page. "c" or "cancel" to exit navigation.\n\n*The Navigation closes automatically after 10sec of inactivity.*')
                                try:
                                    ResE = await self.DClient.wait_for("message", check = ChCHEmFN, timeout = 10)
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
                        elif ReaEm[0].emoji == "➡️" and len(TwExt) == TwTNum+1:
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
                await ctx.message.channel.send("Not Found :expressionless:")
        except UnboundLocalError:
            pass

def setup(DClient):
    DClient.add_cog(TwitterCmds(DClient))