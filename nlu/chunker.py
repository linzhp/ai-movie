#
# To instantiate a chunker:
#
#		x = chunker.Chunker()
#
# To Chunk:
#
#		x.chunk(string)
#
# Example:
#
# 		import chunker
# 		chk = chunker.Chunker()
# 		chunk_tree = chk.chunk("Who directed \"The Big Lebowski\"?")

import nltk
import pickle
from os import path

class Chunker:

	def __init__(self, verbose=False):

		if verbose:
			print "#Initializing chunker:"

		# Define regular expressions for punctuation tags
		tagged_punc = [ (r'\"', ':'), (r'\?', 'QM') ]

		if verbose:
			print "   Loading POS tagged training sentences."

		# Load the tagged training sentences.
		f = open( path.dirname(__file__)+'/training_sentences', 'r' )
		train_sents = pickle.load(f)

	
		# Define the tagger.

		if verbose:
			print "   Loading maxent_treebank_pos_tagger."

		_POS_TAGGER = 'taggers/maxent_treebank_pos_tagger/english.pickle'
		t1 = nltk.data.load(_POS_TAGGER)
		if verbose:
			print "   Training custom Unigram Tagger."		
		t2 = nltk.UnigramTagger( train_sents, backoff=t1 )

		if verbose:
			print "   Instantiating tagger object."

		self.tagger = nltk.RegexpTagger( tagged_punc, backoff=t2 )

		# Define a chunking grammar.
		chunk_grammar = r"""
			B-QUESTION: {<[W].*><DT|RB.*|JJ>*<MD|VB.*|KW_.*>}
						{<WRB>}
			COMMAND: {^(<MD><PRP>)?(<RB>)*<VB.*>}
						{^<PRP><VBP><TO>}
			TITLE: {<:><[^:]*>*<:>}	
			PERSON: {<NNP[S]?>+}
			NP:   {<PRP\$>?<JJ>*<NN|NNS>(<POS>?<JJ>*<NN|NNS>)*}
			PP: { <IN><NP> }
		"""
			#ACTOR_IN_MOVIE: {<PERSON><.*>*<IN><TITLE>}
			#S: {<CC><.*>*}
		   	#B-QUESTION: {^<[W].*|VBD|VBN|VBP|VBZ>}
		if verbose:
			print "   Instantiating RegexpParser object."
		
		# Define a regular expression chunker
		self.cp = nltk.RegexpParser(chunk_grammar)

		if verbose:
			print "Chunker Initialized.#"
		

	# Takes a string and returns a chunk tree.
	def chunk(self, sentence):

		tokd = nltk.word_tokenize(sentence)
		tagged = self.tagger.tag(tokd)
		print tagged
		chunked = self.cp.parse(tagged)

		#print "\n\nChunked - tree\n"
		#print chunked

		return chunked

if __name__ == '__main__':
	chk = Chunker()
	result = chk.chunk("""I want to see some super hero movie?""")
	print result
	result.draw()

"""
Do you know what the most popular movie was in 2004?
Where can I watch avatar? Would you like to show theaters around you?
In what year was "Jumanji" released?
Do you know when "Titanic" came out?
Restart. I like Tom Hanks, but I don't like action movies. I want twenty two
has he won any awards?
Could you tell me about "Titanic"?
"""
