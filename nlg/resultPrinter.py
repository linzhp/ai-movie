#import nltk
import nlg_utils as nlgu

pronounKeys = ["PREV_HE", "PREV_SHE", "PREV_IT"]
pronounSubjects = {"PREV_HE":"he", "PREV_SHE":"she", "PREV_IT":"it"}
pronounObjects = {"PREV_HE":"him","PREV_SHE":"her", "PREV_IT":"it"}

subjFromObj = {
               "actor":[],
               "part":[],
               "title":["director","actor","sort","genre","part"],
               "director":["title"],
               "genre":["title","actor","director"],
               "plot":["title"],
               "voice actor":["part"]
               }

def getPrintSentence(itemType, subjectList):
    subjectString = "_".join(subjectList);
    if len(subjectList)>0:
        subjectString+='_'
    fileName = '../nlg/prs/'+subjectString+itemType + '_sentences.txt'
    rstring = nlgu.get_random_line(fileName)
    if rstring == "":
        print "ERROR"
    return rstring

def getSubjectList(NLUOutput, itemType):
    # if the program fails here add another entry to the dict 
    checklist = subjFromObj[itemType] 
    rlist = []
    for key in NLUOutput[0].keys():
        if key in checklist:
            rlist.append(key)
    return rlist

def do(itemType, NLUOutput, resultList):
    subject = getSubjectList(NLUOutput, itemType)

    printSentence = getPrintSentence(itemType, subject)

    result = printItems(itemType, resultList)

    pronouns = getNouns(NLUOutput, itemType, subject)
        
    printSentence = printSentence.format(pronouns, result)
    
    print printSentence[:1].capitalize()+printSentence[1:],

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
    return ("he", "him", "it")
