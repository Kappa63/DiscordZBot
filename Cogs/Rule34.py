import discord
from discord.ext import commands
from Setup import ChVote, ChNSFW
import asyncio
import random
import rule34

def MakeEmbed(Rule, Type = "R", RuleNum = 0, TotalRules = 0):
    Tags = ", ".join(Rule.tags)
    if len(Tags) > 253:
        RTags = Tags[0:253]
        RTags = RTags + "..."
    else:
        RTags = Tags
    REm = discord.Embed(title = "Rule34", description = RTags, color = 0xdfe31e)
    REm.add_field(name = "Score: ", value = Rule.score)
    if Type == "S":
        REm.add_field(name = f'`Page: {RuleNum+1}/{TotalRules}`', value = "\u200b")
    REm.set_image(url = Rule.file_url)
    REm.set_thumbnail(url = Rule.preview_url)
    if Type == "S":
        REm.set_footer(text = f'{Rule.created_at}\n\nNeed help navigating? zhelp navigation')
    else:
        REm.set_footer(text = Rule.created_at)
    return REm

class Rule34(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.group(name = "rule34", invoke_without_command = True)
    @commands.check(ChNSFW)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def GetRule34(self, ctx, *args):
        if args:
            try:                   
                Rule34 = rule34.Rule34(asyncio.get_event_loop())
                Rule34Choices = await Rule34.getImages(f'-underage -loli -lolicon -lolita -lolita_channel -shota -shotacon {" ".join(args)}')
                ShowRule = random.choice(Rule34Choices)          
            except TypeError:
                await ctx.message.channel.send("Nothing Found :no_mouth:")
                return
            print(ShowRule)
            await ctx.message.channel.send(embed = MakeEmbed(ShowRule))
        
    @GetRule34.command(name = "surf")
    @commands.check(ChVote)
    @commands.check(ChNSFW)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SurfRule34(self, ctx, *args):     
        def ChCHEm(RcM, RuS):
            return RuS.bot == False and RcM.message == RTEm and str(RcM.emoji) in ["⬅️","❌","➡️","#️⃣"]

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

        if args:
            try:                   
                Rule34 = rule34.Rule34(asyncio.get_event_loop())
                Rule34Surf = await Rule34.getImages(f'-underage -loli -lolicon -lolita -lolita_channel -shota -shotacon {" ".join(args)}')       
            except TypeError:
                await ctx.message.channel.send("Nothing Found :no_mouth:")
                return
        else:
            await ctx.message.channel.send("No arguments :no_mouth:")
            return     
        RuleNum = 0
        TotalRules = len(Rule34Surf)
        RTEm = await ctx.message.channel.send(embed = MakeEmbed(Rule34Surf[RuleNum], "S", RuleNum, TotalRules))
        await RTEm.add_reaction("⬅️")
        await RTEm.add_reaction("❌")
        await RTEm.add_reaction("➡️")
        await RTEm.add_reaction("#️⃣")
        while True:
            try:
                Res = await self.DClient.wait_for("reaction_add", check = ChCHEm, timeout = 120) 
                await RTEm.remove_reaction(Res[0].emoji, Res[1])
                if Res[0].emoji == "⬅️" and RuleNum != 0:
                    RuleNum -= 1
                    await RTEm.edit(embed = MakeEmbed(Rule34Surf[RuleNum], "S", RuleNum, TotalRules))
                elif Res[0].emoji == "➡️":
                    if RuleNum < TotalRules-1:
                        RuleNum += 1
                        await RTEm.edit(embed = MakeEmbed(Rule34Surf[RuleNum], "S", RuleNum, TotalRules))
                    else:
                        await RTEm.edit(embed = MakeEmbed(Rule34Surf[RuleNum], "S", RuleNum, TotalRules))
                        await RTEm.remove_reaction("⬅️", self.DClient.user)
                        await RTEm.remove_reaction("❌", self.DClient.user)
                        await RTEm.remove_reaction("➡️", self.DClient.user)
                        await RTEm.remove_reaction("#️⃣", self.DClient.user)
                        break
                elif Res[0].emoji == "#️⃣":
                    if await ChVote(ctx):
                        TemTw = await ctx.message.channel.send('Choose a number to open navigate to page. "c" or "cancel" to exit navigation.')
                        try:
                            ResE = await self.DClient.wait_for("message", check = ChCHEmFN, timeout = 10)
                            await TemTw.delete()
                            await ResE.delete()
                            try:
                                try:
                                    pG = int(ResE.content)
                                    if 0 < pG <= TotalRules-1:
                                        RuleNum = pG-1
                                    elif pG < 1:
                                        RuleNum = 0
                                        pass
                                    else:
                                        RuleNum = TotalRules-1 
                                except TypeError:
                                    pass
                            except ValueError:
                                pass
                            await RTEm.edit(embed = MakeEmbed(Rule34Surf[RuleNum], "S", RuleNum, TotalRules))
                        except asyncio.exceptions.TimeoutError:
                            await TemTw.edit("Request Timeout")
                            await asyncio.sleep(5)
                            await TemTw.delete()
                elif Res[0].emoji == "❌":
                    await RTEm.edit(embed = MakeEmbed(Rule34Surf[RuleNum], "S", RuleNum, TotalRules))
                    await RTEm.remove_reaction("⬅️", self.DClient.user)
                    await RTEm.remove_reaction("❌", self.DClient.user)
                    await RTEm.remove_reaction("➡️", self.DClient.user)
                    await RTEm.remove_reaction("#️⃣", self.DClient.user)
                    break
            except asyncio.TimeoutError:
                await RTEm.edit(embed = MakeEmbed(Rule34Surf[RuleNum], "S", RuleNum, TotalRules))
                await RTEm.remove_reaction("⬅️", self.DClient.user)
                await RTEm.remove_reaction("❌", self.DClient.user)
                await RTEm.remove_reaction("➡️", self.DClient.user)
                await RTEm.remove_reaction("#️⃣", self.DClient.user)
                break

def setup(DClient):
    DClient.add_cog(Rule34(DClient))