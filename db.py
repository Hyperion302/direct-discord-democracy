from action import DDDAction
import pymongo
class DBTable:
    """Wrapper class for the mongo database"""
    def __init__(self,table):
        self.table = table

    def store_action(self,action):
        """Serialies and stores a single action"""
        serial = action.serialize
        self.table.insert_one(serial)
    
    def query_one(self,query):
        """Pases a query to the underlying database and returns a single action"""
        doc = self.table.find_one(query)
        return DDDAction(doc)

    def query_many(self,query):
        """Passes on a query to the underlying database and returns a list of actions"""
        docs = self.table.find(query)
        return [DDDAction(doc) for doc in docs]
    
    def find_by_id(self,id):
        """Queries and returns a single action with the specified ID"""
        doc = self.table.find_one({"_id":id})
        return DDDAction(doc)
