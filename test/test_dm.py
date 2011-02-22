
import unittest
from mock import Mock

class Test(unittest.TestCase):
    def setUp(self):
        self.dm = DialogManager()
        self.dm.state = Mock()
        self.dm.dbi = Mock()

    def test_off_topic(self):
        self.assertEqual("What can I call you?", self.dm.off_topic({"off_topic":"Hi"}))
        
    def test_command(self):
        self.dm.command({"command":"CLEAR"})
        self.dm.state.mockCheckCall(0, 'clear')
        
    def test_request_director(self):
        self.dm.dbi.mockAddReturnValues(query=['James Cameron'])
        self.dm.state.mockAddReturnValues(get_all={'title':'Titanic'})
        result=self.dm.request({'request':'director','title':'Titanic'})
        self.dm.dbi.mockCheckCall(0, 'query','director',{'title':'Titanic'})
        self.dm.state.mockCheckCall(0, 'add_condition',{'title':'Titanic'})
        self.assertEqual({'print':'director','results':['James Cameron']},result)
        
    def test_request_movies(self):
        condition={'director':'James Cameron'}
        self.dm.dbi.mockAddReturnValues(query=30)
        self.dm.state.mockAddReturnValues(get_all=condition)
        result=self.dm.request({'request':'title','director':'James Cameron'})
        self.dm.dbi.mockCheckCall(0, 'query','title',condition)
        self.dm.state.mockCheckCall(0, 'add_condition',condition)
        self.assertEqual({'print':'title', 'list':30, 'question':'HOW_MANY'}, result)
        self.assertEqual('result_length', self.dm.pending_question)
        
    def test_request_opinion1(self):
        condition = {"genre":"action","keyword":"dream"}
        self.dm.dbi.mockAddReturnValues(query=7)
        self.dm.state.mockAddReturnValues(get_all=condition)
        request=dict(condition.items()+[('request','OPINION')])
        result=self.dm.request(request)
        self.dm.dbi.mockCheckCall(0, 'query', 'title',condition, count=True)
        self.dm.state.mockCheckCall(0, 'add_condition',condition)
        self.assertEqual({"list":7,"question":"SEE_RESULT?"}, result)

    def test_request_opinion2(self):
        condition = {"character":"Batman"}
        self.dm.dbi.mockAddReturnValues(query=70,resolve_person='character')
        self.dm.state.mockAddReturnValues(get_all=condition)
        result=self.dm.request({'request':'OPINION', "person":"Batman"})
        self.dm.dbi.mockCheckCall(1, 'query', 'title',condition, count=True)
        self.dm.state.mockCheckCall(0, 'add_condition',condition)
        self.assertEqual({"list":70,"question":"HOW_MANY"}, result)
        
#    def test_request_true_false(self):
#        condition={"actor":"Kate Winslet"}
#        self.dm.dbi.mockAddReturnValues(query=2)
        

if __name__ == "__main__":
    import sys
    sys.path.append("../dm")
    from dm import DialogManager
    unittest.main()