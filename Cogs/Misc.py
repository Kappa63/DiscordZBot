import discord
from discord.ext import commands
from Setup import FormatTime
import asyncio


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
        await ctx.message.channel.send(Calculated)

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
                            await ctx.message.channel.send(
                                f":timer: Its been {FormatTime(AwaitTime)} {ctx.message.author.mention} :timer:"
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
                    await ctx.message.channel.send(
                        "zremind is limited to waiting for 1day max. :cry:"
                    )
            except ValueError:
                await ctx.message.channel.send(
                    'Argument was improper. Check "zhelp misc" to check how to use it. :no_mouth:'
                )
        else:
            await ctx.message.channel.send("No arguments given :no_mouth:")

    @Calculater.error
    async def CalculateError(self, ctx, error):
        if isinstance(error, commands.UnexpectedQuoteError):
            await ctx.message.channel.send("Failed to calculate :confused:")
        raise error


def setup(DClient):
    DClient.add_cog(Misc(DClient))