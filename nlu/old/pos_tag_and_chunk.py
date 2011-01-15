import nltk

#f = open('../sample_input/sample1', 'r')
input_text = "give me a list."

tokd = nltk.word_tokenize(input_text)

print "nltk.tag.pos_tag() \n"
tagged = nltk.tag.pos_tag(tokd)


for x in tagged:
	print x[1], ": ", x[0] 

print "\n\nChunking...\n"


chunk_grammar = r"""

   NP:   {<DT|PRP\$>?<JJ>*<NN|NNS>(<POS>?<JJ>*<NN|NNS>)?}
   PERSON: {<NNP>+}
   PERSONAL_HISTORY: {<PRP>(<VBD>|(<VBP><RB>?<VBN>))}
   PERSONAL_DIRECTIVE: {<PRP>((<VBP>(<RB|RBR|RBS>*<VBG>)?)|<MD><VB>)}
   TITLE: {<:><.*>*<:>}
   QUESTION: {<WP><[V].*>}
"""
   #UVP:  {<PRP><VBP><VBG>}


cp = nltk.RegexpParser(chunk_grammar)

print cp.parse(tagged)
