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
async def ChDM(ctx):
    if ctx.guild:
        return True
    raise Ignore("Ignore")


#_ @DClient.check
#_ async def ChModDown(ctx):
#_     OpenState = open("OpenState.txt")
#_     State = OpenState.readlines()
#_     OpenState.close()
#_     if ("".join(State) == "Down") and ctx.author.id not in [
#_         507212584634548254,
#_         443986051371892746,
#_         224809178793771009,
#_     ]:
#_         raise Ignore("Ignore")
#_     return True


Cogs = [
    "Cogs.Misc",
    "Cogs.MongoDB",
    "Cogs.Covid",
    "Cogs.Nasa",
    "Cogs.Socials",
    "Cogs.AnimeManga",
    "Cogs.HelpInfo",
    "Cogs.Randomizers",
    "Cogs.OnlyMods",
    "Cogs.MainEvents",
    "Cogs.Rule34",
    "Cogs.Images",
    "Cogs.WrittenStuff",
    "Cogs.Movies",
    "Cogs.Games",
    "Cogs.GameAPIs",
    "Cogs.Google",
]

if __name__ != "__main__":
    for Cog in Cogs:
        DClient.load_extension(Cog)
    print("Cogs Loaded...")

DClient.run(os.getenv("DISCORD_SECRET"))