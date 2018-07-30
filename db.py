import action
import pymongo,re
import utils
class DBTable:
    """Wrapper class for the mongo database"""
    def __init__(self,table):
        self.table = table

    def store_action(self,action):
        """Serialies and stores a single action"""
        serial = action.serialize()
        self.table.insert_one(serial)
    
    def query_one(self,query):
        """Pases a query to the underlying database and returns a single action"""
        doc = self.table.find_one(query)
        return action.DDDAction(doc)

    def query_many(self,query):
        """Passes on a query to the underlying database and returns a list of actions"""
        docs = self.table.find(query)
        return [action.DDDAction(doc) for doc in docs]
    
    def find_by_id(self,id):
        """Queries and returns a single action with the specified ID"""
        doc = self.table.find_one({"_id":id})
        return action.DDDAction(doc)
    
    def update_one(self,action,updateQuery):
        """Updated a single action in the DB"""
        self.table.update_one({'messageId':action.messageId,'active':action.active},updateQuery) #TODO: Query filter
        # could be replaced by action.__dict__?

class DBServerWrapper:
    """A wrapper designed to access a server's custom values"""
    def __init__(self,table):
        self.table = table
    
    async def checkServer(self,server):
        """Query for a server, and if it doesn't exist create it's entry in the DB"""
        doc = self.table.find_one({'serverID':server.id})
        if not doc:
            # Add a server in if it doesn't exist
            self.table.insert_one({'serverID':server.id,'quorum':0.25,'delay':utils.toSeconds("0d2h0m")})

    async def getServerData(self,server):
        """Query the DB for a server and return it's custom values"""
        await self.checkServer(server)
        doc = self.table.find_one({'serverID':server.id})
        return {'quorum':doc.quorum,'delay':doc.delay}

    async def updateServerData(self,server,quorum=None,delay=None):
        """Update a server with a new set of values, otherwise default"""
        await self.checkServer(server)
        if quorum:
            self.table.update_one({'serverID':server.id},{'$set':{'quorum':quorum}})
        if delay:
            self.table.update_one({'serverID':server.id},{'$set':{'delay':delay}})
        
        #TODO: Check for DB errors
        return (quorum,delay)
