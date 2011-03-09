from os import path 
import sys
import re
import nltk
from nltk.corpus import wordnet
import dm
import chunker
from dict import ListDict

#TODO Who directed it?
#TODO User: reset. I like Tom Hanks, but I don't like action movies
#nlu_out: [{'genre': 'action', 'person': ['reset.', 'Tom Hanks'], 'request': 'OPINION'}]

class NLUnderstanding:
    """
    Natural Language Understanding class.
    Accepts: user input string
    Output: A list of dictionaries. Each dictionary contains one of the four
        keys: request, command, response and off_topic, corresponding to four
        categories of user input.
        request: handle the user requests concerning movies. The value of request
            can be "title", "year", "plot", "director", "actor", "genre", 
            "country", "filming_loc", "language", "award", "gross", "cast", 
            OPINION, COUNT. True or false
            questions are handled are COUNT. This dictionary also contains 
            conditions of the request.
        command: handle the users requests to change the system state. Possible 
            values are EXIT and CLEAR. This should not be confused with the
            part-of-speech tagged as COMMAND
        response: handle the users response to the question asked previously by
            the system. Possible values are YES, NO, a number and other answers 
            to specific questions
        off_topic: handle off topic user utterances. The value is the full text 
            of user utterance
    """
    def __init__(self):
        self.expect = None    
        self.chk = chunker.Chunker(False)
        self.stemmer = nltk.stem.PorterStemmer()
        self.keywords = []
    

    def process(self, input_string):
        dm.chatbot.submit(input_string)
        chunked = self.chk.chunk(input_string)
        
        result = []
            
        if self.expect:
            response = self._response(chunked)
            if response:
                result.append(response) 
        find_category = False
        for x in chunked:
            if isinstance(x, nltk.Tree):
                index = chunked.index(x)
                if x.node == "B-QUESTION":
                    request = self._parse_question(chunked,index)
                    if request:
                        result.append(request)
                    find_category = True
                elif x.node == "COMMAND":
                    next=chunked[index+1]
                    if isinstance(next, nltk.Tree):
                        next=next.leaves()[0]
                    all_leaves=chunked.leaves()
                    next_index = all_leaves.index(next)
                    keywords=self._search_keywords(all_leaves[next_index:])
                    if len(keywords)>0:
                        request=self._parse_pref(chunked[index:], request=self._keyword2request(keywords[0]))
                        if request:
                            result.append(request)
                        find_category = True
            elif x[1]=="BYE":
                return [{"command":dm.EXIT}]
            elif x[1]=="RESTART":
                result.append({"command":dm.CLEAR})

        if not find_category:
            preference=self._parse_pref(chunked)
            if preference and len(preference)>0:
                result.append(preference)
                
                    
        if len(result)==0:
            result.append(self._off_topic(input_string))
            
        return result
            
    def _response(self, chuncked):
        """
        This method is called when user is supposed to answer a question
        Precondition: self.expect is not None    
        """
        if self.expect == "result_length":
            for node in chuncked:
                if isinstance(node, tuple) and (node[1]=='CD' or node[1]=='LS'):
                    chuncked.remove(node)
                    return {'response':int(node[0])}
        elif self.expect == dm.SEE_RESULT or self.expect == dm.MORE_PREF:
            for node in chuncked.leaves():
                if isinstance(node, tuple) and (node[1]=='YES' or node[1]=='NO'):
                    chuncked.remove(node)
                    return {'response':node[1]}
        return None

    def _parse_question(self, chunked, question_index):
        question_tree = chunked[question_index]
        qtype = question_tree[0][0].lower()
        keywords = self._search_keywords(question_tree.leaves())
        if qtype=="who":
            return self._parse_pref(chunked[question_index:], request="person")
        elif qtype=="when":
            return self._parse_pref(chunked[question_index:], request="year")
        elif qtype=="where":
            # FIXME Any other where question not about filming location? 
            return self._parse_pref(chunked[question_index:], request="filming_loc")
        elif qtype=="how":
            # Handle "how many" and "how much"
            if len(keywords)>0:
                return self._parse_pref(chunked[question_index:], request=dm.COUNT, of=self._keyword2request(keywords[0]))
            elif len(question_tree)>1 and question_tree[1][0]=='much':
                return self._parse_pref(chunked[question_index:], request='gross')
        elif qtype=="what" or qtype=="which":
            # handle cases like which year, what genre, etc
            if len(keywords)>0:
                return self._parse_pref(chunked[question_index:], request=self._keyword2request(keywords[0]))
        # Haven't returned, return as preference
        return self._parse_pref(chunked[question_index:])
    
    def _off_topic(self, input_string):
        return {'off_topic':input_string}
    
    def _search_keywords(self, list):
        """  
        Possible keywords are: KW_YEAR, KW_MOVIE, KW_MOVIES
        KW_DIRECTOR, KW_STAR, KW_PLOT, KW_GENRE, KW_COUNTRY,
        KW_LANGUAGE, KW_SIMILAR, KW_CAST, KW_AWARD
        """
        keywords=[]
        for a in list:
            if a[1][0:2]=="KW":
                keywords.append(a[1])
        return keywords
    
    def _keyword2request(self, keyword):
        if keyword=="KW_MOVIE" or keyword=="KW_MOVIES":
            return "title"
        elif keyword == "KW_STAR":
            return "actor"
        else:
            return keyword[3:].lower()
    
    def _parse_pref(self, chunked, **kargs):
        all_pref=ListDict(request=dm.OPINION)
        all_pref.update(kargs)
        
        
        subsentences=self._partition(chunked)
        pref_list=[]
        
        for sentence in subsentences:
            #TODO break in second type            
            cur_pref = self._process_subsentence(sentence)
            positive = self._decide_opinion(sentence)
            
            if not positive:
                cur_pref.negativate = negativate
                if positive is False:
                    cur_pref=cur_pref.negativate(cur_pref)
                #if positive is None, the negativate method is kept
            elif len(pref_list)>0:
                prev_pref = pref_list.pop()
                if 'negativate' in dir(prev_pref):
                    # The previous preference is unknown
                    pref_list.append(prev_pref.negativate(prev_pref))
                else:
                    pref_list.append(prev_pref)
            pref_list.append(cur_pref)
            
        for pref in pref_list:
            all_pref.concat(pref)
        
        self._resolve_pronouns(all_pref)
        self._resolve_people(all_pref)
        self._clean_unary_values(all_pref, ['result_length','sort','order','request'])

        if all_pref['request'] == dm.OPINION:
            if len(all_pref)==2 and all_pref.get('title')=='PREV_IT':
                all_pref={'like':'title'}
        if len(all_pref)==1:
            all_pref={}
        
        return all_pref
    
    def _clean_unary_values(self, dic, keys):
        for item in keys:
            if isinstance(dic.get(item), list):
                dict[item]=dict[item][-1]
                
            
    def _resolve_pronouns(self, pref):
        titles=pref.get('title')
        if isinstance(titles, list) and 'PREV_IT' in titles:
            titles.remove('PREV_IT')

        titles=pref.get('!title')
        if isinstance(titles, list) and 'PREV_IT' in titles:
            titles.remove('PREV_IT')
            
        people = pref.get('people')
        if isinstance(people, list) and 'PREV_HE' in people:
            people.remove('PREV_HE')

        people = pref.get('!people')
        if isinstance(people, list) and 'PREV_HE' in people:
            people.remove('PREV_HE')
            
    def _resolve_people(self, pref):
        if pref.has_key('people'):
            if 'KW_DIRECTOR' in self.keywords and pref['request'] != 'director':
                name=pref.pop('people')
                pref['director']=name
            elif 'KW_STAR' in self.keywords and pref['request']!='actor':
                name=pref.pop('people')
                pref['actor']=name
        elif pref.has_key('!people'):
            if 'KW_DIRECTOR' in self.keywords and pref['request'] != 'director':
                name=pref.pop('!people')
                pref['!director']=name
            elif 'KW_STAR' in self.keywords and pref['request']!='actor':
                name=pref.pop('!people')
                pref['!actor']=name
                
     
    def _process_subsentence(self, list):
        cur_pref=ListDict()
        first_type = True
        for item in list:
            if isinstance(item, nltk.Tree):
                phrase = self._extract_words(item)
                if item.node == 'TITLE':
                    cur_pref.add('title', phrase)
                elif item.node == 'PERSON':
                    cur_pref.add('person',phrase)
                elif item.node == 'NP':
                    cur_pref.add('keyword',phrase)
                elif item.node == 'B-QUESTION':
                    if first_type:
                        first_type=False
                    else:
                        break
                    for i in item:
                        cur_pref.concat(self._process_word(i))
                elif item.node == 'COMMAND':
                    if first_type:
                        first_type=False
                    else:
                        break
            else:
                cur_pref.concat(self._process_word(item))
        return cur_pref
    
    def _process_word(self, item):
        cur_pref = ListDict()
        if item[0] == "he" or item[0]=="she" \
          or item[0]=="his" or item[0]=="her":
            cur_pref.add('person','PREV_HE')
        elif (item[0] == "it" or item[0]=="this" \
          or item[0]=="they" or item[0]=="them"): #TODO "that"
            cur_pref.add('title','PREV_IT')
        elif item[1] == 'GNRE':
            cur_pref.add('genre',item[0])
        elif item[1] == 'CD':#TODO "a", "one"
            if len(item[0])==4:
                cur_pref.add('year', int(item[0]))
            else:
                cur_pref['result_length']=int(item[0])
        elif item[1] == 'COUNTRY':
            cur_pref.add('country', item[0])
        elif item[1] == 'LANGUAGE':
            cur_pref.add('language', item[0])
        elif item[0] == 'first':
            cur_pref['sort']='year'
            cur_pref['order'] = 'asc'
            cur_pref['result_length']=1
        elif item[0] == 'last' or item[0] == 'latest':
            cur_pref['sort']='year'
            cur_pref['order'] = 'desc' 
            cur_pref['result_length']=1
        elif item[0] == 'worst':
            cur_pref['sort']='rating'
            cur_pref['order'] = 'asc'
            cur_pref['result_length']=1                                              
        elif item[0] == 'best':
            cur_pref['sort']='rating'
            cur_pref['order'] = 'desc'
            cur_pref['result_length']=1                                              
        elif item[1] == 'JJS':
            cur_pref['result_length']=1
            # Default to rating
            cur_pref['sort']='rating'
            if item[0] == 'highest' or item[0] == 'most':
                cur_pref['order'] = 'desc'
            else:
                cur_pref['order'] = 'asc'
        elif item[1][0:3] == 'KW_':
            self.keywords.append(item[1])
        else:
            word=self.stemmer.stem(item[0])
            if cur_pref.has_key('order') and cur_pref.has_key('result_length'):
                if word == 'gross' or word=='earn':
                    cur_pref['sort']='gross'
                elif word == 'recent':
                    cur_pref['sort']='year'
        return cur_pref
        
        
    def _partition(self, chunked):
        """
        Partition a chunked sentence (tree) into several segments, 
        with each segment only have either positive opinion
        or negative opinion about one or more movie attributes,
        but not a mix
        Accepts: a chunked tree, example can be found at the
        bottom of chunker.py
        Returns: a list of lists, consists of children of chunked
        tree
        """
        return [chunked]
        
    def _decide_opinion(self, list):
        """
        Decide the user opinion in the current segment of sentence,
        represented by a list of tuples.
        Example input can be found by printing chunked.leaves(), with
        chunked being the return value of Chunker.chunk
        return: True if it is positive, False if it is negative, None
        if it is unknown
        """
        print list
        modifier = True
        verb = None
        #list should be a list of tuples
        for n in list:
            if isinstance(n, nltk.tree.Tree):
                if n.pos()[0][1][0] == 'V':
                    for item in n[0]:
                        print item
                        if item[0] == "like":
                            verb = True
            else:
                if n[1] == 'RB':
                    if n[0] == "n't":
                        modifier = not modifier
                    if n[0] == "n't":
                        modifier = not modifier
                    print n[0]
        if modifier:
            return verb
        else:
            if verb:
                return not verb
            else:
                return verb
        
    def _extract_words(self, tree):
        leaves = tree.leaves();
        words = [item[0] for item in leaves]
        if words[0]=='"':
            words.remove('"')
            words.remove('"')
        return " ".join(words)

def negativate(self):
    """
    For amending dictionaries only
    """ 
    new_dict = ListDict()    
    for key in self:
        new_dict['!'+key]=self[key]
    return new_dict
