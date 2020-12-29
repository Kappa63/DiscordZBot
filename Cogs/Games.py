import discord
from discord.ext import commands
import requests
import asyncio
import random


def SudokuBoardMaker(Title, BoardName, Board, Difficulty):
    DigitReplace = [
        ":white_large_square:",
        ":one:",
        ":two:",
        ":three:",
        ":four:",
        ":five:",
        ":six:",
        ":seven:",
        ":eight:",
        ":nine:",
    ]
    SEm = discord.Embed(
        title=f"{Title} (ID: {BoardName})",
        description=f"`Difficulty: {Difficulty.upper()}`",
        color=0x83E42C,
    )
    R = 0
    FormSq1 = ""
    for Row in Board:
        R += 1
        D = 0
        for Digit in Row:
            D += 1
            if D > 3:
                FormSq1 += " \u200b "
                D = 1
            FormSq1 += DigitReplace[Digit]
        if R < 3:
            FormSq1 += "\n"
        else:
            R = 0
            SEm.add_field(name="\u200b", value=FormSq1, inline=False)
            FormSq1 = ""
    SEm.set_footer(text='"zhelp sudoku" for more info')
    return SEm


def TTTBoardMaker(Board, User1, User2, AnExtra="\u200b"):
    ItemReplace = {
        "1": ":one:",
        "2": ":two:",
        "3": ":three:",
        "4": ":four:",
        "5": ":five:",
        "6": ":six:",
        "7": ":seven:",
        "8": ":eight:",
        "9": ":nine:",
        "x": ":x:",
        "o": ":o:",
    }
    TEm = discord.Embed(
        title="Tic-Tac-Toe",
        description=f"`{User1.display_name} vs {User2.display_name}`",
        color=0x6AB4AA,
    )
    FormTable = ""
    for Row in Board:
        for Item in Row:
            FormTable += ItemReplace[Item]
        FormTable += "\n"
    TEm.add_field(name=AnExtra, value=FormTable, inline=False)
    TEm.set_footer(text='"zhelp ttt" for more info')
    return TEm


def TTTWinCheck(Board):
    BoardSimplified = []
    for Row in Board:
        BoardSimplified.append("".join(Row))
    if (
        (BoardSimplified[0] == "xxx")
        or (BoardSimplified[1] == "xxx")
        or (BoardSimplified[2] == "xxx")
        or (
            (BoardSimplified[0][0] == "x")
            and (BoardSimplified[1][0] == "x")
            and (BoardSimplified[2][0] == "x")
        )
        or (
            (BoardSimplified[0][1] == "x")
            and (BoardSimplified[1][1] == "x")
            and (BoardSimplified[2][1] == "x")
        )
        or (
            (BoardSimplified[0][2] == "x")
            and (BoardSimplified[1][2] == "x")
            and (BoardSimplified[2][2] == "x")
        )
        or (
            (BoardSimplified[0][2] == "x")
            and (BoardSimplified[1][1] == "x")
            and (BoardSimplified[2][0] == "x")
        )
        or (
            (BoardSimplified[0][0] == "x")
            and (BoardSimplified[1][1] == "x")
            and (BoardSimplified[2][2] == "x")
        )
    ):
        return True
    elif (
        (BoardSimplified[0] == "ooo")
        or (BoardSimplified[1] == "ooo")
        or (BoardSimplified[2] == "ooo")
        or (
            (BoardSimplified[0][0] == "o")
            and (BoardSimplified[1][0] == "o")
            and (BoardSimplified[2][0] == "o")
        )
        or (
            (BoardSimplified[0][1] == "o")
            and (BoardSimplified[1][1] == "o")
            and (BoardSimplified[2][1] == "o")
        )
        or (
            (BoardSimplified[0][2] == "o")
            and (BoardSimplified[1][2] == "o")
            and (BoardSimplified[2][2] == "o")
        )
        or (
            (BoardSimplified[0][2] == "o")
            and (BoardSimplified[1][1] == "o")
            and (BoardSimplified[2][0] == "o")
        )
        or (
            (BoardSimplified[0][0] == "o")
            and (BoardSimplified[1][1] == "o")
            and (BoardSimplified[2][2] == "o")
        )
    ):
        return True
    else:
        return False


def TTTGetForm(Input):
    NumInput = int(Input)
    Form = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
    return Form[NumInput]


