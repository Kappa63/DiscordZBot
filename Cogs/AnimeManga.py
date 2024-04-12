import discord
from discord.ext import commands
# import mal
from discord import app_commands
from Customs.nHentai import Utils, Sort, Hentai, Format
# from Setup import MClient, ErrorEmbeds, Navigator, ChVote, ChVoteUser, ChNSFW, SendWait
from Setup import SendWait, MClient, MALsearch, RefreshMAL
from Customs.Navigators import ButtonNavigator as Navigator
from Customs.UI.Selector import SelectionView as Selector
import asyncio
from CBot import DClient as CBotDClient
import malclient

def EmbedMaker(DentAi, Tags, Page) -> discord.Embed:
    DEmE = discord.Embed(title=DentAi.title(Format.Pretty), description=Tags, url=DentAi.url, color=0x000000)
    DEmE.set_thumbnail(url=DentAi.image_urls[0])
    DEmE.set_footer(text=f"Released on {DentAi.upload_date}\n\nNeed help navigating? zhelp navigation")
    DEmE.set_image(url=DentAi.image_urls[Page])
    DEmE.add_field(name="Doujin ID", value=DentAi.id, inline=False)
    DEmE.add_field(name="\u200b", value=f"`Page: {(Page+1)}/{len(DentAi.image_urls)}`", inline=False)
    return DEmE


