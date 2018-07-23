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

        # _DDD {command} {params}
        # command = add
        #   params[0] = kick
        #       _DDD add kick {target}
        #   params[0] =  ban
        #       _DDD add ban {target} {duration}
        # command = remove
        #   _DDD remove {propIndex}
        # command = status
        #   _DDD status {propIndex}
        # command = help
        #   _DDD help [command]

        # Setup commands
        #NOTE: the add command is so large and diverse, it has it's own ArgumentParser that is passed the result from the
        # add command.
        topParser = argparse.ArgumentParser(prog="DDD")
        addParser = argparse.ArgumentParser(prog="add")

        # Fill out top level parser
        topSubparsers = topParser.add_subparsers(dest="command")

        topSubparser_add = topSubparsers.add_parser("add")
        topSubparser_add.add_argument("parameters",type=str,nargs='+')

        topSubparser_remove = topSubparsers.add_parser("remove")
        topSubparser_remove.add_argument("propIndex",type=int,nargs=1)

        topSubparser_status = topSubparsers.add_parser("status")
        topSubparser_status.add_argument("propIndex",type=int,nargs=1)

        topSubparser_help = topSubparsers.add_parser("help")
        topSubparser_help.add_argument("-c","--helpCommand",required=False,type=str,nargs=1)

        # Fill out add parser
        addSubparsers = addParser.add_subparsers(dest="type")

        addSubparsers_kick = addSubparsers.add_parser("kick")
        addSubparsers_kick.add_argument("target",type=str,nargs=1)

        addSubparsers_ban = addSubparsers.add_parser("ban")
        addSubparsers_ban.add_argument("target",type=str,nargs=1)
        addSubparsers_ban.add_argument("-d","--duration",required=False,type=str,nargs=1)

        # Finalize
        self.topParser = topParser
        self.addParser = addParser
    async def handleMessage(self,message):
        """Routes and executes command methods"""
        if message.content[:4] != '_DDD':
            return
        try:
            parsedCommand = self.topParser.parse_args(message.content[4:].split())
        except: # User error
            #TODO: Implement error handling
            #NOTE: Better error messages (e.g the help messages from the argparse library) aren't possible
            # due to the design of the argparse library not returning those messages in the exception :(
            await self.logger.error("There was an error in your command.\n  If you would like a help message, use the command _DDD help", message.channel)
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
