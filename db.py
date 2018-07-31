import action
import pymongo,re
import utils,errors
class DBTable:
    """Wrapper class for the mongo database"""
    def __init__(self,table):
        self.table = table

    async def store_action(self,action):
        """Serialies and stores a single action"""
        serial = action.serialize()
        try:
            self.table.insert_one(serial)
        except:
            raise errors.DatabaseError(serial,"An error occured while storing a %s action." % action.type)
    
    async def query_one(self,query):
        """Pases a query to the underlying database and returns a single action"""
        try:
            doc = self.table.find_one(query)
        except:
            raise errors.DatabaseError(query,"An error occured while finding an action matching the query %s." % str(query))
        if not doc:
            return None
        return action.DDDAction(doc)

    async def query_many(self,query):
        """Passes on a query to the underlying database and returns a list of actions"""
        try:
            docs = self.table.find(query)
        except:
            raise errors.DatabaseError(query,"An error occured while finding actions matching the query %s." % str(query))
        if len(docs) == 0:
            return None
        return [action.DDDAction(doc) for doc in docs]
    
    async def find_by_id(self,id):
        """Queries and returns a single action with the specified ID"""
        try:
            doc = self.table.find_one({"_id":id})
        except:
            raise errors.DatabaseError(id,"An error occured while finding an action with internal ID %s." % str(id))
        if not doc:
            return None
        return action.DDDAction(doc)
    
    async def update_one(self,action,updateQuery):
        """Updated a single action in the DB"""
        try:
            status = self.table.update_one({'messageId':action.messageId},updateQuery) #TODO: Query filter
        except:
            raise errors.DatabaseError(updateQuery,"An error occured while updating an action with message ID %s." % action.messageId)
        if (not status.modified_count) or (status.modified_count == 0):
            raise errors.DatabaseError(updateQuery,"No actions were found while trying to update an action with message ID %s." % action.messageId)
        # could be replaced by action.__dict__?

class DBServerWrapper:
    """A wrapper designed to access a server's custom values"""
    def __init__(self,table):
        self.table = table
    
    async def checkServer(self,server):
        """Query for a server, and if it doesn't exist create it's entry in the DB"""
        try:
            doc = self.table.find_one({'serverID':server.id})
        except:
            raise errors.DatabaseError(server.id,"An error occured while finding a server with an ID of %s." % server.id)
        if not doc:
            # Add a server in if it doesn't exist
            try:
                self.table.insert_one({'serverID':server.id,'quorum':0.25,'delay':utils.toSeconds("0d2h0m")})
            except:
                raise errors.DatabaseError({'serverID':server.id,'quorum':0.25,'delay':utils.toSeconds("0d2h0m")},
                                            "An error occured while adding a server to the database.")

    async def getServerData(self,server):
        """Query the DB for a server and return it's custom values"""
        await self.checkServer(server)
        try:
            doc = self.table.find_one({'serverID':server.id})
        except:
            raise errors.DatabaseError(server.id,"An error occured while finding a server with an id of %s" % server.id)
        if not doc:
            raise errors.DatabaseError(server.id,"No server can be found with the id of %s" % server.id)
        return {'quorum':doc['quorum'],'delay':doc['delay']}

    async def updateServerData(self,server,quorum=None,delay=None):
        """Update a server with a new set of values, otherwise default"""
        await self.checkServer(server)
        if quorum:
            query = {'serverID':server.id},{'$set':{'quorum':quorum}}
            try:
                status = self.table.update_one(query)
            except:
                raise errors.DatabaseError(query,"An error occured while updating the quorum for a server with the id of %s." % server.id)
            if (not status.modified_count) or (status.modified_count == 0):
                raise errors.DatabaseError(query,"Could not find any servers to update that matched the ID %s." % server.id)
        if delay:
            query = {'serverID':server.id},{'$set':{'delay':delay}}
            try:
                status = self.table.update_one(query)
            except:
                raise errors.DatabaseError(query,"An error occured while updating the quorum for a server with the id of %s." % server.id)
            if (not status.modified_count) or (status.modified_count == 0):
                raise errors.DatabaseError(query,"Could not find any servers to update that matched the ID %s." % server.id)
        return (quorum,delay)
    

