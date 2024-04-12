import discord
from discord.ext import commands
# import requests
from discord import app_commands
# import asyncio
# from PIL import Image
# import os
from Customs.BlackJack import BJ
# import random
# import time
# import io
from CBot import DClient as CBotDClient
from Customs.UI.TicTacToe import TicTacToeView as TTTView
import datetime
# import chess
import numpy as np
# from Setup import ChVote, ChPatreonT2, ChAdmin, FormatTime, TimeTillMidnight, GetPatreonTier, SendWait, AQd
from Setup import SendWait

def SudokuBoardMaker(Title, BoardName, Board, Difficulty):
    DigitReplace = [":white_large_square:", ":one:", ":two:", ":three:", ":four:", ":five:", 
                    ":six:", ":seven:", ":eight:", ":nine:"]
    SEm = discord.Embed(title=f"{Title} (ID: {BoardName})", description=f"`Difficulty: {Difficulty.upper()}`", color=0x83E42C)
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
        if R < 3: FormSq1 += "\n"
        else:
            R = 0
            SEm.add_field(name="\u200b", value=FormSq1, inline=False)
            FormSq1 = ""
    SEm.set_footer(text='"zhelp sudoku" for more info')
    return SEm

def NextSq(grid, i, j):
    for x in range(i,9):
        for y in range(j,9):
            if grid[x][y] == 0: return x,y
    for x in range(0,9):
        for y in range(0,9):
            if grid[x][y] == 0: return x,y
    return -1,-1

