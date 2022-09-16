import discord
import os
# youtube
import youtube_dl
# Commands
from discord.ext import commands
# Asyncio
import asyncio
# TOKEN
from dotenv import load_dotenv

# TOKEN
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Start Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# Connect voice Channel
@bot.command()
async def connect(ctx):
 voiceChannel = discord.utils.get(ctx.guild.voice_channels, name="General")
 voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

 if voice is None or not voice.is_connected():
  await voiceChannel.connect()
  await ctx.send("Connect voice channel")
  # help
  await ctx.send("Command !help to Command Manual ")

# Help -> Command Manual
@bot.command(name='help')
async def help(ctx):
  embed = discord.Embed(
    title = 'Command Manual',
    color = discord.Color.green()
  )
  # connect
  embed.add_field(name='!connect', value='connect voice channel', inline=False)
  # diconnect
  embed.add_field(name='!diconnect', value='diconnect voice channel', inline=False)
  # play
  embed.add_field(name='!play', value='play music', inline=False)
  # stop
  embed.add_field(name='!stop', value='stop music', inline=False)
  # pause
  embed.add_field(name='!pause', value='pause music', inline=False)
  # resume
  embed.add_field(name='!resume', value='resume music', inline=False)
  await ctx.send(embed=embed)

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

  #check if bot is connected to voice channel
  voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
  if not voice_client.is_connected():
    voice.play(audio)
  else:
    await ctx.send("Wait for the music to start")
  voice.play(audio)

# Disconnect voice Channel
@bot.command()
async def disconnect(ctx):
  voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
  if voice.is_connected():
   await voice.disconnect()
   await ctx.send("Disconnect voice channel")
  else:
   await ctx.send("The Music-Bot is not connected to a voice channel")

#Stop
@bot.command()
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