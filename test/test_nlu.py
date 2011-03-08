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
        

    def testNLU(self):
        with open('nlu.txt') as fixture:
            nlu_output=None
            nlu = NLUnderstanding()
            for line in fixture:
                line = line.strip()
                colon = line.find(':')
                if line[:colon].find('user')>=0:
                    nlu_output = nlu.process(line[colon+1:])
                    print "actual:" + str(nlu_output)
                elif line[:colon].find('NLU')>=0 and nlu_output is not None:
                    expected_output = eval(line[colon+1:])
                    print "expected: "+str(expected_output)
                    self.assertEqual(expected_output, nlu_output)
                    nlu_output = None
                    nlu = NLUnderstanding()
                
if __name__ == "__main__":
    import sys
    sys.path.append("../")
    from nlu import NLUnderstanding
    unittest.main()