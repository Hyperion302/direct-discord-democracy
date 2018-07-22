class Action:
    """Base class for other actions. Not in use"""
    def __init__(self,data):
        #Iterate over data and add each one as a key value attribute in __dict__
        self.__dict__ = data
        
    @classmethod
    def KickAction(cls,message,name,longName,target):
        """Creates a kick action through parameters"""
        return cls({
            "type": "kick",
            "name": name,
            "longName": longName,
            "target": target,
            "messageId": message.id,
            "y": 1,
            "n": 0,
            "voters": [message.author.id],
            "server": message.server.id,
            "active": True,
            "threshold": 0.75,
            "quorum": round(message.server.member_count/0.25) # TODO: Make this dynamic for each server.  Owner should
            # be able to choose whether or not it is a percentage or a constant
        })
    
    @classmethod
    def BanAction(cls,message,name,longName,target,duration):
        """Creates a ban action through parameters"""
        return cls({
            "type": "ban",
            "name": name,
            "longName": longName,
            "target": target,
            "duration": duration,
            "messageId": message.id,
            "y": 1,
            "n": 0,
            "voters": [message.author.id],
            "server": message.server.id,
            "active": True,
            "threshold": 1,
            "quorum": round(message.server.member_count/0.25) # TODO: Make this dynamic for each server.  Owner should
            # be able to choose whether or not it is a percentage or a constant
        })

    def serialize(self):
        return self.__dict__
