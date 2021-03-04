import discord
from discord.ext import commands
import requests
from Setup import OClient, PClient, Threader
from Setup import SendWait


def PUBGDataEmbed(data, name):
    PEm = discord.Embed(title=name, color=0x32110A)
    Combiner = lambda x, y: {k: x.get(k, 0) + y.get(k, 0) for k in set(x) | set(y)}
    Duo, Solo, Squad = Threader(
        [Combiner, Combiner, Combiner],
        [
            [data["duo"], data["duo-fpp"]],
            [data["solo"], data["solo-fpp"]],
            [data["squad"], data["squad-fpp"]],
        ],
    )
    PEm.add_field(
        name="***Solo:--***",
        value=f'**Wins:** `{Solo["wins"]:,}` \u2003 **Losses:** `{Solo["losses"]:,}` \u2003 **Top 10s:** `{Solo["top10s"]}`\n*Rounds Played:* `{Solo["roundsPlayed"]:,}` \u2003 *Longest Survival Time:* `{int(Solo["longestTimeSurvived"]):,}`\n\n**Kills:** `{Solo["kills"]:,}` \u2003 **Most Kills:** `{Solo["roundMostKills"]:,}`\n*Headshots:* `{Solo["headshotKills"]:,}` \u2003 *Damage Dealt:* `{int(Solo["damageDealt"]):,}`\n*Longest Kill:* `{int(Solo["longestKill"]):,}` \u2003 *Suicides:* `{Solo["suicides"]:,}`\n*Heals:* `{Solo["heals"]:,}` \u2003 *Revives:* `{Solo["revives"]}`',
        inline=False,
    )
    PEm.add_field(name="\u200b", value="\u200b", inline=False)
    PEm.add_field(
        name="***Duo:--***",
        value=f'**Wins:** `{Duo["wins"]:,}` \u2003 **Losses:** `{Duo["losses"]:,}` \u2003 **Top 10s:** `{Duo["top10s"]}`\n*Rounds Played:* `{Duo["roundsPlayed"]:,}` \u2003 *Longest Survival Time:* `{int(Duo["longestTimeSurvived"]):,}`\n\n**Kills:** `{Duo["kills"]:,}` \u2003 **Most Kills:** `{Duo["roundMostKills"]:,}`\n*Headshots:* `{Duo["headshotKills"]:,}` \u2003 *Damage Dealt:* `{int(Duo["damageDealt"]):,}`\n*Longest Kill:* `{int(Duo["longestKill"]):,}` \u2003 *Suicides:* `{Duo["suicides"]:,}`\n*Heals:* `{Duo["heals"]:,}` \u2003 *Revives:* `{Duo["revives"]}`',
        inline=False,
    )
    PEm.add_field(name="\u200b", value="\u200b", inline=False)
    PEm.add_field(
        name="***Squad:--***",
        value=f'**Wins:** `{Squad["wins"]:,}` \u2003 **Losses:** `{Squad["losses"]:,}` \u2003 **Top 10s:** `{Squad["top10s"]}`\n*Rounds Played:* `{Squad["roundsPlayed"]:,}` \u2003 *Longest Survival Time:* `{int(Squad["longestTimeSurvived"]):,}`\n\n**Kills:** `{Squad["kills"]:,}` \u2003 **Most Kills:** `{Squad["roundMostKills"]:,}`\n*Headshots:* `{Squad["headshotKills"]:,}` \u2003 *Damage Dealt:* `{int(Squad["damageDealt"]):,}`\n*Longest Kill:* `{int(Squad["longestKill"]):,}` \u2003 *Suicides:* `{Squad["suicides"]:,}`\n*Heals:* `{Squad["heals"]:,}` \u2003 *Revives:* `{Squad["revives"]}`',
        inline=False,
    )
    return PEm


