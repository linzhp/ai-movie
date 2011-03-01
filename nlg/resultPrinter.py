#import nltk
import nlg_utils as nlgu

pronounSubjects = {"PREV_HE":"he", "PREV_SHE":"she", "PREV_IT":"it"}
pronounObjects = {"PREV_HE":"him","PREV_SHE":"her", "PREV_IT":"it"}

subjFromObj = {
               "actor":[],
               "part":[],
               "title":["director","actor","sort","genre","part"],
               "director":[],
               "genre":["title","actor","director"],
               "plot":[],
               "voice actor":[]
               }

def getPrintSentence(itemType, subjectType):
    fileName = '../nlg/prs/'+subjectType+itemType + '_sentences.txt'
    rstring = nlgu.get_random_line(fileName)
    if rstring == "":
        print "ERROR"
    return rstring

def getSubject(NLUOutput, itemType):
    # if the program fails here add another entry to the dict 
    checklist = subjFromObj[itemType] 
    rstring = ""
    for key in NLUOutput[0].keys():
        if key in checklist:
            rstring += key +'_'
    return rstring

def do(itemType, NLUOutput, resultList):
    printSentence = getPrintSentence(itemType, getSubject(NLUOutput, itemType))

    result = printItems(itemType, resultList)

    pronouns = getNouns(NLUOutput, itemType)
        
    print printSentence.format(pronouns, result),

def printItems(itemType, resultList):
    if len(resultList)==1:
        return printItem(itemType, resultList[0]) 
    elif len(resultList)<5:
        return printSmallItemList(itemType, resultList) 
    else:
        return printBigItemList(itemType, resultList)
        

def printSmallItemList(itemType, resultList): 
    n = 0
    rstring = ""
    for result in resultList:
        n += 1 
        if n == len(resultList):
            rstring += " and "+result
        elif n == len(resultList)-1:
            rstring += result
        else:
            rstring += result+", "
    return rstring

def printBigItemList(itemType, resultList):
    rstring = ""
    for result in resultList:
        rstring += result+"\n"
    return rstring 
    pass

def printItem(itemType, result):
    return result

def getNouns(NLUOutput, itemType):
    return ("he", "him", "it")
    pass
