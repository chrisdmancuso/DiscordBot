import subprocess
import discord
import os
import random
import time
import datetime
import nacl
import math
import asyncio
from discord.ext import commands
from discord import FFmpegPCMAudio
from sys import platform

################# START STATIC FINAL VARIABLES #################

#PATH/MISC VARS
PATH = os.getcwd()
TXT = '.txt'
BACKSLASH = '\\'
SLASH = '/'
UNDERSCORE = '_'
LOG_FILE = 'discord_log_bot'
TOKEN_FILE = 'discord_bot_token'
FORMATTED_LOG = ''
       
#LISTS
GAMER_LIST = ["Let's Play Some Games!", 'Time To Game Nerds',
              'What Is Up My Gamers?', "I'm About To Game!"]                                    #Gamer_List - Insert any additional gaming messages here
COMMAND_LIST = ['!!game', '!!mention', '!!clear', '!!help', '!!join', '!!leave']                             #Command_List - Insert additional commands here. Any new commands must be updated here
ERROR_LIST = ["That's not a command. Type '!!help' for a list of commands."]                    #Error_List - Insert any additional error messages here
COOLDOWN_LIST = ['Command is on cooldown']                                                      #Cooldown_List - Insert any additonal command messages here
AUDIO_LIST = ['Airplane.mp4', 'gnome.mp3', 'HankBust.mp4', 'HankGoodLord.mp4', 'HotDog.mp4']    #Audio_List - Insert audio filenames here. Path is relative, so audio files must live in the same directory as script
source_list = AUDIO_LIST[:]



################# END STATIC FINAL VARIABLES #################
################# START ALWAYS ON BOT EVENTS #################

### Bot prefix and on_ready() ###
bot = commands.Bot(command_prefix="!!")
@bot.event
async def on_ready():
    print("Logged on as {0}!".format(bot.user))

### General error handling ###
@bot.event
async def on_command_error(self, error):
    curTime, curDate = getDateTime()
    try:
        if isinstance(error, commands.MissingPermissions):
            print(f'PERMISSIONS ERROR: {curTime} {curDate}')
        elif isinstance(error, commands.CommandOnCooldown):
            message = random.choice(COOLDOWN_LIST) + ', try again in {:.0f}s'.format(error.retry_after)
            await self.send(message)
    except:
        print("ERROR")
        
### on_message Logic ###
@bot.event
async def on_message(message):
    #Variable declarations
    curTime, curDate = getDateTime()
    curChannel, curGuild = ' Channel: ' + str(message.channel), ' Guild: ' + str(message.guild)
    curAuthor, curContent = '{0.author}'.format(message), '{0.content}'.format(message)
    FORMATTED_LOG = PATH + BACKSLASH + LOG_FILE + UNDERSCORE + str(message.channel) + UNDERSCORE + str(message.guild) + TXT
    
    #Sanitize and log content
    updContent = sanitizeContent(curContent)
    logMessages(FORMATTED_LOG, curTime, curDate, curAuthor, curChannel, curGuild, curContent, updContent)
    
    #Response to invalid commands
    if ('!!' in curContent and '!!clear' not in curContent and '!!help' not in curContent and '!!join' not in curContent and curContent not in COMMAND_LIST and curAuthor != 'SkreeBot#5635'):
        await message.channel.send(random.choice(ERROR_LIST), reference=message)
        
    #Await to allow bot to process commands without being blocked
    await bot.process_commands(message)
    
################# END ALWAYS ON BOT EVENTS #################        
################# START ALL BOT FUNCTIONS #################

class Gaming(commands.Cog):
    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def game(self, ctx):
        """Ping everyone in the server for some games."""
        await ctx.send('@everyone\n' + random.choice(GAMER_LIST))

class Misc(commands.Cog):
    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def mention(self, ctx):
        """Mentions Everyone"""
        await ctx.send("@everyone\nWhat's up?")
        
class Moderation(commands.Cog):
    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount=None):
        """Clear previous messages. Takes an integer as input. Default is 2"""
        try:
            a = int(amount)
            await ctx.channel.purge(limit = a)
        except:
            await ctx.channel.purge(limit = 2)
            
