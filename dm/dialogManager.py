import sys
from os import path 
import howie.core    
import howie.configFile
from howie import aiml
current_dir = path.dirname(__file__)
sys.path.append(path.join(current_dir, ".."))
import dbi
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

def request(dict):
    pass

def command(dict):
    pass

def response(dict):
    pass

def off_topic(dict):
    return howie.core.submit(dict["off_topic"], "ai-movie-dialog-manager")

def input(list):
    for dict in list:
        if dict.has_key("request"):
            return request(dict)
        elif dict.has_key("command"):
            return command(dict)
        elif dict.has_key("response"):
            return response(dict)
        elif dict.has_key("off_topic"):
            return off_topic(dict)
        else:
            return None