import nltk

from nltk.corpus import treebank

tts = treebank.tagged_sents()

t0 = nltk.DefaultTagger('NN')
t1 = nltk.UnigramTagger(tts)
t2 = nltk.BigramTagger(tts, backoff=t1)


chunk_grammar = r"""

   TITLE: {<:><.*>*<:>}
   NP:   {<DT|PRP\$>?<JJ>*<NN|NNS>(<POS>?<JJ>*<NN|NNS>)?}
   PERSON: {<NNP>+}
   PERSONAL_HISTORY: {<PRP>(<VBD>|(<VBP><RB>?<VBN>))}
   PERSONAL_DIRECTIVE: {<PRP>((<VBP>(<RB|RBR|RBS>*<VBG>)?)|<MD><VB>)}
   B-QUESTION: {^<[W].*>}	
   COMMAND: {^<VB>}

"""
   #UVP:  {<PRP><VBP><VBG>}





cp = nltk.RegexpParser(chunk_grammar)

while 1 is 1:

	input_text = raw_input("\nEnter a sentence:  ")

	tokd = nltk.word_tokenize(input_text)

	print "\nTokenized:\n"

	for x in tokd:
		print x

	print "Treebank tagging \n"
	tagged = t2.tag(tokd)

	for x in tagged:
		print x[1], ": ", x[0] 



	print "\n\nChunked - tree\n"

	chunk = cp.parse(tagged)

	print chunk

