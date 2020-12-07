import discord
from discord.ext import commands
from CBot import Covid
import datetime

class Covid(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient
    
    @commands.command(name = "covid")
    @commands.cooldown(1, 3, commands.BucketType.guild)
    async def Covid19(self, ctx, *args):
        if args:
            CovidLocs = Covid.getLocations()
            LocConfirmed = 0
            LocDeaths = 0
            LocRecovered = 0
            LocDiscovered = False
            for Loc in CovidLocs:
                if Loc["country"].lower() == " ".join(args).lower() or Loc["country_code"].lower() == " ".join(args).lower():
                    LocDiscovered = True
                    LocF = Loc["country"]
                    LocPop = Loc["country_population"]
                    LocConfirmed += Loc["latest"]["confirmed"]
                    LocDeaths += Loc["latest"]["deaths"]
                    LocRecovered += Loc["latest"]["recovered"]
            if LocDiscovered:
                CEm = discord.Embed(title = f'{ConT} Covid-19 Status', description = f'This data was requested on {datetime.date.today()}', color = 0xbd9400)
                CEm.add_field(name = "Population: ", value = f'{LocPop:,}', inline = False)
                CEm.add_field(name = "Confirmed: ", value = f'{LocConfirmed:,}', inline = False)
                CEm.add_field(name = "Deaths: ", value = f'{LocDeaths:,}', inline = False)
                CEm.add_field(name = "Recovered: ", value = f'{LocRecovered:,}', inline = False)
                CEm.set_footer(text = "Note: Data may not be completely accurate")
            else:
                await ctx.message.channel.send("Country not found :pensive:")
        else: 
            CovidWorld = Covid.getLatest()
            CEm = discord.Embed(title = "Worldwide Covid-19 Status", description = f'This data was requested on {datetime.date.today()}', color = 0xbd9400)
            CEm.add_field(name = "Confirmed: ", value = f'{CovidWorld["confirmed"]:,}', inline = False)
            CEm.add_field(name = "Deaths: ", value = f'{CovidWorld["deaths"]:,}', inline = False)
            CEm.add_field(name = "Recovered: ", value = f'{CovidWorld["recovered"]:,}', inline = False)
            CEm.set_footer(text = "Note: Data may not be completely accurate")
        await ctx.message.channel.send(embed = CEm)

def setup(DClient):
    DClient.add_cog(Covid(DClient))