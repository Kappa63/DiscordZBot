import discord
from discord.ext import commands
import mal
from hentai import Utils, Sort, Hentai, Format
from Setup import MClient, ErrorEmbeds, Navigator, ChVote, ChVoteUser, ChNSFW, SendWait
import asyncio

def EmbedMaker(DentAi, Tags, Page):
    DEmE = discord.Embed(title=DentAi.title(Format.Pretty), description=Tags, url=DentAi.url, color=0x000000)
    DEmE.set_thumbnail(url=DentAi.image_urls[0])
    DEmE.set_footer(text=f"Released on {DentAi.upload_date}\n\nNeed help navigating? zhelp navigation")
    DEmE.set_image(url=DentAi.image_urls[Page])
    DEmE.add_field(name="Doujin ID", value=DentAi.id, inline=False)
    DEmE.add_field(name="\u200b", value=f"`Page: {(Page+1)}/{len(DentAi.image_urls)}`", inline=False)
    return DEmE


class AnimeManga(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.command(name="manga")
    @commands.cooldown(1, 3, commands.BucketType.guild)
    async def MangaInfo(self, ctx, *args):
        def ChCHanS(MSg):
            MesS = MSg.content.lower()
            RsT = False
            try:
                if int(MSg.content) <= 10: RsT = True
            except ValueError:
                if MesS in ["cancel", "c"]: RsT = True
            return MSg.guild.id == ctx.guild.id and MSg.channel.id == ctx.channel.id and RsT

        if not args: await SendWait(ctx, "No Arguments :no_mouth:"); return
        try:
            MangaInput = " ".join(args)
            C = 0
            SrchManga = []
            MnSrS = await ctx.message.channel.send(embed=discord.Embed(title=":mag: Searching...", description="\u200b", color=0x3695BA))
            SAEm = discord.Embed(title=f":mag: Results for '{MangaInput}'", description="\u200b", color=0x3695BA)
            for MangaResult in mal.MangaSearch(MangaInput).results:
                C += 1
                SAEm.add_field(name="\u200b", value=f"{C}. `{MangaResult.title}` **({MangaResult.type})**", inline=False)
                SrchManga.append(MangaResult)
                if C == 10: break
            SAEm.set_footer(text='Choose a number to view MAL entry. "c" or "cancel" to exit search.\n\n*The Search closes automatically after 20sec of inactivity.*')
            await MnSrS.edit(embed=SAEm)
            try:
                ResS = await self.DClient.wait_for("message", check=ChCHanS, timeout=20)
                LResS = ResS.content.lower()
                try:
                    if int(ResS.content) <= 10:
                        MangaID = SrchManga[int(ResS.content) - 1].mal_id
                        await MnSrS.edit(embed=discord.Embed(title=":calling: Finding...", description=f"{SrchManga[int(ResS.content)-1].title} **({SrchManga[int(ResS.content)-1].type})**", color=0x3695BA))
                except ValueError:
                    if LResS in ["cancel", "c"]: await MnSrS.edit(embed=discord.Embed(title=":x: Search Cancelled", description="\u200b", color=0x3695BA))
            except asyncio.TimeoutError: await MnSrS.edit(embed=discord.Embed(title=":hourglass: Search Timeout...", description="\u200b", color=0x3695BA))
        except UnboundLocalError:
            SAEm = discord.Embed(title=f':mag: Search for "{MangaInput}"', description="\u200b", color=0x3695BA)
            SAEm.add_field(name="\u200b", value="No Results found :woozy_face:", inline=False)
            await MnSrS.edit(embed=SAEm)

        try:
            MangaGet = MClient.get_manga_details(MangaID)
            MangaGetmal = mal.Manga(MangaID)
            MangaGenres = []
            for Genre in MangaGet.genres: MangaGenres.append(Genre.name)
            AEm = discord.Embed(title=f"{MangaGet.title} / {MangaGet.alternative_titles.ja} **({MangaGetmal.type})**", description=f'{", ".join(MangaGenres)}\n[Mal Page]({MangaGetmal.url})', color=0x3695BA)
            AEm.set_thumbnail(url=MangaGet.main_picture.large)

            MangaSynopsis = MangaGet.synopsis[:1021]

            AEm.add_field(name=f'By: {", ".join(MangaGetmal.authors)}', value="\u200b", inline=False)
            AEm.add_field(name="Synopsis:", value=MangaSynopsis, inline=False)
            if hasattr(MangaGet, "start_date"): AEm.add_field(name="Start Airing on:", value=MangaGet.start_date, inline=True)
            if hasattr(MangaGet, "end_date"): AEm.add_field(name="Finish Airing on:", value=MangaGet.end_date, inline=True)
            AEm.add_field(name="Status:", value=MangaGetmal.status, inline=True)
            AEm.add_field(name="Score:", value=MangaGetmal.score, inline=True)
            AEm.add_field(name="Rank:", value=MangaGetmal.rank, inline=True)
            AEm.add_field(name="Popularity:", value=MangaGetmal.popularity, inline=True)
            AEm.add_field(name="No# Volumes:", value=MangaGetmal.volumes, inline=True)
            AEm.add_field(name="No# Chapters:", value=MangaGetmal.chapters, inline=True)
            MangaAdaptation = []
            MangaAlternate = []
            MangaSummary = []
            MangaSequel = []
            MangaSide = []
            MangaSpin = []
            for TMagAdp in MangaGet.related_manga:
                if TMagAdp.relation_type_formatted == "Adaptation": MangaAdaptation.append(TMagAdp.node.title)
                elif TMagAdp.relation_type_formatted == "Summary": MangaSummary.append(TMagAdp.node.title)
                elif TMagAdp.relation_type_formatted == "Sequel": MangaSequel.append(TMagAdp.node.title)
                elif TMagAdp.relation_type_formatted == "Spin-off": MangaSpin.append(TMagAdp.node.title)
                elif TMagAdp.relation_type_formatted == "Alternative version": MangaAlternate.append(TMagAdp.node.title)
                elif TMagAdp.relation_type_formatted == "Side story": MangaSide.append(TMagAdp.node.title)

            MangaSequelC = "\n".join(MangaSequel)[:950]
            MangaAdaptationC = "\n".join(MangaAdaptation)[:950]
            MangaSummaryC = "\n".join(MangaSummary)[:950]
            MangaAlternateC = "\n".join(MangaAlternate)[:950]
            MangaSpinC = "\n".join(MangaSpin)[:950]
            MangaSideC = "\n".join(MangaSide)[:950]

            if MangaSequelC or MangaAlternateC or MangaAdaptationC or MangaSideC or MangaSummaryC or MangaSpinC: AEm.add_field(name="\u200b", value="\u200b", inline=False)
            if MangaSequelC: AEm.add_field(name="Sequel:", value=MangaSequelC, inline=False)
            if MangaAlternateC: AEm.add_field(name="Alternate Version:", value=MangaAlternateC, inline=False)
            if MangaAdaptationC: AEm.add_field(name="Adaptation:", value=MangaAdaptationC, inline=False)
            if MangaSideC: AEm.add_field(name="Side Story:", value=MangaSideC, inline=False)
            if MangaSummaryC: AEm.add_field(name="Summary:", value=MangaSummaryC, inline=False)
            if MangaSpinC: AEm.add_field(name="Spin Off:", value=MangaSpinC, inline=False)
            await ctx.message.channel.send(embed=AEm)
        except UnboundLocalError: pass   

    @commands.command(name="anime")
    @commands.cooldown(1, 3, commands.BucketType.guild)
    async def AnimeInfo(self, ctx, *args):
        def ChCHanS(MSg):
            MesS = MSg.content.lower()
            RsT = False
            try:
                if int(MSg.content) <= 10: RsT = True
            except ValueError:
                if MesS in ["cancel", "c"]: RsT = True
            return MSg.guild.id == ctx.guild.id and MSg.channel.id == ctx.channel.id and RsT

        if not args: await SendWait(ctx, "No Arguments :no_mouth:"); return
        try:
            AnimeInput = " ".join(args)
            C = 0
            SrchAnime = []
            AnSrS = await ctx.message.channel.send(embed=discord.Embed(title=":mag: Searching...", description="\u200b", color=0x3FC0FF))
            SAEm = discord.Embed(title=f':mag: Results for "{AnimeInput}"', description="\u200b", color=0x3FC0FF)
            for AnimeResult in mal.AnimeSearch(AnimeInput).results:
                C += 1
                SAEm.add_field(name="\u200b", value=f"{C}. `{AnimeResult.title}` **({AnimeResult.type})**", inline=False)
                SrchAnime.append(AnimeResult)
                if C == 10: break
            SAEm.set_footer(text='Choose a number to view MAL entry. "c" or "cancel" to exit search.\n\n*The Search closes automatically after 20sec of inactivity.*')
            await AnSrS.edit(embed=SAEm)
            try:
                ResS = await self.DClient.wait_for("message", check=ChCHanS, timeout=20)
                LResS = ResS.content.lower()
                try:
                    if int(ResS.content) <= 10:
                        AnimeID = SrchAnime[int(ResS.content) - 1].mal_id
                        await AnSrS.edit(embed=discord.Embed(title=":calling: Finding...", description=f"{SrchAnime[int(ResS.content)-1].title} **({SrchAnime[int(ResS.content)-1].type})**", color=0x3FC0FF))
                except ValueError:
                    if LResS in ["cancel", "c"]: await AnSrS.edit(embed=discord.Embed(title=":x: Search Cancelled", description="\u200b", color=0x3FC0FF))
            except asyncio.TimeoutError: await AnSrS.edit(embed=discord.Embed(title=":hourglass: Search Timeout...", description="\u200b", color=0x3FC0FF))
        except UnboundLocalError:
            SAEm = discord.Embed(title=f':mag: Search for "{AnimeInput}"', description="\u200b", color=0x3FC0FF)
            SAEm.add_field(name="\u200b", value="No Results found :woozy_face:", inline=False)
            await AnSrS.edit(embed=SAEm)
        
        try:
            AnimeGet = MClient.get_anime_details(AnimeID)
            AnimeGetmal = mal.Anime(AnimeID)
            AnimeGenres = []
            for Genre in AnimeGet.genres: AnimeGenres.append(Genre.name)
            AEm = discord.Embed(title=f"{AnimeGet.title} / {AnimeGet.alternative_titles.ja} **({AnimeGetmal.type})**", description=f'{", ".join(AnimeGenres)}\n[Mal Page]({AnimeGetmal.url})', color=0x3FC0FF)
            AEm.set_thumbnail(url=AnimeGet.main_picture.large)
            AnimeSynopsis = AnimeGet.synopsis[:1021]

            AEm.add_field(name=f'Studios: {", ".join(AnimeGetmal.studios)}', value="\u200b", inline=False)
            AEm.add_field(name="Synopsis:", value=AnimeSynopsis, inline=False)
            if hasattr(AnimeGet, "start_date"): AEm.add_field(name="Start Airing on:", value=AnimeGet.start_date, inline=True)
            if hasattr(AnimeGet, "end_date"): AEm.add_field(name="Finish Airing on:", value=AnimeGet.end_date, inline=True)
            AEm.add_field(name="Status:", value=AnimeGetmal.status, inline=True)
            AEm.add_field(name="Rating:", value=AnimeGetmal.rating, inline=False)
            AEm.add_field(name="Score:", value=AnimeGetmal.score, inline=True)
            AEm.add_field(name="Rank:", value=AnimeGetmal.rank, inline=True)
            AEm.add_field(name="Popularity:", value=AnimeGetmal.popularity, inline=True)
            AEm.add_field(name="No# Episodes:", value=AnimeGetmal.episodes, inline=True)
            AEm.add_field(name="Episode Duration:", value=AnimeGetmal.duration, inline=True)
            AnimeAdaptation = []
            AnimeAlternate = []
            AnimeSummary = []
            AnimeSequel = []
            AnimeSide = []
            AnimeSpin = []
            for TAniAdp in AnimeGet.related_anime:
                if TAniAdp.relation_type_formatted == "Adaptation": AnimeAdaptation.append(TAniAdp.node.title)
                elif TAniAdp.relation_type_formatted == "Summary": AnimeSummary.append(TAniAdp.node.title)
                elif TAniAdp.relation_type_formatted == "Sequel": AnimeSequel.append(TAniAdp.node.title)
                elif TAniAdp.relation_type_formatted == "Spin-off": AnimeSpin.append(TAniAdp.node.title)
                elif TAniAdp.relation_type_formatted == "Alternative version": AnimeAlternate.append(TAniAdp.node.title)
                elif TAniAdp.relation_type_formatted == "Side story": AnimeSide.append(TAniAdp.node.title)

            AnimeSequelC = "\n".join(AnimeSequel)[:950]
            AnimeAdaptationC = "\n".join(AnimeAdaptation)[:950]
            AnimeSummaryC = "\n".join(AnimeSummary)[:950]
            AnimeAlternateC = "\n".join(AnimeAlternate)[:950]
            AnimeSpinC = "\n".join(AnimeSpin)[:950]
            AnimeSideC = "\n".join(AnimeSide)[:950]

            if AnimeSequelC or AnimeAlternateC or AnimeAdaptationC or AnimeSideC or AnimeSummaryC or AnimeSpinC: AEm.add_field(name="\u200b", value="\u200b", inline=False)
            if AnimeSequelC: AEm.add_field(name="Sequel:", value=AnimeSequelC, inline=False)
            if AnimeAlternateC: AEm.add_field(name="Alternate Version:", value=AnimeAlternateC, inline=False)
            if AnimeAdaptationC: AEm.add_field(name="Adaptation:", value=AnimeAdaptationC, inline=False)
            if AnimeSideC: AEm.add_field(name="Side Story:", value=AnimeSideC, inline=False)
            if AnimeSummaryC: AEm.add_field(name="Summary:", value=AnimeSummaryC, inline=False)
            if AnimeSpinC: AEm.add_field(name="Spin Off:", value=AnimeSpinC, inline=False)
            AEm.add_field(name="\u200b", value="\u200b", inline=False)
            try:
                AnimeOpening = "\n".join(AnimeGetmal.opening_themes)[:950]
                AEm.add_field( name="Opening Theme(s):", value=AnimeOpening, inline=False)
            except TypeError: pass

            try:
                AnimeEnding = ("\n".join(AnimeGetmal.ending_themes))[:950]
                AEm.add_field(name="Ending Theme(s):", value=AnimeEnding, inline=True)
            except TypeError: pass
            await ctx.message.channel.send(embed=AEm)
        except UnboundLocalError: pass
        
    @commands.command(name="hentai")
    @commands.check(ChNSFW)
    @commands.cooldown(1, 3, commands.BucketType.guild)
    async def nHentaiReader(self, ctx, *args):
        def ChCHanS(MSg):
            MesS = MSg.content.lower()
            MeseS = (MSg.content.lower()).split(" ")
            RsT = False
            try:
                if int(MSg.content) <= 10: RsT = True
            except ValueError:
                if MesS in ["cancel", "c", "zhentai"] or MeseS[0] == "zhentai": RsT = True
            return MSg.guild.id == ctx.guild.id and MSg.channel.id == ctx.channel.id and RsT

        if not args: await SendWait(ctx, "No Arguments :no_mouth:"); return
        Chlks = list(args)
        if Chlks[0].lower() == "search":
            Chlks.pop(0)
            C = 0
            SrchDen = []
            if not Chlks: await SendWait(ctx, "No search Argument :woozy_face:"); return
            try:
                if ctx.guild.id != 586940644153622550: Search = Utils.search_by_query(query=f'{" ".join(Chlks)} -tag:"lolicon" -tag:"shotacon"', sort=Sort.Popular)
                else: Search = Utils.search_by_query(query=" ".join(Chlks), sort=Sort.Popular)
                for DeOujin in Search:
                    C += 1
                    if C == 1:
                        SEm = discord.Embed(title=f':mag: Search for "{" ".join(Chlks)}"', description="\u200b", color=0x000000)
                    SEm.add_field(name="\u200b", value=f"{C}. `{DeOujin.title(Format.Pretty)}`", inline=False)
                    SrchDen.append(DeOujin)
                    if C == 10: break
                SEm.set_footer(text='Choose a number to open doujin. "c" or "cancel" to exit search. \n\n*The Search closes automatically after 20sec of inactivity.*')
                DmSent = await ctx.message.channel.send(embed=SEm)
                try:
                    ResS = await self.DClient.wait_for("message", check=ChCHanS, timeout=20)
                    LResS = ResS.content.lower()
                    ReseS = (ResS.content.lower()).split(" ")

                    try:
                        if int(ResS.content) <= 10:
                            Srch = SrchDen[int(ResS.content) - 1].id
                            DentAi = Hentai(Srch)
                            await DmSent.edit(embed=discord.Embed(title=":newspaper: Opening...", description=DentAi.title(Format.Pretty), color=0x000000))
                    except ValueError:
                        if LResS in ["cancel", "c", "zhentai"] or ReseS[0] == "zhentai": await DmSent.edit(embed=discord.Embed(title=":newspaper2: Search Cancelled", description="\u200b", color=0x000000))
                except asyncio.TimeoutError: await DmSent.edit(embed=discord.Embed(title=":hourglass: Search Timeout...", description="\u200b", color=0x000000))
            except UnboundLocalError:
                SEm = discord.Embed(title=f':mag: Search for "{" ".join(Chlks)}"', description="\u200b", color=0x000000)
                SEm.add_field(name="\u200b", value="No Results found :woozy_face:", inline=False)
                await ctx.message.channel.send(embed=SEm)
                
        else:
            try: Srch = int(" ".join(args))
            except ValueError:
                if " ".join(args).lower() == "random":
                    while True:
                        Srch = Utils.get_random_id()
                        DentAi = Hentai(Srch)
                        if (("lolicon" not in [tag.name for tag in DentAi.tag]) and ("shotacon" not in [tag.name for tag in DentAi.tag])) or ctx.guild.id == 586940644153622550: break
                else: await SendWait(ctx, "The argument contained non-numeral characters and wasn't a random request. :no_mouth:")
        try:
            if Hentai.exists(Srch):
                DentAi = Hentai(Srch)
                if (("lolicon" not in [tag.name for tag in DentAi.tag]) and ("shotacon" not in [tag.name for tag in DentAi.tag])) or ctx.guild.id == 586940644153622550:
                    Tags = (", ".join([tag.name for tag in DentAi.tag]))[:253]
                    HentaiPages = [EmbedMaker(DentAi, Tags, P) for P in range(len(DentAi.image_urls))]
                    await Navigator(ctx, HentaiPages)
                else: await SendWait(ctx, "In compliance with discord TOS, this is Unavailable. :upside_down: "); return
            else: await SendWait(ctx, "That Doujin doesn't exist :expressionless:")
        except UnboundLocalError: pass


def setup(DClient):
    DClient.add_cog(AnimeManga(DClient))