class GameAPIs(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.command(name="osu")
    async def OSUuser(self, ctx, *args):
        if args:
            SearchUser = OClient.get_user("".join(args))
            if SearchUser:
                User = SearchUser[0]
                OEm = discord.Embed(
                    title=User.username,
                    description=f"**PP:** `{User.pp_raw:,}`\n**Level:** `{round(User.level,1)}`\n\n**Total Time Played:** `{round(User.total_seconds_played/3600,2):,}`\n**Country({User.country}) Rank:** `{User.pp_country_rank:,}`\n**Global Rank:** `{User.pp_rank:,}`",
                    url=User.url,
                    color=0xDA5B93,
                )
                OEm.add_field(
                    name="\u200b",
                    value=f"**Ranked Score:** `{User.ranked_score:,}`\n**Total Score:** `{User.total_score:,}`",
                    inline=False,
                )
                OEm.add_field(
                    name="\u200b",
                    value=f"**Play Count:** `{User.playcount}`\n**50 Hits:** `{User.count50:,}`\n**100 Hits:** `{User.count100:,}`\n**300 Hits:** `{User.count300:,}`\n**Total Hits:** `{User.total_hits:,}`\n**Accuracy:** `{round(User.accuracy, 2)}`",
                    inline=True,
                )
                OEm.add_field(name="\u200b", value="\u200b", inline=True)
                OEm.add_field(
                    name="\u200b",
                    value=f"**SS:** `{User.count_rank_ss:,}`\n**SSH:** `{User.count_rank_ssh:,}`\n**S:** `{User.count_rank_s:,}`\n**SH:** `{User.count_rank_sh:,}`\n**A:** `{User.count_rank_a:,}`",
                    inline=True,
                )
                OEm.set_thumbnail(url=User.profile_image)
                OEm.set_footer(
                    text=f"User ({User.username}) joined on {str(User.join_date)[:10]}"
                )
                await ctx.message.channel.send(embed=OEm)
            else:
                await SendWait(ctx, "No User Found. Try a Valid Username")
        else:
            await SendWait(ctx, "No Username Given. Try add a Username First.")

    @commands.command(name="fortnite")
    async def FortniteUser(self, ctx, *args):
        if not args:
            await SendWait(ctx, "No Username Given. Try add a Username First.")
            return
        try:
            ImageStats = requests.get(
                "https://fortnite-api.com/v1/stats/br/v2",
                params={"name": " ".join(args), "image": "all"},
            ).json()["data"]["image"]
            FEm = discord.Embed(
                title=f'Fortnite BR Stats for **`{" ".join(args)}`**', color=0x00D8EB
            )
            FEm.set_image(url=ImageStats)
            await ctx.message.channel.send(embed=FEm)
        except KeyError:
            await SendWait(ctx, "No User Found. Try a Valid Username")

    @commands.group(name="pubg")
    async def PUBGUser(self, ctx):
        pass

    @PUBGUser.command(name="all")
    async def GetAllTime(self, ctx, *args):
        if not args:
            await SendWait(ctx, "No Username Given. Try add a Username First.")
            return
        try:
            Player = requests.get(
                "https://api.pubg.com/shards/steam/players",
                headers=PClient,
                params={"filter[playerNames]": " ".join(args)},
            ).json()["data"][0]
            PlayerID, PlayerName = Player["id"], Player["attributes"]["name"]
            AllData = requests.get(
                f"https://api.pubg.com/shards/steam/players/{PlayerID}/seasons/lifetime",
                headers=PClient,
            ).json()["data"]["attributes"]["gameModeStats"]
            await ctx.message.channel.send(embed=PUBGDataEmbed(AllData, PlayerName))
        except KeyError:
            await SendWait(ctx, "No User Found. Try a Valid Username")

    @PUBGUser.command(name="season")
    async def GetSeason(self, ctx, *args):
        if not args:
            await SendWait(ctx, "No Username Given. Try add a Username First.")
            return
        try:
            Player = requests.get(
                "https://api.pubg.com/shards/steam/players",
                headers=PClient,
                params={"filter[playerNames]": " ".join(args)},
            ).json()["data"][0]
            PlayerID, PlayerName = Player["id"], Player["attributes"]["name"]
            SeasonID = requests.get(
                "https://api.pubg.com/shards/steam/seasons", headers=PClient
            ).json()["data"][-1]["id"]
            SeasonData = requests.get(
                f"https://api.pubg.com/shards/steam/players/{PlayerID}/seasons/{SeasonID}",
                headers=PClient,
            ).json()["data"]["attributes"]["gameModeStats"]
            await ctx.message.channel.send(embed=PUBGDataEmbed(SeasonData, PlayerName))
        except KeyError:
            await SendWait(ctx, "No User Found. Try a Valid Username")


def setup(DClient):
    DClient.add_cog(GameAPIs(DClient))