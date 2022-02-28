import discord
from os import getenv
from dotenv import load_dotenv
from database import init_db

load_dotenv()
init_db(getenv("DATABASE"))

client = discord.Client()


def get_client():
    return client


def run_client():
    return client.run(getenv('DISCORD_TOKEN'))
