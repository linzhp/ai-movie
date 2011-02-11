
import nltk
from nltk.corpus import wordnet as wn
import chunker

class NLU:

	def __init__(self, verbose=False):
		self.vb = verbose
		if self.vb:
			print "NLU: Instantiating chunker"
		self.chk = chunker.Chunker(verbose)
		
		if self.vb:
			print "NLU: Generating classifier synsets"
		self.SS_list = [ ( "like", wn.synsets('like') ) ]
		self.SS_list.append(("dislike", wn.synsets('dislike') ))
		self.SS_list.append(("good", wn.synsets('good') ))
		self.SS_list.append(("bad", wn.synsets('bad') ))
		self.SS_list.append(("stupid", wn.synsets('stupid') ))
		self.SS_list.append(("hack", wn.synsets('hack') ))
		self.SS_list.append(("suck", wn.synsets('sucked') ))
		self.SS_list.append(("see", wn.synsets('see') ))
		self.SS_list.append(("think", wn.synsets('think') ))
		self.SS_list.append(("funny", wn.synsets('funny') ))
		self.SS_list.append(("beautiful", wn.synsets('beautiful') ))
		self.SS_list.append(("intellectual", wn.synsets('intellectual') ))

		
	## Classify word into one of the categories in SS_list
	def _classify_word(self, cword):
		word_s = wn.synsets(cword)
		score = 0
		match = 'NONE'
		for x in self.SS_list:
			tmp = self._synset_similarity(x[1], word_s)
			if tmp > score:
				score = tmp
				match = x[0]
			if score == 1:
				return (match, score)
		return (match, score)
		 
	## Takes a flat chunk subtree (one with only tuples -- no subtrees) 
	##	and returns its untagged string representation.
	def _untag_subtree(self, subtree):
		first_quotes = False
		string_rep = ""
		for x in subtree:
			if (x[1] != ":") : 
				string_rep += x[0]
				string_rep += " "
			elif first_quotes == False:
				first_quotes = True
			else:				
				return string_rep.rstrip()
		return string_rep.rstrip()

	##	Question parser: Takes a chunk tree and returns a tuple of strings to pass
	## to a dialog manager.
	def _parse_question(self, chktree):
		
		
		if chktree[0][0][1] == 'MD':
			parameter_list = self._parse_as_what(chktree)
			parameter_list.insert(0, 'trivia')
	
		qtype = chktree[0][0][0].lower()			
		if qtype == "who":
			parameter_list = self._parse_as_who(chktree) 	
			parameter_list.insert(0, 'trivia')
		elif qtype == "what":
			parameter_list = self._parse_as_what(chktree) 	
			parameter_list.insert(0, 'trivia')
		elif qtype == "when":
			parameter_list = self._parse_as_when(chktree) 	
			parameter_list.insert(0, 'trivia')
		elif qtype == "why":
			parameter_list = self._parse_as_why(chktree) 
			parameter_list.insert(0, 'trivia')
		else:
			parameter_list = self._parse_as_TF(chktree) 
			parameter_list.insert(0, 'True_False')

		return parameter_list

	## 'Who' question parser
	def _parse_as_who(self, chktree):
		object_found = False
		negation = False
		parameter_list = ["person"]
		looking_for = 'person'
		for x in chktree:
			if ( "tuple" in str(type(x)) ):
				negation = self._negator(x[0], negation)
				if x[1] == "KW_DIRECTOR":
					if object_found == False:
						parameter_list[0] = "director"
						object_found = True
					else:
						looking_for = "director"
				elif x[1] == "KW_STAR":
					if object_found == False:
						parameter_list[0] = "actor"
						object_found = True
					else:
						looking_for = "actor"
			else:
				if x.node == "TITLE":
					if negation:
						parameter_list.append('!title')
					else:
						parameter_list.append('title')
					parameter_list.append(self._untag_subtree(x))
				elif x.node == "PERSON":
					if negation:
						subject = "!"
					else:
						subject = ""
					subject += looking_for                  
					parameter_list.append(subject)
					parameter_list.append(self._untag_subtree(x))
		return parameter_list

	## 'What' (a piece of garbage) question parser
	def _parse_as_what(self, chktree):
		looking_for = 'other'
		object_found = False
		negation = False
		parameter_list = ["other"]
		flat = chktree.leaves()
		if flat[ len(flat) - 1 ][1] == ":":
			last = flat[ len(flat) - 2 ]
		else:
			last = flat[ len(flat) - 1 ]
		if last[1] == "KW_PLOT":
			parameter_list[0] = 'plot'
			object_found = True
		for i,x in enumerate(chktree):
			if ( "tuple" in str(type(x)) ):
				if object_found == False:
					if x[1] == "KW_YEAR":
						return self._parse_as_when(chktree)
					elif ( x[1] == "KW_DIRECTOR" ) | ( x[1] == "KW_STAR" ):
						return self._parse_as_who(chktree)
					elif x[1] == "KW_GENRE":
						parameter_list[0] = 'genre'
						object_found = 'True'
					elif x[1] == "KW_MOVIE":
						parameter_list[0] = 'title'
						object_found = 'True'		
					elif x[1] == "KW_PLOT":
						parameter_list[0] = 'plot'
						object_found = 'True'
					elif x[1] == "GNRE":
						parameter_list[0] = 'title'
						object_found = 'True'	
						parameter_list.append('genre')
						parameter_list.append(x[0].title())
				else:
					negation = self._negator(x[0], negation)
					if x[1] == "KW_DIRECTOR":
						looking_for = "director"
					elif x[1] == "KW_STAR":
						looking_for = "actor"
					elif x[1] == "KW_PLOT":
						looking_for = "plot"
					elif x[1] == "GNRE":
						if negation:
							parameter_list.append('!genre')
						else:
							parameter_list.append('genre')
						parameter_list.append(x[0].title())
						
			else:
				if x.node == "TITLE":
					if negation:
						parameter_list.append('!title')
					else:
						parameter_list.append('title')
					parameter_list.append(self._untag_subtree(x))
				elif x.node == "PERSON":               
					if negation:
						subject = "!"
					else:
						subject = ""
					if looking_for == 'other':
						looking_for = 'person'
					subject += looking_for                  
					parameter_list.append(subject)
					parameter_list.append(self._untag_subtree(x))
		if len(parameter_list) % 2 == 0:
			parameter_list.append('that')
		return parameter_list
					

	## 'When' question parser
	def _parse_as_when(self, chktree):
		parameter_list = ["year"]
		found_subject = False
		for x in chktree:
			if "Tree" in str(type(x)) :
				if x.node == "TITLE":
					found_subject = True
					parameter_list.append('title')
					parameter_list.append(self._untag_subtree(x)) 
				elif x.node == "PERSON":
					found_subject = True
					parameter_list.append('person')
					parameter_list.append(self._untag_subtree(x)) 

		if found_subject == False:
			parameter_list.append('other')
			parameter_list.append('that')

		return parameter_list

	## True/False question parser
	def _parse_as_TF(self, chktree):
		looking_for = "person"
		negation = False
		parameter_list = []
		for x in chktree:
			if "tuple" in str(type(x)):
				negation = self._negator(x[0], negation)
				if x[1] == "CD":
					parameter_list.append('year')
					parameter_list.append(x[0])
				elif ( x[1] == "KW_DIRECTOR" ):
					looking_for = 'director'
				elif ( x[1] == "KW_STAR" ):
					looking_for = 'actor'
				
				elif x[1] == "KW_PLOT":
					looking_for = "plot"
					
				elif x[1] == "GNRE":
					if negation:
						parameter_list.append('!genre')
					else:
						parameter_list.append('genre')
					parameter_list.append(x[0].title())
			else:
				if x.node == "TITLE":
					parameter_list.append('title')
					parameter_list.append(self._untag_subtree(x))
				elif x.node == "PERSON":
					if looking_for == "actor":
						if negation:
							parameter_list.append('!actor')
						else:
							parameter_list.append('actor')
					elif looking_for == "director":
						if negation:
							parameter_list.append('!director')
						else:
							parameter_list.append('director')
					else:
						if negation:
							parameter_list.append('!person')
						else:
							parameter_list.append('person')

					parameter_list.append(self._untag_subtree(x))
		return parameter_list

			
	## Takes a word and current negation state.
	def _negator(self, word, neg):
		if word == 'n\'t':
			return neg ^ 1
		elif word == 'not':
			return neg ^ 1
		elif word == 'without':
			return neg ^ 1
		elif word == 'but':
			return False
		elif word == 'however':
			return False
		elif word == 'although':
			return False
		else:
			return neg

	## Find the next PERSON or TITLE given a subtree
	def _get_next_subj(self, chktree, index):
		i = index + 1
		print "Checking", chktree[i]
		if ( "Tree" in str(type(chktree[i])) ):
			print "x is a tree"
			if ( chktree[i].node == "TITLE" ) | ( chktree[i].node == "PERSON" ):
				print "Found title or person", chktree[i].node, " :: ", chktree[i]
				return self._untag_subtree(chktree[i])
		i += 1
				

	##	Public function takes user input as a string and returns a list of
	##	tuples of strings where each tuple starts with a dialog classifier
	##	type followed by a number of arguments.
	def process(self, input_string):
		list = False
		if 'list' in input_string:
			list = True
		if 'start over' in input_string.lower():
			return ['restart']

		chunked = self.chk.chunk(input_string)
	
		if self.vb:
			print chunked

		for x in chunked:
			if ( "Tree" in str(type(x)) ):
				if x.node == "B-QUESTION":
					return self._parse_question(chunked)
				elif x.node == "COMMAND":
					parameter_list = self._parse_as_what(chunked)
					parameter_list.insert(0, 'trivia')
					return parameter_list
			else:
				if x[1] == 'YES':
					return ['yes']
				elif x[1] == 'NO':
					return ['no']
				elif x[1] == 'HI':
					return ['hi']
				elif x[1] == 'BYE':
					return ['bye']
				elif x[1] == 'RESET':
					return ['reset']			
				else:
					return self._parse_PRP(chunked)

	## Parse sentences starting with a personal pronoun (hopefully the sentence
	## is something like "I like action movies" or "I thought that movie was bad" ).
	def _parse_PRP(self, chktree):
		parameter_list = []
		looking_for = "other"
		negation = False
		collect_subjects = False
		collect_adjectives = True
		have_subject_waiting_for_opinion = False
		waiting_type = 'other'
		waiting_subject = "that"
		#if chktree[0][0].lower() == 'i':
		if True:
			for x in chktree:
				if 'Tree' in str(type(x)):
					if x.node == "VP" and collect_subjects == False and have_subject_waiting_for_opinion == False:
						for y in x:
							if 'tuple' in str(type(y)):
								verb = self._classify_word(y[0])
								if self.vb:
									print verb
								if verb[0] == 'like':
									if negation:
										parameter_list.append('dislike')
										negation = False
									else:
										parameter_list.append('like')
									collect_subjects = True
								elif verb[0] == 'dislike':
									if negation:
										parameter_list.append('like')
										negation = False
									else:
										parameter_list.append('dislike')
									collect_subjects = True
								elif verb[0] == 'see' and verb[1] > .25:
									if (y[1] != 'VBD' and y[1] != 'VBN'):
										if negation:
											parameter_list.append('dislike')
											negation = False
										else:
											parameter_list.append('like')								
									else:
										if negation == False:
											parameter_list.append('saw_it')
									collect_subjects = True
								elif verb[0] == 'think':
									#collect_subjects = True
									collect_adjectives = True
					elif x.node == "NP":						
						if collect_subjects:
							if negation:
								parameter_list.append('!other')
							else:
								parameter_list.append('other')
							parameter_list.append(self._untag_subtree(x))
						else:
							have_subject_waiting_for_opinion = True
							waiting_subject = self._untag_subtree(x)
					elif x.node == "TITLE":
						if collect_subjects:
							if negation:
								parameter_list.append('!title')
							else:
								parameter_list.append('title')
							parameter_list.append(self._untag_subtree(x))
						else:
							have_subject_waiting_for_opinion = True
							waiting_type = 'title'			
							waiting_subject = self._untag_subtree(x)
					elif x.node == "PERSON":
						if collect_subjects:
							if looking_for == "actor":
								if negation:
									parameter_list.append('!actor')
								else:
									parameter_list.append('actor')
							elif looking_for == "director":
								if negation:
									parameter_list.append('!director')
								else:
									parameter_list.append('director')
							else:
								if negation:
									parameter_list.append('!person')
								else:
									parameter_list.append('person')
							parameter_list.append(self._untag_subtree(x))
						else:
							have_subject_waiting_for_opinion = True			
							waiting_type = looking_for
							waiting_subject = self._untag_subtree(x)	
						 
				else:
					negation = self._negator(x[0], negation) 
					if x[1] == 'KW_DIRECTOR':
						looking_for = 'director'
					elif x[1] == 'KW_STAR':
						looking_for = 'actor'
					elif x[1] == 'KW_GENRE':
						looking_for = 'genre'
					elif x[1] == 'KW_PLOT':
						looking_for = 'plot'
					elif x[1] == 'GNRE':
						parameter_list.append('genre')
						parameter_list.append(x[0])			
					elif x[0].lower() == 'you':
						have_subject_waiting_for_opinion = True			
						waiting_type = 'movie_selector'
						waiting_subject = 'movie_selector'	
						if collect_subjects:
							parameter_list.append(waiting_type)
							parameter_list.append(waiting_subject)

					elif collect_adjectives or have_subject_waiting_for_opinion:
						adj = self._classify_adjective(x[0])
						if adj == 'good':
							parameter_list.append('like')
							parameter_list.append(waiting_type)
							parameter_list.append(waiting_subject)
						elif adj == 'bad':
							parameter_list.append('dislike')
							parameter_list.append(waiting_type)
							parameter_list.append(waiting_subject)	
			
	
		return parameter_list

	## Classify an adjective as 'good' or 'bad' or 'unknown'
	def _classify_adjective(self, word):
		adj = self._classify_word(word)
		if adj[1] > .25:
			if adj[0] in ['like','good','intellectual','funny','beautiful']:
				return 'good'
			elif adj[0] in ['dislike','bad','stupid','hack','suck']:
				return 'bad'
			else:
				return 'unknown'

	##	Takes two synsets as arguments and returns a similarity score from 0 to 1.
	def _synset_similarity(self, set1, set2):
		similar_tos = False	
		similarity = 0

		# Iterate over both synsets
		for x in set1:			
			for y in set2:
	
				# If two entries have the same part of speech calculate their path
				# similarity and keep track of the max so far.
				if x.pos == y.pos:
					tmp_sim = x.path_similarity(y)
					if tmp_sim > similarity:
						similarity = tmp_sim

				# Regardless of POS check both entries against their similar_tos()
				# entries. This is particularly helpful for adjectives.
				for z in x.similar_tos():
					for w in y.similar_tos():
						if (y == z) | (w == x):
							similar_tos = True
				
		# Give similar_tos a score
		if (similar_tos) & (similarity < .2):
			similarity = .35

		return similarity


