from discord.ext import commands
from CBot import IsBot, IsVote, IsPatreon, Ignore


def StrTSTM(SecGiN):
    Day = 0
    Hour = 0
    Min = 0
    while SecGiN >= 60:
        Min += 1
        if Min == 60:
            Hour += 1
            Min -= 60
        if Hour == 24:
            Day += 1
            Hour -= 24
        SecGiN -= 60
    if Day != 0:
        return f'{Day}Day(s) {Hour}Hour(s) {Min}Min(s) {SecGiN}Sec(s)'
    elif Hour != 0:
        return f'{Hour}Hour(s) {Min}Min(s) {SecGiN}Sec(s)'
    elif Min != 0:
        return f'{Min}Min(s) {SecGiN}Sec(s)'
    else:
        return f'{SecGiN}Sec(s)'

class MainEvents(commands.Cog):
    def __init__(self, bot):
       self.bot = bot

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

def setup(bot):
    bot.add_cog(MainEvents(bot))