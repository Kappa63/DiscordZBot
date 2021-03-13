from discord.ext import commands
import discord
import FuncMon
from Setup import Col, ColT
from Setup import ChAdmin, ChSer, RemoveExtra, SendWait, ChSerGuild
import asyncio
import re


class MongoDB(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.command(name="setup")
    @commands.check(ChAdmin)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SMsg(self, ctx):
        if not ColT.count_documents({"IDg":str(ctx.guild.id)}):ColT.insert_one({"IDg":str(ctx.guild.id)})
        await SendWait(ctx, "Setup Complete!")
        
        #!! DEPRECATED Setup
        #! if (
        #!     Col.count_documents(
        #!         {"IDd": "GuildInfo", "IDg": str(ctx.guild.id), "Setup": "Done"}
        #!     )
        #!     == 0
        #! ):
        #!     Col.insert_one(
        #!         {"IDd": "GuildInfo", "IDg": str(ctx.guild.id), "Setup": "Done"}
        #!     )
        #!     for Pid in ctx.guild.members:
        #!         if Pid.bot == False:
        #!             if (
        #!                 Col.count_documents(
        #!                     {"IDd": str(Pid.id), "IDg": str(ctx.guild.id)}
        #!                 )
        #!                 == 0
        #!             ):
        #!                 Col.insert_one({"IDd": str(Pid.id), "IDg": str(ctx.guild.id)})
        #!                 DbB = Col.find({"IDd": "GuildInfo", "IDg": str(ctx.guild.id)})
        #!                 for i in DbB:
        #!                     Kyes = i.keys()
        #!                 for Wp in Kyes:
        #!                     FuncMon.DbAdd(
        #!                         Col,
        #!                         {"IDd": str(Pid.id), "IDg": str(ctx.guild.id)},
        #!                         Wp,
        #!                         0,
        #!                     )
        #!     await SendWait(
        #!         ctx,
        #!         ":partying_face: Setup complete, you can now use tracking commands :partying_face:",
        #!     )
        #! else:
        #!     await SendWait(
        #!         ctx, ":partying_face: This server is already setup :partying_face:"
        #!     )

    @commands.command(name="update")
    @commands.check(ChSer)
    @commands.check(ChAdmin)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SUmsg(self, ctx):
        Members = [str(i.id) for i in ctx.guild.members if not i.bot]
        Get = ColT.find({"IDg":str(ctx.guild.id)})[0]
        Stuff = [i for i in Get.keys() if i not in ["_id", "IDg"]]
        Missing = [i for i in Stuff if len(Get[i]) < len(Members)]
        for i in Missing:
            for j in Members:
                if j not in Get[i].keys(): ColT.update_one(Get, {"$set": {f'{i}.{j}':0}})
        await SendWait(ctx, "Up to Date")
        
        #!! DEPRECATED Update
        #! xNumP = 0
        #! for i in ctx.guild.members:
        #!     if not i.bot:
        #!         xNumP += 1
        #! NumAdD = 0
        #! if xNumP + 1 != Col.count_documents({"IDg": str(ctx.guild.id)}):
        #!     for Pid in ctx.guild.members:
        #!         if Pid.bot == False:
        #!             if (
        #!                 Col.count_documents(
        #!                     {"IDd": str(Pid.id), "IDg": str(ctx.guild.id)}
        #!                 )
        #!                 == 0
        #!             ):
        #!                 Col.insert_one({"IDd": str(Pid.id), "IDg": str(ctx.guild.id)})
        #!                 NumAdD += 1
        #!                 DbB = Col.find({"IDd": "GuildInfo", "IDg": str(ctx.guild.id)})
        #!                 for i in DbB:
        #!                     Kyes = i.keys()
        #!                 for Wp in Kyes:
        #!                     FuncMon.DbAdd(
        #!                         Col,
        #!                         {"IDd": str(Pid.id), "IDg": str(ctx.guild.id)},
        #!                         Wp,
        #!                         0,
        #!                     )
        #!     await SendWait(
        #!         ctx,
        #!         f":partying_face: The server info has been updated (added {NumAdD} members) :partying_face:",
        #!     )
        #! else:
        #!     await SendWait(
        #!         ctx, ":partying_face: This server is already up to date :partying_face:"
        #!     )

    @commands.command(name="add")
    @commands.check(ChAdmin)
    @commands.check(ChSer)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def AWord(self, ctx, *args):
        Word = re.sub(r"\.", "\u2024", ' '.join(args))
        Word = re.sub(r"\$", "\u00A4", Word)
        Get = ColT.find({"IDg":str(ctx.guild.id)})[0]
        if Word not in Get and Word not in ["_id", "IDg"]:    
            E = {}
            [E.update({str(Person.id):0}) for Person in ctx.guild.members if not Person.bot]
            ColT.update_one(Get, {"$set": {Word:E}})
            await SendWait(ctx, "Added!")
            return
        await SendWait(ctx, "Already Exists!")

        #!! DEPRECATED Add Word
        #! WorA = " ".join(args)
        #! if FuncMon.DbAdd(Col, {"IDd": "GuildInfo", "IDg": str(ctx.guild.id)}, WorA, 0):
        #!     Msg = f'"{WorA}" ADDED :thumbsup:'
        #!     FuncMon.DbAppendRest(
        #!         Col,
        #!         {"IDg": str(ctx.guild.id)},
        #!         {"IDd": "GuildInfo", "IDg": str(ctx.guild.id)},
        #!         WorA,
        #!         0,
        #!         "a",
        #!     )
        #! else:
        #!     Msg = f'"{WorA}" ALREADY EXIST :confused:'
        #! await SendWait(ctx, Msg)

    @commands.command(aliases=["rem", "remove"])
    @commands.check(ChAdmin)
    @commands.check(ChSer)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RWord(self, ctx, *args):
        Word = re.sub(r"\.", "\u2024", ' '.join(args))
        Word = re.sub(r"\$", "\u00A4", Word)
        Get = ColT.find({"IDg":str(ctx.guild.id)})[0]
        if Word in Get and Word not in ["_id", "IDg"]:    
            ColT.update_one(Get, {"$unset": {Word: ""}})
            await SendWait(ctx, "Removed!")
            return
        await SendWait(ctx, "Doesn't Exist!")

        #!! DEPRECATED Remove Word
        #! WorA = " ".join(args)
        #! if FuncMon.DbRem(Col, {"IDd": "GuildInfo", "IDg": str(ctx.guild.id)}, WorA):
        #!     Msg = f'"{WorA}" REMOVED :thumbsup:'
        #!     FuncMon.DbAppendRest(
        #!         Col,
        #!         {"IDg": str(ctx.guild.id)},
        #!         {"IDd": "GuildInfo", "IDg": str(ctx.guild.id)},
        #!         WorA,
        #!         0,
        #!         "r",
        #!     )
        #! else:
        #!     Msg = f'"{WorA}" DOESNT EXIST :confused:'
        #! await SendWait(ctx, Msg)

    @commands.command(name="list")
    @commands.check(ChSer)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def LWord(self, ctx):
        LEm = discord.Embed(title="Server List",description="Words/Phrases being tracked",color=0xF59542)
        Get = ColT.find({"IDg":str(ctx.guild.id)})[0]
        Stuff = [i for i in Get.keys() if i not in ["_id", "IDg"]]
        for i in Stuff:
            LEm.add_field(name=i, value="\u200b", inline=True)
        await ctx.message.channel.send(embed=LEm)

        #!! DEPRECATED List Words
        #! LEm = discord.Embed(
        #!     title="Server List",
        #!     description="Words/Phrases being tracked",
        #!     color=0xF59542,
        #! )
        #! DbB = Col.find({"IDd": "GuildInfo", "IDg": str(ctx.guild.id)})
        #! for i in DbB:
        #!     Kyes = i.keys()
        #! for Wp in Kyes:
        #!     if Wp == "_id" or Wp == "IDd" or Wp == "IDg" or Wp == "Setup":
        #!         pass
        #!     else:
        #!         LEm.add_field(name=Wp, value="\u200b", inline=True)
        #! await ctx.message.channel.send(embed=LEm)

    @commands.command(name="clear")
    @commands.check(ChAdmin)
    @commands.check(ChSer)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ReAll(self, ctx):
        def ChCHEm(RcM, RuS):
            return (
                RuS.bot == False
                and RcM.message == ReSConF
                and str(RcM.emoji) in ["✅", "❌"]
            )

        ResEmF = discord.Embed(
            title="Clear ALL server data?",
            description="This is ```IRREVERSIBLE```",
            color=0xF59542,
        )
        ResEmF.set_footer(text="*The Clear request timesout in 10secs.*")
        ReSConF = await ctx.message.channel.send(embed=ResEmF)
        await ReSConF.add_reaction("❌")
        await ReSConF.add_reaction("✅")
        try:
            ReaEm = await self.DClient.wait_for(
                "reaction_add", check=ChCHEm, timeout=10
            )
            await ReSConF.remove_reaction("❌", self.DClient.user)
            await ReSConF.remove_reaction("✅", self.DClient.user)
            if ReaEm[0].emoji == "❌":
                await ReSConF.edit(
                    embed=discord.Embed(
                        title="Cancelled :thumbsup:",
                        description="Nothing was removed",
                        color=0xF59542,
                    )
                )
            elif ReaEm[0].emoji == "✅":
                ColT.delete_one({"IDg":str(ctx.guild.id)})

                #!! DEPRECATED Remove Guild
                #! if (
                #!     Col.count_documents(
                #!         {"IDd": "GuildInfo", "IDg": str(guild.id), "Setup": "Done"}
                #!     )
                #!     > 0
                #! ):
                #!     DbB = Col.find({"IDg": str(guild.id)})
                #!     for DbG in DbB:
                #!         Col.delete_one(DbG)
        except asyncio.TimeoutError:
            await ReSConF.remove_reaction("❌", self.DClient.user)
            await ReSConF.remove_reaction("✅", self.DClient.user)
            await ReSConF.edit(
                embed=discord.Embed(
                    title="Timeout :alarm_clock:",
                    description="Nothing was removed",
                    color=0xF59542,
                )
            )

    @commands.command(name="stats")
    @commands.check(ChSer)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def IMsg(self, ctx, *args):
        Get = ColT.find({"IDg":str(ctx.guild.id)})[0]
        Stuff = [i for i in Get.keys() if i not in ["_id", "IDg"]]
        Mentions = ctx.message.mentions
        args = list(args)
        MentionedUser = False
        if len(Mentions) > 1:
            await SendWait(ctx, "Too Many Mentions")
            return
        if Mentions:
            Mentioned = Mentions[0]
            if Mentioned.mention[2] == "!":
                args.remove(Mentioned.mention)
                MentionedUser = True
            else:
                await SendWait(ctx, "Mentioned User Is A Bot")
                return
        if not args:
            Stuff = [i for i in Get.keys() if i not in ["_id", "IDg"]]
            Person = Mentioned if MentionedUser else ctx.author
            IEm = discord.Embed(title=Person.display_name, description="Word Stats", color=0x3252A8)
            for Word in Stuff: IEm.add_field(name=Word, value=f"{Get[Word][str(Person.id)]:,}", inline=True)
            await ctx.message.channel.send(embed=IEm)
        else:
            Word = re.sub(r"\.", "\u2024", ' '.join(args))
            Word = re.sub(r"\$", "\u00A4", Word)
            Person = Mentioned if MentionedUser else ctx.author
            if Word in Get and Word not in ["_id", "IDg"]:
                IEm = discord.Embed(title=Person.display_name, description="All Stats", color=0x3252A8)
                IEm.add_field(name=Word, value=f"{Get[Word][str(Person.id)]:,}", inline=True)
                await ctx.message.channel.send(embed=IEm)
            else:
                await SendWait(ctx, "Word Doesn't Exist")
                
        #!! DEPRECATED Stats
        #! isBot = False
        #! if ctx.message.mentions:
        #!     if (ctx.message.mentions[0].bot == False and (f"<@!{ctx.message.mentions[0].id}>") == args[0]):
        #!         AUmN = ctx.message.mentions[0]
        #!         aRGu = list(args)
        #!         aRGu.pop(0)
        #!     elif ctx.message.mentions[0].bot == True:
        #!         isBot = True
        #! else:
        #!     AUmN = ctx.author
        #!     aRGu = list(args)
        #! if isBot == False:
        #!     Num = 0
        #!     Enput = " ".join(aRGu)
        #!     DbB = Col.find({"IDd": "GuildInfo", "IDg": str(ctx.guild.id)})
        #!     OSfDb = Col.find({"IDd": str(AUmN.id), "IDg": str(ctx.guild.id)})
        #!     for i in DbB:
        #!         Kyes = i.keys()
        #!     if (Enput == "") or (Enput == " "):
        #!         IEm = discord.Embed(
        #!             title=AUmN.display_name, description="All stats", color=0x3252A8
        #!         )
        #!         for Wp in Kyes:
        #!             OSfDb = Col.find({"IDd": str(AUmN.id), "IDg": str(ctx.guild.id)})
        #!             if Wp == "_id" or Wp == "IDd" or Wp == "IDg" or Wp == "Setup":
        #!                 pass
        #!             else:
        #!                 for j in OSfDb:
        #!                     Num = j[Wp]
        #!                 IEm.add_field(name=Wp, value=f"{Num:,}", inline=True)
        #!         await ctx.message.channel.send(embed=IEm)
        #!     elif Enput in Kyes:
        #!         IEm = discord.Embed(
        #!             title=AUmN.display_name, description="Word stats", color=0x3252A8
        #!         )
        #!         for j in OSfDb:
        #!             Num = j[Enput]
        #!         IEm.add_field(name=Enput, value=f"{Num:,}", inline=True)
        #!         await ctx.message.channel.send(embed=IEm)
        #!     else:
        #!         await SendWait(ctx, "That word doesnt exist yet! :confused:")
        #! else:
        #!     await SendWait(ctx, "Cannot check a bot's stats :confused:")

    @commands.command(name="top")
    @commands.check(ChSer)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ToTMsg(self, ctx, *args):
        Get = ColT.find({"IDg":str(ctx.guild.id)})[0]
        if args:
            Word = re.sub(r"\.", "\u2024", ' '.join(args))
            Word = re.sub(r"\$", "\u00A4", Word)
            if Word in Get and Word not in ["_id", "IDg"]:
                People = Get[Word]
                Tops = sorted(People, key=People.get, reverse = True)[:3]
                IEm = discord.Embed(title=ctx.guild.name, description=f"Leaderboard for {Word}", color=0x3252A8)
                x = 0
                for i in Tops:
                    x+=1
                    Person = ctx.guild.get_member(int(i))
                    Name = Person.nick if Person.nick else Person.name
                    IEm.add_field(name=f"**`{x}. {Name}:`** {Word} = {People[i]:,}", value="\u200b", inline=False)
                await ctx.message.channel.send(embed=IEm)
            else:
                await SendWait(ctx, "Word Doesn't Exist")
        else:
            Stuff = [i for i in Get.keys() if i not in ["_id", "IDg"]]
            All = []
            for i in Stuff:
                for k,v in Get[i].items():
                    All.append({i:{k:v}}) 
            Tops = sorted(All, key=lambda x: list(list(x.values())[0].values())[0], reverse = True)[:3]
            IEm = discord.Embed(title=ctx.guild.name, description="Leaderboard", color=0x3252A8)
            x = 0
            for i in Tops:
                x+=1
                Pid = int(list(list(i.values())[0].keys())[0])
                Word = list(i.keys())[0]
                Num = list(list(i.values())[0].values())[0]
                Person = ctx.guild.get_member(Pid)
                Name = Person.nick if Person.nick else Person.name
                IEm.add_field(name=f"**`{x}. {Name}:`** {Word} = {Num:,}", value="\u200b", inline=False)
            await ctx.message.channel.send(embed=IEm)
            
        #!! DEPRECATED Top Words
        #! def GetNVa(DiDIV, WtRt=0):
        #!     for Mks in DiDIV:
        #!         for MjsD in DiDIV[Mks]:
        #!             if WtRt == 1:
        #!                 return MjsD
        #!             else:
        #!                 return DiDIV[Mks][MjsD]
        #! Top = []
        #! Enput = " ".join(args)
        #! DbB = Col.find({"IDd": "GuildInfo", "IDg": str(ctx.guild.id)})
        #! SrtI = await ctx.message.channel.send(
        #!     embed=discord.Embed(
        #!         title=":mag: Fetching...", description="\u200b", color=0x3252A8
        #!     )
        #! )
        #! for i in DbB:
        #!     Kyes = i.keys()
        #! if not args:
        #!     IEm = discord.Embed(
        #!         title=ctx.guild.name, description="Leaderboard", color=0x3252A8
        #!     )
        #!     for Wp in Kyes:
        #!         OSfDb = Col.find({"IDg": str(ctx.guild.id)})
        #!         if Wp == "_id" or Wp == "IDd" or Wp == "IDg" or Wp == "Setup":
        #!             pass
        #!         else:
        #!             for j in OSfDb:
        #!                 if j["IDd"] != "GuildInfo":
        #!                     Top.append({j["IDd"]: {Wp: j[Wp]}})
        #!     Top = sorted(Top, key=GetNVa)
        #!     for i in range(1, 4):
        #!         x = int(list(Top[-i].keys())[0])
        #!         if (ctx.guild.get_member(x)).nick:
        #!             Cr = (ctx.guild.get_member(x)).nick
        #!         else:
        #!             Cr = (ctx.guild.get_member(x)).name
        #!         IEm.add_field(
        #!             name=f"**`{i}. {Cr}:`** {GetNVa(Top[-i], 1)} = {GetNVa(Top[-i]):,}",
        #!             value="\u200b",
        #!             inline=False,
        #!         )
        #!     await SrtI.edit(embed=IEm)
        #! elif Enput in Kyes:
        #!     IEm = discord.Embed(
        #!         title=ctx.guild.name,
        #!         description=f"Leaderboard for {Enput}",
        #!         color=0x3252A8,
        #!     )
        #!     OSfDb = Col.find({"IDg": str(ctx.guild.id)})
        #!     for j in OSfDb:
        #!         if j["IDd"] != "GuildInfo":
        #!             Top.append({j["IDd"]: {Enput: j[Enput]}})
        #!     Top = sorted(Top, key=GetNVa)
        #!     for i in range(1, 4):
        #!         x = int(list(Top[-i].keys())[0])
        #!         if (ctx.guild.get_member(x)).nick:
        #!             Cr = (ctx.guild.get_member(x)).nick
        #!         else:
        #!             Cr = (ctx.guild.get_member(x)).name
        #!         IEm.add_field(
        #!             name=f"**`{i}. {Cr}:`** {GetNVa(Top[-i], 1)} = {GetNVa(Top[-i]):,}",
        #!             value="\u200b",
        #!             inline=False,
        #!         )
        #!     await SrtI.edit(embed=IEm)
        #! else:
        #!     await SrtI.edit(
        #!         embed=discord.Embed(
        #!             title="That word doesnt exist yet :confused:",
        #!             description="\u200b",
        #!             color=0x3252A8,
        #!         )
        #!     )

    @commands.command(name="total")
    @commands.check(ChSer)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def TMsg(self, ctx, *args):
        Get = ColT.find({"IDg":str(ctx.guild.id)})[0]
        if args:
            Word = re.sub(r"\.", "\u2024", ' '.join(args))
            Word = re.sub(r"\$", "\u00A4", Word)
            if Word in Get and Word not in ["_id", "IDg"]:
                IEm = discord.Embed(title=ctx.guild.name, description=f"Total times {Word} was repeated", color=0x3252A8)
                IEm.add_field(name=Word, value=f"{sum(Get[Word].values()):,}", inline=True)
                await ctx.message.channel.send(embed=IEm)
            else:
                await SendWait(ctx, "Word Doesn't Exist")
        else:
            Stuff = [i for i in Get.keys() if i not in ["_id", "IDg"]]
            IEm = discord.Embed(title=ctx.guild.name, description="Total times repeated", color=0x3252A8)
            for Word in Stuff: IEm.add_field(name=Word, value=f"{sum(Get[Word].values()):,}", inline=True)
            await ctx.message.channel.send(embed=IEm)

        #!! DEPRECATED Total
        #! Num = 0
        #! Enput = " ".join(args)
        #! DbB = Col.find({"IDd": "GuildInfo", "IDg": str(ctx.guild.id)})
        #! OSfDb = Col.find({"IDg": str(ctx.guild.id)})
        #! for i in DbB:
        #!     Kyes = i.keys()
        #! if (Enput == "") or (Enput == " "):
        #!     IEm = discord.Embed(
        #!         title=ctx.guild.name, description="Total times repeated", color=0x3252A8
        #!     )
        #!     for Wp in Kyes:
        #!         Num = 0
        #!         OSfDb = Col.find({"IDg": str(ctx.guild.id)})
        #!         if Wp == "_id" or Wp == "IDd" or Wp == "IDg" or Wp == "Setup":
        #!             pass
        #!         else:
        #!             for j in OSfDb:
        #!                 Num += j[Wp]
        #!             IEm.add_field(name=Wp, value=f"{Num:,}", inline=True)
        #!     await ctx.message.channel.send(embed=IEm)
        #! elif Enput in Kyes:
        #!     IEm = discord.Embed(
        #!         title=ctx.guild.name,
        #!         description=f"Total times {Enput} was repeated",
        #!         color=0x3252A8,
        #!     )
        #!     for j in OSfDb:
        #!         Num += j[Enput]
        #!     IEm.add_field(name=Enput, value=f"{Num:,}", inline=True)
        #!     await ctx.message.channel.send(embed=IEm)
        #! else:
        #!     await SendWait(ctx, "That word doesnt exist yet :confused:")

    @commands.Cog.listener()
    async def on_message(self, message):
        # print(message)
        # print(message.guild)
        if message.author.bot: return
        Get = list(ColT.find({"IDg":str(message.guild.id)}))
        if Get:
            # print("-"*29)
            # print(Get)
            # print("-"*29)
            Get = Get[0]
            Stuff = [i.center(len(i)+2) for i in Get.keys() if i not in ["_id", "IDg"]]
            What = re.sub(r"\.", "\u2024", message.content)
            What = re.sub(r"\$", "\u00A4", What)
            What = What.center(len(What)+2)
            for i in Stuff: 
                Amount = What.count(i)
                i = i[1:-1]
                if Amount > 0: ColT.update_one(Get, {"$set": {f'{i}.{str(message.author.id)}':Get[i][str(message.author.id)]+Amount}})

        #!! DEPRECATED Message Count
        #! CmSLim = 0
        #! if (
        #!     Col.count_documents(
        #!         {"IDd": "GuildInfo", "IDg": str(message.guild.id), "Setup": "Done"}
        #!     )
        #!     != 0
        #! ):
        #!     DbB = Col.find(
        #!         {"IDd": "GuildInfo", "IDg": str(message.guild.id), "Setup": "Done"}
        #!     )
        #!     for i in DbB:
        #!         KMeys = i.keys()
        #!     Remove = "*_"
        #!     PhMsRase = ((message.content.lower()).strip(Remove)).split(" ")
        #!     PhMsRase = RemoveExtra(PhMsRase, "")
        #!     LoKmeys = 1
        #!     for Ph in KMeys:
        #!         if len(Ph.split(" ")) > LoKmeys:
        #!             LoKmeys = len(Ph.split(" "))
        #!     if message.author.bot == False:
        #!         for _ in range(len(PhMsRase)):
        #!             if CmSLim >= 10:
        #!                 print("Broke count")
        #!                 break
        #!             Temp = []
        #!             for MMmsg in PhMsRase:
        #!                 if CmSLim >= 10:
        #!                     break
        #!                 Temp.append(MMmsg)
        #!                 CTemp = " ".join(Temp)
        #!                 if LoKmeys >= len(Temp) > 0:
        #!                     if FuncMon.AddTo(
        #!                         Col,
        #!                         {
        #!                             "IDd": str(message.author.id),
        #!                             "IDg": str(message.guild.id),
        #!                         },
        #!                         CTemp,
        #!                         1,
        #!                     ):
        #!                         print("Added")
        #!                         CmSLim += 1
        #!                 else:
        #!                     break
        #!             try:
        #!                 PhMsRase.pop(0)
        #!             except IndexError:
        #!                 pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot: return
        Get = list(ColT.find({"IDg":str(member.guild.id)}))
        if Get:
            Get = Get[0]
            Stuff = [i for i in Get.keys() if i not in ["_id", "IDg"]]
            [ColT.update_one(Get, {"$set": {f'{i}.{member.id}':0}}) for i in Stuff]

        #!! DEPRECATED Add Person
        #! Pid = member
        #! if Pid.bot == False:
        #!     if (
        #!         Col.count_documents({"IDd": str(Pid.id), "IDg": str(member.guild.id)})
        #!         == 0
        #!         and Col.count_documents(
        #!             {"IDd": "GuildInfo", "IDg": str(member.guild.id), "Setup": "Done"}
        #!         )
        #!         == 1
        #!     ):
        #!         Col.insert_one({"IDd": str(Pid.id), "IDg": str(member.guild.id)})
        #!         DbB = Col.find(
        #!             {"IDd": "GuildInfo", "IDg": str(member.guild.id), "Setup": "Done"}
        #!         )
        #!         print("Adding (join)")
        #!         for i in DbB:
        #!             Kyes = i.keys()
        #!         for Wp in Kyes:
        #!             FuncMon.DbAdd(
        #!                 Col, {"IDd": str(Pid.id), "IDg": str(member.guild.id)}, Wp, 0
        #!             )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.bot: return
        Get = list(ColT.find({"IDg":str(member.guild.id)}))
        if Get:
            Get = Get[0]
            Stuff = [i for i in Get.keys() if i not in ["_id", "IDg"]]
            [ColT.update_one(Get, {"$unset": {f'{Word}.{str(member.id)}':""}}) for Word in Stuff if str(member.id) in Get[Word]]
        
        #!! DEPRECATED Remove Person
        #! Pid = member
        #! if Pid.bot == False:
        #!     if (
        #!         Col.count_documents({"IDd": str(Pid.id), "IDg": str(member.guild.id)})
        #!         != 0
        #!     ):
        #!        Col.delete_one({"IDd": str(Pid.id), "IDg": str(member.guild.id)})

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        try:
            ColT.delete_one({"IDg":str(guild.id)})
        except:
            pass

        #!! DEPRECATED Remove Guild
        #! if (
        #!     Col.count_documents(
        #!         {"IDd": "GuildInfo", "IDg": str(guild.id), "Setup": "Done"}
        #!     )
        #!     > 0
        #! ):
        #!     DbB = Col.find({"IDg": str(guild.id)})
        #!     for DbG in DbB:
        #!         Col.delete_one(DbG)


def setup(DClient):
    DClient.add_cog(MongoDB(DClient))