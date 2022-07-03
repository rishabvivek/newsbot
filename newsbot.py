from asyncio import tasks
from multiprocessing.connection import wait
from pydoc import describe
from turtle import color, title
import discord
import os
import datetime, asyncio
from dotenv import load_dotenv
from discord.ext import commands,tasks
from discord.ext.commands.core import check
from urllib.request import urlopen
import requests
import json




client = discord.Client()
client = commands.Bot(command_prefix = '$')


load_dotenv('token.env')
TOKEN = os.getenv('DISC_TOKEN')
NEWS_API = os.getenv('NEWS_TOKEN')

@client.event
async def on_ready():
    print('NewsBot Ready')
    daily_news.start()


@client.command()
async def hello(ctx):

        await ctx.send('\n> {}'.format('Hello, I am News Bot, use `$help` to learn more commands'))

@client.command()
async def embed(ctx):

        embed = discord.Embed(
                title = "News Bot",
                description = "Top Headlines of the Day",
                color = discord.Color.blurple())
        embed.set_author(name = "NewsBot")
        embed.add_field(name="**What is NewsBot**", value = "NewsBot is a Discord Bot that automatically delivers users the day's headlines provided by Google's News API", inline=False)
        embed.add_field(name="**Commands**", value = "There are NO commands for this bot, this bot automatically updates the news at 9 AM everyday with the news, the only command is this help feed which can be reached using the `$fix` command")
        

        await ctx.send(embed=embed)



@tasks.loop(minutes = 3600)
async def daily_news():
        #timing related 
        channel = client.get_channel(982170812939382784)

        now = datetime.datetime.now()
        then = now + datetime.timedelta(seconds = 0)
        then = then.replace(hour = 9, minute = 0)
        wait_time = (then - now).total_seconds()
        await asyncio.sleep(wait_time)

        #handle news requests

        embed = discord.Embed(
                title = "Top Headlines of the Day",
                color = discord.Color.blurple())
        embed.set_author(name = "NewsBot")

        api_url = "https://newsapi.org/v2/top-headlines?country=us&pageSize=5&apiKey=" + NEWS_API

        news = requests.get(api_url)
        newsJSON = news.json()
        newsDict = json.dumps(newsJSON)
        newsLoad = json.loads(newsDict)

        for i in newsLoad['articles']:
                embed.add_field(name= str(i['title']), value = str(i['description']) + "\n" + str(i['url']), inline=False)

        
        embed.add_field(name = '\n' + "Choose a Category to Read More About", 
        value = "Sports (🏀) | Business (💰) | Entertainment (🍿) | Science(🧪) | Technology(💻) ")

        
        msg = await channel.send(embed=embed)

        
        await msg.add_reaction(emoji='🏀')
        await msg.add_reaction(emoji='💰')
        await msg.add_reaction(emoji='🍿')
        await msg.add_reaction(emoji='🧪')
        await msg.add_reaction(emoji='💻')
        
        
@client.event
async def on_reaction_add(reaction, user):
        if (user.name != 'NewsBot'):
                if (reaction.emoji == '🏀'):
                        msg = await chooseNews("Sports")
                        await msg.add_reaction(emoji='🏀')
                        await msg.add_reaction(emoji='💰')
                        await msg.add_reaction(emoji='🍿')
                        await msg.add_reaction(emoji='🧪')
                        await msg.add_reaction(emoji='💻')
                elif (reaction.emoji == '💰'):
                        msg = await chooseNews("Business")
                        await msg.add_reaction(emoji='🏀')
                        await msg.add_reaction(emoji='💰')
                        await msg.add_reaction(emoji='🍿')
                        await msg.add_reaction(emoji='🧪')
                        await msg.add_reaction(emoji='💻')
                elif (reaction.emoji == '🍿'):
                        msg = await chooseNews("Entertainment")
                        await msg.add_reaction(emoji='🏀')
                        await msg.add_reaction(emoji='💰')
                        await msg.add_reaction(emoji='🍿')
                        await msg.add_reaction(emoji='🧪')
                        await msg.add_reaction(emoji='💻')
                elif (reaction.emoji == '🧪'):
                        msg = await chooseNews("Science")
                        await msg.add_reaction(emoji='🏀')
                        await msg.add_reaction(emoji='💰')
                        await msg.add_reaction(emoji='🍿')
                        await msg.add_reaction(emoji='🧪')
                        await msg.add_reaction(emoji='💻')
                elif (reaction.emoji == '💻'):
                        msg = await chooseNews("Technology")
                        await msg.add_reaction(emoji='🏀')
                        await msg.add_reaction(emoji='💰')
                        await msg.add_reaction(emoji='🍿')
                        await msg.add_reaction(emoji='🧪')
                        await msg.add_reaction(emoji='💻')


async def chooseNews(category):
        channel = client.get_channel(982170812939382784)

        embed = discord.Embed(title = "Top " + category + " Headlines of the Day", color = discord.Color.blurple())
        embed.set_author(name = "NewsBot")

        api_url = "https://newsapi.org/v2/top-headlines?country=us&pageSize=5&category=" + category + "&apiKey=" + NEWS_API

        news = requests.get(api_url)
        newsJSON = news.json()
        newsDict = json.dumps(newsJSON)
        newsLoad = json.loads(newsDict)

        for i in newsLoad['articles']:
                embed.add_field(name= str(i['title']), value = str(i['description']) + "\n" + str(i['url']), inline=False)
        
        await channel.send(embed=embed)



client.run(TOKEN)