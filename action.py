class Action:
    """Base class for other actions."""
    def __init__(self):
        pass

class KickAction(Action):
    """Kicks a user.  A votekick"""
    def __init__(self):
        pass

    def serialize(self):
        """Provides a dict form of the action"""
        pass

class BanAction(Action):
    """Bans a user.  A voteban"""
    def __init__(self):
        pass

    def serialize(self):
        """Provides a dict form of the action"""
        pass