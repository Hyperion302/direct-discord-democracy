import discord
import asyncio
import json
import pymongo,bson


#TODO: Add actual error messages
class InputError(Exception):
	def __init__(self, input_segment):
		super().__init__("Something you said didn't make sense")
		self.input_segment = input_segment

class DatabaseError(Exception):
	def __init__(self, error):
		super().__init__("Could not read database")
		self.error = error

class UserNotFoundError(Exception):
	def __init__(self, userQuery):
		super().__init__("User not found")
		self.userQuery = userQuery

commands = ['add','remove','list','find','status','vote','about','help']
actions = ['kick','ban']
action_storage = {
		"kick" : lambda params,message : {
			"author":message.author.id,
			"action":params[0],
			"target":sref_name(message.server,params[1]),
			"name":params[2],
			"long_name":params[3],
			"votes":1,
			"voters":[message.author.id],
			"server":message.server.id,
			"active":True,
			"threshold":0.75
			},
		"ban" : lambda params,message : {
			"author":message.author.id,
			"action":params[1],
			"target":sref_name(message.server,params[1]),
			"duration":int(params[2]),
			"name":params[3],
			"long_name":params[4],
			"votes":1,
			"voters":[message.author.id],
			"server":message.server.id,
			"active":True,
			"threshold":1
			}
		}

action_output_templates = {
		"kick" : lambda doc,server : (
			"Action: {0}\n"
			"Name: {1}\n"
			"Description: {2}\n"
			"ID: {3}\n"
			"Author: {4}\n"
			"Target: {5}\n"
			"Votes: {6}/{7}\n").format(
			doc['action'],
			doc['name'],
			doc['long_name'],
			str(doc['_id']),
			sderef_name(server,doc['author']),
			sderef_name(server,doc['target']),
			doc['votes'],
			round(doc['threshold']*server.member_count)),
		"ban" : lambda doc,server : (
			"Action: {0}\n"
			"Name: {1}\n"
			"Description: {2}\n"
			"ID: {3}\n"
			"Author: {4}\n"
			"Target: {5}\n"
			"Duration: {6}\n"
			"Votes: {7}/{8}\n").format(
			doc['action'],
			doc['name'],
			doc['long_name'],
			str(doc['_id']),
			sderef_name(server,doc['author']),
			sderef_name(server,doc['target']),
			doc['duration'],
			doc['votes'],
			round(doc['threshold']*server.member_count))
		}
			


config = json.loads(open("config.json",'r').read())

client = discord.Client()
mongoclient = pymongo.MongoClient(config['db_srv'])
db = mongoclient.ddd

async def fmessage(channel,content): #TODO: Handle 2000+ chars by breaking up input string
	padding = '='*round((len(content)-5)/2)
	#await client.send_message(channel,"\n```ini\n{0}[DDD]{0}\n{1}\n```".format(padding,content))
	await client.send_message(channel,"```%s```" % (content))	


def sderef_name(server,uid):
	mem = server.get_member(uid)
	if not mem:
		raise UserNotFoundError(uid)
	else:
		return mem.name

async def deref_name(server,uid): #TODO: Do I need this to be ASYNC?
	mem = server.get_member(uid)
	if not mem:
		raise UserNotFoundError(uid)
	else:
		return mem.name

def sref_name(server,name):
	mem = server.get_member_named(name)
	if not mem:
		raise UserNotFoundError(name)
	else:
		return mem.id

async def execute_action(channel,action_doc):
	pass #TODO


@client.event
async def on_ready():
	print("Logged in as %s" % (client.user.name))

@client.event
async def on_message(message):
	if len(message.content) > 0 and message.content[0] == '.':
		command_string = message.content[1:]
		if command_string.split(' ')[0] in commands:
			command = command_string.split(' ')[0].lower()
			await call_command(command,command_string,message)

