import discord
import os

# Commands
from discord.ext import commands

# TOKEN
from dotenv import load_dotenv

# TOKEN
load_dotenv()
TOKEN = os.getenv('TOKEN')
print(TOKEN)

client = commands.Bot(command_prefix="/")

# Connect voice Channel
@client.command()
async def connect(ctx):
  voiceChannel = discord.utils.get(ctx.guild.voice_channels, name="General")
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice is None or not voice.is_connected():
    await voiceChannel.connect()
    await ctx.send("Connect voice channel")


# Disconnect voice Channel
@client.command()
async def disconnect(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice.is_connected():
   await voice.disconnect()
   await ctx.send("Disconnect voice channel")
  # else:
  #  await ctx.send("The Music-Bot is not connected to a voice channel")

#Stop
async def stop(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  voice.stop()
  await ctx.send("Audio stop")
 
# Pause
@client.command()
async def pause(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice.is_playing():
    voice.pause()
    await ctx.send("Audio pause")
  else:
    await ctx.send("Audio not playing")

#Resume
@client.command()
async def resume(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice.is_paused():
    voice.resume()
    await ctx.send("Audio resume")
  else:
    await ctx.send("The audio is not paused")






























# @client.command()
# async def hello(self,ctx):
#   await ctx.send('hello1 ')

# client=discord.Client()
#Command
# @client.event
# async def on_ready():
#     print('We have logged in as {0.user}'
#     .format(client))

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith('/command'):
#       await message.channel.send('command')

 

  
client.run(TOKEN)