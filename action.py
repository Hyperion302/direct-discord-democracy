import datetime,utils,logger,asyncio,errors
class DDDAction:
    """Base class for actions"""
    def __init__(self,data):
        #Iterate over data and add each one as a key value attribute of self
        self.dbData = data #TODO: Prevent this from being stored in the DB
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
    def KickAction(cls,message,creator,target):
        """Creates a kick action through parameters"""
        return cls({
            "type": "kick",
            "created_by": creator.id,
            "target": target,
            "messageId": message.id,
            "y": 0,
            "n": 0,
            "voters": [],
            "server": message.server.id,
            "active": True,
            "threshold": 0.5, # Majority
            "created_at": int(datetime.datetime.utcnow().timestamp()),
            "channelId": message.channel.id
        })
    
    @classmethod
    def BanAction(cls,message,creator,target,duration):
        """Creates a ban action through parameters"""
        return cls({
            "type": "ban",
            "created_by": creator.id,
            "target": target,
            "duration": duration,
            "messageId": message.id,
            "y": 0,
            "n": 0,
            "voters": [],
            "server": message.server.id,
            "active": True,
            "threshold": 0.66, # Supermajority
            "created_at": int(datetime.datetime.utcnow().timestamp()),
            "channelId": message.channel.id
        })

    def serialize(self):
        """Returns a dictionary form of the action for storage"""
        return self.__dict__
    
    def formatAction(self):
        """Returns the action in a pretty format"""
        # Glorified switch statement
        parentTemplate = ("%s"
                        "Proposition by %s\n\n"
                        "**%d** :thumbsup: **%d** :thumbsdown:\n\n"
                        "%s")
        metadata = None
        if self.type == "kick":
            metadata = "Target: %s" % self.target
        elif self.type == "ban":
            metadata = ("Target: %s\n\n"
                        "Duration: %s") % (self.target,utils.ffromSeconds(self.duration))
        else:
            # TODO: Error handling
            return
        # Check if deactivated
        activityMessage = ""
        if not self.active:
            activityMessage = ":x: INACTIVE :x:\n"
        return parentTemplate % (activityMessage,
                                utils.idToMention(self.created_by),
                                self.y,
                                self.n,
                                metadata)
    async def execute(self,client,server,logger):
        """Applies the given action on a server"""
        if self.type == "kick":
            target = server.get_member(utils.mentionToId(self.target))
            #await logger.success("Kicking %s" % self.target)

            # Retrieve channel from action
            channel = server.get_channel(self.channelId)

            utils.checkPermission(channel,"kick_members")
            await client.kick(target)

        elif self.type == "ban":
            target = server.get_member(utils.mentionToId(self.target))
            #await logger.success("Banning %s" % self.target)
            utils.checkPermission(channel,"kick_members")
            await client.ban(target,delete_message_days=0)

        else:
            raise NotImplementedError
