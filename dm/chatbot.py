from os import path 
import howie.core as core
import howie.configFile
from howie import aiml
current_dir = path.dirname(__file__)

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

core.kernel=kernel

reply = None

sessionID="movie selector"

def submit(input):
    global reply
    reply = core.submit(input, sessionID)
    return reply

def get_name():
    return core.kernel.getPredicate('name', sessionID)

if __name__=="__main__":
    submit("Clive is my name")
    print get_name()