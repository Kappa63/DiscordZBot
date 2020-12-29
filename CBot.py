import discord
from discord.ext import commands
import random
from Setup import Ignore, IsBot
import dbl
from dotenv import load_dotenv
import os

load_dotenv()

REqInt = discord.Intents.default()
REqInt.members = True

DClient = commands.Bot(
    case_insensitive=True, command_prefix=["z", "Z"], help_command=None, intents=REqInt
)

TClient = dbl.client.DBLClient(bot=DClient, token=os.getenv("DBL_TOKEN"), autopost=True)


@DClient.check
async def ChBot(ctx):
    if ctx.author.bot:
        raise IsBot("Bot")
    return True


@DClient.check
async def ChModDown(ctx):
    OpenState = open("OpenState.txt")
    State = OpenState.readlines()
    OpenState.close()
    if ("".join(State) == "Down") and ctx.author.id not in [
        507212584634548254,
        443986051371892746,
        224809178793771009,
    ]:
        raise Ignore("Ignore")
    return True


Cogs = [
    "Cogs.Misc",
    "Cogs.MongoDB",
    "Cogs.Covid",
    "Cogs.Nasa",
    "Cogs.RedditCmds",
    "Cogs.TwitterCmds",
    "Cogs.AnimeManga",
    "Cogs.HelpInfo",
    "Cogs.Randomizers",
    "Cogs.OnlyMods",
    "Cogs.MainEvents",
    "Cogs.Rule34",
    "Cogs.Youtube",
    "Cogs.Image",
    "Cogs.WrittenStuff",
    "Cogs.Movies",
    "Cogs.Games",
]

if __name__ != "__main__":
    for Cog in Cogs:
        DClient.load_extension(Cog)
    print("Cogs Loaded...")

DClient.run(os.getenv("DISCORD_SECRET"))