'''
Created on Feb 9, 2011

@author: linzhp
'''
import unittest


class Test(unittest.TestCase):

    def testNLU(self):
        with open('nlu.txt') as fixture:
            nlu_output=None
            nlu = NLU()
            for line in fixture:
                line = line.strip()
                colon = line.find(':')
                if line[:colon].find('user')>=0:
                    nlu_output = nlu.process(line[colon+1:])
                elif line[:colon].find('NLU')>=0:
                    expected_output = eval(line[colon+1:])
                    self.assertEqual(expected_output, nlu_output)
                
if __name__ == "__main__":
    import sys
    sys.path.append("../")
    from nlu.nlu import NLU
    unittest.main()