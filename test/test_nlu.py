'''
Created on Feb 9, 2011

@author: linzhp
'''
import unittest
#from mock import Mock


class Test(unittest.TestCase):
    
    def setUp(self):
        self.nlu = NLUnderstanding()
        

    def testNLU(self):
        with open('nlu.txt') as fixture:
            nlu_output=None
            nlu = self.nlu
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
#                    nlu.state
                    
    def testEnglish2Int(self):
        self.assertEqual(12,utils.english2int('12'))
        self.assertEqual(1,utils.english2int('a'))
        self.assertEqual(None, utils.english2int('F.D.R'))
                
if __name__ == "__main__":
    import sys
    sys.path.append("../")
    from nlu import NLUnderstanding,utils
    unittest.main()