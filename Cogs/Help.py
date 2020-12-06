import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name = "help", invoke_without_command = True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendH(self, ctx):
        HEm = discord.Embed(title = "**ZBot Help**", description = "\u200b", color = 0x0af531)
        HEm.add_field(name = "zversion: ", value = "Checks the current running version of ZBot", inline = False)
        HEm.add_field(name = "zvote: ", value = "To vote for ZBot", inline = False)
        HEm.add_field(name = "zlog: ", value = "Shows the latest update's update log", inline = False)
        HEm.add_field(name = "zhelp server: ", value = "Provides all the server commands (including word track commands)", inline = False) 
        HEm.add_field(name = "zhelp reddit: ", value = "The Reddit Commands", inline = False)  
        HEm.add_field(name = "zhelp twitter: ", value = "The Twitter Commands", inline = False)   
        HEm.add_field(name = "zhelp anime: ", value = "The Anime Commands", inline = False)
        HEm.add_field(name = "zhelp covid: ", value = "The Covid-19 Commands", inline = False)   
        HEm.add_field(name = "zhelp misc: ", value = "The Miscellaneous Commands", inline = False)
        HEm.add_field(name = "Links: ", value = "[Official Server](https://discord.gg/V6E6prUBPv) / [Patreon](https://www.patreon.com/join/ZBotDiscord) / [Vote](https://top.gg/bot/768397640140062721/vote)")   
        await ctx.message.channel.send(embed = HEm)

    @SendH.command(name = "server")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendS(self, ctx):
        HEm = discord.Embed(title = "**ZBot Server Help**", description = "\u200b", color = 0x0af531)
        HEm.add_field(name = "zsetup: ", value = "Sets up the bot for the first time for counting/tracking", inline = False)
        HEm.add_field(name = "zupdate: ", value = "This is used to add members that join when the bot is down.", inline = False)
        HEm.add_field(name = "zadd: ", value = "Adds a word/phrase to keep track of", inline = False)
        HEm.add_field(name = "zremove: ", value = "Removes an existing word/phrase being tracked", inline = False)
        HEm.add_field(name = "zlist: ", value = "Returns all added words/phrases", inline = False)
        HEm.add_field(name = "zstats (@) (Word): ", value = "Returns stats for word(s)/phrase(s)", inline = False)
        HEm.add_field(name = "ztotal (Word): ", value = "Returns the total number of times word(s)/phrase(s) have been said on server", inline = False)
        HEm.add_field(name = "ztop (Word): ", value = "Returns the top 3 number of times word(s)/phrase(s) have been said on server", inline = False)
        HEm.add_field(name = "zreset: ", value = "Reset everything, AKA remove ALL info(this is irreversable)", inline = False)
        HEm.set_footer(text = "Note: Counting is limited to 10 per Message to reduce spam incentives")
        await ctx.message.channel.send(embed = HEm)

    @SendH.command(name = "reddit")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendR(self, ctx):
        HEm = discord.Embed(title = "**ZBot Reddit Help**", description = "\u200b", color = 0x0af531)
        HEm.add_field(name = "zreddit (Subreddit Name): ", value = "Returns a RANDOM post from the top 100 posts in hot from any subreddit", inline = False)
        HEm.add_field(name = "zreddit surf (Subreddit Name): ", value = "Returns the 100 posts of a subreddit sorted in any format (Voters and Patreons ONLY)", inline = False)
        await ctx.message.channel.send(embed = HEm)

    @SendH.command(name = "covid")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendC(self, ctx):
        HEm = discord.Embed(title = "**ZBot Covid-19 Help**", description = "\u200b", color = 0x0af531)
        HEm.add_field(name = "zcovid: ", value = "Returns the worldwide status of Covid-19", inline = False)
        HEm.add_field(name = "zcovid (Country): ", value = "Returns the status of Covid-19 in country", inline = False)
        await ctx.message.channel.send(embed = HEm)

    @SendH.command(name = "twitter")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendT(self, ctx):
        HEm = discord.Embed(title = "**ZBot Twitter Help**", description = "\u200b", color = 0x0af531)
        HEm.add_field(name = "ztwitter (User @): ", value = "Returns the user profile and 20 of their latest tweets", inline = False)
        HEm.add_field(name = "ztwitter search (Username): ", value = "Searches for 10 users related to search argument", inline = False)
        await ctx.message.channel.send(embed = HEm)

    @SendH.command(name = "anime")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendA(self, ctx):
        HEm = discord.Embed(title = "**ZBot Anime Help**", description = "\u200b", color = 0x0af531)
        HEm.add_field(name = "zanime (Anime Name): ", value = "Searches for anime and returns all the info about chosen one", inline = False)
        HEm.add_field(name = "zmanga (Manga Name): ", value = "Searches for manga and returns all the info about chosen one", inline = False)
        HEm.add_field(name = "zhentai (Magic Numbers): ", value = "Gets doujin from nhentai using magic numbers (NSFW)", inline = False)
        HEm.add_field(name = "zhentai random: ", value = "Gets a random doujin from nhentai (NSFW)", inline = False)
        HEm.add_field(name = "zhentai search (Doujin Name): ", value = "Searches for the 10 most popular doujin (NSFW)", inline = False)
        await ctx.message.channel.send(embed = HEm)

    @SendH.command(aliases = ["misc","misc.","miscellaneous"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SendM(self, ctx):
        HEm = discord.Embed(title = "**ZBot Misc. Help**", description = "\u200b", color = 0x0af531)
        HEm.add_field(name = "zremind (Arguments): ", value = 'Pings you after time is over. Arguments are a number followed by d, h, m, or s for days, hours, minutes, seconds respectively.(Ex. "zremind 2d 3h 52m 14s" is a remind after 2days 3hours 52minutes and 14seconds)', inline = False)
        HEm.add_field(name = "zfry (Image Attachment/Image Url): ", value = "Deep fries the image", inline = False)
        HEm.add_field(name = "zfry profile (@): ", value = "Deep fries the avatar", inline = False)
        HEm.add_field(name = "zpdf (PDF Attachment/PDF Url): ", value = "Views the PDF's first 40 pages", inline = False)
        HEm.add_field(name = "zcalc (Input): ", value = "Calculates and returns", inline = False)
        HEm.add_field(name = "zcolor: ", value = "Returns a RANDOM color with its HEX and RGB color codes", inline = False)
        HEm.add_field(name = "zfact: ", value = "Returns a random fun fact", inline = False)
        HEm.add_field(name = "zapod: ", value = "Astronomy Picture of the Day (Voters and Patreons ONLY)", inline = False)
        HEm.add_field(name = "znasa: ", value = "25 RANDOM mars images out of the 100s taken by NASA's Curiosity rover", inline = False)
        HEm.add_field(name = "zdadjoke: ", value = "Returns a random dad joke", inline = False)
        HEm.add_field(name = "zroll: ", value = "Rolls a dice", inline = False)
        HEm.add_field(name = "zgiphy (Phrase/Word to search for): ", value = "Returns a RANDOM gif from top 50 results on giphy", inline = False)
        HEm.set_footer(text = "Notes: -zremind is limited to 1day max.\n-zremind could sometimes fail to notify you due to the bot going down. So dont rely on it entirely.\n-During testing recovered data from zcovid was extremely inaccurate.\n-Some hentai are not available. This is to abide by the discord TOS.")
        await ctx.message.channel.send(embed = HEm)

def setup(bot):
    bot.add_cog(Help(bot))