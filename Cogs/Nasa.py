import discord
import random
import requests
from discord.ext import commands
from CBot import ChVote

class Nasa(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.command(name = "apod")
    @commands.check(ChVote)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def GetNasaApod(ctx):
        NASAapod = requests.get("https://api.nasa.gov/planetary/apod?api_key=0dsw3SiQmYCeNnwKZROSQIyrcZqjoDzMBo4ggCwS", headers = {"Accept": "application/json"})
        JSONapod = NASAapod.json()
        if len(JSONapod["explanation"]) > 1021:
            Explanation = JSONapod["explanation"][0:1021]
            Explanation = Explanation + "..."
        else:
            Explanation = JSONapod["explanation"]
        DEm = discord.Embed(title = JSONapod["title"], description = f'Date {JSONapod["date"]}', color = 0xa9775a)
        DEm.add_field(name = "Explanation:", value = Explanation, inline = False)
        DEm.set_image(url = JSONapod["hdurl"])
        await ctx.message.channel.send(embed = DEm)

    @DClient.command(name = "nasa")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def GetNasaMars(ctx):
        def MakeEmbed(MarsImagesCH, ImageNum, ImagesExtracted):
            NEm = discord.Embed(title = "Mars", description = "By: Curiosity Rover (NASA)", color = 0xcd5d2e)
            NEm.set_thumbnail(url = "https://i.imgur.com/xmSmG0f.jpeg")
            NEm.add_field(name = "Camera:", value = MarsImagesCH[ImageNum]["camera"]["full_name"], inline = True)
            NEm.add_field(name = "Taken on:", value = MarsImagesCH[ImageNum]["earth_date"], inline = True)
            NEm.add_field(name = f'`Image: {ImageNum+1}/{ImagesExtracted}`', value = "\u200b", inline = False)
            NEm.set_image(url = MarsImagesCH[ImageNum]["img_src"])
            return NEm

        def ChCHEm(RcM, RuS):
            return RuS.bot == False and RcM.message == NTEm and str(RcM.emoji) in ["⬅️","❌","➡️","#️⃣"]

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

        NASAmars = requests.get("https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key=0dsw3SiQmYCeNnwKZROSQIyrcZqjoDzMBo4ggCwS", headers = {"Accept": "application/json"})
        JSONmars = NASAmars.json()
        MarsImagesCH = random.sample(JSONmars["photos"], k = 25)
        ImagesExtracted = len(MarsImagesCH)
        ImageNum = 0
        NTEm = await ctx.message.channel.send(embed = MakeEmbed(MarsImagesCH, ImageNum, ImagesExtracted))
        await NTEm.add_reaction("⬅️")
        await NTEm.add_reaction("❌")
        await NTEm.add_reaction("➡️")
        await NTEm.add_reaction("#️⃣")
        while True:
            try:
                Res = await DClient.wait_for("reaction_add", check = ChCHEm, timeout = 120) 
                await NTEm.remove_reaction(Res[0].emoji, Res[1])
                if Res[0].emoji == "⬅️" and ImageNum != 0:
                    ImageNum -= 1
                    await NTEm.edit(embed = MakeEmbed(MarsImagesCH, ImageNum, ImagesExtracted))
                elif Res[0].emoji == "➡️":
                    if ImageNum < ImagesExtracted-1:
                        ImageNum += 1
                        await NTEm.edit(embed = MakeEmbed(MarsImagesCH, ImageNum, ImagesExtracted))
                    else:
                        await NTEm.edit(embed = MakeEmbed(MarsImagesCH, ImageNum, ImagesExtracted))
                        await NTEm.remove_reaction("⬅️", DClient.user)
                        await NTEm.remove_reaction("❌", DClient.user)
                        await NTEm.remove_reaction("➡️", DClient.user)
                        await NTEm.remove_reaction("#️⃣", DClient.user)
                        break
                elif Res[0].emoji == "#️⃣":
                    if ChPatreonFu(ctx) or (await TClient.get_user_vote(ctx.author.id)):
                        TemTw = await ctx.message.channel.send('Choose a number to open navigate to page. "c" or "cancel" to exit navigation.\n\n*The Navigation closes automatically after 10sec of inactivity.*')
                        try:
                            ResE = await DClient.wait_for("message", check = ChCHEmFN, timeout = 10)
                            await TemTw.delete()
                            await ResE.delete()
                            try:
                                try:
                                    pG = int(ResE.content)
                                    if 0 < pG <= ImagesExtracted-1:
                                        ImageNum = pG-1
                                    elif pG < 1:
                                        ImageNum = 0
                                        pass
                                    else:
                                        ImageNum = ImagesExtracted-1 
                                except TypeError:
                                    pass
                            except ValueError:
                                pass
                            await NTEm.edit(embed = MakeEmbed(MarsImagesCH, ImageNum, ImagesExtracted))
                        except asyncio.exceptions.TimeoutError:
                            await TemTw.edit("Request Timeout")
                            await asyncio.sleep(5)
                            await TemTw.delete()
                    else:
                        TemS = await ctx.message.channel.send("Instant navigation to image is only for voters or Patreon Supporters. \n:robot: zvote or zpatreon to learn more. :robot:")
                        await asyncio.sleep(5)
                        await TemS.delete()
                elif Res[0].emoji == "❌":
                    await NTEm.edit(embed = MakeEmbed(MarsImagesCH, ImageNum, ImagesExtracted))
                    await NTEm.remove_reaction("⬅️", DClient.user)
                    await NTEm.remove_reaction("❌", DClient.user)
                    await NTEm.remove_reaction("➡️", DClient.user)
                    await NTEm.remove_reaction("#️⃣", DClient.user)
                    break
            except asyncio.TimeoutError:
                await NTEm.edit(embed = MakeEmbed(MarsImagesCH, ImageNum, ImagesExtracted))
                await NTEm.remove_reaction("⬅️", DClient.user)
                await NTEm.remove_reaction("❌", DClient.user)
                await NTEm.remove_reaction("➡️", DClient.user)
                await NTEm.remove_reaction("#️⃣", DClient.user)
                break

def setup(DClient):
    DClient.add_cog(Nasa(DClient))