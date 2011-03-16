import chunker
import pickle
import sys
from os import path

sys.path.append(path.join(path.dirname(__file__),"./.."))
import nlu


print "loading chunker"
f  = open('./chunkerpickler.bin','rb')
chk = pickle.load(f)
print "done loading chunker"
#chk = chunker.Chunker(True,True)
input_text = ""

while input_text != "shoebox":

	input_text = raw_input("\nEnter a sentence:  ")
	
	chunked = chk.chunk(input_text)

	print chunked