class Voice(commands.Cog):
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def join(self, ctx, vChannel=None):
        """Bot joins the current voice channel. Can pass Case sensitive channel name to join a specific channel"""
        if len(source_list) != 0:
            source_path, source_audio, source_length = get_audio(source_list)
        else:
            get_audio_list()
            source_path, source_audio, source_length = get_audio(source_list)
            
        if not ctx.author.voice and vChannel == None:
            await ctx.send("You are not in a voice channel")
        elif vChannel != None:
            try:
                try:
                    await ctx.channel.purge(limit = 1)
                except:
                    print('PERMISSION DENIED')
                cChannel = discord.utils.get(ctx.guild.channels, name=vChannel)
                channel_id = cChannel.id
                voice_channel = ctx.guild.get_channel(channel_id)
                voice = await voice_channel.connect()
                player = voice.play(source_audio)
                time.sleep(source_length)
                await ctx.guild.voice_client.disconnect()
            except:
                print('NOT A VOICE CHANNEL')
        else:
            try:
                await ctx.channel.purge(limit = 1)
            except:
                print('PERMISSION DENIED')
            channel = ctx.author.voice.channel
            voice = await channel.connect()
            player = voice.play(source_audio)
            time.sleep(source_length)
            await ctx.guild.voice_client.disconnect()
            
    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def leave(self, ctx):
        """Bot leaves the current voice channel. Mods only."""
        if ctx.voice_client:
            await ctx.guild.voice_client.disconnect()
        else:
            await ctx.send("Not in a voice channel")

################# END ALL BOT FUNCTIONS #################
################# HELPER FUNCTIONS #################

def sanitizeContent(content):
    updContent = []
    try:
        for x in content:
            if x == '\n':
                updContent.append(' ')
                continue
            updContent.append(x)
        updContent = ''.join(updContent)
        return updContent
    except:
        print('ERROR')
        
def getToken():
    if platform == 'linux' or platform == 'darwin':
        path = PATH + SLASH + TOKEN_FILE + TXT
    elif platform == 'win32':
        path = PATH + BACKSLASH + TOKEN_FILE + TXT

    f = open(path, "r")
    token = f.read()
    f.close
    return token

def getFileContents(filePath):
    f = open(filePath + TXT, 'r')
    contents = f.readlines()
    f.close
    return contents
        

def getDateTime():
    return datetime.datetime.now().strftime('%x'), datetime.datetime.now().strftime('%X')

def logMessages(log, curTime, curDate, curAuthor, curChannel, curGuild, curContent, updContent):
    recieved = f'>>> Message from {curAuthor}: {updContent}'
    ### TURNED OFF. UNCOMMENT OPEN, WRITE, LOG SUCCESS, and CLOSE TO TURN ON ###
    #Try logging
    #g = open(log, "a+")
    try:
        #g.write(f'{curTime}:{curDate}: {curChannel} {curGuild} {recieved}' + '\n')
        print(f'{curTime}:{curDate}: {curChannel} {curGuild} {recieved}')
        #print("LOG SUCCESS " + curAuthor + ': ' + curContent)
    except:
        print("LOG ERROR")
        #g.write(f'{curTime}:{curDate}: {curChannel} {curGuild}' + f' >>> Message from {curAuthor}: ' + str(type(updContent)) + ' COMMAND RESULTED IN ERROR\n')
    #g.close()

def updateCog(bot):
    CLASS_LIST = [Gaming(), Moderation(), Misc(), Voice()]
    for i in range(0, len(CLASS_LIST)):
        bot.add_cog(CLASS_LIST[i])

def get_audio_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return int(math.ceil(float(result.stdout)))

def get_audio(audioList):
    source_path = random.choice(source_list)
    source_audio = FFmpegPCMAudio(source_path)
    source_length = get_audio_length(source_path)
    source_list.remove(source_path)
    return source_path, source_audio, source_length

def get_audio_list():
    for i in AUDIO_LIST:
        source_list.append(i)
        
################# END HELPER FUNCTIONS #################
################# START MAIN LOGIC #################
           
### Cog and bot.run ###
if __name__ == '__main__':
    TOKEN = getToken()
    updateCog(bot)
    bot.run(TOKEN)

