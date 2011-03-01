import resultPrinter as rp
import nlg_utils as nlgu

def questionToUser(NLUOutput,DMOutput):
    # DMOutput should contain [question:FLAG]
    if DMOutput['question'] == 'HOW_MANY':
        print "How many would you like to see?"
    elif DMOutput['question'] == 'MORE_PREF':
        print "Could you help me narrow it down a bit?"
    else:
        print"NLG Error: Unknown Question Type"
    pass

def listOutput(NLUOutput,DMOutput):
    # DMOutput should be [list:SIZE,question:FLAG]
    resultNum = DMOutput['list']
    #print listSize #different response depending on size
    if resultNum < 0:
        print "NLG Error: List Size less than zero"
    elif resultNum == 1:
        print "There was one result.",
    elif resultNum < 60:
        print "There were {0} results.".format(nlgu.int_to_english(resultNum)),
    else:
        print "There were {0} results.".format(resultNum),
        
    if DMOutput.has_key("question"):
        questionToUser(NLUOutput,DMOutput)
    else:
        print ""
    pass

def printResults(NLUOutput,DMOutput):
    if not DMOutput.has_key('results'):
        print "NLG Error: invalid print request\n"
        return
    # DMOutput should be [print:ITEM_TYPE,results:[list,of,results,of,item,type]]
    itemType = DMOutput['print']
    resultList = DMOutput['results']
    if NLUOutput[0].has_key('response'):
        print "okay, here you go:"
        print rp.printItems(itemType,resultList)
    else:
        rp.do(itemType,NLUOutput, resultList) #Prints results. see nlg/resultPrinter.py

def likeResponse(NLUOutput,DMOutput):
    # DMOutput should be [like:thing]
    # NLUOutput should be the source of data for this.
    print "That's nice.  Is there anything else you like?"
    pass

def answerResponse(NLUOutput,DMOutput):
    # DMOutput should be [like:thing]or[like:thing,list:#]
    if DMOutput['answer'] == 'yes':
        print 'Yes.',
    elif DMOutput['answer'] == 'no':
        print 'No.',
    else:
        print 'Unknown.',
    if DMOutput.has_key("list"):
        listOutput(NLUOutput,DMOutput)
    pass

def process(NLUOutput, DMOutput):
    if DMOutput.has_key("answer"):
        answerResponse(NLUOutput,DMOutput)
    elif DMOutput.has_key("print"):
        printResults(NLUOutput,DMOutput)
    elif DMOutput.has_key("list"):
        listOutput(NLUOutput,DMOutput)
    elif DMOutput.has_key("question"):
        questionToUser(NLUOutput,DMOutput)
    elif NLUOutput[0].has_key("like"):
        likeResponse(NLUOutput,DMOutput)
    else:
        print "Well then, what would you like to talk about?"
    print ""
