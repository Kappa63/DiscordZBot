import discord
from discord.ext import commands
from Setup import FormatTime, SendWait
from Setup import CClient
import asyncio
import requests


class Misc(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.command(aliases=["calculate", "calc"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def Calculater(self, ctx, *args):
        ToCalc = "".join(args)

        def Calc(Nums):
            ChSafe = True
            for Num in Nums:
                try:
                    int(Num)
                except ValueError:
                    if Num not in ["(", ")", "*", "/", "+", "-", "**"]:
                        ChSafe = False
                        break
            if ChSafe:
                return f"Answer is: {round(eval(Nums),4)}"
            else:
                return "Failed to calculate :confused:"

        Calculated = Calc(ToCalc)
        await SendWait(ctx, Calculated)

    @commands.command(name="remind")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def RemindAfter(self, ctx, *args):
        def TotalWait(Day, Hour, Min, Sec):
            return (Day * 86400) + (Hour * 3600) + (Min * 60) + (Sec)

        def ChCHEm(RcM, RuS):
            return (
                RuS.bot == False
                and RcM.message == ConfirmAwait
                and str(RcM.emoji) in ["✅", "❌"]
            )

        if args:
            try:
                TimeInputs = (" ".join(args)).split(" ")
                D = 0
                H = 0
                M = 0
                S = 0
                for Times in TimeInputs:
                    if Times[-1].lower() == "d":
                        D += int(Times[:-1])
                    elif Times[-1].lower() == "h":
                        H += int(Times[:-1])
                    elif Times[-1].lower() == "m":
                        M += int(Times[:-1])
                    elif Times[-1].lower() == "s":
                        S += int(Times[:-1])
                    else:
                        raise ValueError
                AwaitTime = TotalWait(D, H, M, S)
                if AwaitTime <= 86400:
                    ConfirmAwait = await ctx.message.channel.send(
                        f":timer: Are you sure you want to be reminded in {FormatTime(AwaitTime)}? :timer:"
                    )
                    await ConfirmAwait.add_reaction("❌")
                    await ConfirmAwait.add_reaction("✅")
                    try:
                        ReaEm = await self.DClient.wait_for(
                            "reaction_add", check=ChCHEm, timeout=10
                        )
                        if ReaEm[0].emoji == "✅":
                            await ConfirmAwait.edit(
                                content=f"You will be pinged in {FormatTime(AwaitTime)} :thumbsup:"
                            )
                            await asyncio.sleep(2)
                            await ConfirmAwait.delete()
                            await asyncio.sleep(AwaitTime)
                            await SendWait(
                                ctx,
                                f":timer: Its been {FormatTime(AwaitTime)} {ctx.message.author.mention} :timer:",
                            )
                        elif ReaEm[0].emoji == "❌":
                            await ConfirmAwait.edit(
                                content="Request Cancelled :thumbsup:"
                            )
                            await asyncio.sleep(2)
                            await ConfirmAwait.delete()
                    except asyncio.TimeoutError:
                        await ConfirmAwait.edit(content="Request Timeout :alarm_clock:")
                        await asyncio.sleep(2)
                        await ConfirmAwait.delete()
                else:
                    await SendWait(
                        ctx, "zremind is limited to waiting for 1day max. :cry:"
                    )
            except ValueError:
                await SendWait(
                    ctx,
                    'Argument was improper. Check "zhelp misc" to check how to use it. :no_mouth:',
                )
        else:
            await SendWait(ctx, "No arguments given :no_mouth:")

    @commands.command(aliases=["crypto", "cryptocurrency"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def GetCrypto(self, ctx):
        def ChCHEm(RcM, RuS):
            return (
                RuS.bot == False
                and RcM.message == Crypter
                and str(RcM.emoji) in ["⬅️", "❌", "➡️"]
            )

        Crypts = requests.get(
            "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest",
            headers=CClient,
        ).json()
        CrEm = discord.Embed(
            title="Markets",
            description="Today's Cryptocurrency Prices by Market Cap.",
            color=0xF3F18A,
        )
        C = 0
        CryptNum = 1
        TotalCrypts = 5
        Embeds = []
        CrEm.add_field(name=f"Page: [{CryptNum} / 5]", value="\u200b", inline=False)
        for i in Crypts["data"][:50]:
            CrEm.add_field(
                name=f'{i["name"]} ({i["symbol"]}): `${i["quote"]["USD"]["price"]}`',
                value=f'**%Change (24h):** *`{i["quote"]["USD"]["percent_change_24h"]}%`* // **%Change (7d):** *`{i["quote"]["USD"]["percent_change_7d"]}%`* // **Market Cap:** *`{i["quote"]["USD"]["market_cap"]}`*',
                inline=False,
            )
            C += 1
            if C == 10:
                C = 0
                CrEm.set_footer(
                    text=f'Data Extracted on: {Crypts["status"]["timestamp"][:10]}'
                )
                CryptNum += 1
                Embeds.append(CrEm)
                CrEm = discord.Embed(
                    title="Markets",
                    description="Today's Cryptocurrency Prices by Market Cap.",
                    color=0xF3F18A,
                )
                CrEm.add_field(
                    name=f"Page: `[{CryptNum} / 5]`", value="\u200b", inline=False
                )
        CryptNum = 0
        Crypter = await ctx.message.channel.send(embed=Embeds[CryptNum])
        await Crypter.add_reaction("⬅️")
        await Crypter.add_reaction("❌")
        await Crypter.add_reaction("➡️")
        while True:
            try:
                Res = await self.DClient.wait_for(
                    "reaction_add", check=ChCHEm, timeout=120
                )
                await Crypter.remove_reaction(Res[0].emoji, Res[1])
                if Res[0].emoji == "⬅️" and CryptNum != 0:
                    CryptNum -= 1
                    await Crypter.edit(embed=Embeds[CryptNum])
                elif Res[0].emoji == "➡️":
                    if CryptNum < TotalCrypts - 1:
                        CryptNum += 1
                        await Crypter.edit(embed=Embeds[CryptNum])
                    else:
                        await Crypter.edit(embed=Embeds[CryptNum])
                        await Crypter.remove_reaction("⬅️", self.DClient.user)
                        await Crypter.remove_reaction("❌", self.DClient.user)
                        await Crypter.remove_reaction("➡️", self.DClient.user)
                        break
                elif Res[0].emoji == "❌":
                    await Crypter.edit(embed=Embeds[CryptNum])
                    await Crypter.remove_reaction("⬅️", self.DClient.user)
                    await Crypter.remove_reaction("❌", self.DClient.user)
                    await Crypter.remove_reaction("➡️", self.DClient.user)
                    break
            except asyncio.TimeoutError:
                await Crypter.edit(embed=Embeds[CryptNum])
                await Crypter.remove_reaction("⬅️", self.DClient.user)
                await Crypter.remove_reaction("❌", self.DClient.user)
                await Crypter.remove_reaction("➡️", self.DClient.user)
                break

    @Calculater.error
    async def CalculateError(self, ctx, error):
        if isinstance(error, commands.UnexpectedQuoteError):
            await SendWait(ctx, "Failed to calculate :confused:")
        raise error


def setup(DClient):
    DClient.add_cog(Misc(DClient))