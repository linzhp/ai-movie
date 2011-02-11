import sys
sys.path.append("../dbi")
import dbi

def __request(dict):
    pass

def __command(dict):
    pass

def __response(dict):
    pass

def __off_topic(dict):

def input(list):
    for dict in list:
        if dict.has_key("request"):
            __request(dict)
        elif dict.has_key("command"):
            __command(dict)
        elif dict.has_key("response"):
            __response(dict)
        elif dict.has_key("off_topic"):
            __off_topic(dict)
            
    