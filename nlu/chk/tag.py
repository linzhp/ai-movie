import nltk

f = open('../sample_input/sample_input_data', 'r')
input_text = f.read()

tokd = nltk.word_tokenize(input_text)

tagged_punc = [ (r'foobar', 'FOO') ,
	(r'\"', ':'),
	(r'\?', 'QM') ]

_POS_TAGGER = 'taggers/maxent_treebank_pos_tagger/english.pickle'

t1 = nltk.data.load(_POS_TAGGER)
tagger = nltk.RegexpTagger(tagged_punc, backoff=t1)

tagged = tagger.tag(tokd)


with open('./tagged', 'w') as outfile:

	for x in tagged:
		pair = "%s/%s " % (x[0], x[1])	
		outfile.write(pair)
		if ( x[1] == '.' ) | ( x[1] == 'QM' ):
			outfile.write('\n')
	
outfile.closed

 


