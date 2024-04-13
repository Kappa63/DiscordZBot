import discord
from discord.ext import commands
from Setup import Covid as CVd
from Setup import SendWait, Navigator
import datetime
import json

class Covid(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.command(name="covidcodes")
    @commands.cooldown(1, 3, commands.BucketType.guild)
    async def Covid19Codes(self, ctx):
        CountryFile = open("countries.json")
        Countries = json.load(CountryFile).items()
        CountryFile.close()
        CountryPages = []
        for n, i in enumerate(Countries):
            if not n%20: CountryPages.append(discord.Embed(title=f"Country Codes", color=0xBD9400))
            CountryPages[-1].add_field(name=f"{i[0]}:  {i[1]}", value="\u200b", inline=False)
        await Navigator(ctx, CountryPages, Type="Not #")

    @commands.command(name="covid")
    @commands.cooldown(1, 3, commands.BucketType.guild)
    async def Covid19(self, ctx, *args):
        if args:
            CovidLocs = CVd.getLocations()
            LocConfirmed = 0
            LocDeaths = 0
            LocRecovered = 0
            LocDiscovered = False
            for Loc in CovidLocs:
                if " ".join(args).lower() in [Loc["country_code"].lower(), Loc["country"].lower()]:
                    LocDiscovered = True
                    LocF = Loc["country"]
                    LocPop = Loc["country_population"]
                    LocConfirmed += Loc["latest"]["confirmed"]
                    LocDeaths += Loc["latest"]["deaths"]
                    LocRecovered += Loc["latest"]["recovered"]
            if LocDiscovered:
                CEm = discord.Embed(title=f"{LocF} Covid-19 Status", description=f"This data was requested on {datetime.date.today()}", color=0xBD9400)
                CEm.add_field(name="Population: ", value=f"{LocPop:,}", inline=False)
                CEm.add_field(name="Confirmed: ", value=f"{LocConfirmed:,}", inline=False)
                CEm.add_field(name="Deaths: ", value=f"{LocDeaths:,}", inline=False)
                CEm.add_field(name="Recovered: ", value=f"{LocRecovered:,}", inline=False)
                CEm.set_footer(text="Note: Data may not be completely accurate")
            else: await SendWait(ctx, "Country not found :pensive:"); return
        else:
            CovidWorld = CVd.getLatest()
            CEm = discord.Embed(title="Worldwide Covid-19 Status", description=f"This data was requested on {datetime.date.today()}", color=0xBD9400)
            CEm.add_field(name="Confirmed: ", value=f'{CovidWorld["confirmed"]:,}', inline=False)
            CEm.add_field(name="Deaths: ", value=f'{CovidWorld["deaths"]:,}', inline=False)
            CEm.add_field(name="Recovered: ", value=f'{CovidWorld["recovered"]:,}', inline=False)
            CEm.set_footer(text="Note: Data may not be completely accurate")
        await ctx.message.channel.send(embed=CEm)


def setup(DClient):
    DClient.add_cog(Covid(DClient))