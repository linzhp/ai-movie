#import nltk

statePronounSubjects = {"PREV_HE":"he", "PREV_SHE":"she", "PREV_IT":"it"}
statePronounObjects = {"PREV_HE":"him","PREV_SHE":"her", "PREV_IT":"it"}

def getPrintSentence(itemType):
    with open('../nlg/prs/'+itemType + '_sentences.txt') as fixture:
        for line in fixture:
            return line
    pass

def do(itemType, NLUOutput, resultList):
    printSentence = getPrintSentence(itemType)

    result = printItems(itemType, resultList)

    pronouns = getNouns(NLUOutput, itemType)
        
    print printSentence.format(pronouns, result)

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
    return ("he", "him")
    pass
