import discord
from discord.ext import commands
import malclient
import mal
from hentai import Utils, Sort, Hentai, Format

MClient = malclient.Client()
MClient.init(access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImY5OWNmNDExZjY5NDMwMGY0ZjcwMDAyM2JlOTYyYTkyYjQxYzUwNGQ0NzA0MzQyOWYxMjEyZmNkOTBmNWNiZjlkNmFmZWNkYWRmMTViMzdjIn0.eyJhdWQiOiIyYjcwMWQzNjY5NzFmYTFmMTgyYmZkNTBkMTUxNzJhZSIsImp0aSI6ImY5OWNmNDExZjY5NDMwMGY0ZjcwMDAyM2JlOTYyYTkyYjQxYzUwNGQ0NzA0MzQyOWYxMjEyZmNkOTBmNWNiZjlkNmFmZWNkYWRmMTViMzdjIiwiaWF0IjoxNjA1MTc4ODM5LCJuYmYiOjE2MDUxNzg4MzksImV4cCI6MTYwNzc3MDgzOSwic3ViIjoiNzQ5Njc5MSIsInNjb3BlcyI6W119.B8X86ggNC43bZwzKF6993WSnY1AUGQ2wgdxbL2kRhGPJAm4M3epzbTixTxxs3RmWOsUfypoU3U2vnlYs69enzwsdGxzpoLh-hO_Mav4kSTxeXqrvPk23_7fSyC1Q8AOFE_EszhI6DG67BcFAZWVdgFia8th6vZ_7HTugWd9dDrf1PIBDfNrpWrsTs1tUImTbsZ41Y_19uT2p3-oTpmQY_YwSbLxgzkdVZmASWdDkXyFjTNnYW5y_fCDYQrDJrNrId5Dvm1N02d66TNaJgyDn86L0Dr-lYqjU9qM45agHff4T8MpkIzqzA3pKT874QUOW5QXks46-9JaCCpSB-nIrfQ")
MClient.refresh_bearer_token(client_id = "2b701d366971fa1f182bfd50d15172ae", client_secret = "e01505a84d5e611e2e59b66f0dc245888656104b1529e1a25954d8ff51780f5c", refresh_token = "def50200b66cd79fef2e2b550556891e5d1a4c7774d4db62ff64a49900570a29f94680d1a93ba950d8af2f3b98a4b8af587e2fd939cb94f5a8ce5fc4498a26469da1973224c916e11ed3fbb73d7cfca981c865c3cd9d611674d113159746a6759cfcf4a646132332007b3228f7c83a761ef1226693a7b9e27c6d6b621602943c690ce1351f993088872976c25fa680f1622e7bbf38000fdc00a0e7557f4ef70e3cc4af93ea213ef090c155a9deb37a7c3db56fcabaef4a13783bb5d2a22cf100e5928292df6cb468b63497ad74b4a93fe3d2d086043bf51c9a58fd5341f519fa3a6946cd8ada2c554fffce8d59e35380ddbfb341d7777056e4c0da0a87a1e2cd5d0944ccc54f6593f2ccb5345cb827e0587cb07e66ae931d0e74d14f1a295110f5a4b402ab9a53b244168d629bc21925fb4aefc9aa201d48ccdff77d36557fb49bd5e89ce979aeb0c22972f6cdc5bc1dc2dcceb38b137a305b647bc1ccd3c18eac108cb5159e1c64ef17dd4059d64dd1b53c2000a74f8b4013a90e9325be2cc30ded29d8b72907c7")

class AnimeManga(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.command(name = "manga")
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def MagMa(self, ctx, *args):
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
        if args:
            try:
                Srks = " ".join(args)
                C = 0
                SrchMag = []
                MnSrS = await ctx.message.channel.send(embed = discord.Embed(title = ":mag: Searching...",  description = "\u200b", color = 0x3695ba))
                SAEm = discord.Embed(title = f":mag: Results for '{Srks}'",  description = "\u200b", color = 0x3695ba)
                for MagRes in mal.MangaSearch(Srks).results:
                    C += 1
                    SAEm.add_field(name = "\u200b", value = f'{C}. `{MagRes.title}` **({MagRes.type})**', inline = False)
                    SrchMag.append(MagRes)
                    if C == 10:
                        print(MagRes)
                        break
                SAEm.set_footer(text = 'Choose a number to view MAL entry. "c" or "cancel" to exit search.\n\n*The Search closes automatically after 20sec of inactivity.*')
                await MnSrS.edit(embed = SAEm)
                try:
                    ResS = await self.DClient.wait_for('message', check = ChCHanS, timeout = 20)
                    LResS = ResS.content.lower()
                    try:
                        if int(ResS.content) <= 10:
                            MagI = SrchMag[int(ResS.content)-1].mal_id
                            await MnSrS.edit(embed = discord.Embed(title = ":calling: Finding...",  description = f'{SrchMag[int(ResS.content)-1].title} **({SrchMag[int(ResS.content)-1].type})**', color = 0x3695ba)) 
                    except ValueError:
                        if (LResS == "cancel") or (LResS == "c"):
                            await MnSrS.edit(embed = discord.Embed(title = ":x: Search Cancelled",  description = "\u200b", color = 0x3695ba))
                except asyncio.TimeoutError:
                    await MnSrS.edit(embed = discord.Embed(title = ":hourglass: Search Timeout...",  description = "\u200b", color = 0x3695ba))
            except UnboundLocalError:
                SAEm = discord.Embed(title = f':mag: Search for "{Srks}"',  description = "\u200b", color = 0x3695ba)
                SAEm.add_field(name = "\u200b", value = "No Results found :woozy_face:", inline = False)
                await MnSrS.edit(embed = SAEm)

            try:
                MagF = MClient.get_manga_details(MagI)
                MagFmal = mal.Manga(MagI)
                MagG = []
                for TMagG in MagF.genres:
                    MagG.append(TMagG.name)
                AEm = discord.Embed(title = f'{MagF.title} / {MagF.alternative_titles.ja} **({MagFmal.type})**',  description = f'{", ".join(MagG)}\n[Mal Page]({MagFmal.url})', color = 0x3695ba)
                AEm.set_thumbnail(url = MagF.main_picture.large)
                if len(MagF.synopsis) > 1021:
                    MagSyn = MagF.synopsis[0:1021]
                    MagSyn = MagSyn + "..."
                else:
                    MagSyn = MagF.synopsis
                AEm.add_field(name = f'By: {", ".join(MagFmal.authors)}', value = "\u200b", inline = False)
                AEm.add_field(name = "Synopsis:", value = MagSyn, inline = False)
                try:
                    AEm.add_field(name = "Start Airing on:", value = MagF.start_date, inline = True)
                except AttributeError:
                    pass
                try:
                    AEm.add_field(name = "Finish Airing on:", value = MagF.end_date, inline = True)
                except AttributeError:
                    pass
                AEm.add_field(name = "Status:", value = MagFmal.status, inline = True)
                AEm.add_field(name = "Score:", value = MagFmal.score, inline = True)
                AEm.add_field(name = "Rank:", value = MagFmal.rank, inline = True)
                AEm.add_field(name = "Popularity:", value = MagFmal.popularity, inline = True)
                AEm.add_field(name = "No# Volumes:", value = MagFmal.volumes, inline = True)
                AEm.add_field(name = "No# Chapters:", value = MagFmal.chapters, inline = True)
                MagAdp = []
                MagAlt = []
                MagSum = []
                MagSeq = []
                MagSiSt = []
                MagSpO = []
                for TMagAdp in MagF.related_manga:
                    if TMagAdp.relation_type_formatted == "Adaptation":
                        MagAdp.append(TMagAdp.node.title)
                    elif TMagAdp.relation_type_formatted == "Summary":
                        MagSum.append(TMagAdp.node.title)
                    elif TMagAdp.relation_type_formatted == "Sequel":
                        MagSeq.append(TMagAdp.node.title)
                    elif TMagAdp.relation_type_formatted == "Spin-off":
                        MagSpO.append(TMagAdp.node.title)
                    elif TMagAdp.relation_type_formatted == "Alternative version":
                        MagAlt.append(TMagAdp.node.title)
                    elif TMagAdp.relation_type_formatted == "Side story":
                        MagSiSt.append(TMagAdp.node.title)

                if len("\n".join(MagSeq)) > 950:
                    MagSeqF = "\n".join(MagSeq)[0:950]
                    MagSeqF = MagSeqF + "..."
                else:
                    MagSeqF = "\n".join(MagSeq)

                if len("\n".join(MagAdp)) > 950:
                    MagAdpF = "\n".join(MagAdp)[0:950]
                    MagAdpF = MagAdpF + "..."
                else:
                    MagAdpF = "\n".join(MagAdp)

                if len("\n".join(MagSum)) > 950:
                    MagSumF = "\n".join(MagSum)[0:950]
                    MagSumF = MagSumF + "..."
                else:
                    MagSumF = "\n".join(MagSum)

                if len("\n".join(MagAlt)) > 950:
                    MagAltF = "\n".join(MagAlt)[0:950]
                    MagAltF = MagAltF + "..."
                else:
                    MagAltF = "\n".join(MagAlt)

                if len("\n".join(MagSpO)) > 950:
                    MagSpOF = "\n".join(MagSpO)[0:950]
                    MagSpOF = MagSpOF + "..."
                else:
                    MagSpOF = "\n".join(MagSpO)

                if len("\n".join(MagSiSt)) > 950:
                    MagSiStF = "\n".join(MagSiSt)[0:950]
                    MagSiStF = MagSiStF + "..."
                else:
                    MagSiStF = "\n".join(MagSiSt)
                if MagSeqF or MagAltF or MagAdpF or MagSiStF or MagSumF or MagSpOF:
                    AEm.add_field(name = "\u200b", value = "\u200b", inline = False)
                if MagSeqF:
                    AEm.add_field(name = "Sequel:", value = MagSeqF, inline = False)
                if MagAltF:
                    AEm.add_field(name = "Alternate Version:", value = MagAltF, inline = False)
                if MagAdpF:
                    AEm.add_field(name = "Adaptation:", value = MagAdpF, inline = False)
                if MagSiStF:
                    AEm.add_field(name = "Side Story:", value = MagSiStF, inline = False)
                if MagSumF:
                    AEm.add_field(name = "Summary:", value = MagSumF, inline = False)
                if MagSpOF:
                    AEm.add_field(name = "Spin Off:", value = MagSpOF, inline = False)
                await ctx.message.channel.send(embed = AEm)
            except UnboundLocalError:
                pass
        else:
            await ctx.message.channel.send("No Arguments :no_mouth:")

    @commands.command(name = "anime")
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def AniMa(self, ctx, *args):
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
        if args:
            try:
                Srks = " ".join(args)
                C = 0
                SrchAni = []
                AnSrS = await ctx.message.channel.send(embed = discord.Embed(title = ":mag: Searching...",  description = "\u200b", color = 0x3fc0ff))
                SAEm = discord.Embed(title = f':mag: Results for "{Srks}"',  description = "\u200b", color = 0x3fc0ff)
                for AniRes in mal.AnimeSearch(Srks).results:
                    C += 1
                    SAEm.add_field(name = "\u200b", value = f"{C}. `{AniRes.title}` **({AniRes.type})**", inline = False)
                    SrchAni.append(AniRes)
                    if C == 10:
                        break
                SAEm.set_footer(text = 'Choose a number to view MAL entry. "c" or "cancel" to exit search.\n\n*The Search closes automatically after 20sec of inactivity.*')
                await AnSrS.edit(embed = SAEm)
                try:
                    ResS = await self.DClient.wait_for('message', check = ChCHanS, timeout = 20)
                    LResS = ResS.content.lower()
                    try:
                        if int(ResS.content) <= 10:
                            AniI = SrchAni[int(ResS.content)-1].mal_id
                            await AnSrS.edit(embed = discord.Embed(title = ":calling: Finding...",  description = f'{SrchAni[int(ResS.content)-1].title} **({SrchAni[int(ResS.content)-1].type})**', color = 0x3fc0ff)) 
                    except ValueError:
                        if (LResS == "cancel") or (LResS == "c"):
                            await AnSrS.edit(embed = discord.Embed(title = ":x: Search Cancelled",  description = "\u200b", color = 0x3fc0ff))
                except asyncio.TimeoutError:
                    await AnSrS.edit(embed = discord.Embed(title = ":hourglass: Search Timeout...",  description = "\u200b", color = 0x3fc0ff))
            except UnboundLocalError:
                SAEm = discord.Embed(title = f':mag: Search for "{Srks}"',  description = "\u200b", color = 0x3fc0ff)
                SAEm.add_field(name = "\u200b", value = "No Results found :woozy_face:", inline = False)
                await AnSrS.edit(embed = SAEm)

            try:
                AniF = MClient.get_anime_details(AniI)
                AniFmal = mal.Anime(AniI)
                AniG = []
                for TAniG in AniF.genres:
                    AniG.append(TAniG.name)
                AEm = discord.Embed(title = f'{AniF.title} / {AniF.alternative_titles.ja} **({AniFmal.type})**',  description = f'{", ".join(AniG)}\n[Mal Page]({AniFmal.url})', color = 0x3fc0ff)
                AEm.set_thumbnail(url = AniF.main_picture.large)
                if len(AniF.synopsis) > 1021:
                    AniSyn = AniF.synopsis[0:1021]
                    AniSyn = AniSyn + "..."
                else:
                    AniSyn = AniF.synopsis
                AEm.add_field(name = f'Studios: {", ".join(AniFmal.studios)}', value = "\u200b", inline = False)
                AEm.add_field(name = "Synopsis:", value = AniSyn, inline = False)
                try:
                    AEm.add_field(name = "Start Airing on:", value = AniF.start_date, inline = True)
                except AttributeError:
                    pass
                try:
                    AEm.add_field(name = "Finish Airing on:", value = AniF.end_date, inline = True)
                except AttributeError:
                    pass
                AEm.add_field(name = "Status:", value = AniFmal.status, inline = True)
                AEm.add_field(name = "Rating:", value = AniFmal.rating, inline = False)
                AEm.add_field(name = "Score:", value = AniFmal.score, inline = True)
                AEm.add_field(name = "Rank:", value = AniFmal.rank, inline = True)
                AEm.add_field(name = "Popularity:", value = AniFmal.popularity, inline = True)
                AEm.add_field(name = "No# Episodes:", value = AniFmal.episodes, inline = True)
                AEm.add_field(name = "Episode Duration:", value = AniFmal.duration, inline = True)
                AniAdp = []
                AniAlt = []
                AniSum = []
                AniSeq = []
                AniSiSt = []
                AniSpO = []
                for TAniAdp in AniF.related_anime:
                    if TAniAdp.relation_type_formatted == "Adaptation":
                        AniAdp.append(TAniAdp.node.title)
                    elif TAniAdp.relation_type_formatted == "Summary":
                        AniSum.append(TAniAdp.node.title)
                    elif TAniAdp.relation_type_formatted == "Sequel":
                        AniSeq.append(TAniAdp.node.title)
                    elif TAniAdp.relation_type_formatted == "Spin-off":
                        AniSpO.append(TAniAdp.node.title)
                    elif TAniAdp.relation_type_formatted == "Alternative version":
                        AniAlt.append(TAniAdp.node.title)
                    elif TAniAdp.relation_type_formatted == "Side story":
                        AniSiSt.append(TAniAdp.node.title)
                if len("\n".join(AniSeq)) > 950:
                    AniSeqF = "\n".join(AniSeq)[0:950]
                    AniSeqF = AniSeqF + "..."
                else:
                    AniSeqF = "\n".join(AniSeq)

                if len("\n".join(AniAdp)) > 950:
                    AniAdpF = "\n".join(AniAdp)[0:950]
                    AniAdpF = AniAdpF + "..."
                else:
                    AniAdpF = "\n".join(AniAdp)

                if len("\n".join(AniSum)) > 950:
                    AniSumF = "\n".join(AniSum)[0:950]
                    AniSumF = AniSumF + "..."
                else:
                    AniSumF = "\n".join(AniSum)

                if len("\n".join(AniAlt)) > 950:
                    AniAltF = "\n".join(AniAlt)[0:950]
                    AniAltF = AniAltF + "..."
                else:
                    AniAltF = "\n".join(AniAlt)

                if len("\n".join(AniSpO)) > 950:
                    AniSpOF = "\n".join(AniSpO)[0:950]
                    AniSpOF = AniSpOF + "..."
                else:
                    AniSpOF = "\n".join(AniSpO)

                if len("\n".join(AniSiSt)) > 950:
                    AniSiStF = "\n".join(AniSiSt)[0:950]
                    AniSiStF = AniSiStF + "..."
                else:
                    AniSiStF = "\n".join(AniSiSt)
                if AniSeqF or AniAltF or AniAdpF or AniSiStF or AniSumF or AniSpOF:
                    AEm.add_field(name = "\u200b", value = "\u200b", inline = False)
                if AniSeqF:
                    AEm.add_field(name = "Sequel:", value = AniSeqF, inline = False)
                if AniAltF:
                    AEm.add_field(name = "Alternate Version:", value = AniAltF, inline = False)
                if AniAdpF:
                    AEm.add_field(name = "Adaptation:", value = AniAdpF, inline = False)
                if AniSiStF:
                    AEm.add_field(name = "Side Story:", value = AniSiStF, inline = False)
                if AniSumF:
                    AEm.add_field(name = "Summary:", value = AniSumF, inline = False)
                if AniSpOF:
                    AEm.add_field(name = "Spin Off:", value = AniSpOF, inline = False)
                AEm.add_field(name = "\u200b", value = "\u200b", inline = False)
                try:
                    if len("\n".join(AniFmal.opening_themes)) > 950:
                        AniOT = ("\n".join(AniFmal.opening_themes))[0:950]
                        AniOT = AniOT + "..."
                    else:
                        AniOT = "\n".join(AniFmal.opening_themes)
                    AEm.add_field(name = "Opening Theme(s):", value = AniOT, inline = False)
                except TypeError:
                    pass

                try:
                    if len("\n".join(AniFmal.ending_themes)) > 950:
                        AniET = ("\n".join(AniFmal.ending_themes))[0:950]
                        AniET = AniET + "..."
                    else:
                        AniET = "\n".join(AniFmal.ending_themes)
                    AEm.add_field(name = "Ending Theme(s):", value = AniET, inline = True)
                except TypeError:
                    pass
                await ctx.message.channel.send(embed = AEm)
            except UnboundLocalError:
                pass
        else:
            await ctx.message.channel.send("No Arguments :no_mouth:")

    @commands.command(name = "hentai")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def nHen(self, ctx, *args):  
        def ChCHanS(MSg):
            MesS = MSg.content.lower()
            MeseS = (MSg.content.lower()).split(" ")
            RsT = False
            try:
                if int(MSg.content) <= 10:
                    RsT = True
            except ValueError:
                if (MesS == "cancel") or (MesS == "c") or (MesS == "zhentai") or (MeseS[0] == "zhentai"):
                    RsT = True
            return MSg.guild.id == ctx.guild.id and MSg.channel.id == ctx.channel.id and RsT

        def ChCHEm(RcM, RuS):
            return RuS.bot == False and RcM.message == DmSent and str(RcM.emoji) in ["⬅️","❌","➡️","#️⃣"]

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

        def EmbedMaker(DentAi,Page, State):
            DEmE = discord.Embed(title = DentAi.title(Format.Pretty),  description = FdesCtI, color = 0x000000)
            DEmE.set_thumbnail(url = DentAi.image_urls[0])
            DEmE.set_footer(text = f'Released on {DentAi.upload_date}\n\n.\n\n*The Doujin closes automatically after 2mins of inactivity.*')
            DEmE.set_image(url = DentAi.image_urls[Page])
            DEmE.add_field(name = "Doujin ID", value = DentAi.id, inline = False)
            DEmE.add_field(name = "\u200b", value = f'**Doujin {State}**\n\n`Page: {(Page+1)}/{len(DentAi.image_urls)}`', inline = False)
            return DEmE

        if args:
            Chlks = " ".join(args).split(" ")
            if Chlks[0].lower() == "search":
                Chlks.pop(0)
                C = 0
                SrchDen = []
                if " ".join(Chlks):
                    try:
                        for DeOujin in Utils.search_by_query(query =  f'{" ".join(Chlks)} -tag:"lolicon" -tag:"shotacon"', sort = Sort.Popular):
                            C += 1
                            if C == 1:
                                SEm = discord.Embed(title = f':mag: Search for "{" ".join(Chlks)}"',  description = "\u200b", color = 0x000000)
                            SEm.add_field(name = "\u200b", value = f'{C}. `{DeOujin["title"]["english"]}`', inline = False)
                            SrchDen.append(DeOujin)
                            if C == 10:
                                break
                        SEm.set_footer(text = 'Choose a number to open doujin. "c" or "cancel" to exit search. \n\n*The Search closes automatically after 20sec of inactivity.*' )
                        DmSent = await ctx.message.channel.send(embed = SEm)
                        try:
                            ResS = await self.DClient.wait_for("message", check = ChCHanS, timeout = 20)
                            LResS = ResS.content.lower()
                            ReseS = (ResS.content.lower()).split(" ")

                            try:
                                if int(ResS.content) <= 10:
                                    Srch = SrchDen[int(ResS.content)-1]["id"]
                                    DentAi = Hentai(Srch)
                                    await DmSent.edit(embed = discord.Embed(title = ":newspaper: Opening...",  description = DentAi.title(Format.Pretty), color = 0x000000)) 
                            except ValueError:
                                if (LResS == "cancel") or (LResS == "c") or (LResS == "zhentai") or (ReseS[0] == "zhentai"):
                                    await DmSent.edit(embed = discord.Embed(title = ":newspaper2: Search Cancelled",  description = "\u200b", color = 0x000000))
                        except asyncio.TimeoutError:
                            await DmSent.edit(embed = discord.Embed(title = ":hourglass: Search Timeout...",  description = "\u200b", color = 0x000000))
                    except UnboundLocalError:
                        SEm = discord.Embed(title = f':mag: Search for "{" ".join(Chlks)}"',  description = "\u200b", color = 0x000000)
                        SEm.add_field(name = "\u200b", value = "No Results found :woozy_face:", inline = False)
                        await ctx.message.channel.send(embed = SEm)    
                else:
                    await ctx.message.channel.send("No search argument :woozy_face:")     
            elif len(Chlks) >= 1:
                try:
                    Srch = int(" ".join(args))
                except ValueError:
                    if " ".join(args).lower() == "random":
                        while True:
                            Srch = Utils.get_random_id()
                            DentAi = Hentai(Srch)
                            if ("lolicon" not in [tag.name for tag in DentAi.tag]) and ("shotacon" not in [tag.name for tag in DentAi.tag]):
                                break
                    else:
                        await ctx.message.channel.send("The argument contained non-numeral characters and wasn't a random request. :no_mouth:")
            try:
                if (Hentai.exists(Srch)):
                    DentAi = Hentai(Srch)
                    if ("lolicon" not in [tag.name for tag in DentAi.tag]) and ("shotacon" not in [tag.name for tag in DentAi.tag]):
                        if ctx.channel.is_nsfw(): 
                            Tags = ", ".join([tag.name for tag in DentAi.tag])
                            if len(Tags) > 253:
                                FdesCtI = Tags[0:253]
                                FdesCtI = FdesCtI + "..."
                            else:
                                FdesCtI = Tags
                            Page = 0
                            DEm = discord.Embed(title = DentAi.title(Format.Pretty),  description = FdesCtI, color = 0x000000)
                            DEm.set_thumbnail(url = DentAi.image_urls[0])
                            DEm.set_footer(text = f'Released on {DentAi.upload_date}\n\n React with :hash: then type in a page number to instantly navigate to it (voters only).\n\n*The Doujin closes automatically after 2mins of inactivity.*')
                            DEm.set_image(url = DentAi.image_urls[0])
                            DEm.add_field(name = "Doujin ID", value = str(DentAi.id), inline = False)
                            DEm.add_field(name = "\u200b", value = f'**Doujin OPEN**\n\n`Page: {(Page+1)}/{len(DentAi.image_urls)}`', inline = False)
                            await ctx.message.channel.send("**WARNING:** ALL messages sent after the embed will be deleted until doujin is closed. This is to ensure a proper reading experience.")
                            DmSent = await ctx.message.channel.send(embed = DEm)
                    await DmSent.add_reaction("⬅️")
                    await DmSent.add_reaction("❌")
                    await DmSent.add_reaction("➡️")
                    await DmSent.add_reaction("#️⃣")
                    while True:
                        try:
                            Res = await self.DClient.wait_for("reaction_add", check = ChCHEm, timeout = 120) 
                            await DmSent.remove_reaction(Res[0].emoji, Res[1])
                            if Res[0].emoji == "⬅️" and Page != 0:
                                Page -= 1
                                await DmSent.edit(embed = EmbedMaker(DentAi, Page, "OPEN"))
                            elif Res[0].emoji == "➡️":
                                if Page < len(DentAi.image_urls)-1:
                                    Page += 1
                                    await DmSent.edit(embed = EmbedMaker(DentAi, Page, "OPEN"))
                                else:
                                    await DmSent.edit(embed = EmbedMaker(DentAi, Page, "CLOSED"))
                                    await DmSent.remove_reaction("⬅️", self.DClient.user)
                                    await DmSent.remove_reaction("❌", self.DClient.user)
                                    await DmSent.remove_reaction("➡️", self.DClient.user)
                                    await DmSent.remove_reaction("#️⃣", self.DClient.user)
                                    break
                            elif Res[0].emoji == "#️⃣":
                                if ChPatreonFu(ctx) or (await TClient.get_user_vote(ctx.author.id)):
                                    TempNG = await ctx.message.channel.send('Choose a number to open navigate to page. "c" or "cancel" to exit navigation.\n\n*The Navigation closes automatically after 10sec of inactivity.*')
                                    try:
                                        ResE = await self.DClient.wait_for("message", check = ChCHEmFN, timeout = 10)
                                        await TempNG.delete()
                                        await ResE.delete()
                                        try:
                                            try:
                                                pG = int(ResE.content)
                                                if 0 < pG <= len(DentAi.image_urls)-1:
                                                    Page = pG-1
                                                elif pG < 1:
                                                    Page = 0
                                                    pass
                                                else:
                                                    Page = len(DentAi.image_urls)-1 
                                            except TypeError:
                                                pass
                                        except ValueError:
                                            pass
                                        await DmSent.edit(embed = EmbedMaker(DentAi, Page, "OPEN"))
                                    except asyncio.TimeoutError:
                                        await TempNG.edit("Request Timeout")
                                        await asyncio.sleep(5)
                                        await TempNG.delete()
                                else:
                                    TemS = await ctx.message.channel.send("Instant navigation to page is only for voters or Patreon Supporters. \n:robot: zvote or zpatreon to learn more. :robot:")
                                    await asyncio.sleep(5)
                                    await TemS.delete()
                            elif Res[0].emoji == "❌":
                                await DmSent.edit(embed = EmbedMaker(DentAi, Page, "CLOSED"))
                                await DmSent.remove_reaction("⬅️", self.DClient.user)
                                await DmSent.remove_reaction("❌", self.DClient.user)
                                await DmSent.remove_reaction("➡️", self.DClient.user)
                                await DmSent.remove_reaction("#️⃣", self.DClient.user)
                                break
                        except asyncio.TimeoutError:
                            await DmSent.edit(embed = EmbedMaker(DentAi, Page, "CLOSED"))
                            break
                    await ctx.message.channel.send(":newspaper2: Doujin Closed :newspaper2:")
                else:
                    await ctx.message.channel.send("That Doujin doesn't exist :expressionless:")
            except UnboundLocalError:
                pass
        else:
            await ctx.message.channel.send("No arguments :no_mouth:")

def setup(DClient):
    DClient.add_cog(AnimeManga(DClient))