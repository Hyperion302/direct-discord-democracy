from db import DBTable
from action import Action
from logger import Logger
class CommandManager:
    """Handles command detection and emoji reaction detection"""
    def __init__(self):
        pass
    
    def parseMessage(self,message):
        """Handles a message and returns a list containing the command and it's parameters.\n  If not command is present, returns None"""
        if message[0] != '>':
            return None
        # Strip first character
        command = message[1:]

        # Break into command parameters
        command_params = command.split(':')

        return command_params
    def handleMessage(self,message):
        """Routes and executes command methods"""
        command_parameters = self.parseMessage(message.content)
        if not command_parameters:
            return
        route = {
            "add": self.add,
            "list": self.list_,#TODO: Better name
            "status": self.status,
            "help": self.help,
            "about": self.about,
            "find": self.find
        }
        route[command_parameters[0]](command_parameters,message)
    def handleEmoji(self,emoji,message):
        """Handles an emoji reaction to a message"""
        pass

    def add(self,params,message):
        """The add command adds a proposition"""
        pass
    
    def list_(self,params,message):
        """The list command lists quick info about all current propositions"""
        pass
    
    def status(self,params,message):
        """The status command creates a new link message that you can add emoji\n reactions to"""
        pass
    
    def help(self,params,message):
        """The help command prints out help info on commands"""
        pass
    
    def about(self,params,message):
        """The about command lists quick facts about the bot"""
        pass
    
    def find(self,params,message):
        """The find command queries for a proposition and prints a new status command\ne.g. status command above"""
        pass
    
    def handleVote(self,user,action):
        """Handle function that should only be called by handleMessage"""
        pass