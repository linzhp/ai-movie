'''
Created on Feb 9, 2011

@author: linzhp
'''
import unittest
from mock import Mock


class Test(unittest.TestCase):
    
    def setUp(self):
        # Let NLUnderstanding inherit from Mock so that we can test
        # it before implementing all methods
        NLUnderstanding.__bases__+=(Mock,)
        nlu = NLUnderstanding()
        Mock.__init__(nlu)
        

    def _testNLU(self):
        with open('nlg.txt') as fixture:
            nlu_output=None
            nlu = NLU()
            for line in fixture:
                line = line.strip()
                colon = line.find(':')
                if line[:colon].find('user')>=0:
                    nlu_output = nlu.process(line[colon+1:])
                elif line[:colon].find('NLU')>=0 and nlu_output is not None:
                    expected_output = eval(line[colon+1:])
                    self.assertEqual(expected_output, nlu_output)
                    nlu_output = None
                
if __name__ == "__main__":
    import sys
    sys.path.append("../")
    from nlu import NLUnderstanding
    unittest.main()