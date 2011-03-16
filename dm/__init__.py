import sys
from os import path 
current_dir = path.dirname(__file__)
sys.path.append(path.join(current_dir, ".."))
from dbi import dbi
import chatbot
from state import State

# TODO check people names before calling
# TODO when user's preference include 'title', don't search 'title' anymore
class DialogManager:
    def __init__(self):
        self.pending_question = None
        self.state = State()
        self.dbi = dbi 

    def request(self, dict):
        # NLG does not need to be aware of below operations
        # to dict, make a copy of dict to hide the operations
        internal_dict = dict.copy()
        # Resolve pronouns
        not_resolved = []
        for key in internal_dict:
            if internal_dict[key] in ["PREV_HE", "PREV_IT"]:
                resolved_pronoun= self.state.resolve_pronoun(internal_dict[key])
                if resolved_pronoun == 'error':
                    not_resolved.append(key)
                else:
                    internal_dict[key] = resolved_pronoun
        for key in not_resolved:
            internal_dict.pop(key)
        request_type = internal_dict.pop("request")
        if request_type == OPINION:
            internal_dict['request']='title'
            self.state.add_request(internal_dict)
            internal_dict = self.state.get_all()

            count=self.dbi.query('title',internal_dict, count=True)
            if count>10:
                self.pending_question = "result_length"
                return {"list":count, "question":MORE_PREF}
            else:
                self.pending_question = SEE_RESULT
                return {"list":count, "question":self.pending_question}
        elif request_type == COUNT:
            of = internal_dict.pop("of")
            state_dict = {'request':of}
            state_dict.update(internal_dict)
            self.state.add_request(state_dict)
            count=self.dbi.query(of, internal_dict, count=True)
            result={}
            if count>10:
                self.pending_question = "result_length"
                result={"list":count, "question":HOW_MANY}
            else:
                self.pending_question = SEE_RESULT
                result={"list":count, "question":self.pending_question}
            return result
        elif request_type == SIMILAR:
            self.state.add_request(internal_dict)
            internal_dict = self.state.get_all()
            if not internal_dict.has_key('title'):
                return {'off_topic':chatbot.reply}
            title = internal_dict['title']
            if internal_dict.has_key('result_length'):
                result_length= internal_dict.pop('result_length')
            else:
                result_length = 10
            internal_dict.pop('title')
            if len(internal_dict) <3:
                if not internal_dict.has_key('director'):
                    title_dict={'title':title}
                    internal_dict['director']=self.dbi.query("director",\
                                         title_dict, [0,1])[0]
                if not internal_dict.has_key('genre'):
                    internal_dict['genre']=self.dbi.query('genre', title_dict, [0,1])[0]
            
            movie_list = self.dbi.query("title", internal_dict, [0,result_length*5])
            if title in movie_list:
                movie_list.remove(title)
            if len(movie_list)>result_length:
                commonalities = [dbi.commonality(title, movie) for movie in movie_list]
                title_common=zip(movie_list, commonalities)
                title_common=sorted(title_common, \
                                    lambda x,y:cmp(x[1],y[1]))[0,result_length]
                results = [item[0] for item in title_common]
            else:
                results = movie_list
            return {'print':'title','results':results}
        else:
            count = internal_dict.get('result_length')
            if count:
                internal_dict.pop('result_length')
                count = [0,count]
            elif request_type=="plot" or request_type=="year":
                count = [0, 1]
            results=self.dbi.query(request_type, internal_dict, count=count)
            state_dict = {'request':request_type}
            state_dict.update(internal_dict)
            self.state.add_request(state_dict)
            if isinstance(results, int):
                if len(internal_dict)<2:
                    self.pending_question=MORE_PREF
                    return {"question":MORE_PREF}
                else:
                    self.pending_question = "result_length"
                    return {'print':request_type,"list":results, "question":HOW_MANY}
            else:
                self.state.add_result({request_type:results})
                return {'print':request_type,'results':results}
            
    
    def command(self, dict):
        if dict["command"]==CLEAR:
            self.state.clear()
    
    def response(self, dict):
        internal_dict = dict.copy()
        response = internal_dict.pop("response")
        if response=="NO":
            # FIXME check any problem here 
            return {}
        elif response == "YES":
            if self.pending_question:
                internal_dict["request"]=self.state.last_request()
                internal_dict.update(self.state.get_all())
        elif self.pending_question:
            internal_dict[self.pending_question]=response
            internal_dict["request"]=self.state.last_request()
            internal_dict.update(self.state.get_all())
        self.pending_question = None
        return self.request(internal_dict)
    
    def off_topic(self, dict):
        reply = chatbot.reply
        if reply is None:
            reply = chatbot.submit(dict['off_topic'])
        return {'off_topic':reply}
    
    def input(self, list):
        result_dict={}
        for dict in list:
            if dict.has_key("request"):
                result_dict.update(self.request(dict))
            elif dict.has_key("command"):
                self.command(dict)
            elif dict.has_key("response"):
                result_dict.update(self.response(dict))
            elif dict.has_key("off_topic"):
                result_dict=self.off_topic(dict)
        self.state.add_result(result_dict)
        return result_dict
        
# Define constants        
HOW_MANY = "HOW_MANY"
SEE_RESULT="SEE_RESULT?"
MORE_PREF="MORE_PREF"
EXIT="EXIT"
CLEAR="CLEAR"
COUNT="COUNT"
OPINION='OPINION'
SIMILAR = 'SIMILAR'
