from db import DBTable
from action import DDDAction
from logger import Logger
from errors import UserError,DatabaseError,SoftwareError

import argparse,sys

class CommandManager:
    """Handles command detection and emoji reaction detection"""
    def __init__(self,client,logger):
        self.client = client
        self.logger = logger
        # Setup commands
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()
       
        # Add command
        parserAdd = subparsers.add_parser("add")
        parserAdd.add_argument("type",type=str,choices=['kick','ban'],help="The type of proposition to add.")
        parserAdd.add_argument("name",type=str,nargs='+',help="The user friendly name of the proposition")
        
        # Finalize
        self.parser = parser
    async def handleMessage(self,message):
        """Routes and executes command methods"""
        if message.content[:4] != '_DDD':
            return
        try:
            parsedCommand = self.parser.parse_args(message.content[4:].split())
        except: # User error
            #TODO: Implement error handling
            #NOTE: Better error messages (e.g the help messages from the argparse library) aren't possible
            # due to the design of the argparse library not returning those messages in the exception :(
            await self.logger.error("There was an error in your command", message.channel)
            return

    async def handleEmoji(self,reaction,user):
        """Handles an emoji reaction to a message"""
        pass

    async def add(self,params,message):
        """The add command adds a proposition, and it's response is the status message"""
        pass

    async def list_(self,params,message):
        """The list command lists quick info about all current propositions"""
        pass
    
    async def status(self,params,message):
        """The status command creates a new link message that you can add emoji\n reactions to"""
        pass
    
    async def help(self,params,message):
        """The help command prints out help info on commands"""
        pass
    
    async def about(self,params,message):
        """The about command lists quick facts about the bot"""
        pass
    
    async def find(self,params,message):
        """The find command queries for a proposition and prints a new status command\ne.g. status command above"""
        pass
    
    async def handleVote(self,user,action):
        """Handle function that should only be called by handleMessage"""
        pass
