'''
Created on Feb 9, 2011

@author: linzhp
'''
import unittest


class Test(unittest.TestCase):

    def testnlg(self):
        with open('corpus.txt') as fixture:
            nlg_output=None
            for line in fixture:
                line = line.strip()
                colon = line.find(':')
                if line[:colon].find('user')>=0:
                    pass
                elif line[:colon].find('NLU')>=0:
                    nlu_input = eval(line[colon+1:])
                    #print nlu_input
                elif line[:colon].find('NLG')>=0:
                    nlg_input = eval(line[colon+1:])
                    print nlg_input
                    nlg_output = nlg.process(nlu_input,nlg_input)
                    #print nlg_output
                else: #if line[:colon].find('BOT')>=0:
                    #print (line)
                    pass
                    

                
if __name__ == "__main__":
    import sys
    sys.path.append("../")
    from nlg import nlg 
    unittest.main()