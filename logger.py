import discord
import asyncio

class Logger:
    """Logs messages to channels and provides debug logging"""
    def __init__(self,client):
        self.client = client
        self.colors = {
            "error": discord.Color.red(),
            "log": discord.Color.blue(),
            "success": discord.Color.green(),
            "status": discord.Color.dark_green()
        }
    
    async def error(self,error_message,channel):
        """Logs an error message in a channel"""
        embed = discord.Embed(type="rich",color=self.colors['error'],description=error_message)
        print("[ERROR] %s" % error_message)
        await self.client.send_message(channel,embed = embed)
    
    async def log(self,log_message,channel):
        """Logs a neutral message in a channel"""
        embed = discord.Embed(type="rich",color=self.colors['log'],description=log_message)
        print("[LOG] %s" % log_message)
        await self.client.send_message(channel,embed = embed)
    
    async def success(self,success_message,channel):
        """Logs a success message in a channel"""
        embed = discord.Embed(type="rich",color=self.colors['success'],description=success_message)
        print("[SUCCESS] %s" % success_message)
        await self.client.send_message(channel,embed = embed)

    async def status(self,action,channel):
        """Logs a status message and returns it's ID"""

        log_message = '\n'.join([str(value) for key,value in action.serialize().items()]) #TODO: Beautify
        embed = discord.Embed(type="rich",color=self.colors['status'],description=log_message)
        msg = await self.client.send_message(channel,embed = embed)
        return msg.id