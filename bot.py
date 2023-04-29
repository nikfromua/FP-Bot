import asyncio
import discord
from discord.ext import commands, tasks
import os 
from dotenv import load_dotenv
import youtube_dl

load_dotenv()

DISCORD_TOKEN = os.getenv('DSTOKEN')


intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!',intents=intents)


youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'no_check_certificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn',
    'executable': '/path/to/ffmpeg'
}



ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self,source,*,data,volume = 0.5):
        super().__init__(source,volume)
        self.data = data
        self.title = data.get('title')
        self.url = ''

    @classmethod
    async def from_url(cls,url,*,loop = None, stream = False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download = not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename
    

@bot.command(name = 'join')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send ('{} is not connected to a voice channel.'.format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
        await channel.connect()

@bot.command(name = 'play_song')
async def play(ctx, url):
    server = ctx.message.guild
    voice_channel = server.voice_client
    async with ctx.typing():
        filename = await YTDLSource.from_url(url, loop = bot.loop)
        voice_channel.play(discord.FFmpegPCMAudio(executable= r'C:\Users\nikit\Desktop\SoftServe\Bots\DiscordBotYT\ffmpeg-2023-04-24-git-2aad9765ef-full_build\bin', source=filename))
        await ctx.send('**Now Playing: ** {}'.format(filename))

@bot.command(name = 'pause')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send('The bot has pause the music or its not playing anything')

@bot.command(name='resume')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send('The bot is not playing any song')

@bot.command(name= 'leave')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()   
    else:
        await ctx.send('The bot has not joined a voice channel')

@bot.command(name= 'stop')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()   
    else:
        await ctx.send('The bot is not playing anything')


if __name__ == '__main__':
    bot.run('DSTOKEN')





# import discord

# intents = discord.Intents.all()
# client = discord.Client(command_prefix='!',intents = intents)

# @client.event
# async def on_ready():
#     print('We have logged in as {0.user}'.format(client))

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     if message.content.startswith('hi'):
#         await message.channel.send('hello')
    
#     if message.content.startswith('image'):
#         await message.channel.send(file = discord.File('robot.png'))
    
#     if message.content.startswith('admin'):
#         await message.channel.send(file = discord.File('astley.mp4'))
        
#     if message.content.startswith('audio'):
#         await message.channel.send(file = discord.File('scooter.mp3'))
    
#     if message.content.startswith('file'):
#         await message.channel.send(file = discord.File('DevDoc.pdf'))
        


# client.run('DSTOKEN')


















