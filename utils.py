import re,math,asyncio

def toSeconds(ts):
    """Converts a time string in format DD:HH:MM into into seconds"""
    #TODO: Protect string from matching large numbers like 29h
    match = re.match(r"([0-9]{1,3})d([0-2]*[0-9])h([0-6]*[0-9])m",ts).groups()
    if not match:
        return None
    #      1 DAY = 86400 SEC            1 HOUR = 3600 SEC          1 MINUTE = 60 SEC
    return int(match[0])*86400 + int(match[1])*3600 + int(match[2])*60
    #TODO: ERROR HANDLING
def fromSeconds(sec):
    """Converts a seconds count into DD:HH:MM format and returns it as a tuple"""
    days = math.floor(sec/86400)
    sec = sec - days * 86400

    hours = math.floor(sec/3600)
    sec = sec - hours * 3600

    minutes = math.floor(sec/60)
    sec = sec - hours * 3600

    #TODO: If sec is now >0, throw an error.

    return (days,hours,minutes)

def ffromSeconds(sec):
    """Wraps fromSeconds to return a formatted string"""
    return "%dd%dh%dm" % fromSeconds(sec)

def fffromSeconds(sec):
    """Provides an extra layer of formatting for fromSeconds"""
    string = ""
    time = fromSeconds(sec)
    if time[0]:
        string = string + "%d Day%s " % (time[0],'s' if time[0] > 1 else '')
    if time[1]:
        string = string + "%d Hour%s " % (time[1],'s' if time[1] > 1 else '')
    if time[2]:
        string = string + "%d Minute%s " % (time[2],'s' if time[2] > 1 else '')
    if string == "":
        string = "No Time"

    return string

def mentionToId(mention):
    """Converts a mention string to an ID"""
    return mention.replace('<@!','').replace('>','')
def idToMention(id):
    """Converts an ID to a mention string"""
    return "<@!%s>" % id

