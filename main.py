import asyncio
import discord
import json
import pymongo,bson
# Custom modules
from commands import CommandManager
from logger import Logger
from db import DBTable,GeneralDB

# GLOBAL TODO:
#TODO: Add time delays for actions (adjustable by admin)
#TODO: Set the quorum and thresholds to be adjustable by admin
#TODO: Store admin settings in a new table (servers)
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
gndb = GeneralDB(mongoclient.ddd.servers)
log = Logger(client)
cm = CommandManager(client,log,db)

# Event handlers
@client.event
async def on_message(message):
    await cm.handleMessage(message)

@client.event
async def on_ready():
	print("Logged in as %s" % (client.user.name))

@client.event
async def on_server_join(server):
    doc = gndb.query_one({'server_id':server.id})
@client.event
async def on_server_leave(server):
    pass

client.run(config['bot_token'])
