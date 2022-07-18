import discord
import os

# Commands
from discord.ext import commands

# TOKEN
from dotenv import load_dotenv

# TOKEN
load_dotenv()
TOKEN = os.getenv('TOKEN')
# client = discord.Client()
print(TOKEN)

client = commands.Bot(command_prefix="/")

@client.command()
async def play(ctx,url_: str):
  voiceChannel = discord.utils.get(ctx.guild.voice_channels, name="General")
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  await voiceChannel.connect()
  print("voice Channel connect")


client.run(TOKEN)