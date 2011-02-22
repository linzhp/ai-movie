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
        self.pending_question = None

    def request(self, dict):
        # Resolve role of a person
        if dict.has_key("person"):
            name = dict.pop("person")
            role=dbi.resolve_person(name)
            dict[role]=name
        # NLG does not need to be aware of below operations
        # to dict, make a copy of dict to hide the operations
        internal_dict = dict.copy()
        # Resolve pronouns
        for key in internal_dict:
            if internal_dict[key] in ["PRE_HE", "PRE_IT"]:
                internal_dict[key] = state.resolve_pronoun(internal_dict[key])
        
        request_type = internal_dict["request"]
        state.add_condition(internal_dict)
        internal_dict = state.get_all()
        if request_type == "opinion":
            internal_dict["request"]="count"
            internal_dict["of"]="title"
            self.pending_question = "SEE_RESULT?"
            dbi.query(internal_dict)
        elif request_type == "true_false":
            pass
            
    
    def command(self, dict):
        if dict["command"]=="clear":
            state.clear()
    
    def response(self, dict):
        internal_dict = dict.copy()
        response = internal_dict.pop("response")
        if response=="no":
            state.clear()
        elif response == "yes":
            internal_dict["request"]="title"
        elif self.pending_question:
            internal_dict[self.pending_question]=response
            self.pending_question = None
            internal_dict["request"]="title"
        return self.request(internal_dict)
    
    def off_topic(self, dict):
        return howie.core.submit(dict["off_topic"], "ai-movie-dialog-manager")
    
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
        return result_dict
