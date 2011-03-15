from os import path 
import logging
import sys
import re
import nltk
import pickle
from nltk.corpus import wordnet
import dm
import chunker
from utils import *

#TODO animated->animation
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
        with open(path.join(path.dirname(__file__), "chunkerpickler.bin"),'rb') as pickled_file:
            __import__("nlu.chunker")
            self.chk = pickle.load(pickled_file)
        self.chk = chunker.Chunker(False, True)
        self.stemmer = nltk.stem.PorterStemmer()
        self.keywords = []
        self.sure_role = False
    

    def process(self, input_string):
        dm.chatbot.submit(input_string)
        chunked = self.chk.chunk(input_string)
        logging.debug("Chunked Tree:"+str(chunked))
        result = []

        if self.expect:
            response = self._response(chunked)
            if response:
                result.append(response)
        category = None
        index = 0
        for x in chunked:
            if isinstance(x, nltk.Tree):
                if x.node == "B-QUESTION":
                    category = x.node
                    index = chunked.index(x)
                elif x.node == "COMMAND" and category != "B-QUESTION":
                    category = x.node                    
                    index = chunked.index(x)
                elif x.node == 'TRUE_FALSE':
                    category = x.node
            elif x[1]=="BYE":
                return [{"command":dm.EXIT}]
            elif x[1]=="RESTART":
                result.append({"command":dm.CLEAR})
                
        if category == "B-QUESTION":
            request = self._parse_question(chunked, index)
        elif category == "COMMAND":
            request = self._parse_command(chunked, index)
        elif category == 'TRUE_FALSE':
            request = self._parse_pref(chunked, request='COUNT',of='title')
        else:
            request=self._parse_pref(chunked)
        
        if request and len(request)>0:
                result.append(request)
                
                    
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
    
    def _parse_command(self, chunked, command_index):
        request = None
        next=chunked[command_index+1]
        if isinstance(next, nltk.Tree):
            next=next.leaves()[0]
        all_leaves=chunked.leaves()
        next_index = all_leaves.index(next)
        keywords=self._search_keywords(all_leaves[next_index:])
        if len(keywords)>0:
            request=self._parse_pref(chunked, request=self._keyword2request(keywords[0]))
        return request


    def _parse_question(self, chunked, question_index):
        question_tree = chunked[question_index]
        qtype = question_tree[0][0].lower()
        subtree = chunked[question_index:]
        if qtype=="who":
            keywords = self._search_keywords(question_tree)
            if len(keywords)>0:
                self.sure_role = True
                return self._parse_pref(subtree, request=self._keyword2request(keywords[0]))
            else:
                return self._parse_pref(subtree, request="person")
        elif qtype=="when":
            return self._parse_pref(subtree, request="year")
        elif qtype=="where":
            # FIXME Any other where question not about filming location? 
            return self._parse_pref(subtree, request="filming_loc")
        elif qtype=="how":
            # Handle "how about", "how many" and "how much"
            keywords = self._search_keywords(question_tree)
            for kw in keywords:
                if kw == 'KW_PLOT':
                    # How about ...
                    return self._parse_command(chunked, question_index)
                else:
                    return self._parse_pref(subtree, request=dm.COUNT, of=self._keyword2request(keywords[0]))
            if len(question_tree)>1 and question_tree[1][0]=='much':
                return self._parse_pref(subtree, request='gross')
        elif qtype=="what" or qtype=="which":
            # handle cases like which year, what genre, etc
            keywords = self._search_keywords(subtree)
            if len(keywords)>0:
                return self._parse_pref(subtree, request=self._keyword2request(keywords[0]))
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
            if isinstance(a, nltk.Tree):
                keywords.extend(self._search_keywords(a))
            elif a[1][0:2]=="KW":
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
        prev_op = None
        for sentence in subsentences:
            cur_pref = self._process_subsentence(sentence)
            positive = self._decide_opinion(sentence, prev_op)
            
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
            prev_op = positive
            
        for pref in pref_list:
            all_pref.concat(pref)
        
        if 'KW_SIMILAR' in self.keywords:
            all_pref['request']=dm.SIMILAR
        self._resolve_pronouns(all_pref)
        self._resolve_person(all_pref)
        self._clean_unary_values(all_pref, ['result_length','sort','order','request'])
        
        if all_pref.has_key('title') and all_pref.has_key('keyword'):
            all_pref.pop('keyword')

        if all_pref['request'] == dm.OPINION:
            if len(all_pref)==2 and all_pref.get('title')=='PREV_IT':
                all_pref={'like':'title'}
        if len(all_pref)==1 and all_pref.get('request') == dm.OPINION:
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
            if len(titles) == 0:
                pref.pop('title')
            
        if titles is not None and pref['request']=='title':
            pref.pop('title')

        titles=pref.get('!title')
        if isinstance(titles, list) and 'PREV_IT' in titles:
            titles.remove('PREV_IT')
            if len(titles) == 0:
                pref.pop('title')
                
        person = pref.get('person')
        if isinstance(person, list) and 'PREV_HE' in person:
            person.remove('PREV_HE')

        person = pref.get('!person')
        if isinstance(person, list) and 'PREV_HE' in person:
            person.remove('PREV_HE')
            
    def _resolve_person(self, pref):
        """
        Try to resolve person's role locally from the current
        user utterance.
        If the role related keywords (KW_DIRECTOR, KW_STAR) is found,
        there are two cases:
        1. if pref['request']=='person', set it to the role and continue
           searching other keywords
        2. if the keyword appears in the B-QUESTION, i.e. self.sure_role==True
           then continue to search for other keywords
        3. if the keyword does not appear in the B-QUESTION, and the 
           pref['request'] is that same with current keyword, get current role
           and set pref['request'] to next keyword
        """
        #TODO if request is actor, then the other person in the question is 
        #character.
        # Who played Marty in "Back to the Future"?                
        role = None
        for keyword in self.keywords:
            if keyword=='KW_DIRECTOR' or keyword == 'KW_STAR':
                cur_role = self._keyword2request(keyword)
                if pref['request']=='person':
                    pref['request']=cur_role
                    continue
                elif pref['request']==cur_role:
                    if not self.sure_role:
                        role=cur_role
                        pref['request']=None
                        continue
                else:
                    role=cur_role
                    break
            if pref['request'] is None:
                pref['request'] = self._keyword2request(keyword)
                break

        if pref['request'] is None:
            pref['request'] = 'title'
            
        if not role and pref['request']=='actor':
            role = 'character'
        if role:
            if pref.has_key('person'):
                name=pref.pop('person')
                pref[role]=name
            elif pref.has_key('!person'):
                name=pref.pop('!person')
                pref["!"+role]=name
            
                
                
     
    def _process_subsentence(self, list):
        self.cur_pref=ListDict()
        first_type = True
        for item in list:
            if isinstance(item, nltk.Tree):
                phrase = self._extract_words(item)
                if item.node == 'TITLE':
                    self.cur_pref.add('title', phrase)
                elif item.node == 'PERSON':
                    self.cur_pref.add('person',phrase)
                elif item.node == 'NP':
                    self.cur_pref.add('keyword',phrase)
                elif item.node == 'B-QUESTION':
                    if first_type:
                        first_type=False
                    else:
                        break
                    for i in item:
                        self._process_word(i)
                elif item.node == 'COMMAND':
                    if first_type:
                        first_type=False
                    else:
                        break
            else:
                self._process_word(item)
                
        if not self.cur_pref.has_key('order') and self.cur_pref.has_key('sort'):
            self.cur_pref.pop('sort')
        return self.cur_pref
    
    def _process_word(self, item):
        cur_word = item[0].lower()
        if cur_word == "he" or cur_word=="she" \
          or cur_word=="his" or cur_word=="her":
            self.cur_pref.add('person','PREV_HE')
        elif (cur_word == "it" or cur_word=="this" \
          or cur_word=="they" or cur_word=="them" \
          or cur_word=="ones"): #TODO "that"
            self.cur_pref.add('title','PREV_IT')
        elif item[1] == 'GNRE':
            self.cur_pref.add('genre',cur_word)
        elif item[1] == 'CD':
            number = english2int(cur_word)
            if number:
                if len(cur_word)==4:
                    self.cur_pref.add('year', number)
                else:
                    self.cur_pref['result_length']=number
        elif item[1] == 'COUNTRY':
            self.cur_pref.add('country', cur_word)
        elif item[1] == 'LANGUAGE':
            self.cur_pref.add('language', cur_word)
        elif cur_word == 'first':
            self.cur_pref['sort']='year'
            self.cur_pref['order'] = 'asc'
            self.cur_pref['result_length']=1
        elif cur_word == 'last' or cur_word == 'latest':
            self.cur_pref['sort']='year'
            self.cur_pref['order'] = 'desc' 
            self.cur_pref['result_length']=1
        elif cur_word == 'worst':
            self.cur_pref['sort']='rating'
            self.cur_pref['order'] = 'asc'
            self.cur_pref['result_length']=1                                              
        elif item[1] == 'JJS' or item[1]=='RBS':
            self.cur_pref['result_length']=1
            # Default to rating
            if not self.cur_pref.has_key('sort'):
                self.cur_pref['sort']='rating'
            if cur_word == 'highest' or cur_word == 'most' \
                or cur_word == 'best':
                self.cur_pref['order'] = 'desc'
            else:
                self.cur_pref['order'] = 'asc'
        elif item[1][0:3] == 'KW_':
            self.keywords.append(item[1])
        else:
            word=self.stemmer.stem(cur_word)
            if word == 'gross' or word=='earn':
                self.cur_pref['sort']='gross'
            elif word == 'recent':
                self.cur_pref['sort']='year'
        
        
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
        temp1 = []
        temp2 = []
        counter = 0
        for tuples in chunked:
            if isinstance(tuples, tuple) and tuples[1] == 'CC':
                temp1 = chunked[0:counter]
                temp2 = chunked[counter:]
                return [temp1, temp2]
            counter = counter + 1
        return [chunked]

    def _decide_opinion(self, list, prev):
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
        verb = prev
        
        for node in list:
            if isinstance(node, tuple):
                if node[1]=='RB':
                    if node[0] == "n't" or node[0] == "not":
                        modifier = not modifier
                        print modifier
                if node[1]=='IN':
                    if node[0] == "without":
                        modifier = not modifier
                        print modifier
                if node[1][0]=='V':
                    if node[0] in positiveList:
                        verb = True
                    if node[0] in negativeList:
                        verb = False
#                    if node[0] in toBeList:
#                        if node[0] in positiveAdjectiveList:
#                            verb = True
#                        if node[0] in negativeAdjectiveList:
#                            verb = False 
#                   
#
        #list should be a list of tuples
        if verb == None or modifier == True:
            return verb
        else:
            return not verb

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

positiveList = ["like","love"]
negativeList = ["hate","dislike"]
if __name__ == "__main__":
    nlu = NLUnderstanding()
    chuncked = nlu.process("I like Tom Hanks but don't like action movies!")
    nlu._partition(chuncked)