class Games(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient

    @commands.command(name="sudoku")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def PlaySudoku(self, ctx, *args):
        def ChCHEm(RcM, RuS):
            return (
                RuS.bot == False
                and RcM.message == OriginalBoard
                and str(RcM.emoji) in ["👁️", "❌"]
            )

        Difficulty = " ".join(args).split(" ")[0].lower()
        RanChars = "abcdefghijklmnopqrstuvwxyz1234567890"
        BoardName = "".join((random.choice(RanChars) for i in range(5)))
        if Difficulty not in ["easy", "hard", "medium", "random"]:
            await ctx.message.channel.send("Not valid difficulty :confused:")
            return
        SudokuBoard = requests.get(
            f"https://sugoku.herokuapp.com/board?difficulty={Difficulty}"
        )
        JSONboard = SudokuBoard.json()["board"]
        OriginalBoard = await ctx.message.channel.send(
            embed=SudokuBoardMaker("Sudoku", BoardName, JSONboard, Difficulty)
        )
        await OriginalBoard.add_reaction("👁️")
        await OriginalBoard.add_reaction("❌")
        try:
            ReaEm = await self.DClient.wait_for(
                "reaction_add", check=ChCHEm, timeout=3600
            )
            await OriginalBoard.remove_reaction(ReaEm[0].emoji, ReaEm[1])
            if ReaEm[0].emoji == "👁️":
                await ctx.message.channel.send(
                    embed=SudokuBoardMaker(
                        "Solution",
                        BoardName,
                        requests.post(
                            "https://sugoku.herokuapp.com/solve",
                            data=SudokuBoard.content.decode("utf-8"),
                            headers={"Accept": "x-www-form-urlencoded"},
                        ).json()["solution"],
                        Difficulty,
                    )
                )
            await OriginalBoard.remove_reaction("👁️", self.DClient.user)
            await OriginalBoard.remove_reaction("❌", self.DClient.user)
        except asyncio.TimeoutError:
            await ctx.message.channel.send(
                embed=SudokuBoardMaker(
                    "Solution",
                    BoardName,
                    requests.post(
                        "https://sugoku.herokuapp.com/solve",
                        data=SudokuBoard.content.decode("utf-8"),
                        headers={"Accept": "x-www-form-urlencoded"},
                    ).json()["solution"],
                    Difficulty,
                )
            )

    @commands.command(aliases=["ttt", "tictactoe"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def PlayTTT(self, ctx):
        def ChCHanS(MSg):
            MesS = MSg.content.lower()
            RsT = False
            try:
                if 0 < int(MSg.content) < 10:
                    Position = int(MSg.content) - 1
                    PlaceOnBoard = TTTGetForm(Position)
                    if (
                        Table[PlaceOnBoard[0]][PlaceOnBoard[1]] != "x"
                        and Table[PlaceOnBoard[0]][PlaceOnBoard[1]] != "o"
                    ):
                        RsT = True
            except ValueError:
                if (MesS == "end") or (MesS == "endgame"):
                    RsT = True
            return (
                MSg.guild.id == ctx.guild.id
                and MSg.channel.id == ctx.channel.id
                and RsT
                and MSg.author == Player
            )

        if len(ctx.message.mentions) > 0:
            Table = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
            Players = random.sample([ctx.message.author, ctx.message.mentions[0]], 2)
            PlayerAssign = {Players[0]: "x", Players[1]: "o"}
            R = 1
            OriginalBoard = await ctx.message.channel.send(
                embed=TTTBoardMaker(Table, Players[0], Players[1])
            )
            while True:
                if R == 10:
                    await ctx.message.channel.send("Its a DRAW!! :partying_face:")
                    return
                if R % 2 == 0:
                    Player = Players[1]
                else:
                    Player = Players[0]
                MentionTurn = await ctx.message.channel.send(
                    f"{Player.mention} Your turn. Please choose a cell number to play."
                )
                try:
                    if R > 1:
                        await ResS.delete()
                    ResS = await self.DClient.wait_for(
                        "message", check=ChCHanS, timeout=30
                    )
                    await MentionTurn.delete()
                    LResS = ResS.content.lower()
                    try:
                        if int(ResS.content) < 10:
                            Position = int(ResS.content) - 1
                            PlaceOnBoard = TTTGetForm(Position)
                            Table[PlaceOnBoard[0]][PlaceOnBoard[1]] = PlayerAssign[
                                ResS.author
                            ]
                            if TTTWinCheck(Table):
                                await OriginalBoard.edit(
                                    embed=TTTBoardMaker(
                                        Table,
                                        Players[0],
                                        Players[1],
                                        f"{Player.display_name} WINS",
                                    )
                                )
                                await ctx.message.channel.send(
                                    f"{Player.mention} Wins!! :partying_face:"
                                )
                                return
                            await OriginalBoard.edit(
                                embed=TTTBoardMaker(Table, Players[0], Players[1])
                            )
                    except ValueError:
                        if (LResS == "end") or (LResS == "endgame"):
                            return
                except asyncio.TimeoutError:
                    await ctx.message.channel.send("Player did not play :sad:!")
                    return
                R += 1
        else:
            await ctx.message.channel.send("No second player mentioned :sad:!")


def setup(DClient):
    DClient.add_cog(Games(DClient))