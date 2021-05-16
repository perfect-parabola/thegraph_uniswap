import datetime
import os

def toUnixtime(str):
    os.environ["TZ"] = "UTC"
    timestamp = datetime.datetime.strptime(str, '%Y-%m-%d').strftime("%s")
    return timestamp

def toString(unix):
    os.environ["TZ"] = "UTC"
    string = datetime.datetime.utcfromtimestamp(unix).strftime('%Y-%m-%d')
    return string