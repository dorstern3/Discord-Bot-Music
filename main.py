# 1. fix bot and play without download

import discord
import os
# youtube
import youtube_dl
# Commands
from discord.ext import commands
# TOKEN
from dotenv import load_dotenv
#Asyncio
import asyncio

# TOKEN
load_dotenv()
TOKEN = os.getenv('TOKEN')

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
async def play(ctx, url: str):
  

  voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

  #Streaming
  class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        youtube_dl.utils.bug_reports_message = lambda: ''
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0'
        }
        ffmpeg_options = {
            'options': '-vn',
        }
        ytdl = youtube_dl.YoutubeDL(ydl_opts)
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
  
  #get a stream
  audio = await YTDLSource.from_url(url=url, loop=bot.loop, stream=True)
  
  #check if bot is connected to voice channel.
  voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
  if not voice_client.is_connected():
    voice.play(audio)
  else:
    await ctx.send("Wait for the current playing music to end or use the 'stop' command")

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