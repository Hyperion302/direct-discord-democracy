import discord

class Logger:
    """Logs messages to channels and provides debug logging"""
    def __init__(self,client):
        self.client = client
        self.colors = {
            "error": discord.Color.red,
            "log": discord.Color.blue,
            "success": discord.Color.green,
            "status": discord.Color.dark_green
        }
    
    def error(self,error_message,channel):
        """Logs an error message in a channel"""
        embed = discord.Embed(type="rich",colour=self.colors['error'],description=error_message)
        self.client.send_message(channel,embed)
    
    def log(self,log_message,channel):
        """Logs a neutral message in a channel"""
        embed = discord.Embed(type="rich",colour=self.colors['log'],description=log_message)
        self.client.send_message(channel,embed)
    
    def success(self,success_message,channel):
        """Logs a success message in a channel"""
        embed = discord.Embed(type="rich",colour=self.colors['success'],description=success_message)
        self.client.send_message(channel,embed)

    def status(self,action,channel):
        """Logs a status message and returns it's ID"""
        log_message = '\n'.join([element for element in action.serialize()])
        embed = discord.Embed(type="rich",colour=self.colors['status'],description=log_message)
        self.client.send_message(channel,embed)