class Action:
    """Base class for other actions. Not in use"""
    def __init__(self,data):
        #Iterate over data and add each one as a key value attribute in __dict__
        self.__dict__ = data
        
    @classmethod
    def KickAction(cls,message,name,longName,target):
        """Creates a kick action through parameters"""
        return cls({
            "name": name,
            "longName": longName,
            "target": target,
            "messageId": message.id,
            "votes": 1,
            "voters": [message.author.id],
            "server": message.server.id,
            "active": True,
            "threshold": 0.75
        })
    
    @classmethod
    def BanAction(cls,message,name,longName,target,duration):
        """Creates a ban action through parameters"""
        return cls({
            "name": name,
            "longName": longName,
            "target": target,
            "duration": duration,
            "messageId": message.id,
            "votes": 1,
            "voters": [message.author.id],
            "server": message.server.id,
            "active": True,
            "threshold": 1
        })

    def serialize(self):
        return self.__dict__
#NOTE: There is probably a better way to construct these actions
class KickAction(Action):
    """Kicks a user.  A votekick"""
    def __init__(self,data):
        self.name = data['name']
        self.longName = data['longName']
        self.target = data['target']
        self.messageId = data['messageId']
        self.votes = data['votes']
        self.voters = data['voters']
        self.server = data['server']
        self.active = data['active']
        self.threshold = data['threshold']
    
    #TODO: Better name
    @classmethod
    def immediate(cls,message,name,longName,target):
        """Allows initializing with fields as seperate parameters"""
        return cls({
            "name": name,
            "longName": longName,
            "target": target,
            "messageId": message.id,
            "votes": 1,
            "voters": [message.author.id],
            "server": message.server.id,
            "active": True,
            "threshold": 0.75
        })

    def serialize(self):
        """Provides a dict form of the action"""
        return {
            "type": "kick",
            "name": self.name,
            "longName": self.longName,
            "target": self.target,
            "messageId": self.messageId,
            "votes": self.votes,
            "voters": self.voters,
            "server": self.server,
            "active": self.active,
            "threshold": self.threshold
        }

class BanAction(Action):
    """Bans a user.  A voteban"""
    def __init__(self,data):
        self.name = data['name']
        self.longName = data['longName']
        self.target = data['target']
        self.messageId = data['messageId']
        self.duration = data['duration']
        self.votes = data['votes']
        self.voters = data['voters']
        self.server = data['server']
        self.active = data['active']
        self.threshold = data['threshold']
    
    #TODO: Better name
    @classmethod
    def immediate(cls,message,name,longName,target,duration):
        """Allows initializing with fields as seperate parameters"""
        return cls({
            "name": name,
            "longName": longName,
            "target": target,
            "duration": duration,
            "messageId": message.id,
            "votes": 1,
            "voters": [message.author.id],
            "server": message.server.id,
            "active": True,
            "threshold": 0.75
        })

    def serialize(self):
        """Provides a dict form of the action"""
        return {
            "type": "ban",
            "name": self.name,
            "longName": self.longName,
            "target": self.target,
            "messageId": self.messageId,
            "duration": self.duration,
            "votes": self.votes,
            "voters": self.voters,
            "server": self.server,
            "active": self.active,
            "threshold": self.threshold
        }
