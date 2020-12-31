import discord
from discord.ext import commands
import requests
from Setup import Imgur
from Setup import ChVoteUser
from Setup import ErrorEmbeds
from pdf2image import convert_from_path
import random
from PIL import Image
import deeppyer
import asyncio
import os
import qrcode


class Image(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.command(aliases=["kitten", "kitty", "cat"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RandomCat(self, ctx):
        CatGot = requests.get(
            "https://aws.random.cat/meow", headers={"Accept": "application/json"}
        )
        CatJSON = CatGot.json()
        CEm = discord.Embed(title="Meow", color=0xA3D7C1)
        CEm.set_image(url=CatJSON["file"])
        await ctx.message.channel.send(embed=CEm)

    @commands.command(aliases=["doggo", "dog", "pupper", "puppy"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RandomDoggo(self, ctx):
        DoggoGot = requests.get(
            "https://random.dog/woof.json", headers={"Accept": "application/json"}
        )
        DoggoJSON = DoggoGot.json()
        DEm = discord.Embed(title="Woof Woof", color=0xFF3326)
        DEm.set_image(url=DoggoJSON["url"])
        await ctx.message.channel.send(embed=DEm)

    @commands.command(name="fox")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RandomFox(self, ctx):
        FoxGot = requests.get(
            "https://randomfox.ca/floof/", headers={"Accept": "application/json"}
        )
        FoxJSON = FoxGot.json()
        FEm = discord.Embed(title="What does the fox say?", color=0x9DAA45)
        FEm.set_image(url=FoxJSON["image"])
        await ctx.message.channel.send(embed=FEm)

    @commands.command(aliases=["food", "dishes", "dish"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RandomDishes(self, ctx):
        Hungry = requests.get(
            "https://foodish-api.herokuapp.com/api/",
            headers={"Accept": "application/json"},
        ).json()
        FEm = discord.Embed(title="Hungry?", color=0xDE8761)
        FEm.set_image(url=Hungry["image"])
        await ctx.message.channel.send(embed=FEm)

    @commands.command(aliases=["taylor", "tswift", "taylorswift"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RandomDishes(self, ctx):
        TaylorImage = requests.get(
            "https://api.taylor.rest/image", headers={"Accept": "application/json"}
        ).json()
        TaylorQuote = requests.get(
            "https://api.taylor.rest/", headers={"Accept": "application/json"}
        ).json()
        TEm = discord.Embed(
            title="Taylor Swift", description=TaylorQuote["quote"], color=0xD29EC1
        )
        TEm.set_image(url=TaylorImage["url"])
        await ctx.message.channel.send(embed=TEm)

    @commands.command(name="pdf")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def PDFreader(self, ctx, *args):
        def EmbTI(PDFname, PDFimages, PDFpage, PDFcache):
            try:
                ImgurLink = PDFcache[PDFpage]
                print("Cached...")
                CHcache = False
            except IndexError:
                print("Uploading...")
                PDFimages[PDFpage].save(f"{PDFname}.jpg", "JPEG")
                ImgurLink = Imgur.upload_from_path(f"{PDFname}.jpg")["link"]
                CHcache = True
            PEm = discord.Embed(title="PDF Viewer")
            PEm.set_image(url=ImgurLink)
            PEm.add_field(name=f"```{PDFpage+1}/{len(PDFimages)}```", value="\u200b")
            PEm.set_footer(text="Need help navigating? zhelp navigation")
            return CHcache, ImgurLink, PEm

        def ChCHEm(RcM, RuS):
            return (
                RuS.bot == False
                and RcM.message == PTEm
                and str(RcM.emoji) in ["⬅️", "❌", "➡️", "#️⃣"]
            )

        def ChCHEmFN(MSg):
            MesS = MSg.content.lower()
            RsT = False
            try:
                if int(MSg.content):
                    RsT = True
            except ValueError:
                if (MesS == "cancel") or (MesS == "c"):
                    RsT = True
            return (
                MSg.guild.id == ctx.guild.id
                and MSg.channel.id == ctx.channel.id
                and RsT
            )

        if (len(ctx.message.attachments) == 1 and len(args) == 0) or (
            len(ctx.message.attachments) == 0 and len(args) == 1
        ):
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
                    ChPDF = (
                        requests.head(GetPDF).headers.get("content-type").split("/")[1]
                    )
                    if ChPDF == "pdf":
                        RanLetters = "ioewsahkzcldnpq"
                        PDFname = "".join(
                            (random.choice(RanLetters) for i in range(10))
                        )
                        PDFcontent = requests.get(GetPDF, allow_redirects=True)
                        open(f"{PDFname}.pdf", "wb").write(PDFcontent.content)
                        PDFimages = convert_from_path(
                            f"{PDFname}.pdf", 500, last_page=40
                        )
                        print(PDFimages)
                        PDFpage = 0
                        PDFcache = []
                        PTEm = await ctx.message.channel.send(
                            embed=discord.Embed(
                                title="Uploading Page...",
                                description="After upload a page will no longer be uploaded again (Faster navigation to page)",
                            )
                        )
                        CHcache, ImgurLink, PEm = EmbTI(
                            PDFname, PDFimages, PDFpage, PDFcache
                        )
                        if CHcache:
                            PDFcache.append(ImgurLink)
                        await PTEm.edit(embed=PEm)
                        await PTEm.add_reaction("⬅️")
                        await PTEm.add_reaction("❌")
                        await PTEm.add_reaction("➡️")
                        await PTEm.add_reaction("#️⃣")
                        while True:
                            try:
                                ReaEm = await self.DClient.wait_for(
                                    "reaction_add", check=ChCHEm, timeout=120
                                )
                                await PTEm.remove_reaction(ReaEm[0].emoji, ReaEm[1])
                                if ReaEm[0].emoji == "⬅️" and PDFpage != 0:
                                    PDFpage -= 1
                                    CHcache, ImgurLink, PEm = EmbTI(
                                        PDFname, PDFimages, PDFpage, PDFcache
                                    )
                                    if CHcache:
                                        PDFcache.append(ImgurLink)
                                    await PTEm.edit(embed=PEm)
                                elif ReaEm[0].emoji == "➡️":
                                    if PDFpage < len(PDFimages) - 1:
                                        PDFpage += 1
                                        CHcache, ImgurLink, PEm = EmbTI(
                                            PDFname, PDFimages, PDFpage, PDFcache
                                        )
                                        if CHcache:
                                            PDFcache.append(ImgurLink)
                                        await PTEm.edit(embed=PEm)
                                    else:
                                        await PTEm.remove_reaction(
                                            "⬅️", self.DClient.user
                                        )
                                        await PTEm.remove_reaction(
                                            "❌", self.DClient.user
                                        )
                                        await PTEm.remove_reaction(
                                            "➡️", self.DClient.user
                                        )
                                        await PTEm.remove_reaction(
                                            "#️⃣", self.DClient.user
                                        )
                                        os.remove(f"{PDFname}.jpg")
                                        os.remove(f"{PDFname}.pdf")
                                        break
                                elif ReaEm[0].emoji == "#️⃣":
                                    if await ChVoteUser(ReaEm[1].id):
                                        NavNote = await ctx.message.channel.send(
                                            'Choose a number to open navigate to page. "c" or "cancel" to exit navigation.'
                                        )
                                        try:
                                            ResE = await self.DClient.wait_for(
                                                "message", check=ChCHEmFN, timeout=10
                                            )
                                            await NavNote.delete()
                                            await ResE.delete()
                                            try:
                                                try:
                                                    pG = int(ResE.content)
                                                    if 0 < pG <= len(PDFimages) - 1:
                                                        PDFpage = pG - 1
                                                    elif pG < 1:
                                                        PDFpage = 0
                                                        pass
                                                    else:
                                                        PDFpage = len(PDFimages) - 1
                                                except TypeError:
                                                    pass
                                            except ValueError:
                                                pass
                                            CHcache, ImgurLink, PEm = EmbTI(
                                                PDFname, PDFimages, PDFpage, PDFcache
                                            )
                                            if CHcache:
                                                PDFcache.append(ImgurLink)
                                            await PTEm.edit(embed=PEm)
                                        except asyncio.TimeoutError:
                                            await NavNote.edit("Request Timeout")
                                            await asyncio.sleep(5)
                                            await NavNote.delete()
                                    else:
                                        await ctx.message.channel.send(
                                            embed=ErrorEmbeds("Vote")
                                        )
                                elif ReaEm[0].emoji == "❌":
                                    await PTEm.remove_reaction("⬅️", self.DClient.user)
                                    await PTEm.remove_reaction("❌", self.DClient.user)
                                    await PTEm.remove_reaction("➡️", self.DClient.user)
                                    await PTEm.remove_reaction("#️⃣", self.DClient.user)
                                    os.remove(f"{PDFname}.jpg")
                                    os.remove(f"{PDFname}.pdf")
                                    break
                            except asyncio.TimeoutError:
                                await PTEm.remove_reaction("⬅️", self.DClient.user)
                                await PTEm.remove_reaction("❌", self.DClient.user)
                                await PTEm.remove_reaction("➡️", self.DClient.user)
                                await PTEm.remove_reaction("#️⃣", self.DClient.user)
                                os.remove(f"{PDFname}.jpg")
                                os.remove(f"{PDFname}.pdf")
                                break
                except requests.exceptions.MissingSchema:
                    await ctx.message.channel.send("Not a PDF :woozy_face:")
        else:
            await ctx.message.channel.send("No or too many attachments :woozy_face:")

    @commands.group(aliases=["fry", "deepfry"], invoke_without_command=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ImageFrier(self, ctx, *args):
        if args or len(ctx.message.attachments) > 0:
            Attached = []
            if args:
                URLargs = " ".join(args).split(" ")
                try:
                    for url in URLargs:
                        Attached.append(url)
                except TypeError:
                    pass
            if len(ctx.message.attachments) > 0:
                for AtT in ctx.message.attachments:
                    Attached.append(AtT.url)
            Files = []
            C = 0
            for File in Attached:
                try:
                    if (
                        requests.head(File).headers.get("content-type").split("/")[0]
                        == "image"
                    ):
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
                    else:
                        await ctx.message.channel.send(
                            f"File({C}) isnt a valid image type :sweat:"
                        )
                except requests.exceptions.MissingSchema:
                    pass
        else:
            await ctx.message.channel.send(
                "No image(s) or link(s) were attached :woozy_face:"
            )

    @ImageFrier.command(name="profile")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ProfileFrier(self, ctx):
        if len(ctx.message.mentions) > 0:
            Profile = str((ctx.message.mentions[0]).avatar_url)
        else:
            Profile = str(ctx.author.avatar_url)
        try:
            Files = []
            C = 0
            if (
                requests.head(Profile).headers.get("content-type").split("/")[0]
                == "image"
            ):
                C += 1
                GetURLimg = requests.get(Profile, allow_redirects=True)
                open("NsRndo.jpg", "wb").write(GetURLimg.content)
                Img = Image.open("NsRndo.jpg")
                Img = await deeppyer.deepfry(Img, flares=False)
                Img.save("NsRndo.jpg")
                Files.append(discord.File("NsRndo.jpg"))
                await ctx.message.channel.send(files=Files)
                Files.pop(0)
                os.remove("NsRndo.jpg")
            else:
                await ctx.message.channel.send(
                    f"File({C}) isnt a valid image type :sweat:"
                )
        except requests.exceptions.MissingSchema:
            pass

    @commands.command(aliases=["qr","qrcode"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def QRmake(self, ctx, *args):
        if args:
            Files = []
            ToQR = " ".join(args).split(" ")
            QRcode = qrcode.make(ToQR)
            QRcode.save("QR.png")
            Files.append(discord.File("QR.png"))
            await ctx.message.channel.send(files=Files)
            os.remove("QR.png")
        else:
            await ctx.message.channel.send("Nothing to QR")


def setup(DClient):
    DClient.add_cog(Image(DClient))