class AnimeManga(commands.Cog):
    def __init__(self, DClient:CBotDClient) -> None:
        self.DClient = DClient
    
    @app_commands.command(name="manga", description="Retrieves a Manga from MAL.")
    @app_commands.describe(manga="Manga Name")
    @app_commands.check(RefreshMAL)
    @app_commands.checks.cooldown(1, 3)
    async def MangaInfo(self, ctx:discord.Interaction, manga:str) -> None:
        async def exTimOt():
            await ctx.edit_original_response(embed=discord.Embed(title=":x: Search Timeout or Cancelled", color=0x3695BA), view=None)

        async def getSel(id):
            MangaF = SrchManga[int(id)-1]
            await ctx.edit_original_response(embed=discord.Embed(title=":calling: Finding...", description=f"{MangaF.title} **({MangaF.media_type.value})**", color=0x3695BA), view=None)
            MangaGet = MClient.get_manga_details(MangaF.id)
            # MangaGetmal = mal.Manga(MangaID)
            MangaGenres = []
            for Genre in MangaGet.genres: MangaGenres.append(Genre.name)
            altEn = MangaGet.alternative_titles.get("en")
            altJa = MangaGet.alternative_titles.get("ja")
            AEm = discord.Embed(title=f"{MangaGet.title}  /  {altEn if altEn else ''}  /  {altJa if altJa else ''} **({MangaGet.media_type.value})**", 
                                description=f'{", ".join(MangaGenres)}\n[Mal Page](https://myanimelist.net/manga/{MangaGet.id})', color=0x3695BA)
            AEm.set_thumbnail(url=MangaGet.main_picture.large)

            MangaSynopsis = MangaGet.synopsis[:1021]

            AEm.add_field(name=f'By: {", ".join([i.node.first_name+" "+i.node.last_name for i in MangaGet.authors])}', value="\u200b", inline=False)
            AEm.add_field(name="Synopsis:", value=MangaSynopsis, inline=False)
            if hasattr(MangaGet, "start_date"): AEm.add_field(name="Start Airing on:", value=MangaGet.start_date, inline=True)
            if hasattr(MangaGet, "end_date"): AEm.add_field(name="Finish Airing on:", value=MangaGet.end_date, inline=True)
            AEm.add_field(name="Status:", value=MangaGet.status.value, inline=True)
            AEm.add_field(name="Score:", value=MangaGet.mean, inline=True)
            AEm.add_field(name="Rank:", value=MangaGet.rank, inline=True)
            AEm.add_field(name="Popularity:", value=MangaGet.popularity, inline=True)
            AEm.add_field(name="No# Volumes:", value=MangaGet.num_volumes, inline=True)
            AEm.add_field(name="No# Chapters:", value=MangaGet.num_chapters, inline=True)
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
            await ctx.edit_original_response(embed=AEm)
        
        if not manga: await SendWait(ctx, "No Arguments :no_mouth:"); return
        # try:
        MangaInput = manga
        C = 0
        SrchManga = []
        await ctx.response.send_message(embed=discord.Embed(title=":mag: Searching...", color=0x3695BA))
        SAEm = discord.Embed(title=f":mag: Results for '{MangaInput}'", color=0x3695BA)
        for MangaResult in MClient.search_manga(MangaInput, limit=10, fields=MALsearch):
            C += 1
            SAEm.add_field(name="\u200b", value=f"{C}. `{MangaResult.title}` **({MangaResult.media_type.value})**", inline=False)
            SrchManga.append(MangaResult)
        SAEm.set_footer(text='Choose a number to view MAL entry. "c" or "cancel" to exit search.\n\n*The Search closes automatically after 20sec of inactivity.*')
        await ctx.edit_original_response(embed=SAEm, view=Selector(getSel, exTimOt, list(range(1, C+1))))
            # try:
            #     ResS = await self.DClient.wait_for("message", check=ChCHanS, timeout=20)
            #     LResS = ResS.content.lower()
            #     try:
            #         if int(ResS.content) <= 10:
            #             MangaID = SrchManga[int(ResS.content) - 1].id
                        
            #     except ValueError:
            #         if LResS in ["cancel", "c"]: await MnSrS.edit_message()
            # except asyncio.TimeoutError: await MnSrS.edit_message(embed=discord.Embed(title=":hourglass: Search Timeout...", color=0x3695BA))
        # except (UnboundLocalError, ValueError) as e:
        #     SAEm = discord.Embed(title=f':mag: Search for "{MangaInput}"', description="\u200b", color=0x3695BA)
        #     SAEm.add_field(name="\u200b", value="No Results found :woozy_face:", inline=False)
        #     await ctx.edit_original_response(embed=SAEm)
        #     return

        # try:
        
        # except UnboundLocalError: pass   

    @app_commands.command(name="anime", description="Retrieves a Anime from MAL.")
    @app_commands.describe(anime="Anime Name")
    @app_commands.check(RefreshMAL)
    @app_commands.checks.cooldown(1, 3)
    async def AnimeInfo(self, ctx:discord.Interaction, anime:str) -> None:
        async def exTimOt():
            await ctx.edit_original_response(embed=discord.Embed(title=":x: Search Timeout or Cancelled", color=0x3695BA), view=None)

        async def getSel(id):
            AnimeF = SrchAnime[int(id)-1]
            await ctx.edit_original_response(embed=discord.Embed(title=":calling: Finding...", 
                                                            description=f"{AnimeF.title}", color=0x3FC0FF), view=None)
            AnimeGet = MClient.get_anime_details(AnimeF.id)
            # print(AnimeGet.dict().keys())
            # AnimeGetmal = mal.Anime(AnimeID)
            AnimeGenres = []
            for Genre in AnimeGet.genres: AnimeGenres.append(Genre.name)
            altEn = AnimeGet.alternative_titles.get("en")
            altJa = AnimeGet.alternative_titles.get("ja")
            AEm = discord.Embed(title=f"{AnimeGet.title}  /  {altEn if altEn else ''}  /  {altJa if altJa else ''} **({AnimeGet.media_type.value})**", 
                                description=f'{", ".join(AnimeGenres)}\n[Mal Page](https://myanimelist.net/anime/{AnimeGet.id})', color=0x3FC0FF)
            AEm.set_thumbnail(url=AnimeGet.main_picture.large)
            AnimeSynopsis = AnimeGet.synopsis[:1021]
            # print("d")
            AEm.add_field(name=f'Studios: {", ".join([i.name for i in AnimeGet.studios])}', value="\u200b", inline=False)
            AEm.add_field(name="Synopsis:", value=AnimeSynopsis, inline=False)
            if hasattr(AnimeGet, "start_date"): AEm.add_field(name="Start Airing on:", value=AnimeGet.start_date, inline=True)
            if hasattr(AnimeGet, "end_date"): AEm.add_field(name="Finish Airing on:", value=AnimeGet.end_date, inline=True)
            AEm.add_field(name="Status:", value=AnimeGet.status, inline=True)
            AEm.add_field(name="Rating:", value=AnimeGet.rating, inline=False)
            AEm.add_field(name="Score:", value=AnimeGet.mean, inline=True)
            AEm.add_field(name="Rank:", value=AnimeGet.rank, inline=True)
            AEm.add_field(name="Popularity:", value=AnimeGet.popularity, inline=True)
            AEm.add_field(name="No# Episodes:", value=AnimeGet.num_episodes, inline=True)
            AEm.add_field(name="Episode Duration:", value=int(AnimeGet.average_episode_duration/60), inline=True)
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
            # AEm.add_field(name="\u200b", value="\u200b", inline=False)
            # try:
            #     AnimeOpening = "\n".join(AnimeGetmal.opening_themes)[:950]
            #     AEm.add_field( name="Opening Theme(s):", value=AnimeOpening, inline=False)
            # except TypeError: pass

            # try:
            #     AnimeEnding = ("\n".join(AnimeGetmal.ending_themes))[:950]
            #     AEm.add_field(name="Ending Theme(s):", value=AnimeEnding, inline=True)
            # except TypeError: pass
            await ctx.edit_original_response(embed=AEm)


        if not anime: await SendWait(ctx, "No Arguments :no_mouth:"); return
        # try:
        AnimeInput = anime
        C = 0
        SrchAnime = []
        await ctx.response.send_message(embed=discord.Embed(title=":mag: Searching...", color=0x3FC0FF))
        SAEm = discord.Embed(title=f':mag: Results for "{AnimeInput}"', color=0x3FC0FF)
        for AnimeResult in MClient.search_anime(AnimeInput, limit=10):
            C += 1
            SAEm.add_field(name="\u200b", value=f"{C}. `{AnimeResult.title}`", inline=False)#**({AnimeResult.id})**
            SrchAnime.append(AnimeResult)
        SAEm.set_footer(text='Choose a number to view MAL entry. "c" or "cancel" to exit search.\n\n*The Search closes automatically after 20sec of inactivity.*')
        await ctx.edit_original_response(embed=SAEm, view=Selector(getSel, exTimOt, list(range(1, C+1))))
        # try:
        #     ResS = await self.DClient.wait_for("message", check=ChCHanS, timeout=20)
        #     LResS = ResS.content.lower()
        #     try:
        #         if int(ResS.content) <= 10:
        #             AnimeID = SrchAnime[int(ResS.content) - 1].id
                    # await ctx.edit_original_response(embed=discord.Embed(title=":calling: Finding...", 
                    #                                         description=f"{SrchAnime[int(ResS.content)-1].title}", color=0x3FC0FF)) #**({SrchAnime[int(ResS.content)-1].id})**
        #     except ValueError:
        #         if LResS in ["cancel", "c"]: await ctx.edit_original_response(embed=discord.Embed(title=":x: Search Cancelled", color=0x3FC0FF))
        # except asyncio.TimeoutError: await ctx.edit_original_response(embed=discord.Embed(title=":hourglass: Search Timeout...", color=0x3FC0FF))
        # except (UnboundLocalError, ValueError) as e:
        #     SAEm = discord.Embed(title=f':mag: Search for "{AnimeInput}"', description="\u200b", color=0x3FC0FF)
        #     SAEm.add_field(name="\u200b", value="No Results found :woozy_face:", inline=False)
        #     await AnSrS.edit(embed=SAEm)
        #     return
        
        # try:
        
        # except UnboundLocalError: 
        #     pass
        
    # @commands.command(name="hentai", description="nHentai \"Manga\" (Cause THATS what You're Looking for).")
    # @commands.cooldown(1, 3, commands.BucketType.guild)
    # async def nHentaiReader(self, ctx:commands.Context, *args) -> None:
    #     def ChCHanS(MSg) -> bool:
    #         MesS = MSg.content.lower()
    #         MeseS = (MSg.content.lower()).split(" ")
    #         RsT = False
    #         try:
    #             if int(MSg.content) <= 10: RsT = True
    #         except ValueError:
    #             if MesS in ["cancel", "c", "zhentai"] or MeseS[0] == "zhentai": RsT = True
    #         return MSg.guild.id == ctx.guild.id and MSg.channel.id == ctx.channel.id and RsT

    #     if not args: await SendWait(ctx, "No Arguments :no_mouth:"); return
    #     Chlks = list(args)
    #     if Chlks[0].lower() == "search":
    #         Chlks.pop(0)
    #         C = 0
    #         SrchDen = []
    #         if not Chlks: await SendWait(ctx, "No search Argument :woozy_face:"); return
    #         try:
    #             if ctx.guild.id != 586940644153622550: Search = Utils.search_by_query(query=f'{" ".join(Chlks)} -tag:"lolicon" -tag:"shotacon"', sort=Sort.Popular)
    #             else: Search = Utils.search_by_query(query=" ".join(Chlks), sort=Sort.Popular)
    #             for DeOujin in Search:
    #                 C += 1
    #                 if C == 1:
    #                     SEm = discord.Embed(title=f':mag: Search for "{" ".join(Chlks)}"', description="\u200b", color=0x000000)
    #                 SEm.add_field(name="\u200b", value=f"{C}. `{DeOujin.title(Format.Pretty)}`", inline=False)
    #                 SrchDen.append(DeOujin)
    #                 if C == 10: break
    #             SEm.set_footer(text='Choose a number to open doujin. "c" or "cancel" to exit search. \n\n*The Search closes automatically after 20sec of inactivity.*')
    #             DmSent = await ctx.response.send_message(embed=SEm)
    #             try:
    #                 ResS = await self.DClient.wait_for("message", check=ChCHanS, timeout=20)
    #                 LResS = ResS.content.lower()
    #                 ReseS = (ResS.content.lower()).split(" ")

    #                 try:
    #                     if int(ResS.content) <= 10:
    #                         Srch = SrchDen[int(ResS.content) - 1].id
    #                         DentAi = Hentai(Srch)
    #                         await DmSent.edit(embed=discord.Embed(title=":newspaper: Opening...", description=DentAi.title(Format.Pretty), color=0x000000))
    #                 except ValueError:
    #                     if LResS in ["cancel", "c", "zhentai"] or ReseS[0] == "zhentai": await DmSent.edit(embed=discord.Embed(title=":newspaper2: Search Cancelled", 
    #                                                                                                                            color=0x000000))
    #             except asyncio.TimeoutError: await DmSent.edit(embed=discord.Embed(title=":hourglass: Search Timeout...", color=0x000000))
    #         except UnboundLocalError:
    #             SEm = discord.Embed(title=f':mag: Search for "{" ".join(Chlks)}"', description="\u200b", color=0x000000)
    #             SEm.add_field(name="\u200b", value="No Results found :woozy_face:", inline=False)
    #             await ctx.response.send_message(embed=SEm)
                
    #     else:
    #         try: Srch = int(" ".join(args))
    #         except ValueError:
    #             if " ".join(args).lower() == "random":
    #                 while True:
    #                     Srch = Utils.get_random_id()
    #                     DentAi = Hentai(Srch)
    #                     if (("lolicon" not in [tag.name for tag in DentAi.tag]) and ("shotacon" not in [tag.name for tag in DentAi.tag])) or ctx.guild.id == 586940644153622550: break
    #             else: await SendWait(ctx, "The argument contained non-numeral characters and wasn't a random request. :no_mouth:")
    #     try:
    #         if Hentai.exists(Srch)or Srch == 455417:
    #             DentAi = Hentai(Srch)
    #             if (("lolicon" not in [tag.name for tag in DentAi.tag]) and ("shotacon" not in [tag.name for tag in DentAi.tag])) or ctx.guild.id == 586940644153622550:
    #                 Tags = (", ".join([tag.name for tag in DentAi.tag]))[:253]
    #                 HentaiPages = [EmbedMaker(DentAi, Tags, P) for P in range(len(DentAi.image_urls))]
    #                 await Navigator(ctx, HentaiPages).autoRun()
    #             else: await SendWait(ctx, "In compliance with discord TOS, this is Unavailable. :upside_down: "); return
    #         else: await SendWait(ctx, "That Doujin doesn't exist :expressionless:")
    #     except UnboundLocalError: pass

    async def cog_load(self) -> None:
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self) -> None:
        print(f"{self.__class__.__name__} unloaded!")


async def setup(DClient:CBotDClient) -> None:
   await DClient.add_cog(AnimeManga(DClient))