def CheckSudoku(grid, i, j, e):
    RowCheck = all([e != grid[i][x] for x in range(9)])
    if RowCheck:
        ColumnCheck = all([e != grid[x][j] for x in range(9)])
        if ColumnCheck:
            TopX, TopY = 3 *(i//3), 3 *(j//3)
            for x in range(TopX, TopX+3):
                for y in range(TopY, TopY+3):
                    if grid[x][y] == e: return False
            return True
    return False

def SudokuSolver(grid, i=0, j=0):
    i,j = NextSq(grid, i, j)
    if i == -1: return True
    for e in range(1,10):
        if CheckSudoku(grid,i,j,e):
            grid[i][j] = e
            if SudokuSolver(grid, i, j): return True
            grid[i][j] = 0
    return False


def TTTBoardMaker(Board, User1, User2, AnExtra="\u200b"):
    ItemReplace = {"1": ":one:", "2": ":two:", "3": ":three:", "4": ":four:", "5": ":five:", "6": ":six:",
                   "7": ":seven:", "8": ":eight:", "9": ":nine:", "x": ":x:", "o": ":o:"}
    TEm = discord.Embed(title="Tic-Tac-Toe", description=f"`{User1.display_name} vs {User2.display_name}`", color=0x6AB4AA)
    FormTable = ""
    for Row in Board:
        for Item in Row: FormTable += ItemReplace[Item]
        FormTable += "\n"
    TEm.add_field(name=AnExtra, value=FormTable, inline=False)
    TEm.set_footer(text='"zhelp ttt" for more info')
    return TEm

def TTTWinCheck(Board):
    if any(any(i in j for j in [Board, np.dstack(Board)[0].tolist(), [np.diag(Board).tolist(), np.diag(np.fliplr(Board)).tolist()]]) for i in [["o"]*3, ["x"]*3]): return True
    return False

def TTTGetForm(Input):
    NumInput = int(Input)
    Form = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
    return Form[NumInput]


def MakeChessBoard(Board, PlayerTimes, Players):
    OnWhite = {".": "<:10:793974818286469120>", "P": "<:24:793974817648541707>", "R": "<:9_:793974818302853170>", "N": "<:22:793974817715781633>",
               "B": "<:19:793974817912258580>", "Q": "<:26:793974817496891424>", "K": "<:12:793974818269298689>", "p": "<:18:793974818013577266>",
               "r": "<:14:793974818172829716>", "n": "<:7_:793974818416492564>", "b": "<:16:793974818106114118>", "q": "<:15:793974818126168065>",
               "k": "<:8_:793974818335883265>"}
    OnGrey = {".": "<:11:793974818269560882>", "P": "<:5_:793974818449784882>", "R": "<:3_:793987203721723915>", "N": "<:2_:793974819535847434>",
              "B": "<:1_:793974819518677013>", "Q": "<:25:793974817627570188>", "K": "<:13:793974818252783616>", "p": "<:23:793974817706868737>",
              "r": "<:21:793974817794555923>", "n": "<:6_:793974818436939826>", "b": "<:17:793974818105720842>", "q": "<:4_:793974818453848074>",
              "k": "<:20:793974817883422751>"}
    RowMarker = ["8\u2002", "7\u2002", "6\u2002", "5\u2002", "4\u2002", "3\u2002", "2\u2002", "1\u2002"]
    Sub = 1
    EmBoard = f'Stuck? "zhelp chess"\n\n{Players[0].display_name} vs {Players[1].display_name}\n\u2002 Time: P1: {str(datetime.timedelta(seconds = PlayerTimes[Players[0]]))[2:]} / P2: {str(datetime.timedelta(seconds = PlayerTimes[Players[1]]))[2:]}\n'
    for Row in range(8):
        for Sq in range(8):
            if Sq == 0: EmBoard += RowMarker[Row]
            if (Sq - Sub) % 2 == 0: EmBoard += OnGrey[Board[Row][Sq]]
            else: EmBoard += OnWhite[Board[Row][Sq]]
        if Row % 2 == 0: Sub = 0
        else: Sub = 1
        EmBoard += "\n"
    EmBoard += "\u2003a\u2003b\u2003c\u2003d\u2003e\u2003f\u2003g\u2003h"
    return EmBoard


class Games(commands.Cog):
    def __init__(self, DClient:CBotDClient) -> None:
        self.DClient = DClient

    @app_commands.command(name="blackjack", description="Start a Game of Blackjack.")
    @app_commands.checks.cooldown(1, 2)
    async def PlayBJ(self, ctx:discord.Interaction) -> None:
        await ctx.response.defer(thinking=True)
        await BJ(ctx).autoRun()

    # @commands.command(name="sudoku")
    # @commands.cooldown(1, 2, commands.BucketType.user)
    # async def PlaySudoku(self, ctx:commands.Context, *args) -> None:
    #     ChCHEm = lambda RcM, RuS: not RuS.bot and RcM.message == OriginalBoard and str(RcM.emoji) in ["👁️", "❌"]
        
    #     Difficulty = list(args)[0].lower() if args else "random"
    #     RanChars = "abcdefghijklmnopqrstuvwxyz1234567890"
    #     BoardName = "".join((random.choice(RanChars) for i in range(5)))
    #     if Difficulty not in ["easy", "hard", "medium", "random"]: await SendWait(ctx, "Not valid difficulty :confused:"); return
    #     SudokuBoard = requests.get(f"https://sugoku.onrender.com/board?difficulty={Difficulty}").json()["board"]
    #     #- JSONboard = SudokuBoard.json()["board"]
    #     OriginalBoard = await ctx.response.send_message(embed=SudokuBoardMaker("Sudoku", BoardName, SudokuBoard, Difficulty))
    #     await OriginalBoard.add_reaction("👁️")
    #     await OriginalBoard.add_reaction("❌")
    #     try:
    #         ReaEm = await self.DClient.wait_for("reaction_add", check=ChCHEm, timeout=3600)
    #         await OriginalBoard.remove_reaction(ReaEm[0].emoji, ReaEm[1])
    #         if ReaEm[0].emoji == "👁️":
    #             SudokuSolver(SudokuBoard)
    #             await ctx.response.send_message(embed=SudokuBoardMaker("Solution", BoardName, SudokuBoard, Difficulty))
    #         await OriginalBoard.remove_reaction("👁️", self.DClient.user)
    #         await OriginalBoard.remove_reaction("❌", self.DClient.user)
    #     except asyncio.TimeoutError:
    #         SudokuSolver(SudokuBoard)
    #         await ctx.message.channel.send(embed=SudokuBoardMaker("Solution", BoardName, SudokuBoard, Difficulty))

    @app_commands.command(name="tictactoe", description="Start a Game of TicTacToe with Another User.")
    @app_commands.rename(usr="user")
    @app_commands.describe(usr="@ User to Start Game Against")
    @app_commands.checks.cooldown(1, 3)
    async def PlayTTT(self, ctx:discord.Interaction, usr:discord.Member) -> None:
        async def noP(pl, fin):
            await ctx.edit_original_response(content=f"{pl.mention} did not Respond. Game Ended.", view=fin)
        # def ChCHanS(MSg):
        #     MesS = MSg.content.lower()
        #     RsT = False
        #     try:
        #         if 0 < int(MSg.content) < 10:
        #             Position = int(MSg.content) - 1
        #             PlaceOnBoard = TTTGetForm(Position)
        #             if Table[PlaceOnBoard[0]][PlaceOnBoard[1]] not in ["x", "o"]: RsT = True
        #     except ValueError:
        #         if MesS in ["end", "endgame"]: RsT = True
        #     return MSg.guild.id == ctx.guild.id and MSg.channel.id == ctx.channel.id and RsT and MSg.author == Player
        # (len(ctx.message.mentions) > 0 and not ctx.message.mentions[0].bot) or 
        if (usr and not usr.bot and usr.id != ctx.user.id):
            Table = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
            Players = [ctx.user, usr] # ctx.message.mentions[0]
            PlayerAssign = {Players[0]: "x", Players[1]: "o"}
            # R = 1
            await ctx.response.send_message(content=f"{Players[0].mention}'s Turn", view=TTTView(Players[0], Players[1], noP)) # embed=TTTBoardMaker(Table, Players[0], Players[1])
            # while True:
            #     if R == 10: await SendWait(ctx, "Its a DRAW!! :partying_face:"); return
            #     if R % 2 == 0: Player = Players[1]
            #     else: Player = Players[0]   
            #     MentionTurn = await ctx.response.send_message(f"{Player.mention} Your turn. Please choose a cell number to play.")
            #     try:
            #         if R > 1: await ResS.delete()
            #         ResS = await self.DClient.wait_for("message", check=ChCHanS, timeout=30)
            #         await MentionTurn.delete()
            #         # await Board.delete()
            #         LResS = ResS.content.lower()
            #         try:
            #             if int(ResS.content) < 10:
            #                 Position = int(ResS.content) - 1
            #                 PlaceOnBoard = TTTGetForm(Position)
            #                 Table[PlaceOnBoard[0]][PlaceOnBoard[1]] = PlayerAssign[ResS.author]
            #                 if TTTWinCheck(Table):
            #                     await Board.edit(embed=TTTBoardMaker(Table, Players[0], Players[1], f"`{Player.display_name}` WINS"))
            #                     await SendWait(ctx, f"`{Player.display_name}` Wins!! :partying_face:")
            #                     return
            #                 await Board.edit(embed=TTTBoardMaker(Table, Players[0], Players[1]))
            #         except ValueError:
            #             if LResS in ["end", "endgame"]: Board.edit(embed=TTTBoardMaker(Table, Players[0], Players[1], "ENDED")); return
            #     except asyncio.TimeoutError:
            #         await ctx.response.send_message(embed=TTTBoardMaker(Table, Players[0], Players[1], f"`{Player.display_name}` DID NOT RESPOND"))
            #         await SendWait(ctx, f"`{Player.display_name}` did not play :slight_frown:!")
            #         return
            #     R += 1
        else: await SendWait(ctx, "No second player mentioned or Mentioned a bot :slight_frown:!")

    # @commands.command(name="chess")
    # @commands.cooldown(1, 2, commands.BucketType.user)
    # async def PlayChess(self, ctx, *args):
    #     def ChCHanS(MSg):
    #         MesS = MSg.content.lower()
    #         RsT = False
    #         if MSg.content in LegalMoves: RsT = True
    #         elif MesS == "resign": RsT = True
    #         elif CanClaimDraw and MesS == "claimdraw": RsT = True
    #         return MSg.guild.id == ctx.guild.id and MSg.channel.id == ctx.channel.id and RsT and MSg.author == Player

    #     if len(ctx.message.mentions) > 0 and not ctx.message.mentions[0].bot:
    #         Players = [ctx.message.author, ctx.message.mentions[0]]
    #         ChessBoard = chess.Board()
    #         R = 0
    #         CanClaimDraw = False
    #         PlayerTimes = {Players[0]: 600, Players[1]: 600}
    #         Board = await ctx.message.channel.send(MakeChessBoard(("".join(str(ChessBoard).split(" "))).splitlines(), PlayerTimes, Players))
    #         Moves = []
    #         while True:
    #             LegalMoves = [ChessBoard.san(i) for i in list(ChessBoard.legal_moves)]
    #             if R % 2 == 0: Player = Players[1]
    #             else: Player = Players[0]
    #             MentionTurn = await ctx.message.channel.send(f'{Player.mention} Please choose where to play: {", ".join(LegalMoves)}')
    #             try:
    #                 TimeTemp = int(time.time())
    #                 ResS = await self.DClient.wait_for("message", check=ChCHanS, timeout=PlayerTimes[Player])
    #                 if R > 1: PlayerTimes[Player] -= int(time.time()) - TimeTemp
    #                 Moves.append(ResS)
    #                 await MentionTurn.delete()
    #                 LResS = ResS.content.lower()
    #                 if ResS.content in LegalMoves:
    #                     await Board.delete()
    #                     ChessBoard.push_san(ResS.content)
    #                     if ChessBoard.is_checkmate(): await SendWait(ctx, f"`{Player.display_name}` WINS by Checkmate!!"); return
    #                     elif ChessBoard.is_insufficient_material(): await SendWait(ctx, "DRAW by Insufficient Material!!"); return
    #                     elif ChessBoard.is_stalemate(): await SendWait(ctx, "DRAW by Stalemate!!"); return
    #                     elif ChessBoard.can_claim_draw():
    #                         await SendWait(ctx, "A DRAW Can Now be Claimed")
    #                         CanClaimDraw = True
    #                     Board = await ctx.message.channel.send(MakeChessBoard(("".join(str(ChessBoard).split(" "))).splitlines(), PlayerTimes, Players))
    #                 elif LResS == "resign":
    #                     if R % 2 == 0: await SendWait(ctx, f"`{Players[0].display_name}` WINS by Resignation")
    #                     else: await SendWait(ctx, f"`{Players[1].display_name}` WINS by Resignation")
    #                     return
    #                 elif LResS == "claimdraw": await SendWait(ctx, f"`{Player.display_name}` Claims DRAW!!"); return
    #             except asyncio.TimeoutError:
    #                 if R % 2 == 0: await SendWait(ctx, f"`{Players[0].display_name}` WINS by Timeout")
    #                 else: await SendWait(ctx, f"`{Players[1].display_name}` WINS by Timeout")
    #                 return
    #             R += 1
    #     else: await SendWait(ctx, "No second player mentioned or Mentioned a bot :slight_frown:!")

    # @commands.command(aliases=["cptd", "chesspuzzleoftheday"])
    # @commands.cooldown(1, 3, commands.BucketType.user)
    # async def SendCPTD(self, ctx):
    #     GetCPTD = requests.get("https://api.chess.com/pub/puzzle", headers={"Accept": "application/json"}, params={'User-Agent': 'mycontact@gmail.com'})
    #     print(GetCPTD)
    #     CEm = discord.Embed(title=GetCPTD["title"], description=f'[Daily Puzzle]({GetCPTD["url"]}) from [Chess.com](https://www.chess.com/)', color=0x6C9D41)
    #     CEm.set_image(url=GetCPTD["image"])
    #     await ctx.response.send_message(embed=CEm)

    # @commands.group(name="cptddaily", invoke_without_command=True)
    # @commands.cooldown(1, 1, commands.BucketType.user)
    # async def CptdDAILY(self, ctx):
    #     TimeLeft = FormatTime(TimeTillMidnight())
    #     await SendWait(ctx, f'The next Daily CPTD is in {TimeLeft}.\n You can be added to CPTD Daily with "zcptddaily start" (If patreon tier 2+).\n Check "zhelp cptd" for more info')

    # @CptdDAILY.command(name="start")
    # @commands.check(ChPatreonT2)
    # @commands.check(ChAdmin)
    # @commands.cooldown(1, 1, commands.BucketType.user)
    # async def StartCptdDAILY(self, ctx):
    #     TierApplicable = {"Tier 2 Super": 1, "Tier 3 Legend": 2, "Tier 4 Ultimate": 4}
    #     TierLimit = TierApplicable[GetPatreonTier(ctx.author.id)]
    #     if AQd.count_documents({"Type": "CPTD", "IDd": ctx.author.id}) >= TierLimit:
    #         await SendWait(ctx, "You already added the max amount of channels to CPTD daily.\nDifferent donator levels get more channels\nCheck 'zpatreon'")
    #         return
    #     UserToCheckAdd = {"Type": "CPTD", "IDd": ctx.author.id, "IDg": ctx.guild.id, "Channel": ctx.message.channel.id}
    #     if AQd.count_documents(UserToCheckAdd):
    #         await SendWait(ctx, "This channel is already added to CPTD daily")
    #         return
    #     AQd.insert_one(UserToCheckAdd)
    #     await SendWait(ctx, "Added to CPTD daily successfully")

    # @CptdDAILY.command(aliases=["stop", "end"])
    # @commands.check(ChPatreonT2)
    # @commands.check(ChAdmin)
    # @commands.cooldown(1, 1, commands.BucketType.user)
    # async def RemoveCptdDAILY(self, ctx):
    #     UserToCheckRemove = {"Type": "CPTD", "IDd": ctx.author.id, "IDg": ctx.guild.id, "Channel": ctx.message.channel.id}
    #     if AQd.count_documents(UserToCheckRemove):
    #         Users = AQd.find(UserToCheckRemove)
    #         for User in Users: AQd.delete_one(User)
    #         await SendWait(ctx, "Removed from CPTD daily successfully")
    #         return
    #     await SendWait(ctx, "You are already not in CPTD daily")


async def setup(DClient):
    await DClient.add_cog(Games(DClient))