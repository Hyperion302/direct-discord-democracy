import datetime,utils
class DDDAction:
    """Base class for actions"""
    def __init__(self,data):
        #Iterate over data and add each one as a key value attribute of self
        self.dbData = data
        for key,value in data.items():
            setattr(self,key,value)
    
    def __getattr__(self, attr):
        """Otherwise unneeded function to satisfy PyLint.  This is only called when something fails to normally
        find an attribute, so it returns an error only"""
        if attr not in self.dbData:
            raise AttributeError("Attribute %s not found" % attr)
        else:
            return self.dbData[attr]

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
            "threshold": 0.5,
            "created_at": int(datetime.datetime.utcnow().timestamp())
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
            "threshold": 0.66,
            "created_at": int(datetime.datetime.utcnow().timestamp())
        })

    def serialize(self):
        return self.__dict__
    
    def formatAction(self):
        """Returns the action in a pretty format"""
        # Glorified switch statement
        parentTemplate = ("Proposition **#%d**: %s\n"
                        "**%d** :thumbsup: **%d** :thumbsdown:\n"
                        "%s")
        metadata = None
        if self.type == "kick":
            metadata = "Target: %s" % self.target
        elif self.type == "ban":
            metadata = ("Target: %s\n"
                        "Duration: %s\n") % (self.target,utils.ffromSeconds(self.duration))
        else:
            # TODO: Error handling
            return
        return parentTemplate % (self.internalID,
                                self.type,
                                self.y,
                                self.n,
                                metadata)
