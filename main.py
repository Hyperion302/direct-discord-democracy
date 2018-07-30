import asyncio
import discord
import json
import pymongo,bson,sys,datetime,pickle
from collections import deque
# Custom modules
from commands import CommandManager
from logger import Logger
from db import DBTable,DBServerWrapper
from threading import Thread
from action import DDDAction
from voteChecker import voteCheckingClient
# GLOBAL TODO:

#TODO: IMPORTANT! Run cleanMessageDeque in a seperate thread!

#TODO: Bugcheck the vote execution/checking system.  It was finalized in a hurry

#TODO: Add a check to make sure the bot's rank is on top of the heiarchy

#TODO: When someone removes their reaction, remove their vote
#TODO: When someone votes, remove their other vote on the same prop (if it exists)
#TODO: Transition from messageId to uniqueId
#TODO: Add time delays for actions (adjustable by admin)
#TODO: Add other commands such as status/remove/help✓/about
#TODO: Status logs should De activate their respective props when deleted, and revert when edited. (use on_delete_message and on_edit_message)
#TODO: Have command messages deleted after ~30s


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

# Because we offer minute precision on delays, I must run a seperate client every minute to
# update vote counts and execute actions
voteCheckClient = voteCheckingClient(mongoclient.ddd.props,sw,log)

# Event handlers
@client.event
async def on_message(message):
    await cm.handleMessage(message)

@client.event
async def on_ready():
    print("Booting up...")
    print("Logged in as %s" % (client.user.name))
    print("Loading old messages from messageBackup.bin")
    try:
        backupFile = open('messageBackup.bin','rb')
        client.messages.clear()
        client.messages.extend(pickle.load(backupFile))
        backupFile.close()
        print("Loaded %d old messages into messages deque" % len(client.messages))
    except Exception as e:
        print("Error loading from backup: %s" % str(e))

@client.event
async def on_reaction_add(reaction,user):
    await cm.handleEmoji(reaction,user)

@client.event
async def on_server_join(server):
    await sw.checkServer(server)
@client.event
async def on_server_leave(server):
    pass #TODO: Purge server from server DB

# Oh Boi.  DiscordPY stores all messages that it receives in a deque.  
# This deque is stored in memory and has a default cap of 5000 messages.
# When the bot (process) shutsdown, this deque is cleared, and the bot looses all ability to
# reference any messages that were in it.  The worst part is that the on_reaction_add event is ONLY TRIGGERED
# FOR MESSAGES ON THE DEQUE.  My current solution consists of going through the entire deque regularily and cleaning it of
# non-prop messages.  When it does hit a prop message, it stores it in a new table on the DB where it will be backed up.
# If the bot has a crash/shutdown/update, the props will be restored in the deque when the bot starts back up.
# Luckily the deque and the client object are mutable, which means I can pass the client class into both the store loop and start it's task
# in the event loop.  As long as I use non-assignment operators in storeLoop, the changes I make to the deque should carry over.
async def cleanDequeLoop(client): #TODO: Prevent drifing by accounting for how long execution took
    while True:
        print("Cleaning deque...")
        print("Current length: %d\nCurrent Size: %d" % (len(client.messages),sys.getsizeof(client.messages)))
        startTime = asyncio.get_event_loop().time()
        # This small bit loops over all elements and pulls out the status messages
        # Find the ids of the prop messages
        ids = [d['messageId'] for d in mongoclient.ddd.props.find({'active':True})]
        #Temporary destination deque
        temp = deque()
        # Loop over all messages and append any matching ones to the temp deque
        for a in range(len(client.messages)):
            if client.messages[0].id in ids:
                temp.append(client.messages[0])
            else:
                print("Removing message with content: %s" % client.messages[0].content)
            client.messages.rotate(-1)
        # Clear the messages deque
        client.messages.clear()
        # Fill it in with the temporary deque (Prop messages)
        client.messages.extend(temp)
        # Empty temp deque
        del temp
        executionTime = (asyncio.get_event_loop().time())-startTime
        print("Finished cleaning deque! It took %d seconds" % int(executionTime))
        print("New length: %d\nNew Size: %d" % (len(client.messages),sys.getsizeof(client.messages)))
        await asyncio.sleep(120-executionTime) #Prevent drifting


#client.run(config['bot_token'])

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(asyncio.gather(
                            client.start(config['bot_token']),
                            cleanDequeLoop(client),
                            voteCheckClient.start(config['bot_token'])))
except KeyboardInterrupt:
    loop.run_until_complete(client.logout())
    loop.run_until_complete(voteCheckClient.logout())
    print("Backing up messages in messageBackup.bin")
    try:
        backupFile = open("messageBackup.bin",'wb')
        pickle.dump(client.messages,backupFile)
        print("Finished backing up messages")
    except Exception as e:
        print("Error writing backup: %s" % str(e))
except SystemExit:
    loop.run_until_complete(client.logout())
    loop.run_until_complete(voteCheckClient.logout())
    print("Backing up messages in messageBackup.bin")
    try:
        backupFile = open("messageBackup.bin",'wb')
        pickle.dump(client.messages,backupFile)
        print("Finished backing up messages")
    except Exception as e:
        print("Error writing backup: %s" % str(e))
except Exception as e:
    loop.run_until_complete(client.logout())
    loop.run_until_complete(voteCheckClient.logout())
    print("Backing up messages in messageBackup.bin")
    try:
        backupFile = open("messageBackup.bin",'wb')
        pickle.dump(client.messages,backupFile)
        print("Finished backing up messages")
    except Exception as e:
        print("Error writing backup: %s" % str(e))
    # After backing up messages, re-raise the error
    raise e
finally:
    loop.close()
