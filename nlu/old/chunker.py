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

class Chunker:

	def __init__(self):

		# Define regular expressions for punctuation tags
		tagged_punc = [ (r'\"', ':'), (r'\?', 'QM') ]

		# Load the tagged training sentences.
		f = open( './training_sentences', 'r' )
		train_sents = pickle.load(f)
	
		# Define the tagger.
		_POS_TAGGER = 'taggers/maxent_treebank_pos_tagger/english.pickle'
		t1 = nltk.data.load(_POS_TAGGER)
		t2 = nltk.BigramTagger( train_sents, backoff=t1 )
		self.tagger = nltk.RegexpTagger( tagged_punc, backoff=t2 )

		# Define a chunking grammar.
		chunk_grammar = r"""

		   NP:   {<DT|PRP\$>?<JJ>*<NN|NNS>(<POS>?<JJ>*<NN|NNS>)?}
		   B-QUESTION: {^<[W].*|VBD|VBN|VBP|VBZ>}
	   	COMMAND: {^<VB.*>}
			VP: { <MD>?<[V].*>+<IN|CC>?<NP|PP>* }
			TITLE: {<:><.*>*<:>}	
		   PERSON: {<NNP[S]?>+}

		"""

		# Define a regular expression chunker
		self.cp = nltk.RegexpParser(chunk_grammar)


	# Takes a string and returns a chunk tree.
	def chunk(self, sentence):

		tokd = nltk.word_tokenize(sentence)
		tagged = self.tagger.tag(tokd)
		chunked = self.cp.parse(tagged)

		#print "\n\nChunked - tree\n"
		#print chunked

		return chunked
