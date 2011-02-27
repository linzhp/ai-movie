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
        self.dm.state.mockAddReturnValues(get_all={'request':'director','title':'Titanic'})
        result=self.dm.request({'request':'director','title':'Titanic'})
        self.dm.dbi.mockCheckCall(0, 'query','director',{'title':'Titanic'})
        self.dm.state.mockCheckCall(0, 'add_request',{'request':'director','title':'Titanic'})
        self.assertEqual({'print':'director','results':['James Cameron']},result)

    def test_request_movies(self):
        condition={'director':'James Cameron'}
        self.dm.dbi.mockAddReturnValues(query=30)
        self.dm.state.mockAddReturnValues(get_all={'request':'title','director':'James Cameron'})
        result=self.dm.request({'request':'title','director':'James Cameron'})
        self.dm.dbi.mockCheckCall(0, 'query','title',condition)
        self.dm.state.mockCheckCall(0, 'add_request',{'request':'title','director':'James Cameron'})
        self.assertEqual({'question':'MORE_PREF'}, result)
        self.assertEqual('MORE_PREF', self.dm.pending_question)

    def test_request_opinion1(self):
        condition = {"genre":"action","keyword":"dream"}
        self.dm.dbi.mockAddReturnValues(query=7)
        self.dm.state.mockAddReturnValues(get_all={"genre":"action","keyword":"dream",'request':'OPINION'})
        request=dict(condition.items()+[('request','OPINION')])
        result=self.dm.request(request)
        self.dm.dbi.mockCheckCall(0, 'query', 'title',condition, count=True)
        self.dm.state.mockCheckCall(0, 'add_request',{"genre":"action","keyword":"dream",'request':'OPINION'})
        self.assertEqual({"list":7,"question":"SEE_RESULT?"}, result)

    def test_request_opinion2(self):
        condition = {"character":"Batman"}
        self.dm.dbi.mockAddReturnValues(query=70,resolve_person='character')
        self.dm.state.mockAddReturnValues(get_all={'request':'OPINION', "character":"Batman"})
        result=self.dm.request({'request':'OPINION', "person":"Batman"})
        self.dm.dbi.mockCheckCall(1, 'query', 'title',condition, count=True)
        self.dm.state.mockCheckCall(0, 'add_request',{'request':'OPINION', "character":"Batman"})
        self.assertEqual({"list":70,"question":"HOW_MANY"}, result)
        
    def test_request_count(self):
        condition={"actor":"Kate Winslet"}
        self.dm.dbi.mockAddReturnValues(query=2)
        self.dm.state.mockAddReturnValues(get_all={'request':'COUNT',"actor":"Kate Winslet", 'of':"Academy Award"})
        result=self.dm.request({'request':'COUNT','of':'Academy Award',"actor":"Kate Winslet"})
        self.dm.dbi.mockCheckCall(0, 'query', 'Academy Award',condition, count=True)
        self.dm.state.mockCheckCall(0, 'add_request',{'request':'COUNT',"actor":"Kate Winslet", 'of':"Academy Award"})
        self.assertEqual({'list':2,'question':"SEE_RESULT?"},result)
        
    def test_response_yes(self):
        self.dm.pending_question='SEE_RESULT?'
        self.dm.dbi.mockAddReturnValues(query=["Titanic", "The Reader"])
        self.dm.state.mockAddReturnValues(get_all={'request':'title','actor':'Kate Winslet'},last_request='title')
        result = self.dm.response({'response':'yes'})
        self.dm.dbi.mockCheckCall(0, 'query', 'title', {'actor':'Kate Winslet'})
        self.dm.state.mockCheckCall(1, 'add_request',{'request':'title'})
        self.assertEqual({'print':'title','results':["Titanic", "The Reader"]},result)
        
    def test_response_2(self):
        self.dm.dbi.mockAddReturnValues(query=["Pirates of the Caribbean", "Pride and Prejudice"])
        self.dm.state.mockAddReturnValues(get_all={'request':'title','actor':'Keira Knightley'},last_request='title')
        self.dm.pending_question='result_length'
        result = self.dm.response({'response':2})
        self.dm.dbi.mockCheckCall(0, 'query', 'title', {'actor':'Keira Knightley'})
        self.dm.state.mockCheckCall(1, 'add_request',{'request':'title'})
        self.assertEqual({'print':'title','results':["Pirates of the Caribbean", "Pride and Prejudice"]},result)

if __name__ == "__main__":
    import sys
    sys.path.append("../dm")
    from dm import DialogManager
    unittest.main()
