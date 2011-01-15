import nltk
import pickle

tagged_punc = [ (r'foobar', 'FOO') ,
	(r'\"', ':'),
	(r'\?', 'QM') ]

f = open( './training_sentences', 'r' )
train_sents = pickle.load(f)

for x in train_sents:
	print x

chunk_grammar = r"""

   NP:   {<DT|PRP\$>?<JJ>*<NN|NNS>(<POS>?<JJ>*<NN|NNS>)?}
   B-QUESTION: {^<[W].*|VBD|VBN|VBP|VBZ>}
   COMMAND: {^<VB.*>}
	VP: { <MD>?<[V].*>+<IN|CC>?<NP|PP>* }
	TITLE: {<:><.*>*<:>}	
   PERSON: {<NNP[S]?>+}

"""


_POS_TAGGER = 'taggers/maxent_treebank_pos_tagger/english.pickle'
t1 = nltk.data.load(_POS_TAGGER)
t2 = nltk.BigramTagger( train_sents, backoff=t1 )
tagger = nltk.RegexpTagger( tagged_punc, backoff=t2 )


cp = nltk.RegexpParser(chunk_grammar)

while 1 is 1:

	input_text = raw_input("\nEnter a sentence:  ")

	tokd = nltk.word_tokenize(input_text)

	print "\nTokens:\n"

	for x in tokd:
		print x

	#sents = sentencize(tokd)
	
	#for x in sents:
	#	print "SENTENCE: ", x

	print "Custom Tagging: \n"
	tagged = tagger.tag(tokd)
	for x in tagged:
		print x[1], ": ", x[0] 


	print "\n\nChunked - tree\n"
	chunk = cp.parse(tagged)

	print chunk

