from discord.ext import commands
import discord
from Setup import IsBot, IsVote, IsPatreon, Ignore, IsAdmin, IsSetup, IsNSFW
from Setup import FormatTime
import random

Doing = ["Playing with the laws of physics", "Torture", "Just Vibin'", "With my toes", "Chess with god", "With Leona"]

class MainEvents(commands.Cog):
    def __init__(self, DClient):
       self.DClient = DClient

    @commands.Cog.listener()
    async def on_ready(self):
        if "".join(open("OpenState.txt").read().splitlines()) == "Up":
            await self.DClient.change_presence(activity = discord.Game(random.choice(Doing)))
        else:
            await self.DClient.change_presence(status = discord.Status.invisible)
        print(f'Online in {len(self.DClient.guilds)}...')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.message.channel.send(embed = discord.Embed(title = "Oops", description = f'Hold the spam. Wait atleast {FormatTime(round(error.retry_after, 2))}'))
        elif isinstance(error, IsBot):
            await ctx.message.channel.send(embed = discord.Embed(title = "Oops", description = "Bots can't use commands :pensive:"))
        elif isinstance(error, IsAdmin):
            await ctx.message.channel.send(embed = discord.Embed(title = "Oops", description = "Non-admins are not allowed to use this command"))
        elif isinstance(error, IsVote):
            await ctx.message.channel.send(embed = discord.Embed(title = "Oops", description = "This command is only for voters or patreon! [Official Server](https://discord.gg/V6E6prUBPv) / [Patreon](https://www.patreon.com/join/ZBotDiscord) / [Vote](https://top.gg/bot/768397640140062721/vote)"))
        elif isinstance(error, IsSetup):
            await ctx.message.channel.send(embed = discord.Embed(title = "Oops", description = 'Please setup your server first (with "zsetup")! Check all server commands (with "zhelp server")'))  
        elif isinstance(error, IsNSFW):
            await ctx.message.channel.send(embed = discord.Embed(title = "Oops", description = "This can only be used in NSFW channels."))
        elif isinstance(error, commands.CommandNotFound) or isinstance(error, Ignore):
            pass 
        else:
            raise error

def setup(DClient):
    DClient.add_cog(MainEvents(DClient))