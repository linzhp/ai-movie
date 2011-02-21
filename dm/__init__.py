import sys
from os import path 
import howie.core    
import howie.configFile
from howie import aiml
current_dir = path.dirname(__file__)
sys.path.append(path.join(current_dir, ".."))
import dbi

class DialogManager:
    def __init__(self):
        config = howie.configFile.load(path.join(current_dir, "../howie.ini"))
        config['cla.localMode']="yes"
        kernel = aiml.Kernel()
        
        # set up the kernel
        kernel.verbose(False)
        kernel.setPredicate("secure", "yes") # secure the global session
        kernel.bootstrap(
                         learnFiles=[path.join(current_dir, "../std-startup.xml"),path.join(howie.__path__[0], "../standard/std-*.aiml")], 
                         commands="bootstrap")
        kernel.setPredicate("secure", "no") # and unsecure it.
        
        # Initialize bot predicates
        for k,v in config.items():
            if k[:8] != "botinfo.":
                continue
            kernel.setBotPredicate(k[8:], v)
        
        howie.core.kernel=kernel    

    def request(self, dict):
        # Resolve role of a person
        if dict.has_key("person"):
            name = dict.pop("person")
            role=dbi.resolve_person(name)
            dict[role]=name
        # NLG does not need to be aware of below operations
        # to dict, make a copy of dict to hide the operations
        in_dict = dict.copy()
        # Resolve pronouns
        for key in in_dict:
            if in_dict[key] in ["PRE_HE", "PRE_IT"]:
                in_dict[key] = state.resolve_pronoun(in_dict[key])
                
        if in_dict["request"] == "opinion":
            pass
    #    dbi.query("director", {"genre":"action","keyword":"dream"}
    
    def command(self, dict):
        pass
    
    def response(self, dict):
        query_dict = {}
        if dict["response"]=="no":
            state.clear()
        elif dict["response"] == "yes":
            query_dict.update(state.get_all())
        elif self.pending_question:
            state.add({self.pending_question, dict["response"]})
            query_dict.update(state.get_all())
    
    def off_topic(self, dict):
        return howie.core.submit(dict["off_topic"], "ai-movie-dialog-manager")
    
    def input(self, list):
        query_dict=dict()
        for dict in list:
            if dict.has_key("request"):
                query_dict.update(self.request(dict))
            elif dict.has_key("command"):
                self.command(dict)
            elif dict.has_key("response"):
                self.response(dict)
            elif dict.has_key("off_topic"):
                self.off_topic(dict)
        