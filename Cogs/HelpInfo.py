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
            name="zhelp (Category): ",
            value="Provides help for the category",
            inline=False,
        )
        HEm.add_field(
            name="Categories: ",
            value="**`-Social(s)`**\n**`-Anime/Manga/Doujin/Hentai`**\n**`-Rule34`**\n**`-Image`**\n**`-Joke`**\n**`-Quotes/Advice/Insult`**\n**`-Info/Informatics`**\n**`-IMDb`**\n**`-Games`**\n**`-Server/Counting`**\n**`-Misc/Miscellaneous`**\n**`-Navigation/Nav`**",
            inline=False,
        )
        HEm.add_field(
            name="Links: ",
            value="[Official Server](https://discord.gg/V6E6prUBPv) / [Patreon](https://www.patreon.com/join/ZBotDiscord) / [Vote](https://top.gg/bot/768397640140062721/vote)",
        )
        await ctx.message.channel.send(embed=HEm)

    @SendH.command(aliases=["server", "counting", "tracking", "count", "track"])
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
            name="zadd [word]: ", value="Adds a word/phrase to keep track of", inline=False
        )
        HEm.add_field(
            name="zremove [word]: ",
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
            text="Note that counting is limited to 10 per Message to reduce spam incentives"
        )
        await ctx.message.channel.send(embed=HEm)

    @SendH.command(aliases=["social", "socials", "reddit", "twitter", "youtube", "multireddit", "multireddits", "redditor"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendR(self, ctx):
        HEm = discord.Embed(
            title="**ZBot Social(s) Help**", description="\u200b", color=0x0AF531
        )
        HEm.add_field(
            name="zreddit [Subreddit Name]: ",
            value="Returns a RANDOM post from the top 100 posts in hot from any subreddit",
            inline=False,
        )
        HEm.add_field(
            name="zreddit surf [Subreddit Name]: ",
            value="100 Posts of The Subreddit Sorted in Any Format (Voters and Patreons ONLY)",
            inline=False,
        )
        HEm.add_field(
            name="zredditor [Redditor name]: ",
            value="View a redditor's profile and 100 of their latest posts",
            inline=False,
        )
        HEm.add_field(
            name="zmultireddit [Multireddit Name]: ",
            value="Opens the multireddit and allows you to scroll through its subreddits all together (For Tier 2 patreons or more)",
            inline=False,
        )
        HEm.add_field(
            name="zmultireddit list: ",
            value="List all the Multireddits you created along with the Subreddits in them (For Tier 2 patreons or more)",
            inline=False,
        )
        HEm.add_field(
            name="zmultireddit create [Desired Multireddit Name]: ",
            value="Creates a new Multireddit with the desired name (For Tier 2 patreons or more)",
            inline=False,
        )
        HEm.add_field(
            name="zmultireddit delete [Multireddit name]: ",
            value="Deletes a created Multireddit (For Tier 2 patreons or more)",
            inline=False,
        )
        HEm.add_field(
            name="zmultireddit add [Multireddit name] [Subreddit name]: ",
            value="Adds a Subreddit to your multireddit (For Tier 2 patreons or more)",
            inline=False,
        )
        HEm.add_field(
            name="zmultireddit remove [Multireddit name] [Subreddit name]: ",
            value="Removes a subreddit from your Multireddit (For Tier 2 patreons or more)",
            inline=False,
        )
        HEm.add_field(
            name="ztwitter (User @): ",
            value="Details About the User Profile and 20 of Their Latest Tweets",
            inline=False,
        )
        HEm.add_field(
            name="ztwitter search (Search Term): ",
            value="Searches for 10 Users Related to Search Term",
            inline=False,
        )
        HEm.add_field(
            name="ztwitter trending: ",
            value="Shows whats currently trending (USA)",
            inline=False,
        )
        HEm.add_field(
            name="zyoutube (Channel Name): ",
            value="Details About the Channel and 20 of The Latest Uploads",
            inline=False,
        )
        HEm.add_field(
            name="zyoutube search (Search Term): ",
            value="Searches for 10 Channels Related to Search Term",
            inline=False,
        )
        HEm.add_field(
            name="Aliases:", value="**-Youtube =** `youtube, yt`", inline=False
        )
        await ctx.message.channel.send(embed=HEm)

    @SendH.command(aliases=["game", "games", "sudoku", "ttt", "tictactoe", "chess", "cptd"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendG(self, ctx):
        HEm = discord.Embed(
            title="**ZBot Game Help**", description="\u200b", color=0x0AF531
        )
        HEm.add_field(
            name="zsudoku [easy/medium/hard/random]: ",
            value="Returns a sudoku puzzle with the given difficulty",
            inline=False,
        )
        HEm.add_field(
            name="zttt [mention]: ",
            value="Starts a Tic-Tac-Toe game vs the mentioned user",
            inline=False,
        )
        HEm.add_field(
            name="zchess [mention]: ",
            value="Starts a Chess game vs the mentioned user",
            inline=False,
        )
        HEm.add_field(
            name="zcptddaily: ",
            value="Returns when the next CPTD Daily will happen",
            inline=False,
        )
        HEm.add_field(
            name="zcptddaily start: ",
            value="Start receiving daily CPTDs in the current channel (Tier 2 or more Patreons ONLY)",
            inline=False,
        )
        HEm.add_field(
            name="zcptddaily end/stop: ",
            value="Stop receiving daily CPTDs (Tier 2 or more Patreons ONLY)",
            inline=False,
        )
        HEm.add_field(
            name="Note:",
            value="-In sudoku react with the eye to get the solution or with the X to never get the solution. If X isn't pressed solution is auto given after 1 hour\n\n-In TTT each player has 30sec to play. A player should enter the number of the corresponding square to play there. If a player enters 'end' the game ends\n\n-In Chess a standard 10min time is given to each player. Time starts after each player has made 1 move. Every turn the legal moves are listed. Typing in a move is case sensetive (Must be as listed). Typing in 'resign' will result in loss by resignation. Draws automatically happen if Stalemate or Insufficient Material. A Draw can be Claimed by Typing in 'claimdraw' (Only after a threefold-repition or 50 move-rule). The bot announces if a Draw Claim is allowed. Win by Checkmate.",
            inline=False,
        )
        await ctx.message.channel.send(embed=HEm)

    @SendH.command(
        aliases=[
            "covid",
            "info",
            "informatics",
            "informatic",
            "information",
            "nasa",
            "apod",
            "facts",
            "fact",
        ]
    )
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendC(self, ctx):
        HEm = discord.Embed(
            title="**ZBot Informatics Help**", description="\u200b", color=0x0AF531
        )
        HEm.add_field(
            name="zcovid: ",
            value="Worldwide status of Covid-19",
            inline=False,
        )
        HEm.add_field(
            name="zcovid [Country]: ",
            value="Status of Covid-19 in country",
            inline=False,
        )
        HEm.add_field(name="zfact: ", value="Random fun fact", inline=False)
        HEm.add_field(
            name="zapod: ",
            value="Astronomy Picture of the Day (Voters and Patreons ONLY)",
            inline=False,
        )
        HEm.add_field(
            name="zapoddaily: ",
            value="Returns when the next APOD Daily will happen",
            inline=False,
        )
        HEm.add_field(
            name="zapoddaily start: ",
            value="Start receiving daily APODs in the current channel (Tier 2 or more Patreons ONLY)",
            inline=False,
        )
        HEm.add_field(
            name="zapoddaily end/stop: ",
            value="Stop receiving daily APODs (Tier 2 or more Patreons ONLY)",
            inline=False,
        )
        HEm.add_field(
            name="znasa: ",
            value="25 RANDOM mars images out of the 100s taken by NASA's Curiosity rover (Different each roll)",
            inline=False,
        )
        HEm.add_field(
            name="Notes",
            value="**-Covid:** Recovered data seemed to be off in some countries, therefore the recovered data is innacurate most of the time.",
            inline=False,
        )
        await ctx.message.channel.send(embed=HEm)

    @SendH.command(aliases=["imdb", "shows", "show", "movie", "movies"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendIM(self, ctx):
        HEm = discord.Embed(
            title="**ZBot IMDb Help**", description="\u200b", color=0x0AF531
        )
        HEm.add_field(
            name="zimdb [Movie/Series]: ",
            value="Returns info about the Movie/Series",
            inline=False,
        )
        HEm.add_field(
            name="zimdb search [Search Argument]: ",
            value="Searches for 10 Movies/Series related to search argument",
            inline=False,
        )
        await ctx.message.channel.send(embed=HEm)

    @SendH.command(name="rule34")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendT(self, ctx):
        HEm = discord.Embed(
            title="**ZBot Rule34 Help**", description="\u200b", color=0x0AF531
        )
        HEm.add_field(
            name="zrule34 [Search Term]: ",
            value="Returns a RANDOM rule34 image (NSFW)",
            inline=False,
        )
        HEm.add_field(
            name="zrule34 surf [Search Term]: ",
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
            name="zanime [Anime Name]: ",
            value="Searches for anime and returns all the info about chosen one",
            inline=False,
        )
        HEm.add_field(
            name="zmanga [Manga Name]: ",
            value="Searches for manga and returns all the info about chosen one",
            inline=False,
        )
        HEm.add_field(
            name="zhentai [Magic Numbers]: ",
            value="Gets doujin from nhentai using magic numbers (NSFW)",
            inline=False,
        )
        HEm.add_field(
            name="zhentai random: ",
            value="Gets a random doujin from nhentai (NSFW)",
            inline=False,
        )
        HEm.add_field(
            name="zhentai search [Doujin Name]: ",
            value="Searches for the 10 most popular doujin (NSFW)",
            inline=False,
        )
        HEm.add_field(
            name="Notes: ",
            value="**-Hentai: **Some hentai are not available. This is to abide by the discord TOS.",
            inline=False,
        )
        await ctx.message.channel.send(embed=HEm)

    @SendH.command(aliases=["image", "images", "fry", "qr"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendI(self, ctx):
        HEm = discord.Embed(
            title="**ZBot Image Help**", description="\u200b", color=0x0AF531
        )
        HEm.add_field(name="zcat: ", value="Cat Pics", inline=False)
        HEm.add_field(name="zdog: ", value="Dog Pics", inline=False)
        HEm.add_field(name="zfox: ", value="Fox Pics", inline=False)
        HEm.add_field(name="zfood: ", value="Food Pics", inline=False)
        HEm.add_field(name="ztpde: ", value="This Person Doesn't Exist. An AI generated person that did not and probably will never exist", inline=False)
        HEm.add_field(
            name="zfry [Image Attachment/Image Url]: ",
            value="Deep fries the image",
            inline=False,
        )
        HEm.add_field(
            name="zfry profile (@): ", value="Deep fries the avatar", inline=False
        )
        HEm.add_field(
            name="zgiphy [Search argument]: ",
            value="Returns a RANDOM gif from top 50 results on giphy",
            inline=False,
        )
        HEm.add_field(
            name="zqr [Text]: ",
            value="Makes a qrcode of the Text",
            inline=False,
        )
        HEm.add_field(
            name="zpdf [PDF Attachment/PDF Url]: ",
            value="Views the PDF's first 40 pages as images",
            inline=False,
        )
        HEm.add_field(
            name="Aliases:",
            value="**-Cat =** `cat, kitten, kitty`\n\n**-Dog =** `doggo, dog, pupper, puppy`\n\n**-Food =** `food, dishes, dish`\n\n**-QR =** `qrcode, qr`",
        )
        await ctx.message.channel.send(embed=HEm)

    @SendH.command(aliases=["joke", "jokes"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendJ(self, ctx):
        HEm = discord.Embed(
            title="**ZBot Joke Help**", description="\u200b", color=0x0AF531
        )
        HEm.add_field(name="zdadjoke: ", value="Dad Jokes", inline=False)
        HEm.add_field(
            name="zjoke: ", value="Jokes (No sensetive material)", inline=False
        )
        HEm.add_field(
            name="zdarkjoke: ",
            value="Darker Jokes (Might contain sensetive material, at own descretion)",
            inline=False,
        )
        HEm.add_field(name="zpun: ", value="Puns.", inline=False)
        await ctx.message.channel.send(embed=HEm)

    @SendH.command(
        aliases=[
            "quotes",
            "quote",
            "insult",
            "insults",
            "advice",
            "kanye",
            "taylor",
            "taylorswift",
            "qotd",
        ]
    )
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendQ(self, ctx):
        HEm = discord.Embed(
            title="**ZBot Quotes/Advice/Insult Help**",
            description="\u200b",
            color=0x0AF531,
        )
        HEm.add_field(
            name="zadvice: ",
            value="Good old advice",
            inline=False,
        )
        HEm.add_field(
            name="zkanye: ",
            value="Words by Kanye",
            inline=False,
        )
        HEm.add_field(
            name="ztaylor: ",
            value="Image and Quote of Taylor Swift",
            inline=False,
        )
        HEm.add_field(
            name="zqotd: ",
            value="Quote Of The Day (Voters and Patreons ONLY)",
            inline=False,
        )
        HEm.add_field(
            name="zqotddaily: ",
            value="Returns when the next QOTD Daily will happen (Tier 2 or more Patreons ONLY)",
            inline=False,
        )
        HEm.add_field(
            name="zqotddaily start: ",
            value="Start receiving daily QOTDs in the current channel (Tier 2 or more Patreons ONLY)",
            inline=False,
        )
        HEm.add_field(
            name="zqotddaily end/stop: ",
            value="Stop receiving daily QOTDs (Tier 2 or more Patreons ONLY)",
            inline=False,
        )
        HEm.add_field(name="zinsult: ", value="Returns an insult", inline=False)
        HEm.add_field(
            name="Aliases:",
            value="**-Kanye =** `kanye, kanyewest`\n\n**-Taylor =** `taylor, taylorswift`",
        )
        await ctx.message.channel.send(embed=HEm)

    @SendH.command(aliases=["misc", "misc.", "miscellaneous"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendM(self, ctx):
        HEm = discord.Embed(
            title="**ZBot Misc. Help**", description="\u200b", color=0x0AF531
        )
        HEm.add_field(
            name="zremind [Arguments]: ",
            value='Pings you after time is over. Arguments are a number followed by d, h, m, or s for days, hours, minutes, seconds respectively.(Ex. "zremind 2d 3h 52m 14s" is a remind after 2days 3hours 52minutes and 14seconds)',
            inline=False,
        )
        HEm.add_field(
            name="zcalc [Input]: ", value="Calculates and returns", inline=False
        )
        HEm.add_field(
            name="zcolor: ",
            value="Returns a RANDOM color with its HEX and RGB color codes",
            inline=False,
        )
        HEm.add_field(name="zroll: ", value="Rolls a dice", inline=False)
        HEm.add_field(
            name="Notes:",
            value="**-zremind:** is limited to 1day max. Could occasionally fail to notify you due to the bot going down, so dont rely on it entirely.",
            inline=False,
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
        VEm.add_field(name="Version: ", value="2.1a", inline=False)
        VEm.add_field(name="Version Release: ", value="12/1/2021", inline=False)
        VEm.add_field(name="Initial Release: ", value="21/11/2020", inline=False)
        await ctx.message.channel.send(embed=VEm)

    @commands.command(name="log")
    async def UpdLog(self, ctx):
        LogUps = open("UpdateLog.txt")
        LOggLin = LogUps.readlines()
        LogUps.close()
        LEm = discord.Embed(title=LOggLin[0], color=0x1F002A)
        LOggLin.pop(0)
        for Logs in LOggLin:
            LogTem = Logs.split(" ")
            LEm.add_field(name=LogTem[0], value=" ".join(LogTem[1:]), inline=False)
        LEm.set_footer(
            text="Make sure to report any bugs you pass by on the official server. Check zbug"
        )
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
            name="*-Using instant navigation to page/image/post/tweet*\n*-Surfing Reddit and using all sorting formats*\n*-Surfing Rule34*\n*-Using zapod (Astronomy Picture of the Day)*\n*-Using zqotd (Quote of the Day)*\n",
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
            description="**Want to support ZBot's development?\n\nI currently have no idea what kind of perks should be added (I clearly need more). Suggestions are welcome on the official support server (zsupport)**",
            color=0x000000,
        )
        SEm.add_field(
            name="**-Tier 1:** `All voting perks without having to vote`\n\n**-Tier 2 (Super):** `Previous tier's perks`, `Setting up apoddaily, qotddaily, and cptddaily in 1 channel each`, `Making 1 Multireddit`\n\n**-Tier 3 (Legend):** `Previous tiers' perks`, `Setting up apoddaily, qotddaily, and cptddaily in 2 channels each`, `Making 2 Multireddits`\n\n**-Tier 4 (Ultimate):** `Previous tiers' perks`, `Setting up apoddaily, qotddaily, and cptddaily in 4 channels each`, `Making 4 Multireddits`",
            value="\u200b",
            inline=False,
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