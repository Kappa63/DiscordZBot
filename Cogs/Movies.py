import discord
from discord.ext import commands
from Setup import IMClient, SendWait
import asyncio
from CBot import DClient as CBotDClient

class Movies(commands.Cog):
    def __init__(self, DClient:CBotDClient) -> None:
        self.DClient = DClient

    @commands.command(name="imdb", description="Search and Find Info About Your Favourite Movies.")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def MovieGetter(self, ctx:commands.Context, *args) -> None:
        def ChCHanS(MSg) -> bool:
            MesS = MSg.content.lower()
            RsT = False
            try:
                if int(MSg.content) <= 10: RsT = True
            except ValueError:
                if (MesS == "cancel") or (MesS == "c"): RsT = True
            return MSg.guild.id == ctx.guild.id and MSg.channel.id == ctx.channel.id and RsT

        if not args: await SendWait(ctx, "No Arguments :no_mouth:"); return
        
        await SendWait(ctx, ":tv: Getting Movie/Show...")
        MVinput = list(args)
        if MVinput[0].lower() == "search" and args:
            IDorName = "ID"
            MVinput.pop(0)
            if not MVinput: await SendWait(ctx, "No search argument :woozy_face:"); return
            C = 0
            SrchIMDb = []
            for Movie in IMClient.search_movie(" ".join(MVinput), results=10):
                C += 1
                if C == 1: SYem = discord.Embed(title=f':mag: Search for "{" ".join(MVinput)}"', description="\u200b", color=0xDBA506)
                Md = ""
                if "kind" in Movie.data: Mk = Movie.data["kind"]
                My = ""
                if "year" in Movie.data: My = Movie.data["year"]
                SYem.add_field(name="\u200b", value=f'{C}. `{Movie.data["title"]} ({Mk}) ({My})`', inline=False)
                SrchIMDb.append(Movie)
            if not C: await SendWait(ctx, "Nothing Found :woozy_face:"); return
            SYem.set_footer(text='Choose a number to check Movie or Series. "c" or "cancel" to exit search.\n\n*The Search closes automatically after 20sec of inactivity.*')
            IMDbSent = await ctx.send(embed=SYem)
            try:
                ResS = await self.DClient.wait_for("message", check=ChCHanS, timeout=20)
                LResS = ResS.content.lower()
                try:
                    if int(ResS.content) <= 10:
                        IMDbChoice = SrchIMDb[int(ResS.content) - 1]
                        IMDbID = IMDbChoice.movieID
                        Md = ""
                        if "kind" in IMDbChoice.data: Mk = IMDbChoice.data["kind"]
                        My = ""
                        if "year" in IMDbChoice.data: My = IMDbChoice.data["year"]
                        await IMDbSent.edit(embed=discord.Embed(title=":calling: Finding...", 
                                                                description=f'{IMDbChoice.data["title"]} ({Mk}) ({My})',
                                                                color=0xDBA506))
                except ValueError:
                    if (LResS == "cancel") or (LResS == "c"):
                        await IMDbSent.edit(embed=discord.Embed(title=":x: Search Cancelled", description="\u200b", color=0xDBA506))
                        return
            except asyncio.TimeoutError:
                await IMDbSent.edit(embed=discord.Embed(title=":hourglass: Search Timeout...", description="\u200b", color=0xDBA506))
                return
        elif args:
            MVname = " ".join(args)
            IDorName = "NAME"

        if IDorName == "NAME":
            try:
                IMDbtempID = IMClient.search_movie(MVname, results=1)[0].movieID
                IMDbinfo = IMClient.get_movie(IMDbtempID).data
            except IndexError: await SendWait(ctx, "Nothing Found :woozy_face:"); return
        elif IDorName == "ID": IMDbinfo = IMClient.get_movie(IMDbID).data

        PlotF = None
        if "plot outline" in IMDbinfo: PlotF = IMDbinfo["plot outline"][:100]

        YEm = discord.Embed(title=IMDbinfo["original title"], description=", ".join(IMDbinfo["genres"]), url=f'https://www.imdb.com/title/tt{IMDbinfo["imdbID"]}', 
                            color=0xDBA506)
        if PlotF: YEm.add_field(name="Plot:", value=PlotF + "\n", inline=False)
        if "original air date" in IMDbinfo: YEm.add_field(name="Original Air Date:", value=IMDbinfo["original air date"], inline=False)
        if "box office" in IMDbinfo:
            Box = ""
            if "Budget" in IMDbinfo["box office"]: Box += f'Budget: {IMDbinfo["box office"]["Budget"].split(" ")[0]}'
            if "Opening Weekend United States" in IMDbinfo["box office"]: Box += f'\nOpening Week: {IMDbinfo["box office"]["Opening Weekend United States"].split(" ")[0]}'
            if "Cumulative Worldwide Gross" in IMDbinfo["box office"]: Box += f'\nTotal Gross: {IMDbinfo["box office"]["Cumulative Worldwide Gross"].split(" ")[0]}'
            if Box: YEm.add_field(name="Box Office:", value=Box, inline=True)
        if "number of seasons" in IMDbinfo: YEm.add_field(name="Seasons:", value=IMDbinfo["number of seasons"], inline=True)
        if "rating" in IMDbinfo: YEm.add_field(name="Rating:", value=IMDbinfo["rating"], inline=True)
        if "cast" in IMDbinfo:
            Cast = [Member["name"] for Member in IMDbinfo["cast"][:10]]
            Note = "\n**And more...**" if len(IMDbinfo["cast"]) > 10 else ""
            YEm.add_field(name="Cast:", value="\n".join(Cast[:10]) + Note, inline=False)
        if "cover url" in IMDbinfo: YEm.set_thumbnail(url=IMDbinfo["cover url"])
        await ctx.send(embed=YEm)

    async def cog_load(self) -> None:
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self) -> None:
        print(f"{self.__class__.__name__} unloaded!")

async def setup(DClient:CBotDClient) -> None:
    await DClient.add_cog(Movies(DClient))