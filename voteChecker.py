import discord,asyncio,datetime
import action as Action
class voteCheckingClient(discord.Client):
    def __init__(self,table,sw):
        self.table = table
        self.sw = sw
        super().__init__()
    async def on_ready(self):
        print("Logged in voteCheckingClient")
        while True:
            print("Checking votes...")
            startTime = asyncio.get_event_loop().time()
            for action in self.table.find({'active':True}):
                channel = self.get_channel(action['channelId'])
                if not channel:
                    print("Missed channel")
                    continue
                server = channel.server
                action = Action.DDDAction(action)
                # Check delay
                print(server.id)
                serverData = await self.sw.getServerData(server)
                delay = serverData['delay']
                if action.created_at+delay <= int(datetime.datetime.utcnow().timestamp()):
                    # Tally votes and check ratio
                    yae = action.y
                    nae = action.n
                    # Check quorum
                    if (yae+nae)/server.member_count < serverData['quorum']:
                        print("Quorum not reached")
                        continue
                    ratio = yae/(yae+nae) #TODO: Should I be doing this?
                    if ratio <= action.threshold:
                        print("Threshold not reached")
                    # If the vote passed, call action
                    print("Executing action #%d" % action.internalID)
                    action.execute(server)
            executionTime = (asyncio.get_event_loop().time())-startTime
            print("Done checking votes after %d seconds" % executionTime)
            await asyncio.sleep(60-executionTime)