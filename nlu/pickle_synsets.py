from nltk.corpus import wordnet as wn
import pickle

with open('./classifiers', 'w') as outfile:

	SS_list = [ ( "like", wn.synsets('like') ) ]
	SS_list.append(("dislike", wn.synsets('dislike') ))
	SS_list.append(("good", wn.synsets('good') ))
	SS_list.append(("bad", wn.synsets('bad') ))
	SS_list.append(("stupid", wn.synsets('stupid') ))
	SS_list.append(("hack", wn.synsets('hack') ))
	SS_list.append(("suck", wn.synsets('sucked') ))
	SS_list.append(("see", wn.synsets('see') ))
	SS_list.append(("think", wn.synsets('think') ))
	SS_list.append(("funny", wn.synsets('funny') ))
	SS_list.append(("beautiful", wn.synsets('beautiful') ))
	SS_list.append(("intellectual", wn.synsets('intellectual') ))

	pickle.dump(SS_list, outfile)
	outfile.closed
