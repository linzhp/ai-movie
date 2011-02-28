import sys
from os import path 
current_dir = path.dirname(__file__)
sys.path.append(path.join(current_dir, ".."))
import dbi
import chatbot

#TODO increase the priority of movie title in state
class DialogManager:
    def __init__(self):
        self.pending_question = None
        self.state = None #TODO initialize state here
        self.dbi = None #TODO initialize dbi here

    def request(self, dict):
        # Resolve role of a person
        if dict.has_key("person"):
            name = dict.pop("person")
            role=self.dbi.resolve_person(name)
            dict[role]=name
        # NLG does not need to be aware of below operations
        # to dict, make a copy of dict to hide the operations
        internal_dict = dict.copy()
        # Resolve pronouns
        for key in internal_dict:
            if internal_dict[key] in ["PRE_HE", "PRE_IT"]:
                internal_dict[key] = self.state.resolve_pronoun(internal_dict[key])
        if internal_dict.has_key("result_length"):
            state_dict=internal_dict.copy()
            state_dict.pop("result_length")
            self.state.add_request(state_dict)
        else:
            self.state.add_request(internal_dict)
        internal_dict = self.state.get_all()
        request_type = internal_dict.pop("request")
        if request_type == OPINION:
            self.pending_question = HOW_MANY
            count=self.dbi.query('title',internal_dict, count=True)
            if count>10:
                self.pending_question = HOW_MANY
            else:
                self.pending_question = SEE_RESULT
            return {"list":count, "question":self.pending_question}
        elif request_type == COUNT:
            of = internal_dict.pop("of")
            count=self.dbi.query(of, internal_dict, count=True)
            result={}
            if count>10:
                self.pending_question = "result_length"
                result={"list":count, "question":HOW_MANY}
            else:
                self.pending_question = SEE_RESULT
                result={"list":count, "question":self.pending_question}
            return result
        else:
            results=self.dbi.query(request_type, internal_dict)
            if isinstance(results, int):
                if len(internal_dict)<2:
                    self.pending_question=MORE_PREF
                    return {"question":MORE_PREF}
                else:
                    self.pending_question = "result_length"
                    return {'print':request_type,"list":results, "question":HOW_MANY}
            else:
                self.state.add_result(results)
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
        elif self.pending_question:
            internal_dict[self.pending_question]=response
            internal_dict["request"]=self.state.last_request()
        self.pending_question = None
        return self.request(internal_dict)
    
    def off_topic(self, dict):
        return chatbot.submit(dict["off_topic"])
    
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