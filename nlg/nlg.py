import nltk

class NLG:

    def __init__(self, verbose=False):
        print "NLG initiated /n"
        pass

    def __listOutput(NLUinput,NLGinput):
        print "There were many results:", NLG[0].value, "\n"
        print "How many would you like to see?\n"
        pass

    def __printResults(NLUinput,NLGinput):
        print NLG[0].value, ":\n"
        if NLG[1].key == "results":
            for result in NLG[1].value:
                print result, "\n"
        pass

    def __likeResponse(NLUinput,NLGinput):
        print "That's nice.  Is there anything else you like?\n"
        pass

    def parseToOutput(self, NLUinput, NLGinput):

        if NLGinput[0].key == "list":
            __listOutput(NLUinput,NLGinput)
        elif NLGinput[0].key == "print":
            __printResults(NLUinput,NLGinput)
        elif NLGinput[0].key == "like":
            __likeResponse(NLUinput,NLGinput)




