# Gives a score from 0 - 1 of the similarity of two words using 
# wordnet.path_similarity()

import nltk
from nltk.corpus import wordnet as wn


while 1 is 1:
	raw_in = raw_input('Enter two words separated by a spaces >')

	words = nltk.word_tokenize(raw_in)

	first = wn.synsets(words[0])
	second = wn.synsets(words[1])
	similar_tos = False	

	similarity = 0
	for x in first:
		if x.pos == x.pos:
			for y in second:
				if x.pos == y.pos:
					tmp_sim = x.path_similarity(y)
					print tmp_sim
					if tmp_sim > similarity:
						similarity = tmp_sim
				for z in x.similar_tos():
					for w in y.similar_tos():
						if (y == z) | (w == x):
							similar_tos = True
						

	print "Maximum similarity found:", similarity
	print "similar_tos():", similar_tos
#	print "Maximum lch_similarity found:", lchsim




