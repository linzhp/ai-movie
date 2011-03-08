import resultPrinter as rp
import nlg_utils as nlgu

def questionToUser(NLUOutput,DMOutput):
    # DMOutput should contain [question:FLAG]
    if DMOutput['question'] == 'HOW_MANY':
        return "How many would you like to see?\n"
    elif DMOutput['question'] == 'MORE_PREF':
        return "Could you help me narrow it down a bit?\n"
    else:
        print "NLG Error: Unknown Question Type"
        return ""

def listOutput(NLUOutput,DMOutput):
    # DMOutput should be [list:SIZE,question:FLAG]
    resultNum = DMOutput['list']
    #return listSize #different response depending on size
    rstring = ""
    if resultNum < 0:
        print "NLG Error: List Size less than zero"
    elif resultNum == 1:
        rstring += "There was one result."
    elif resultNum < 60:
        rstring += "There were {0} results.".format(nlgu.int_to_english(resultNum))
    else:
        rstring += "There were {0} results.".format(resultNum)
        
    if DMOutput.has_key("question"):
        rstring += ' '+questionToUser(NLUOutput,DMOutput)
    else:
        rstring += "\n"
    return rstring

def printResults(NLUOutput,DMOutput):
    if not DMOutput.has_key('results'):
        print "NLG Error: invalid print request\n"
        return ""
    if DMOutput['results']== None:
        print "Error: None Type Returned"
    if len(DMOutput['results'])==0:
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
        return DMOutput["off_topic"]
    elif NLUOutput[0].has_key("like"):
        rstring += likeResponse(NLUOutput,DMOutput)
    elif NLUOutput[0].get("command")=="EXIT":
        rstring += exitResponse(NLUOutput,DMOutput)
    else:
        return "Well then, what would you like to talk about?"
    return rstring
