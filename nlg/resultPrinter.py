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
    elif len(subjectList)==0 and itemType != "director":
        itemType = "default"
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

def do(givenItemType, NLUOutput, resultList):
    itemType = givenItemType
    subject = getSubjectList(NLUOutput, itemType)
    if subject== None:
        itemType = "default"
        subject = []   

    printSentence = ""

    if len(resultList)<5:
        printSentence = getPrintSentence(itemType, subject)
    else:
        printSentence = getPrintSentence("default", [])

    result = printItems(givenItemType, resultList)

    nouns = getNouns(NLUOutput, subject)
        
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
            rstring += " and " + nlgu.flipPersons(itemType,str(result))
        elif n == len(resultList)-1:
            rstring += nlgu.flipPersons(itemType,str(result))
        else:
            rstring += nlgu.flipPersons(itemType,str(result))+", "
    return rstring

def printBigItemList(itemType, resultList):
    rstring = ""
    for result in resultList:
        rstring += nlgu.flipPersons(itemType,str(result))+"\n"
    return rstring 
    pass

def printItem(itemType, result):
    return nlgu.flipPersons(itemType,str(result))

def getNouns(NLUOutput, subjectList):
    returnList = []
    
    for subject in subjectList:
        a = []
        if NLUOutput[0][subject] in pronounKeys:
            a = [pronounSubjects[NLUOutput[0][subject]],pronounObjects[NLUOutput[0][subject]]]
        elif subject == "sort":
            order = NLUOutput[0].get("order")
            sortType = NLUOutput[0][subject]
            b = ""
            if order == "asc":
                if sortType == "gross":
                    b = "least profitable"
                if sortType == "rating":
                    b = "least popular"
                if sortType == "year":
                    b = "oldest"
            else: #if order == "desc":
                if sortType == "gross":
                    b = "most profitable"
                if sortType == "rating":
                    b = "most popular"
                if sortType == "year":
                    b = "newest"
            a = [b,b]
        else:
            a = [nlgu.flipPersons(subject, NLUOutput[0][subject]), nlgu.flipPersons(subject, NLUOutput[0][subject])]
        returnList.append(a)
#    print subjectList, returnList
    return returnList
