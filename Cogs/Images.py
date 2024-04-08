import discord
from discord.ext import commands
import requests
import pyimgbox
# from Setup import ChVoteUser, SendWait, Threader, ErrorEmbeds, Navigator
from Setup import SendWait, Threader, Navigator
# from pdf2image import convert_from_path
import random
from PIL import Image
import deeppyer
import asyncio
import os
import qrcode
import cv2


class Images(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.command(aliases=["kitten", "kitty", "cat"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RandomCat(self, ctx):
        CatGot = requests.get("https://cataas.com/cat", headers={"Accept": "application/json"}, timeout=5).json()
        CEm = discord.Embed(title="Meow", color=0xA3D7C1)
        CEm.set_image(url=f'https://cataas.com/cat/{CatGot["_id"]}')
        await ctx.message.channel.send(embed=CEm)

    # @commands.command(aliases=["pog","poggers", "pogger", "pogchamp"])
    # @commands.cooldown(1, 1, commands.BucketType.user)
    # async def POOOGGERRRS(self, ctx):
    #     Pog = random.choice(open("Pog.txt").readlines())
    #     await ctx.message.channel.send(Pog)

    @commands.command(aliases=["doggo", "dog", "pupper", "puppy"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RandomDoggo(self, ctx):
        DoggoGot = requests.get("https://random.dog/woof.json", headers={"Accept": "application/json"}).json()
        DEm = discord.Embed(title="Woof Woof", color=0xFF3326)
        DEm.set_image(url=DoggoGot["url"])
        await ctx.message.channel.send(embed=DEm)

    @commands.command(aliases=["thispersondoesnotexist", "thispersondoesntexist", "tpde"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def GetAnImaginedPerson(self, ctx):
        PEm = discord.Embed(title="This Person Does NOT Exist.", color=0x753684)
        GetTpde = requests.get("https://thispersondoesnotexist.com/image", allow_redirects=True)
        This = open("Tpde.png", "wb").write(GetTpde.content)
        TpdeImg = discord.File("Tpde.png")
        PEm.set_image(url="attachment://Tpde.png")
        await ctx.send(file=TpdeImg, embed=PEm)
        os.remove("Tpde.png")

    @commands.command(name="fox")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RandomFox(self, ctx):
        FoxGot = requests.get("https://randomfox.ca/floof/", headers={"Accept": "application/json"}).json()
        FEm = discord.Embed(title="What does the fox say?", color=0x9DAA45)
        FEm.set_image(url=FoxGot["image"])
        await ctx.message.channel.send(embed=FEm)

    @commands.command(aliases=["food", "dishes", "dish"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RandomDishes(self, ctx):
        Hungry = requests.get("https://foodish-api.herokuapp.com/api/", headers={"Accept": "application/json"}).json()
        FEm = discord.Embed(title="Hungry?", color=0xDE8761)
        FEm.set_image(url=Hungry["image"])
        await ctx.message.channel.send(embed=FEm)

    # @commands.command(aliases=["taylor", "tswift", "taylorswift"])
    # @commands.cooldown(1, 1, commands.BucketType.user)
    # async def RandomTSwift(self, ctx):
    #     TaylorImage = requests.get("https://api.taylor.rest/image", headers={"Accept": "application/json"}).json()
    #     TaylorQuote = requests.get("https://api.taylor.rest/", headers={"Accept": "application/json"}).json()
    #     TEm = discord.Embed(title="Taylor Swift", description=TaylorQuote["quote"], color=0xD29EC1)
    #     TEm.set_image(url=TaylorImage["url"])
    #     await ctx.message.channel.send(embed=TEm)

    # @commands.command(name="pdf")
    # @commands.cooldown(1, 5, commands.BucketType.user)
    # async def PDFreader(self, ctx, *args):
    #     def ChCHEmFN(MSg):
    #         MesS = MSg.content.lower()
    #         RsT = False
    #         try:
    #             if int(MSg.content): RsT = True
    #         except ValueError:
    #             if MesS in ["cancel", "c"]: RsT = True
    #         return MSg.guild.id == ctx.guild.id and MSg.channel.id == ctx.channel.id and RsT

    #     if args and ctx.message.attachments: await SendWait(ctx, "No or too many attachments :woozy_face:"); return
    #     PDFattach = []
    #     if args: PDFattach.append("".join(args))
    #     if ctx.message.attachments:
    #         for AtT in ctx.message.attachments: PDFattach.append(AtT.url)
    #     GetPDF = PDFattach[0]
    #     try:
    #         ChPDF = requests.head(GetPDF).headers.get("content-type").split("/")[1]
    #         if ChPDF != "pdf": await SendWait(ctx, "Not a PDF :woozy_face:"); return
    #         RanLetters = "ioewsahkzcldnpq"
    #         PDFname = "".join((random.choice(RanLetters) for i in range(10)))
    #         await SendWait(ctx, ":printer: Converting...")
    #         PDFcontent = requests.get(GetPDF, allow_redirects=True)
    #         open(f"{PDFname}.pdf", "wb").write(PDFcontent.content)
    #         PDFimages = convert_from_path(f"{PDFname}.pdf", 500, last_page=40)
    #         PDFcnvrt = []
    #         PageNum = 1
    #         TotalPages = len(PDFimages)
    #         Sub = []
    #         async with pyimgbox.Gallery(title=PDFname) as gallery:
    #             for i in PDFimages:
    #                 i.save(f"{PDFname}.jpg", "JPEG")
    #                 Sub.append(await gallery.upload(f"{PDFname}.jpg"))

    #         for Up in Sub:
    #             PEm = discord.Embed(title="PDF Viewer", description=f"**`{PageNum}/{TotalPages}`**")
    #             PEm.set_image(url=Up["image_url"])
    #             PDFcnvrt.append(PEm)
    #             PageNum += 1
    #         await Navigator(ctx, PDFcnvrt)
    #     except requests.exceptions.MissingSchema: await SendWait(ctx, "Not a PDF :woozy_face:")

    @commands.group(aliases=["fry", "deepfry"], invoke_without_command=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ImageFrier(self, ctx, *args):
        if not args and not ctx.message.attachments and not (ctx.message.reference.resolved.attachments if ctx.message.type == discord.MessageType.reply else False): await SendWait(ctx, "No image(s) or link(s) were attached :woozy_face:"); return 
        Attached = []
        if args:
            URLargs = list(args)
            try:
                for url in URLargs: Attached.append(url)
            except TypeError: pass
        elif ctx.message.attachments:
            for AtT in ctx.message.attachments: Attached.append(AtT.url)
            Files = []
            C = 0
            for File in Attached:
                try:
                    if requests.head(File).headers.get("content-type").split("/")[0] == "image":
                        C += 1
                        GetURLimg = requests.get(File, allow_redirects=True)
                        open("NsRndo.jpg", "wb").write(GetURLimg.content)
                        Img = Image.open("NsRndo.jpg")
                        Img = await deeppyer.deepfry(Img, flares=False)
                        Img.save("NsRndo.jpg")
                        Files.append(discord.File("NsRndo.jpg"))
                        await ctx.message.channel.send(files=Files)
                        Files.pop(0)
                        os.remove("NsRndo.jpg")
                    else: await SendWait(ctx, f"File({C}) isnt a valid image type :sweat:")
                except requests.exceptions.MissingSchema: pass
        for AtT in ctx.message.reference.resolved.attachments: Attached.append(AtT.url)
        Files = []
        C = 0
        for File in Attached:
            try:
                if requests.head(File).headers.get("content-type").split("/")[0] == "image":
                    C += 1
                    GetURLimg = requests.get(File, allow_redirects=True)
                    open("NsRndo.jpg", "wb").write(GetURLimg.content)
                    Img = Image.open("NsRndo.jpg")
                    Img = await deeppyer.deepfry(Img, flares=False)
                    Img.save("NsRndo.jpg")
                    Files.append(discord.File("NsRndo.jpg"))
                    await ctx.message.channel.send(files=Files)
                    Files.pop(0)
                    os.remove("NsRndo.jpg")
                else: await SendWait(ctx, f"File({C}) isnt a valid image type :sweat:")
            except requests.exceptions.MissingSchema: pass

    # @ImageFrier.command(name="profile")
    # @commands.cooldown(1, 1, commands.BucketType.user)
    # async def ProfileFrier(self, ctx):
    #     if ctx.message.mentions: Profile = str((ctx.message.mentions[0]).avatar_url)
    #     else: Profile = str(ctx.author.avatar_url)
    #     try:
    #         Files = []
    #         C = 0
    #         if requests.head(Profile).headers.get("content-type").split("/")[0] == "image":
    #             C += 1
    #             GetURLimg = requests.get(Profile, allow_redirects=True)
    #             open("NsRndo.jpg", "wb").write(GetURLimg.content)
    #             Img = Image.open("NsRndo.jpg")
    #             Img = await deeppyer.deepfry(Img, flares=False)
    #             Img.save("NsRndo.jpg")
    #             Files.append(discord.File("NsRndo.jpg"))
    #             await ctx.message.channel.send(files=Files)
    #             Files.pop(0)
    #             os.remove("NsRndo.jpg")
    #         else: await SendWait(ctx, f"File({C}) isnt a valid image type :sweat:")
    #     except requests.exceptions.MissingSchema: pass

    @commands.group(aliases=["qr", "qrcode"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def QRCodes(self,ctx): pass

    @QRCodes.command(aliases=["make", "create"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def QRmake(self, ctx, *args):
        if not args and not ctx.message.attachments: await SendWait(ctx, "Nothing to QR"); return
        Stuff = []
        Files = []
        if args: Stuff.append(" ".join(args))
        for i in ctx.message.attachments: Stuff.append(i.url)
        for ToQR in Stuff:
            QRcode = qrcode.make(ToQR)
            QRcode.save("QR.png")
            Files.append(discord.File("QR.png"))
            await ctx.message.channel.send(files=Files)
            os.remove("QR.png")

    @QRCodes.command(name="read")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def QRread(self, ctx, *args):
        if args or ctx.message.attachments:
            Attached = []
            if args:
                URLargs = list(args)
                try:
                    for url in URLargs: Attached.append(url)
                except TypeError: pass
            for AtT in ctx.message.attachments: Attached.append(AtT.url)
            Files = []
            C = 0
            for File in Attached:
                try:
                    if requests.head(File).headers.get("content-type").split("/")[0] == "image":
                        C += 1
                        GetURLimg = requests.get(File, allow_redirects=True)
                        open("QrStf.png", "wb").write(GetURLimg.content)
                        Data = cv2.QRCodeDetector().detectAndDecode(cv2.imread("QrStf.png"))[0]
                        try:
                            requests.get(Data)
                            await ctx.message.channel.send(Data)
                        except: await SendWait(ctx, Data)
                        os.remove("QrStf.png")
                    else: await SendWait(ctx, f"File({C}) doesnt contain a qrcode :sweat:")
                except requests.exceptions.MissingSchema: pass
        else: await SendWait(ctx, "No image(s) or link(s) were attached :woozy_face:")

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded!")

async def setup(DClient):
    await DClient.add_cog(Images(DClient))
