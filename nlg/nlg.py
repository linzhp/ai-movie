import nltk

def listOutput(NLUinput,NLGinput):
    # NLGinput should be [list:SIZE,question:TYPE]
    print "There were many results: ", NLGinput[0]['list']
    if NLGinput[0].has_key('question'):
        if NLGinput[0]['question'] == 'RESULT_LENGTH':
            print "How many would you like to see?\n"
        elif NLGinput[0]['question'] == 'MORE_PREF':
            print "Could you help me narrow it down a bit?\n"
    pass

def printResults(NLUinput,NLGinput):
    # NLGinput should be [print:ITEM_TYPE,results:[list,of,results,of,item,type]]
    print NLGinput[0]['print'], ":"
    for result in NLGinput[0]['results']:
        print result
    print
    pass

def likeResponse(NLUinput,NLGinput):
    # NLGinput should be [like:thing]
    print "That's nice.  Is there anything else you like?\n"
    pass

def answerResponse(NLUinput,NLGinput):
    # NLGinput should be [like:thing]
    if NLGinput[0].has_key("list"):
        listOutput(NLUinput,NLGinput)
    print "That's nice.  Is there anything else you like?\n"
    pass

def process(NLUinput, NLGinput):
    if NLGinput[0].has_key("answer"):
        answerResponse(NLUinput,NLGinput)
    elif NLGinput[0].has_key("print"):
        printResults(NLUinput,NLGinput)
    elif NLGinput[0].has_key("like"):
        likeResponse(NLUinput,NLGinput)
    elif NLGinput[0].has_key("list"):
        listOutput(NLUinput,NLGinput)
