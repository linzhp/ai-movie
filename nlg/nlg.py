import resultPrinter as rp
import nlg_utils as nlgu
from os import path
import random

def questionToUser(NLUOutput,DMOutput):
    # DMOutput should contain [question:FLAG]
    if DMOutput['question'] == 'HOW_MANY':
        return "How many would you like to see?\n"
    elif DMOutput['question'] == 'MORE_PREF':
        return "Could you help me narrow it down a bit?\n"
    elif DMOutput['question'] == 'SEE_RESULT?':
        return "Would you like to see the results?\n"
    elif DMOutput['question'] == 'CHOICE':
        DMOutput.pop('question')
        return giveSpellingOptions(DMOutput)
    else:
        print "NLG Error: Unknown Question Type: "+DMOutput['question']
        return ""
    
def giveSpellingOptions(misspelled_names):
    rstring = "I'm sorry I couldn't quite understand that.\n"
    misspelled_names  = misspelled_names 
    for name in misspelled_names:
        rstring+= "Specifically, who do you mean by {0}? ".format(nlgu.given_first(name))        
        i=0
        options = ""
        spellings = misspelled_names[name]
        while i<len(spellings): 
            if i == len(spellings)-1:
                options += " or "+nlgu.given_first(spellings[i])
            elif i == 0:
                options += nlgu.given_first(spellings[i])
            else:
                options += ", "+ nlgu.given_first(spellings[i])
            i = i+1
        rstring+="Could it be {0}?".format(options)
    if len(misspelled_names) >1:
        rstring += "Please list the correct spellings separated by commas so I can better understand you. Thanks!"
    return rstring
        
            

def listOutput(NLUOutput,DMOutput):
    # DMOutput should be [list:SIZE,question:FLAG]
    resultNum = DMOutput['list']
    #return listSize #different response depending on size
    if isinstance(resultNum, long):
        resultNum = int(resultNum)
    rstring = ""
    filePath = path.dirname(__file__)+'/prs/'
    if resultNum < 0:
        print "NLG Error: List Size less than zero"
    elif resultNum == 1:
        rstring += nlgu.get_random_line(filePath+"one_result.txt")
    elif resultNum == 0:
        rstring += nlgu.get_random_line(filePath+"no_result.txt")
    elif resultNum < 60:
        rstring += nlgu.get_random_line(filePath+"multi_result.txt").format(nlgu.int_to_english(resultNum))
    elif resultNum < 101:
        rstring += nlgu.get_random_line(filePath+"multi_result.txt").format(resultNum)
    else:
        print resultNum
        rstring += nlgu.get_random_line(filePath+"multi_result.txt").format(getRandomQuantifier())
        DMOutput['question'] == 'MORE_PREF'

    if resultNum == 0:
        rstring += "  Type 'reset' to start over." # This should be removed
    elif DMOutput.has_key("question"):
        rstring += ' '+questionToUser(NLUOutput,DMOutput)
    else:
        rstring += "\n"
    return rstring

def getRandomQuantifier():
    largeNumbers = ["hella","a lot of","many","a large number of","tons of"]
    return largeNumbers[random.randrange(0,len(largeNumbers))]


def printResults(NLUOutput,DMOutput):
    if isinstance(DMOutput['results'],long):
        DMOutput['list'] = DMOutput['results']
    
    if DMOutput.has_key("list"):
        return listOutput(NLUOutput,DMOutput)
    elif not DMOutput.has_key('results'):
        print "NLG Error: invalid print request\n"
        return ""
    
    if DMOutput['results']== None:
        print "Error: None Type Returned"
    if not isinstance(DMOutput['results'], list):
        print "Error: Non-List Type 'results' Returned"
        return
    elif len(DMOutput['results'])==0:
        return "Sorry, no results were found.\n"
    
    rstring = ""
    # DMOutput should be [print:ITEM_TYPE,results:[list,of,results,of,item,type]]
    itemType = DMOutput['print']
    resultList = DMOutput['results']
    if NLUOutput[0].has_key('response'):
        rstring += "okay, here you go:\n"
        rstring += rp.printItems(itemType,resultList)+'\n'
    else:
        rstring += rp.do(itemType,NLUOutput, resultList) #Prints results. see nlg/resultPrinter.py
    return rstring

def likeResponse(NLUOutput,DMOutput):
    # NLUOutput should be the source of data for this.
    return "That's nice.  Is there anything else you like?\n"

def exitResponse(NLUOutput,DMOutput):
    return "Goodbye. Thanks for using IMDB Chatbot Inernational.\n"

def answerResponse(NLUOutput,DMOutput):
    # DMOutput should be [like:thing]or[like:thing,list:#]
    rstring = ""
    if DMOutput['answer'] == 'yes':
        rstring += 'Yes. '
    elif DMOutput['answer'] == 'no':
        rstring += 'No. '
    else:
        rstring += 'Unknown. '
    if DMOutput.has_key("list"):
        rstring += listOutput(NLUOutput,DMOutput)
    else:
        rstring += '\n'
    return rstring

def offtopicResponse(offtopic_string):
    return offtopic_string

def process(NLUOutput, DMOutput):
    rstring = ""
    if DMOutput.has_key("answer"):
        rstring += answerResponse(NLUOutput,DMOutput)
    elif DMOutput.has_key("print"):
        rstring += printResults(NLUOutput,DMOutput)
    elif DMOutput.has_key("list"):
        rstring += listOutput(NLUOutput,DMOutput)
    elif DMOutput.has_key("question"):
        rstring += questionToUser(NLUOutput,DMOutput)
    elif DMOutput.has_key("off_topic"):
        return offtopicResponse(DMOutput["off_topic"])
    elif NLUOutput[0].has_key("like"):
        rstring += likeResponse(NLUOutput,DMOutput)
    elif NLUOutput[0].get("command")=="EXIT":
        rstring += exitResponse(NLUOutput,DMOutput)
    else:
        return "Well then, what would you like to talk about?"
    return rstring
