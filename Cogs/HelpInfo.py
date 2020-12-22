import discord
from discord.ext import commands


class HelpInfo(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.group(name="help", invoke_without_command=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendH(self, ctx):
        HEm = discord.Embed(title="**ZBot Help**", description="\u200b", color=0x0AF531)
        HEm.add_field(
            name="zversion: ",
            value="Checks the current running version of ZBot",
            inline=False,
        )
        HEm.add_field(
            name="zlog: ", value="Shows the latest update's update log", inline=False
        )
        HEm.add_field(
            name="zhelp server: ",
            value="Provides all the server commands (including word track commands)",
            inline=False,
        )
        HEm.add_field(name="zhelp reddit: ", value="The Reddit Commands", inline=False)
        HEm.add_field(
            name="zhelp twitter: ", value="The Twitter Commands", inline=False
        )
        HEm.add_field(name="zhelp anime: ", value="The Anime Commands", inline=False)
        HEm.add_field(name="zhelp images: ", value="The Image Commands", inline=False)
        HEm.add_field(name="zhelp jokes: ", value="The Joke Commands", inline=False)
        HEm.add_field(name="zhelp covid: ", value="The Covid-19 Commands", inline=False)
        HEm.add_field(name="zhelp imdb: ", value="The IMDb Commands", inline=False)
        HEm.add_field(
            name="zhelp youtube: ", value="The YouTube Commands", inline=False
        )
        HEm.add_field(
            name="zhelp misc: ", value="The Miscellaneous Commands", inline=False
        )
        HEm.add_field(name="zhelp nav: ", value="How to Navigate", inline=False)
        HEm.add_field(name="zhelp rule34: ", value="The Rule34 Commands", inline=False)
        HEm.add_field(
            name="Links: ",
            value="[Official Server](https://discord.gg/V6E6prUBPv) / [Patreon](https://www.patreon.com/join/ZBotDiscord) / [Vote](https://top.gg/bot/768397640140062721/vote)",
        )
        await ctx.message.channel.send(embed=HEm)

    @SendH.command(name="server")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendS(self, ctx):
        HEm = discord.Embed(
            title="**ZBot Server Help**", description="\u200b", color=0x0AF531
        )
        HEm.add_field(
            name="zsetup: ",
            value="Sets up the bot for the first time for counting/tracking",
            inline=False,
        )
        HEm.add_field(
            name="zupdate: ",
            value="This is used to add members that join when the bot is down.",
            inline=False,
        )
        HEm.add_field(
            name="zadd: ", value="Adds a word/phrase to keep track of", inline=False
        )
        HEm.add_field(
            name="zremove: ",
            value="Removes an existing word/phrase being tracked",
            inline=False,
        )
        HEm.add_field(
            name="zlist: ", value="Returns all added words/phrases", inline=False
        )
        HEm.add_field(
            name="zstats (@) (Word): ",
            value="Returns stats for word(s)/phrase(s)",
            inline=False,
        )
        HEm.add_field(
            name="ztotal (Word): ",
            value="Returns the total number of times word(s)/phrase(s) have been said on server",
            inline=False,
        )
        HEm.add_field(
            name="ztop (Word): ",
            value="Returns the top 3 number of times word(s)/phrase(s) have been said on server",
            inline=False,
        )
        HEm.add_field(
            name="zreset: ",
            value="Reset everything, AKA remove ALL info(this is irreversable)",
            inline=False,
        )
        HEm.set_footer(
            text="Note: Counting is limited to 10 per Message to reduce spam incentives"
        )
        await ctx.message.channel.send(embed=HEm)

    @SendH.command(name="reddit")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendR(self, ctx):
        HEm = discord.Embed(
            title="**ZBot Reddit Help**", description="\u200b", color=0x0AF531
        )
        HEm.add_field(
            name="zreddit (Subreddit Name): ",
            value="Returns a RANDOM post from the top 100 posts in hot from any subreddit",
            inline=False,
        )
        HEm.add_field(
            name="zreddit surf (Subreddit Name): ",
            value="Returns the 100 posts of a subreddit sorted in any format (Voters and Patreons ONLY)",
            inline=False,
        )
        await ctx.message.channel.send(embed=HEm)

    @SendH.command(name="covid")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendC(self, ctx):
        HEm = discord.Embed(
            title="**ZBot Covid-19 Help**", description="\u200b", color=0x0AF531
        )
        HEm.add_field(
            name="zcovid: ",
            value="Returns the worldwide status of Covid-19",
            inline=False,
        )
        HEm.add_field(
            name="zcovid (Country): ",
            value="Returns the status of Covid-19 in country",
            inline=False,
        )
        await ctx.message.channel.send(embed=HEm)

    @SendH.command(name="twitter")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendT(self, ctx):
        HEm = discord.Embed(
            title="**ZBot Twitter Help**", description="\u200b", color=0x0AF531
        )
        HEm.add_field(
            name="ztwitter (User @): ",
            value="Returns the user profile and 20 of their latest tweets",
            inline=False,
        )
        HEm.add_field(
            name="ztwitter search (Username): ",
            value="Searches for 10 users related to search argument",
            inline=False,
        )
        await ctx.message.channel.send(embed=HEm)

    @SendH.command(name="imdb")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendIM(self, ctx):
        HEm = discord.Embed(
            title="**ZBot IMDb Help**", description="\u200b", color=0x0AF531
        )
        HEm.add_field(
            name="zimdb (Movie/Series): ",
            value="Returns info about the Movie/Series",
            inline=False,
        )
        HEm.add_field(
            name="zimdb search (Search Argument): ",
            value="Searches for 10 Movies/Series related to search argument",
            inline=False,
        )
        await ctx.message.channel.send(embed=HEm)

    @SendH.command(aliases=["youtube", "yt"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendY(self, ctx):
        HEm = discord.Embed(
            title="**ZBot YouTube Help**", description="\u200b", color=0x0AF531
        )
        HEm.add_field(
            name="zyoutube (Channel Name): ",
            value="Returns info about the channel and 20 of the latest uploads",
            inline=False,
        )
        HEm.add_field(
            name="zyoutube search (Search Term): ",
            value="Searches for 10 channels related to search argument",
            inline=False,
        )
        HEm.set_footer(text='Aliases: "youtube" / "yt"')
        await ctx.message.channel.send(embed=HEm)

    @SendH.command(name="rule34")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendT(self, ctx):
        HEm = discord.Embed(
            title="**ZBot Rule34 Help**", description="\u200b", color=0x0AF531
        )
        HEm.add_field(
            name="zrule34 (Search Term): ",
            value="Returns a RANDOM rule34 image (NSFW)",
            inline=False,
        )
        HEm.add_field(
            name="zrule34 surf (Search Term): ",
            value="Returns 100 rule34 images from a random page (Voters and Patreons ONLY) (NSFW)",
            inline=False,
        )
        await ctx.message.channel.send(embed=HEm)

    @SendH.command(aliases=["anime", "manga", "hentai", "doujin"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendA(self, ctx):
        HEm = discord.Embed(
            title="**ZBot Anime Help**", description="\u200b", color=0x0AF531
        )
        HEm.add_field(
            name="zanime (Anime Name): ",
            value="Searches for anime and returns all the info about chosen one",
            inline=False,
        )
        HEm.add_field(
            name="zmanga (Manga Name): ",
            value="Searches for manga and returns all the info about chosen one",
            inline=False,
        )
        HEm.add_field(
            name="zhentai (Magic Numbers): ",
            value="Gets doujin from nhentai using magic numbers (NSFW)",
            inline=False,
        )
        HEm.add_field(
            name="zhentai random: ",
            value="Gets a random doujin from nhentai (NSFW)",
            inline=False,
        )
        HEm.add_field(
            name="zhentai search (Doujin Name): ",
            value="Searches for the 10 most popular doujin (NSFW)",
            inline=False,
        )
        await ctx.message.channel.send(embed=HEm)

    @SendH.command(aliases = ["image", "images"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendI(self, ctx):
        HEm = discord.Embed(
            title="**ZBot Image Help**", description="\u200b", color=0x0AF531
        )
        HEm.add_field(name="zcat: ", value="Cat Pics", inline=False)
        HEm.add_field(name="zdog: ", value="Dog Pics", inline=False)
        HEm.add_field(name="zfox: ", value="Fox Pics", inline=False)
        HEm.add_field(name="zfood: ", value="Food Pics", inline=False)
        HEm.set_footer(text='Aliases: -"cat" / "kitten" / "kitty"\n-"doggo" / "dog" / "pupper" / "puppy"\n-"food" / "dishes" / "dish"')
        await ctx.message.channel.send(embed=HEm)

    @SendH.command(aliases = ["joke", "jokes"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendJ(self, ctx):
        HEm = discord.Embed(
            title="**ZBot Joke Help**", description="\u200b", color=0x0AF531
        )
        HEm.add_field(
            name="zdadjoke: ", value="Dad Jokes", inline=False
        )
        HEm.add_field(
            name="zjoke: ", value="Jokes (No sensetive material)", inline=False
        )
        HEm.add_field(
            name="zdarkjoke: ", value="Darker Jokes (Might contain sensetive material, at own descretion)", inline=False
        )
        HEm.add_field(
            name="zpun: ", value="Puns.", inline=False
        )
        await ctx.message.channel.send(embed=HEm)

    @SendH.command(aliases=["misc", "misc.", "miscellaneous"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendM(self, ctx):
        HEm = discord.Embed(
            title="**ZBot Misc. Help**", description="\u200b", color=0x0AF531
        )
        HEm.add_field(
            name="zremind (Arguments): ",
            value='Pings you after time is over. Arguments are a number followed by d, h, m, or s for days, hours, minutes, seconds respectively.(Ex. "zremind 2d 3h 52m 14s" is a remind after 2days 3hours 52minutes and 14seconds)',
            inline=False,
        )
        HEm.add_field(
            name="zfry (Image Attachment/Image Url): ",
            value="Deep fries the image",
            inline=False,
        )
        HEm.add_field(
            name="zadvice: ",
            value="Good old advice",
            inline=False,
        )
        HEm.add_field(
            name="zfry profile (@): ", value="Deep fries the avatar", inline=False
        )
        HEm.add_field(
            name="zpdf (PDF Attachment/PDF Url): ",
            value="Views the PDF's first 40 pages",
            inline=False,
        )
        HEm.add_field(
            name="zcalc (Input): ", value="Calculates and returns", inline=False
        )
        HEm.add_field(
            name="zcolor: ",
            value="Returns a RANDOM color with its HEX and RGB color codes",
            inline=False,
        )
        HEm.add_field(name="zinsult: ", value="Returns an insult", inline=False)
        HEm.add_field(name="zfact: ", value="Returns a random fun fact", inline=False)
        HEm.add_field(
            name="zkanye: ",
            value="Words by Kanye",
            inline=False,
        )
        HEm.add_field(
            name="zqotd: ",
            value="Quote Of The Day (Voters and Patreons ONLY)",
            inline=False,
        )
        HEm.add_field(
            name="zapod: ",
            value="Astronomy Picture of the Day (Voters and Patreons ONLY)",
            inline=False,
        )
        HEm.add_field(
            name="znasa: ",
            value="25 RANDOM mars images out of the 100s taken by NASA's Curiosity rover",
            inline=False,
        )
        HEm.add_field(name="zroll: ", value="Rolls a dice", inline=False)
        HEm.add_field(
            name="zgiphy (Phrase/Word to search for): ",
            value="Returns a RANDOM gif from top 50 results on giphy",
            inline=False,
        )
        HEm.set_footer(
            text="Notes: -zremind is limited to 1day max.\n-zremind could sometimes fail to notify you due to the bot going down. So dont rely on it entirely.\n-During testing recovered data from zcovid was extremely inaccurate.\n-Some hentai are not available. This is to abide by the discord TOS."
        )
        await ctx.message.channel.send(embed=HEm)

    @SendH.command(aliases=["nav", "navigation"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendN(self, ctx):
        HEm = discord.Embed(
            title="**ZBot Navigation Help**", description="\u200b", color=0x0AF531
        )
        HEm.add_field(
            name="Right Arrow (-->): ", value="Flips to the next image", inline=False
        )
        HEm.add_field(
            name="Left Arrow (<--): ", value="Flip to the previous image", inline=False
        )
        HEm.add_field(
            name="Red X: ",
            value="Exits the embed. (No longer navigateable)",
            inline=False,
        )
        HEm.add_field(
            name="Hashtag (#): ",
            value='After you click it you can input a number of an image to instantly go to it. You can type "c" or "cancel" to cancel(Only for voters/patreon)',
            inline=False,
        )
        HEm.add_field(
            name="\nNotes: ",
            value="-In instant navigation you have 10sec to make an input before its automatically cancelled.\n-Navigateables close automatically after 2mins of not using them.",
        )
        await ctx.message.channel.send(embed=HEm)

    @commands.command(aliases=["ver", "version"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RetVer(self, ctx):
        VEm = discord.Embed(
            title="Active Version",
            description="ZBot build version and info",
            color=0x3695BA,
        )
        VEm.add_field(name="Dev: ", value="Kappa#5173", inline=False)
        VEm.add_field(name="Version: ", value="1.6a", inline=False)
        VEm.add_field(name="Version Release: ", value="22/12/2020", inline=False)
        VEm.add_field(name="Initial Release: ", value="21/11/2020", inline=False)
        await ctx.message.channel.send(embed=VEm)

    @commands.command(name="log")
    async def UpdLog(self, ctx):
        LogUps = open("UpdateLog.txt")
        LOggLin = LogUps.read().splitlines()
        LEm = discord.Embed(title=LOggLin[0], color=0x1F002A)
        LOggLin.pop(0)
        for Logs in LOggLin:
            LogTem = Logs.split(" ")
            LEm.add_field(name=LogTem[0], value=" ".join(LogTem[1:]), inline=False)
        LEm.set_footer(text = "Make sure to report any bugs you pass by on the official server. Check zbug")
        await ctx.message.channel.send(embed=LEm)

    @commands.command(name="vote")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def BotVotF(self, ctx):
        SEm = discord.Embed(
            title="Vote For ZBot",
            url="https://top.gg/bot/768397640140062721/vote",
            description="**You can vote once every 12 hours for the following perks**",
            color=0x000000,
        )
        SEm.add_field(
            name="*-Using instant navigation to page/image/post/tweet*\n*-Surfing Reddit and using all sorting formats*\n*-Surfing Rule34*\n*-Using zapod (Astronomy Picture of the Day)*\n\n",
            value="\u200b",
            inline=False,
        )
        await ctx.message.channel.send(embed=SEm)

    @commands.command(name="patreon")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def BotPatrF(self, ctx):
        SEm = discord.Embed(
            title="Join Patreon",
            url="https://www.patreon.com/join/ZBotDiscord",
            description="**Want to support ZBot's development?**",
            color=0x000000,
        )
        await ctx.message.channel.send(embed=SEm)

    @commands.command(aliases=["support", "bug", "bugs"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SupportServer(self, ctx):
        SEm = discord.Embed(
            title="ZBot Official Server",
            url="https://discord.gg/V6E6prUBPv",
            description="**Report Bugs, Get Support, and Join the Community**",
            color=0x000000,
        )
        await ctx.message.channel.send(embed=SEm)


def setup(DClient):
    DClient.add_cog(HelpInfo(DClient))