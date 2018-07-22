import discord
import asyncio
import json
import pymongo,bson
# Custom modules
from commands import CommandManager
from logger import Logger
from db import DBTable

# Load config file
config = json.loads(open("config.json",'r').read())

# Setup discord client
client = discord.Client()

# Setup DB
mongoclient = pymongo.MongoClient(config['db_srv'])

# Instantiate classes
db = DBTable(mongoclient.ddd.props)
log = Logger(client)
cm = CommandManager(client,log)

# Event handlers
@client.event
async def on_message(message):
    cm.handleMessage(message)

#@client.event
#async def on_reaction_add(reaction,user)
#    cm.handleEmoji(reaction,user)


