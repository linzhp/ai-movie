import nltk

class NLG:

    def __init__(self, verbose=False):
        print "NLG initiated /n"
        pass

    def __listOutput(NLUinput,NLGinput):
        pass

    def __printResults(NLUinput,NLGinput):
        print NLG[0].value
        if NLG[1].key == "results":
            for result in NLG[1].value:
                print result + "\n"
        pass

    def __likeResponse(NLUinput,NLGinput):
        pass

    def parseToOutput(self, NLUinput, NLGinput):

        if NLGinput[0].key == "list":
            __listOutput(NLUinput,NLGinput)
        elif NLGinput[0].key == "print":
            __printResults(NLUinput,NLGinput)
        elif NLGinput[0].key == "like":
            __likeResponse(NLUinput,NLGinput)