async def call_command(command,command_string,message):
	# Split input by spaces, pull off command, stick back together, and add split by ':'
	user_params = ' '.join(command_string.split(' ')[1:]).split(':')
	if command == 'add':
		if user_params[0] not in actions: return
		try:
			template = action_storage[user_params[0]](user_params,message)
			docID = db.props.insert_one(template).inserted_id
		except UserNotFoundError as e:
			await fmessage(message.channel,'An error has occured with the name %s' % e.userQuery)
		except:
			await fmessage(message.channel,'An error has occured')
		else:
			await fmessage(message.channel,'Successfully added proposition #%s' % (str(docID)))
	elif command == 'remove':
		pass
	elif command == 'list':
		# 1. Queres for docs that are active + in this server
		# 2. Looks up it's template lambda according to it's action
		# 3. Joins up the strings
		# string = "--\n".join([action_output_templates[doc['action']](doc,message.server) for doc in db.props.find({"active":True,"server":message.server.id})])
		# New: Simple output
		try:
			docs = [doc for doc in db.props.find({"active":True,"server":message.server.id})]
			string = "--\n".join([(
					"Action: {0}\n"
					"Author: {1}\n"
					"Name: {2}\n"
					"ID: {3}\n").format(doc['action'],await deref_name(message.channel.server,doc['author']),doc['name'],doc['_id']) for doc in docs])
		except UserNotFoundError as e:
			await fmessage(message.channel,"An error occured with retrieving the proposition's author: %s" % e.userQuery)
		except:
			await fmessage(message.channel,"An error occured")
		else:
			if(len(string) >= 2000):
				await fmessage(message.channel,"Too many entries. You could try .find?")
			else:
				await fmessage(message.channel,string)
	elif command == 'status':
		# Print out verbose information

		doc = db.props.find_one({"_id":bson.objectid.ObjectId(user_params[0])}) #TODO: Query by name, not ID
		try:
			string = action_output_templates[doc['action']](doc,message.server)
		except UserNotFoundError as e:
			await fmessage(message.channel,"An error occured when processing %s" % e.userQuery)
		except:
			await fmessage(message.channel,"An error occured")
		else:
			await fmessage(message.channel,string)
	elif command == 'vote':
		# 1. Update vote count
		# 2. Add voter to list
		# 3. Check vote threshold
		
		# Pymongo requires objID fields to be objectID objects.
		obj_id = bson.objectid.ObjectId(user_params[0])
		doc = db.props.find_one({"_id":obj_id}) #TODO: Query by name, not ID
		# Save doc_id for next query
		doc_id = doc['_id']
		# Check to make sure user hasn't already voted
		if message.author.id not in doc['voters']:
			db.props.update_one({"_id":obj_id},{
				"$inc":{"votes":1},
				"$addToSet":{"voters":message.author.id}
			})
			await fmessage(message.channel,"Thanks for voting")
		else:
			await fmessage(message.channel,"You already voted!")
		# Check vote threshold
		doc = db.props.find_one({"_id":doc_id})
		if doc['votes'] >= doc['threshold'] * message.channel.server.member_count:
			await fmessage(message.channel,"Proposition #%s has been accepted, executing..." % (str(doc['id'])))
			await execute_action(message.channel,doc)
	elif command == 'help':
		pass
	elif command == 'about':
		pass
	elif command == 'find':
		# Query DB for docs of a specific name

		docs = db.props.find({"name":{'$regex': user_params[0]}})
		try:
			string = "--\n".join([(
					"Action: {0}\n"
					"Author: {1}\n"
					"Name: {2}\n"
					"ID: {3}\n").format(doc['action'],await deref_name(message.channel.server,doc['author']),doc['name'],doc['_id']) for doc in docs])	
		except UserNotFoundError as e:
			await fmessage(message.channel,"An error occured while retrieving the proposition's author: %s" % e.userQuery)
		except:
			await fmessage(message.channel,"An error occured")
		else:
			if(len(string) >= 2000):
				await fmessage(message.channel,"Too many entries for %s. Try narrowing your search" % user_params[0])
			else:
				await fmessage(message.channel,string)
	else: #Default case
		pass

print("Starting DDD with:\nToken: %s\nSrv: %s" % (config['token'],config['db_srv']))

client.run(config['token'])


