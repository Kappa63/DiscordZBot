import discord
from discord.ext import commands
from Setup import OClient

class GameAPIs(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.command(name="osu")
    async def OSUuser(self, ctx, *args):
        if args:
            SearchUser = OClient.get_user("".join(args))
            if SearchUser:
                User = SearchUser[0]
                OEm = discord.Embed(title=User.username, description=f'**PP:** `{User.pp_raw:,}`\n**Level:** `{round(User.level,1)}`\n\n**Total Time Played:** `{round(User.total_seconds_played/3600,2):,}`\n**Country({User.country}) Rank:** `{User.pp_country_rank:,}`\n**Global Rank:** `{User.pp_rank:,}`', url= User.url, color=0xda5b93)
                OEm.add_field(name="\u200b", value=f'**Ranked Score:** `{User.ranked_score:,}`\n**Total Score:** `{User.total_score:,}`', inline=False)
                OEm.add_field(name="\u200b", value=f'**Play Count:** `{User.playcount}`\n**50 Hits:** `{User.count50:,}`\n**100 Hits:** `{User.count100:,}`\n**300 Hits:** `{User.count300:,}`\n**Total Hits:** `{User.total_hits:,}`\n**Accuracy:** `{round(User.accuracy, 2)}`', inline=True)
                OEm.add_field(name="\u200b",value="\u200b",inline=True)
                OEm.add_field(name="\u200b", value=f'**SS:** `{User.count_rank_ss:,}`\n**SSH:** `{User.count_rank_ssh:,}`\n**S:** `{User.count_rank_s:,}`\n**SH:** `{User.count_rank_sh:,}`\n**A:** `{User.count_rank_a:,}`', inline=True)
                OEm.set_thumbnail(url=User.profile_image)
                OEm.set_footer(text=f'User ({User.username}) joined on {str(User.join_date)[:10]}')
                await ctx.message.channel.send(embed=OEm)
            else:
                await ctx.message.channel.send(embed=discord.Embed(title="Oops...", description="No User Found. Try a Valid Username"))
        else:
            await ctx.message.channel.send(embed=discord.Embed(title="Oops...", description="No Username Given. Try add a Username First."))

def setup(DClient):
    DClient.add_cog(GameAPIs(DClient))