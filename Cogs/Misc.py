import discord
from discord.ext import commands
from Setup import Imgur
from Setup import FormatTime
from Setup import ChVote
from pdf2image import convert_from_path
import requests
from PIL import Image
import deeppyer
import asyncio
import os

class Misc(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient
    
    @commands.command(aliases = ["calculate","calc"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def Calculater(self, ctx, *args):
        ToCalc = "".join(args)
        def Calc(Nums):
            ChSafe = True
            for Num in Nums:
                try:
                    int(Num)
                except ValueError:
                    if Num not in ["(",")","*","/","+","-","**"]:
                        ChSafe = False 
                        break
            if ChSafe:
                return f'Answer is: {round(eval(Nums),4)}'
            else:
                return "Failed to calculate :confused:"
        Calculated = Calc(ToCalc)
        await ctx.message.channel.send(Calculated)

    @commands.command(name = "remind")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RemindAfter(self, ctx, *args):
        def TotalWait(Day, Hour, Min, Sec):
            return (Day*86400) + (Hour*3600) + (Min*60) + (Sec)
        def ChCHEm(RcM, RuS):
            return RuS.bot == False and RcM.message == ConfirmAwait and str(RcM.emoji) in ["✅","❌"]
        if args:
            try:
                TimeInputs = (" ".join(args)).split(" ")
                D = 0
                H = 0
                M = 0
                S = 0
                for Times in TimeInputs:
                    if Times[-1].lower() == "d":
                        D += int(Times[:-1])
                    elif Times[-1].lower() == "h":
                        H += int(Times[:-1])
                    elif Times[-1].lower() == "m":
                        M += int(Times[:-1])
                    elif Times[-1].lower() == "s":
                        S += int(Times[:-1])
                    else:
                        raise ValueError
                AwaitTime = TotalWait(D,H,M,S)
                if AwaitTime <= 86400:
                    ConfirmAwait = await ctx.message.channel.send(f':timer: Are you sure you want to be reminded in {FormatTime(AwaitTime)}? :timer:')
                    await ConfirmAwait.add_reaction("❌")
                    await ConfirmAwait.add_reaction("✅")
                    try:
                        ReaEm = await self.DClient.wait_for("reaction_add", check = ChCHEm, timeout = 10)
                        if ReaEm[0].emoji == "✅":
                            await ConfirmAwait.edit(content = f'You will be pinged in {FormatTime(AwaitTime)} :thumbsup:')
                            await asyncio.sleep(2)
                            await ConfirmAwait.delete()
                            await asyncio.sleep(AwaitTime)
                            await ctx.message.channel.send(f':timer: Its been {FormatTime(AwaitTime)} {ctx.message.author.mention} :timer:') 
                        elif  ReaEm[0].emoji == "❌":
                            await ConfirmAwait.edit(content = "Request Cancelled :thumbsup:")
                            await asyncio.sleep(2)
                            await ConfirmAwait.delete()
                    except asyncio.TimeoutError:
                        await ConfirmAwait.edit(content = "Request Timeout :alarm_clock:")
                        await asyncio.sleep(2)
                        await ConfirmAwait.delete()
                else:
                    await ctx.message.channel.send("zremind is limited to waiting for 1day max. :cry:")      
            except ValueError:
                await ctx.message.channel.send('Argument was improper. Check "zhelp misc" to check how to use it. :no_mouth:')    
        else:
            await ctx.message.channel.send("No arguments given :no_mouth:")

    @commands.command(name = "pdf")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def PDFreader(self, ctx, *args):
        def EmbTI(PDFname, PDFimages, PDFpage, PDFcache):
            try:
                ImgurLink = PDFcache[PDFpage]
                print("Cached...")
                CHcache = False
            except IndexError:
                print("Uploading...")
                PDFimages[PDFpage].save(f'{PDFname}.jpg', "JPEG")
                ImgurLink = Imgur.upload_from_path(f'{PDFname}.jpg')["link"]
                CHcache = True
            PEm = discord.Embed(title = "PDF Viewer")
            PEm.set_image(url = ImgurLink)
            PEm.add_field(name = f'```{PDFpage+1}/{len(PDFimages)}```', value = "\u200b")
            PEm.set_footer(text = "Need help navigating? zhelp navigation")
            return CHcache, ImgurLink, PEm

        def ChCHEm(RcM, RuS):
            return RuS.bot == False and RcM.message == PTEm and str(RcM.emoji) in ["⬅️","❌","➡️","#️⃣"]

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

        if (len(ctx.message.attachments) == 1 and len(args) == 0) or (len(ctx.message.attachments) == 0 and len(args) == 1):
            PDFattach = []
            URLargs = " ".join(args).split(" ")
            if len(ctx.message.attachments) == 1:
                for AtT in ctx.message.attachments:
                    PDFattach.append(AtT.url)
            else:
                try:
                    for Lin in URLargs:
                        PDFattach.append(Lin)
                except TypeError:
                    pass

            for GetPDF in PDFattach:
                try:
                    ChPDF = requests.head(GetPDF).headers.get("content-type").split("/")[1]
                    if ChPDF == "pdf":
                        RanLetters = "ioewsahkzcldnpq"
                        PDFname = "".join((random.choice(RanLetters) for i in range(10)))
                        PDFcontent = requests.get(GetPDF, allow_redirects = True)
                        open(f'{PDFname}.pdf', "wb").write(PDFcontent.content)
                        PDFimages = convert_from_path(f'{PDFname}.pdf', 500, last_page = 40) 
                        print(PDFimages)
                        PDFpage = 0   
                        PDFcache = [] 
                        PTEm = await ctx.message.channel.send(embed = discord.Embed(title = "Uploading Page...", description = "After upload a page will no longer be uploaded again (Faster navigation to page)"))
                        CHcache, ImgurLink, PEm = EmbTI(PDFname, PDFimages, PDFpage, PDFcache)
                        if CHcache:
                            PDFcache.append(ImgurLink)
                        await PTEm.edit(embed = PEm)
                        await PTEm.add_reaction("⬅️")
                        await PTEm.add_reaction("❌")
                        await PTEm.add_reaction("➡️")
                        await PTEm.add_reaction("#️⃣")
                        while True:
                            try:
                                ReaEm = await self.DClient.wait_for("reaction_add", check = ChCHEm, timeout = 120) 
                                await PTEm.remove_reaction(ReaEm[0].emoji, ReaEm[1])
                                if ReaEm[0].emoji == "⬅️" and PDFpage != 0:
                                    PDFpage -= 1     
                                    CHcache, ImgurLink, PEm = EmbTI(PDFname, PDFimages, PDFpage, PDFcache)
                                    if CHcache:
                                        PDFcache.append(ImgurLink)
                                    await PTEm.edit(embed = PEm)
                                elif ReaEm[0].emoji == "➡️":
                                    if PDFpage < len(PDFimages)-1:
                                        PDFpage += 1
                                        CHcache, ImgurLink, PEm = EmbTI(PDFname, PDFimages, PDFpage, PDFcache)
                                        if CHcache:
                                            PDFcache.append(ImgurLink)
                                        await PTEm.edit(embed = PEm)
                                    else:
                                        await PTEm.remove_reaction("⬅️", self.DClient.user)
                                        await PTEm.remove_reaction("❌", self.DClient.user)
                                        await PTEm.remove_reaction("➡️", self.DClient.user)
                                        await PTEm.remove_reaction("#️⃣", self.DClient.user)
                                        os.remove(f'{PDFname}.jpg')
                                        os.remove(f'{PDFname}.pdf')
                                        break
                                elif ReaEm[0].emoji == "#️⃣":
                                    if ChVote(ctx):
                                        NavNote = await ctx.message.channel.send('Choose a number to open navigate to page. "c" or "cancel" to exit navigation.')
                                        try:
                                            ResE = await self.DClient.wait_for("message", check = ChCHEmFN, timeout = 10)
                                            await NavNote.delete()
                                            await ResE.delete()
                                            try:
                                                try:
                                                    pG = int(ResE.content)
                                                    if 0 < pG <= len(PDFimages)-1:
                                                        PDFpage = pG-1
                                                    elif pG < 1:
                                                        PDFpage = 0
                                                        pass
                                                    else:
                                                        PDFpage = len(PDFimages)-1 
                                                except TypeError:
                                                    pass
                                            except ValueError:
                                                pass
                                            CHcache, ImgurLink, PEm = EmbTI(PDFname, PDFimages, PDFpage, PDFcache)
                                            if CHcache:
                                                PDFcache.append(ImgurLink)
                                            await PTEm.edit(embed = PEm)
                                        except asyncio.TimeoutError:
                                            await NavNote.edit("Request Timeout")
                                            await asyncio.sleep(5)
                                            await NavNote.delete()
                                elif ReaEm[0].emoji == "❌":
                                    await PTEm.remove_reaction("⬅️", self.DClient.user)
                                    await PTEm.remove_reaction("❌", self.DClient.user)
                                    await PTEm.remove_reaction("➡️", self.DClient.user)
                                    await PTEm.remove_reaction("#️⃣", self.DClient.user)
                                    os.remove(f'{PDFname}.jpg')
                                    os.remove(f'{PDFname}.pdf')
                                    break
                            except asyncio.TimeoutError:
                                await PTEm.remove_reaction("⬅️", self.DClient.user)
                                await PTEm.remove_reaction("❌", self.DClient.user)
                                await PTEm.remove_reaction("➡️", self.DClient.user)
                                await PTEm.remove_reaction("#️⃣", self.DClient.user)
                                os.remove(f'{PDFname}.jpg')
                                os.remove(f'{PDFname}.pdf')
                                break
                except requests.exceptions.MissingSchema:
                    await ctx.message.channel.send("Not a PDF :woozy_face:")
        else:
            await ctx.message.channel.send("No or too many attachments :woozy_face:")

    @commands.group(name = "fry", invoke_without_command = True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ImageFrier(self, ctx, *args):
        if args:
            URLargs = " ".join(args).split(" ")
            Attached = []
            try:
                for url in URLargs:
                    Attached.append(url)
            except TypeError:
                pass
            for AtT in ctx.message.attachments:
                Attached.append(AtT.url)
            Files = []
            C = 0
            for File in Attached:
                try:
                    if requests.head(File).headers.get("content-type").split("/")[0] == "image":
                        C += 1
                        GetURLimg = requests.get(File, allow_redirects = True)
                        open("NsRndo.jpg", "wb").write(GetURLimg.content)
                        Img = Image.open("NsRndo.jpg")
                        Img = await deeppyer.deepfry(Img, flares = False)
                        Img.save("NsRndo.jpg")
                        Files.append(discord.File("NsRndo.jpg"))
                        await ctx.message.channel.send(files = Files)
                        Files.pop(0)
                        os.remove("NsRndo.jpg")
                    else:
                        await ctx.message.channel.send(f'File({C}) isnt a valid image type :sweat:')
                except requests.exceptions.MissingSchema:
                    pass
        else:
            await ctx.message.channel.send("No image(s) or link(s) were attached :woozy_face:")

    @ImageFrier.command(name = "profile")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ProfileFrier(self, ctx):
        if len(ctx.message.mentions) > 0:
            Profile = str((ctx.message.mentions[0]).avatar_url)
        else:
            Profile = str(ctx.author.avatar_url)
        try:
            Files = []
            C = 0
            if requests.head(Profile).headers.get("content-type").split("/")[0] == "image":
                C += 1
                GetURLimg = requests.get(Profile, allow_redirects = True)
                open("NsRndo.jpg", "wb").write(GetURLimg.content)
                Img = Image.open("NsRndo.jpg")
                Img = await deeppyer.deepfry(Img, flares = False)
                Img.save("NsRndo.jpg")
                Files.append(discord.File("NsRndo.jpg"))
                await ctx.message.channel.send(files = Files)
                Files.pop(0)
                os.remove("NsRndo.jpg")
            else:
                await ctx.message.channel.send(f'File({C}) isnt a valid image type :sweat:')
        except requests.exceptions.MissingSchema:
            pass

    @Calculater.error
    async def CalculateError(self, ctx, error):
        if isinstance(error, commands.UnexpectedQuoteError):
            await ctx.message.channel.send("Failed to calculate :confused:")
        raise error

def setup(DClient):
    DClient.add_cog(Misc(DClient))