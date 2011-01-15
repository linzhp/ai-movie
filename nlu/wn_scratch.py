
from nltk.corpus import wordnet as wn


while 1 is 1:

	print ""
	choice = raw_input("Enter a word:  ")


	l = wn.synsets(choice)

	for x in l:
		strv = "%s" % (x)
		beg = strv.find( '\'' )
		end = strv.rfind( '\'' )
	
		word = strv[beg+1:end]
		print "\n\n*********", word, ": "
		

		print "   hypernyms(): ", wn.synset(word).hypernyms()
		print "   instance_hypernyms(): ", wn.synset(word).instance_hypernyms()
		print "   hyponyms(): ", wn.synset(word).hyponyms()
		print "   instance_hyponyms(): ", wn.synset(word).instance_hyponyms()
		print "   attributes(): ", wn.synset(word).attributes()
		print "   entailments(): ", wn.synset(word).entailments()
		print "   causes(): ", wn.synset(word).causes()
		print "   also_sees(): ", wn.synset(word).also_sees()
		print "   verb_groups(): ", wn.synset(word).verb_groups()
		print "   similar_tos(): ", wn.synset(word).similar_tos()
		print "   member_meronyms(): ", wn.synset(word).member_meronyms()
		print "   part_meronyms(): ", wn.synset(word).part_meronyms()
		print "   substance_meronyms(): ", wn.synset(word).substance_meronyms()
		print "   member_holonyms(): ", wn.synset(word).member_holonyms()
		print "   part_holonyms(): ", wn.synset(word).part_holonyms()
		print "   substance_holonyms(): ", wn.synset(word).substance_holonyms()
	
		raw_input("Press return to see the next entry")

