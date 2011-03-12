import chunker
import pickle


chk = chunker.Chunker(True)

with open('./chunkerpickler','w') as outfile:
    print "starting pickle"
    pickle.dump(chk,outfile)
    outfile.closed

    

