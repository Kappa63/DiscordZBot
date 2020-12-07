from discord.ext import commands
from CBot import IsBot, IsVote, IsPatreon, Ignore, IsAdmin, ProfSer
from CBot import StrTSTM

Doing = ["Playing with the laws of physics", "Torture", "Just Vibin'", "With my toes", "Chess with god", "With Leona"]

class MainEvents(commands.Cog):
    def __init__(self, DClient):
       self.DClient = DClient

    @commands.Cog.listener()
    async def on_ready(self):
        await self.DClient.change_presence(activity = discord.Game(random.choice(Doing)))
        print(f'Online in {len(self.DClient.guilds)}...')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.message.channel.send(f'Hold the spam. Wait atleast {StrTSTM(round(error.retry_after, 2))}')
        elif isinstance(error, IsBot):
            await ctx.message.channel.send("Bots can't use commands :pensive:")
        elif isinstance(error, IsAdmin):
            await ctx.message.channel.send("Non-admins are not allowed to use this command :face_with_raised_eyebrow:")
        elif isinstance(error, IsVote):
            await ctx.message.channel.send("This command is only for voters! You can vote [here](https://top.gg/bot/768397640140062721/vote) :no_mouth:")
        elif isinstance(error, ProfSer):
            await ctx.message.channel.send(":point_right: Please setup your server first (with 'zsetup')! Check all server commands with 'zhelp server' :point_left:")   
        elif isinstance(error, commands.CommandNotFound) or isinstance(error, Ignore):
            pass 
        else:
            raise error

def setup(DClient):
    DClient.add_cog(MainEvents(DClient))