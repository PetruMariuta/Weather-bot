import datetime
import discord
import time
import asyncio
from discord.ext import commands, tasks
import requests,json
from pprint import pprint
from weather import *
from aiohttp import ClientSession
import time
from datetime import timedelta
import emoji
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN=os.environ.get("TOKEN")        
api_key=os.environ.get("api_key")

'''
Token key and API key as environment variables since these values are my bots credentials, 
for personal use they can be generated for free using https://openweathermap.org/api for the api_key
and https://discord.com/developers/applications for the bot Token
'''

intents = discord.Intents.all()
command_prefix="!"
bot = commands.Bot(command_prefix="!",intents=intents)
id=["insert your desired channel ids"]

@bot.event
async def on_guild_join(guild):
    embed=discord.Embed(title="**Thanks For Adding Me! **", description="Hello @everyone, eu sunt un bot de vreme si voi afisa vremea zilnic la ora 6:00 in Bucuresti si Craiova, dar si prin comanda !ping.", color=0xd89522)
    await guild.text_channels[0].send(embed=embed)
    #id.append( guild.text_channels[0].id)    
    #append channel ids when the bot joins different groups, i didn't intend for this bot to be used on unknown groups but it can, i tested it on a max of 5  groups
        

  
@bot.command()
async def ping(ctx):
        await ctx.channel.send("Hei, aici e vremea in Bucuresti si Craiova 🌨")     #on command: !ping message

        url = f'https://api.openweathermap.org/data/2.5/weather?q=Bucharest&appid={api_key}&units=metric' 
	#you can add any desired city instead of Bucharest and the api will provide the information
        
	data = json.loads(requests.get(url).content) 
        data = parse_data(data)
        await ctx.channel.send(embed=weather_message(data,"Bucuresti"))
          
        url2 = f'https://api.openweathermap.org/data/2.5/weather?q=Craiova&appid={api_key}&units=metric' #same here for replacing the city
        data = json.loads(requests.get(url2).content) #json.loads  converts to dictionary 
        data = parse_data(data)
        await ctx.channel.send(embed=weather_message(data,"Craiova"))
        
	#messages can be sent to the groups with as many cities as you want, however the free api key limits this so consider upgrading to a premium one if needed
	#aiohttp could have been used as well, since it provides better performance than requests in  this application
	
def until_morning():
    now = datetime.datetime.now()
    target = (now+timedelta(days=0)).replace(hour=6,minute=0,second=0,microsecond=0)
    # if the target hour is earlier than the current hour, days=1, for example: target = (now+timedelta(days=1)).replace(hour=x,minute=x,second=x,microsecond=x) 	
    difference=(target-now).total_seconds()
     
    return difference
  


@tasks.loop(hours=24)
async def called_once_a_day():
    await asyncio.sleep(until_morning())
    for i in set(id):
		
    # use a set(id) instead of a list so that the bot doesn't send more of of the same messages  to the same groups if the bot appends more channel IDs  
       
	message_channel = bot.get_channel(i)
        
        await message_channel.send("**🥱Neata lume, e ora 6:00, vremea in Bucuresti si Craiova va fi 🌨🌡**:")
        
        url = f'https://api.openweathermap.org/data/2.5/weather?q=Bucharest&appid={api_key}&units=metric'
        data = json.loads(requests.get(url).content) 
        data = parse_data(data)
        await message_channel.send(embed=weather_message(data,"Bucuresti"))

        url2 = f'https://api.openweathermap.org/data/2.5/weather?q=Craiova&appid={api_key}&units=metric'
        data = json.loads(requests.get(url2).content) #json.loads  converts to dictionary 
        data = parse_data(data)
        await message_channel.send(embed=weather_message(data,"Craiova"))
    


@called_once_a_day.before_loop
async def before():
    await bot.wait_until_ready()

@bot.event
async def on_ready():    
 called_once_a_day.start()
 await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='!ping')) #change bots activity into "Listening to !ping"
 #If you want the bot Actibity to be listed as Playing instead, use await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='!ping'))

bot.run(TOKEN)

