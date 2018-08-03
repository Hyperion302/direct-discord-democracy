def getAvailableProps(server):
    """Checks all props for their permission status on a server.  Returns a list of available prop types"""
    p = server.me.server_permissions
    props = []
    if p.kick_members:
        props.append('kick')
    if p.ban_members:
        props.append('ban')
    return props
def fgetAvailableProps(server):
    """The same as getAvailableProps except it returns a string containing each prop, an example, and their parameters"""
    props = getAvailableProps(server)
    outStrings = []
    if 'kick' in props:
        outStrings.append("**kick** : target(user)\ne.g. `_DDD add kick @billy` (Kick @billy)")
    if 'ban' in props:
        outStrings.append("**ban** : target(user) duration(time)\ne.g. `_DDD add ban @billy 2d3h4m` (Ban @billy for 2 days, 3 hours, and 4 minutes)")
    return '\n'.join(outStrings)
genGeneralHelp = lambda server,utils : ("**Use the command `_DDD help -c <command>` to get more help on a specific command**\n"\
            "Available commands:\n"\
            "`add`\n"\
            "`admin`\n\n"\
            "**What is a 'proposition'?**\n\n"\
            "A 'proposition' is what this bot calls the various votes that you can create.  When you create a poll with the `_DDD add`, the bot creates a proposition and prints out it's ***status message***.\n\n"\
            "**How to vote:**\n\n"\
            "To vote on a specific proposition, add a :thumbsup: or :thumbsdown: reaction to the status message.\n\n"\
            "**How to cancel your proposition**:\n\n"\
            "If you want to cancel the proposition that *you* created, react to the status message with a :x: emoji.\n\n"\
            "**The following roles have immunity to the bot:**\n"\
            "%s\n"\
            "**To prevent immunity, put the Direct Discord Democracy role above their roles on the hierarchy.**") % '\n'.join([role.mention for role in utils.checkHierarchy(server,server.me)[0]])
genAddHelp = lambda server : ("**The add command is the focus of this bot.  Use it to add propositions to the server list.**\n"\
        "Provide parameters (if neccessary) to a proposition by adding them after the proposition.\n\n*user* type parameters MUST be specified in @mention form.\n*date* and *time* type parameters MUST be specified in DdHhMm (e.g. 0d0h1m)\n\n"\
        "Available proposition types and their parameters:\n<prop type> : <parameter 1>(<parameter 1 type>) etc.\n"\
        "%s\n\n"\
        "**NOTE: For the bot to execute actions that require a target, the target's highest role must be *below* the bot's highest role**") % fgetAvailableProps(server)
removeHelp = "**The remove command *deactivates* a proposition.  This will make votes ineffective and prevent the proposition from being executed.**\n"\
        "Remove requires the ID of the proposition to remove, and it can **ONLY** be run by the *creator* of the proposition\n\n"\
        "Example:\n"\
        "_DDD remove 2 (removes the proposition with the ID 2)"
statusHelp = "**The status command prints a new view message and deletes the old one**\n"\
        "The 'view message' is the message that desplays votes and is where users vote.\n"\
        "Status requires the ID of the proposition to print, and it can **ONLY** be run by the *creator* of the proposition\n"\
        "**CAUTION: All current votes will become undoable, as the voters won't be able to remove their reactions!**\n\n"\
        "Example:\n"\
        "_DDD status 2 (prints the status message of the proposition with the ID 2)"
adminHelp = "**The admin command is meant for values that are to be configured during bot setup.  These values *cannot* be changed by vote.**\n"\
        "The values that can be changed are both optionally specified in shell-style optionals (`-q` or `--quorum` for quorum, `-d` or `--delay` for delay)\n"\
        "Default values are 25 for quorum and 2 hours for delay.\n\n"\
        "Delay:\n"\
        "The bot will wait for a certain period of time before tallying the vote count on an action.\nThis period of time is specified server wide by the delay value.\n"\
        "The delay should be specified as DdHhMm (e.g. 0d0h1m).\n"\
        "**NOTE: If a vote fails after the delay, the bot will *still* tally votes *every minute* for that action.  This is by design.**\n\n"\
        "Quorum:\n"\
        "**'quorum. [(kwawr-uhm)] The minimum number of members of a committee or legislative body who must be present before business can officially or legally be conducted.'**\n"\
        "After the delay, one of the things the bot will check for when the delay is over is the quorum.\nThe server has a global quorum that must be reached which is used to calculate: `(yae+nae)/server.member_count >= serverData.quorum`\n"\
        "The quourum should be specified as an integer between 1 and 100, inclusive.  This is converted to a *percent* of the server."
aboutHelp = "**The about command displays introductory information about the DDD bot**"