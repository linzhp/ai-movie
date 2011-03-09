#import nltk
import nlg_utils as nlgu
from os import path

pronounKeys = ["PREV_HE", "PREV_SHE", "PREV_IT"]
pronounSubjects = {"PREV_HE":"he", "PREV_SHE":"she", "PREV_IT":"it"}
pronounObjects = {"PREV_HE":"him","PREV_SHE":"her", "PREV_IT":"it"}

subjFromObj = {
#               "actor":[],
#               "part":[],
               "voice actor":["part"],
               "director":["title"],
#               "person":[],
               "title":["director","actor","sort","genre","part"],
               "genre":["title","actor","director"],
               "plot":["title"]
               }

def getPrintSentence(itemType, subjectList):
    subjectString = "_".join(subjectList);
    if len(subjectList)>0:
        subjectString+='_'
    fileName = path.dirname(__file__)+'/prs/'+subjectString+itemType + '_sentences.txt'
    rstring = nlgu.get_random_line(fileName)
    if rstring == "":
        print "ERROR"
    return rstring

def getSubjectList(NLUOutput, itemType):
    if subjFromObj.has_key(itemType):
        checklist = subjFromObj[itemType]
    else:
        return None

    rlist = []
    for key in NLUOutput[0].keys():
        if key in checklist:
            rlist.append(key)
    return rlist

def do(itemType, NLUOutput, resultList):
    subject = getSubjectList(NLUOutput, itemType)
    
    if subject== None:
        itemType = "default"
        subject = []
        
    printSentence = getPrintSentence(itemType, subject)

    result = printItems(itemType, resultList)

    nouns = getNouns(NLUOutput, itemType, subject)
        
    printSentence = printSentence.format(nouns, result)
    
    printSentence = printSentence[:1].capitalize()+printSentence[1:]
    return printSentence
    

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
            rstring += " and "+str(result)
        elif n == len(resultList)-1:
            rstring += str(result)
        else:
            rstring += str(result)+", "
    return rstring

def printBigItemList(itemType, resultList):
    rstring = ""
    for result in resultList:
        rstring += str(result)+"\n"
    return rstring 
    pass

def printItem(itemType, result):
    return str(result)

def getNouns(NLUOutput, itemType, subjectList):
    returnList = []
    for subject in subjectList:
        a = []
        if NLUOutput[0][subject] in pronounKeys:
            a = [pronounSubjects[NLUOutput[0][subject]],pronounObjects[NLUOutput[0][subject]]]
        else:
            a = [NLUOutput[0][subject],NLUOutput[0][subject]]
        returnList.append(a)
    print subjectList, returnList
    return returnList
