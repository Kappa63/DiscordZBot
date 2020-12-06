import discord
from discord.ext import commands
import praw
from prawcore import NotFound, Forbidden
import requests
import os 

twitter = tweepy.OAuthHandler("2lv4MgQDREClbQxjeWOQU5aGf", "4vq5UjqJetyLm37YhQtpc6htb0WPimFJVV088TL0LDMXHUdYTA")
twitter.set_access_token("1297802233841623040-rYG0sXCKz0PSDUNAhUPx9hecf507LY", "02dNbliU0EJOfUzGx8UVmrbaqZTlYOmwwKAWqnkecWzgd")
Twitter = tweepy.API(twitter)

Reddit = praw.Reddit(client_id = "ntnBVsoqGHtoNw", client_secret = "ZklNqu4BQK4jWRp9dYXb4ApoQ10", user_agent = "ZBot by u/Kamlin333")

class Social(commands.Cog):
    def __init__(self, DClient):
        self.DClient = DClient
    

def setup(DClient):
    DClient.add_cog(Social(DClient))