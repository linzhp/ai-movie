import string
import random
import logging

ten = {1:"ten", 2:"twenty", 3:"thirty", 4:"fourty", 5:"fifty"}
ones = {0:"zero", 1:"one", 2:"two", 3:"three", 4:"four", 5:"five", 6:"six", 7:"seven", 8:"eight", 9:"nine"}
teens = {0:"ten", 1:"eleven", 2:"twelve", 3:"thirteen", 4:"fourteen", 5:"fifteen", 6:"sixteen", 7:"nineteen"}

def int_to_english(myInt):
    if not isinstance(myInt,int):
        logging.debug( "NLG Integer Error: '"+str(myInt)+"'is not an integer")
        return myInt
    if myInt > 59 or myInt < 0:
        return "Error"
    returnString = ""
    if myInt > 19:
        returnString += ten[myInt/10]
        if myInt%10 != 0:
            returnString += " "+ones[myInt%10]
    elif myInt > 9:
        returnString += teens[myInt%10]
    else:
        returnString += ones[myInt]
    return returnString

def get_random_line(fileName):
    with open(fileName) as file:
        lines = file.readlines()
        return (lines[random.randrange(0,len(lines))].replace('\n',' ')).rstrip()

def flipPersons(itemType, item):
    if itemType in ['person','actor','director','voice actor']:
        return given_first(item).strip('.')
    else:
        return item.strip()

def given_first(name):
    if (name.count(',')):
        return invert_name(name)
    return name

# Take a name in the form Given1 Given2 GevenN FamilyName and return it as FamilyName, Given1 Given2 ...
def invert_name(s):
    if (s.count(',')):
        a=s.split(', ', 1)
    else:
        a=s.rsplit(' ', 1)
    a.reverse()
    return ' '.join(a)