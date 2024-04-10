from discord.ext import commands
import discord
from discord import app_commands
from Setup import ColT, ChAdmin, ChSer, RemoveExtra, SendWait, ChSerGuild, ChDev
import asyncio
import re
from CBot import DClient as CBotDClient
from typing import Optional


class MongoDB(commands.Cog):
    def __init__(self, DClient:CBotDClient):
        self.DClient = DClient

    @commands.hybrid_command(name="setup", description="Sets up the Word Counter in Server")
    @commands.check(ChAdmin)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SMsg(self, ctx:commands.Context):
        if not ColT.count_documents({"IDg":str(ctx.guild.id)}):ColT.insert_one({"IDg":str(ctx.guild.id)})
        await SendWait(ctx, "Setup Complete!")

    @commands.hybrid_command(name="update", description="Update to Make Sure All Users are Updated.")
    @commands.check(ChSer)
    @commands.check(ChAdmin)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def SUmsg(self, ctx:commands.Context):
        Members = [str(i.id) for i in ctx.guild.members if not i.bot]
        Get = ColT.find({"IDg":str(ctx.guild.id)})[0]
        Missing = [i for i in Get if i not in ["_id", "IDg"] and len(Get[i]) < len(Members)]
        Dict = {f'{i}.{j}':0 for i in Missing for j in Members if j not in Get[i]}
        ColT.update_one(Get, {"$set": Dict})
        await SendWait(ctx, "Up to Date")

    @commands.hybrid_command(name="add", description="Adds New Words to the Counter.")
    @commands.check(ChAdmin)
    @commands.check(ChSer)
    @app_commands.rename(wrd="word")
    @app_commands.describe(wrd="Word to Add to Counter")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def AWord(self, ctx:commands.Context, wrd:str):
        Word = re.sub(r"\.", "\u2024", wrd.split(" ")[0])
        Word = re.sub(r"\$", "\u00A4", Word)
        Get = ColT.find({"IDg":str(ctx.guild.id)})[0]
        if Word not in Get and Word not in ["_id", "IDg"]:    
            E = {}
            [E.update({str(Person.id):0}) for Person in ctx.guild.members if not Person.bot]
            ColT.update_one(Get, {"$set": {Word:E}})
            await SendWait(ctx, "Added!")
            return
        await SendWait(ctx, "Already Exists!")

    @commands.hybrid_command(name="remove", aliases=["rem"], description="Removes New Words from the Counter.")
    @commands.check(ChAdmin)
    @commands.check(ChSer)
    @app_commands.rename(wrd="word")
    @app_commands.describe(wrd="Word to Remove from Counter")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RWord(self, ctx:commands.Context, wrd:str):
        Word = re.sub(r"\.", "\u2024", wrd.split(" ")[0])
        Word = re.sub(r"\$", "\u00A4", Word)
        Get = ColT.find({"IDg":str(ctx.guild.id)})[0]
        if Word in Get and Word not in ["_id", "IDg"]:    
            ColT.update_one(Get, {"$unset": {Word: ""}})
            await SendWait(ctx, "Removed!")
            return
        await SendWait(ctx, "Doesn't Exist!")

    @commands.hybrid_command(name="list", description="Lists All Words in the Counter.")
    @commands.check(ChSer)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def LWord(self, ctx:commands.Context):
        LEm = discord.Embed(title="Server List",description="Words/Phrases being tracked",color=0xF59542)
        Get = ColT.find({"IDg":str(ctx.guild.id)})[0]
        Stuff = [i for i in Get if i not in ["_id", "IDg"]]
        for i in Stuff: LEm.add_field(name=i, value="\u200b", inline=True)
        await ctx.send(embed=LEm)

    @commands.hybrid_command(name="clear", description="Completely Removes Counter Data.")
    @commands.check(ChAdmin)
    @commands.check(ChSer)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ReAll(self, ctx:commands.Context):
        ChCHEm = lambda RcM, RuS: not RuS.bot and RcM.message == ReSConF and str(RcM.emoji) in ["✅", "❌"]

        ResEmF = discord.Embed(title="Clear ALL server data?", description="This is ```IRREVERSIBLE```", color=0xF59542)
        ResEmF.set_footer(text="*The Clear request timesout in 10secs.*")
        ReSConF = await ctx.send(embed=ResEmF)
        await ReSConF.add_reaction("❌")
        await ReSConF.add_reaction("✅")
        try:
            ReaEm = await self.DClient.wait_for("reaction_add", check=ChCHEm, timeout=10)
            await ReSConF.remove_reaction("❌", self.DClient.user)
            await ReSConF.remove_reaction("✅", self.DClient.user)
            if ReaEm[0].emoji == "❌": await ReSConF.edit(embed=discord.Embed(title="Cancelled :thumbsup:", description="Nothing was removed", color=0xF59542))
            elif ReaEm[0].emoji == "✅": ColT.delete_one({"IDg":str(ctx.guild.id)})
        except asyncio.TimeoutError:
            await ReSConF.remove_reaction("❌", self.DClient.user)
            await ReSConF.remove_reaction("✅", self.DClient.user)
            await ReSConF.edit(embed=discord.Embed(title="Timeout :alarm_clock:", description="Nothing was removed", color=0xF59542))

    @commands.command(name="stats", description="All/Word Stats for a User.")
    @commands.check(ChSer)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def IMsg(self, ctx:commands.Context, *, wd:str):
        print(wd)
        Get = ColT.find({"IDg":str(ctx.guild.id)})[0]
        Stuff = [i for i in Get if i not in ["_id", "IDg"]]
        Mentions = ctx.message.mentions
        args = list(wd.split(" "))
        MentionedUser = False
        if len(Mentions) > 1: await SendWait(ctx, "Too Many Mentions"); return
        if Mentions:
            print(Mentions)
            Mentioned:discord.Member = Mentions[0]
            if not Mentioned.bot:
                if f"<@!{Mentioned.id}>" in args: args.remove(f"<@!{Mentioned.id}>"); print("id")
                else: args = args[1:]; print("random")
                MentionedUser = True
            else: await SendWait(ctx, "Mentioned User Is A Bot"); return
        if not args:
            Stuff = [i for i in Get if i not in ["_id", "IDg"]]
            Person = Mentioned if MentionedUser else ctx.author
            IEm = discord.Embed(title=Person.display_name, description="Word Stats", color=0x3252A8)
            for Word in Stuff: IEm.add_field(name=Word, value=f"{Get[Word][str(Person.id)]:,}", inline=True)
            await ctx.send(embed=IEm)
        else:
            Word = re.sub(r"\.", "\u2024", ' '.join(args))
            Word = re.sub(r"\$", "\u00A4", Word)
            Person = Mentioned if MentionedUser else ctx.author
            if Word in Get and Word not in ["_id", "IDg"]:
                IEm = discord.Embed(title=Person.display_name, description="All Stats", color=0x3252A8)
                IEm.add_field(name=Word, value=f"{Get[Word][str(Person.id)]:,}", inline=True)
                await ctx.send(embed=IEm)
            else: await SendWait(ctx, "Word Doesn't Exist")

    @commands.hybrid_command(name="top", description="Leaderboard for Word(s).")
    @commands.check(ChSer)
    @app_commands.rename(wrd="word")
    @app_commands.describe(wrd="Word to Show Leaderboard for")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ToTMsg(self, ctx:commands.Context, wrd:Optional[str]):
        Get = ColT.find({"IDg":str(ctx.guild.id)})[0]
        if wrd:
            Word = re.sub(r"\.", "\u2024", wrd.split(" ")[0])
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
                await ctx.send(embed=IEm)
            else: await SendWait(ctx, "Word Doesn't Exist")
        else:
            Stuff = [i for i in Get if i not in ["_id", "IDg"]]
            All = [{i:{k:v}} for i in Stuff for k,v in Get[i].items()]
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
            await ctx.send(embed=IEm)

    @commands.hybrid_command(name="total", description="Total Times a Word was Counted by Everyone.")
    @commands.check(ChSer)
    @app_commands.rename(wrd="word")
    @app_commands.describe(wrd="Word to Show Total for")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def TMsg(self, ctx:commands.Context, wrd:Optional[str]):
        Get = ColT.find({"IDg":str(ctx.guild.id)})[0]
        if wrd:
            Word = re.sub(r"\.", "\u2024", wrd.split(" ")[0])
            Word = re.sub(r"\$", "\u00A4", Word)
            if Word in Get and Word not in ["_id", "IDg"]:
                IEm = discord.Embed(title=ctx.guild.name, description=f"Total times {Word} was repeated", color=0x3252A8)
                IEm.add_field(name=Word, value=f"{sum(Get[Word].values()):,}", inline=True)
                await ctx.send(embed=IEm)
            else: await SendWait(ctx, "Word Doesn't Exist")
        else:
            Stuff = [i for i in Get if i not in ["_id", "IDg"]]
            IEm = discord.Embed(title=ctx.guild.name, description="Total times repeated", color=0x3252A8)
            for Word in Stuff: IEm.add_field(name=Word, value=f"{sum(Get[Word].values()):,}", inline=True)
            await ctx.send(embed=IEm)

    @commands.command(name="updateforall")
    @commands.check(ChDev)
    async def UpdateForGuilds(self, ctx:commands.Context):
        Gets = ColT.find()
        for Get in Gets:
            Guild = self.DClient.get_guild(int(Get["IDg"]))
            Members = [str(i.id) for i in Guild.members if not i.bot]
            Missing = [i for i in Get if i not in ["_id", "IDg"] and len(Get[i]) < len(Members)]
            Dict = {f'{i}.{j}':0 for i in Missing for j in Members if j not in Get[i]}
            if Dict: ColT.update_one(Get, {"$set": Dict})

    @commands.Cog.listener("on_message")
    async def on_message(self, message):
        if message.author.bot: return
        Get = list(ColT.find({"IDg":str(message.guild.id)}))
        if Get:
            Get = Get[0]
            Stuff = [i.center(len(i)+2) for i in Get if i not in ["_id", "IDg"]]
            What = re.sub(r"\.", "\u2024", message.content)
            What = re.sub(r"\$", "\u00A4", What)
            What = What.center(len(What)+2)
            for i in Stuff: 
                Amount = What.count(i)
                i = i[1:-1]
                if Amount > 0: ColT.update_one(Get, {"$set": {f'{i}.{str(message.author.id)}':Get[i][str(message.author.id)]+Amount}})

    @commands.Cog.listener("on_member_join")
    async def on_member_join(self, member):
        if member.bot: return
        Get = list(ColT.find({"IDg":str(member.guild.id)}))
        if Get:
            Get = Get[0]
            Stuff = [i for i in Get if i not in ["_id", "IDg"]]
            Dict = {f'{i}.{member.id}':0 for i in Stuff}
            ColT.update_one(Get, {"$set": Dict})

    @commands.Cog.listener("on_member_remove")
    async def on_member_remove(self, member):
        if member.bot: return
        Get = list(ColT.find({"IDg":str(member.guild.id)}))
        if Get:
            Get = Get[0]
            Stuff = [i for i in Get if i not in ["_id", "IDg"]]
            Dict = {f'{Word}.{str(member.id)}':""  for Word in Stuff if str(member.id) in Get[Word]}
            ColT.update_one(Get, {"$unset": Dict})

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        try: ColT.delete_one({"IDg":str(guild.id)})
        except: pass

async def setup(DClient:CBotDClient):
    await DClient.add_cog(MongoDB(DClient))