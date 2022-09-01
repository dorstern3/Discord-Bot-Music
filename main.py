import discord
import os
# youtube
import youtube_dl
# Commands
from discord.ext import commands
# TOKEN
from dotenv import load_dotenv

# TOKEN
load_dotenv()
TOKEN = os.getenv('TOKEN')
print(TOKEN)

bot = commands.Bot(command_prefix="/")

# Connect voice Channel
@bot.command()
async def connect(ctx):
 voiceChannel = discord.utils.get(ctx.guild.voice_channels, name="General")
 voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
 
 if voice is None or not voice.is_connected():
  await voiceChannel.connect()
  await ctx.send("Connect voice channel")

# Play music
@bot.command()
async def play(ctx, url_: str):
  song = os.path.isfile("song.mp3")
  try:
      if song:
          os.remove("song.mp3")
  except PermissionError:
      await ctx.send("Wait for the current playing music to end or use the 'stop' command")
      return

  # voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

  ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
  for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
  voice.play(discord.FFmpegPCMAudio("song.mp3"))

# Disconnect voice Channel
@bot.command()
async def disconnect(ctx):
  voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
  if voice.is_connected():
   await voice.disconnect()
   await ctx.send("Disconnect voice channel")
  # else:
  #  await ctx.send("The Music-Bot is not connected to a voice channel")

#Stop
async def stop(ctx):
  voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
  voice.stop()
  await ctx.send("Audio stop")
 
# Pause
@bot.command()
async def pause(ctx):
  voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
  if voice.is_playing():
    voice.pause()
    await ctx.send("Audio pause")
  else:
    await ctx.send("Audio not playing")

#Resume
@bot.command()
async def resume(ctx):
  voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
  if voice.is_paused():
    voice.resume()
    await ctx.send("Audio resume")
  else:
    await ctx.send("The audio is not paused")

bot.run(TOKEN)