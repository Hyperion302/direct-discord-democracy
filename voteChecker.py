import discord,asyncio,datetime
import action as Action
class voteCheckingClient(discord.Client):
    def __init__(self,table,sw,logger):
        self.table = table
        self.sw = sw
        self.logger = logger
        super().__init__()
    async def on_ready(self):
        print("Logged in voteCheckingClient")
        while True:
            print("Checking votes...")
            startTime = asyncio.get_event_loop().time()
            for action in self.table.find({'active':True}):
                channel = self.get_channel(action['channelId'])
                if not channel:
                    print("Missed channel") #TODO: Error handling
                    continue

                server = channel.server
                action = Action.DDDAction(action)

                print("Checking action...")

                # Check delay
                serverData = await self.sw.getServerData(server)
                delay = serverData['delay']
                if action.created_at+delay > int(datetime.datetime.utcnow().timestamp()):
                    print("Delay not reached")
                    continue

                # Tally votes and check ratio
                yae = action.y
                nae = action.n
                    
                # If the server is large, update the user cache to contain offline members.
                if server.large:
                    await self.request_offline_members(server)

                # Check quorum
                totalPercent = (yae+nae)/server.member_count
                if totalPercent < serverData['quorum']:
                    print("Quorum not reached")
                    continue
                    
                # Check threshold
                ratio = yae/(yae+nae)
                if ratio <= action.threshold:
                    print("Threshold not reached")
                    continue
                    
                # If the vote passed, call action
                print("Executing action ")
                await self.logger.success("Executing action",channel) #TODO: Instead of logging, add "Executed" to the embed
                await action.execute(self,server,self.logger)
                
                # Deactivate prop
                self.table.update_one({"messageId":action.messageId},{"$set":{"active":False}})

                # Update prop message
                status_message = self.get_message(channel,action.messageId)
                log_message = action.formatAction()
                embed = discord.Embed(type="rich",color=self.logger.colors['inactive'],description=log_message)
                #NOTE: This permission does not exist, as you can always edit your own message
                await self.client.edit_message(status_message,embed=embed)
                print("\n")
            executionTime = (asyncio.get_event_loop().time())-startTime
            print("Done checking votes after %d seconds" % executionTime)
            await asyncio.sleep(60-executionTime)