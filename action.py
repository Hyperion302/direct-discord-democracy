class DDDAction:
    """Base class for other actions. Not in use"""
    def __init__(self,data):
        #Iterate over data and add each one as a key value attribute in __dict__
        self.__dict__ = data
        
    # Internal ID's:
    # <serverID>_<incrementing_integer>
    # Users will only ever see and use the incrementing integer
    @classmethod
    def KickAction(cls,message,target):
        """Creates a kick action through parameters"""
        return cls({
            "type": "kick",
            "internalID": 0, #TODO: Generate UUID
            "target": target,
            "messageId": message.id,
            "y": 1,
            "n": 0,
            "voters": [message.author.id],
            "server": message.server.id,
            "active": True,
            "threshold": 0.5
        })
    
    @classmethod
    def BanAction(cls,message,target,duration):
        """Creates a ban action through parameters"""
        return cls({
            "type": "ban",
            "internalID": 0, #TODO: Generate UUID
            "target": target,
            "duration": duration,
            "messageId": message.id,
            "y": 1,
            "n": 0,
            "voters": [message.author.id],
            "server": message.server.id,
            "active": True,
            "threshold": 0.66
        })

    def serialize(self):
        return self.__dict__
