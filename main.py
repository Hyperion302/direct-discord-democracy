import asyncio
import discord
import json
import pymongo,bson
# Custom modules
from commands import CommandManager
from logger import Logger
from db import DBTable,DBServerWrapper

# GLOBAL TODO:
#TODO: Add time delays for actions (adjustable by admin)
#TODO: Set the quorum and thresholds to be adjustable by admin
#TODO: Add logic to actions (So they do stuff when they complete)
#TODO: Add other commands such as status/remove/help/about
#TODO: Beautify status logs
#TODO: Status logs should De activate their respective props when deleted, and revert when edited. (use on_delete_message and on_edit_message)


# Load config file
config = json.loads(open("config.json",'r').read())

# Setup discord client
client = discord.Client()

# Setup DB
mongoclient = pymongo.MongoClient(config['db_srv'])

# Instantiate classes
db = DBTable(mongoclient.ddd.props)
sw = DBServerWrapper(mongoclient.ddd.servers)
log = Logger(client)
cm = CommandManager(client,log,db,sw)


# Event handlers
@client.event
async def on_message(message):
    await cm.handleMessage(message)

@client.event
async def on_ready():
	print("Logged in as %s" % (client.user.name))

@client.event
async def on_server_join(server):
    sw.checkServer(server)
@client.event
async def on_server_leave(server):
    pass #TODO: Purge server from server DB

client.run(config['bot_token'])
