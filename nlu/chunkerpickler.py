import sys
import pickle
from os import path


sys.path.append(path.join(path.dirname(__file__),"./.."))
import nlu



chk = nlu.chunker.Chunker(True)

with open('./chunkerpickler','wb') as outfile:
    print "starting pickle"
    pickle.dump(chk,outfile)
    outfile.closed
    print "finished pickle"

    

