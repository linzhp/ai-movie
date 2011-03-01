from os import path 
import sys
import re
import nltk
from nltk.corpus import wordnet
import dm
import chunker
#TODO return cast
class NLUnderstanding:
    """
    Natural Language Understanding class.
    Accepts: user input string
    Output: A list of dictionaries. Each dictionary contains one of the four
        keys: request, command, response and off_topic, corresponding to four
        categories of user input.
        request: handle the user requests concerning movies. The value of request
            can be "title", "year", "plot", "director", "star", "country", 
            "filming_loc", "language", OPINION, COUNT. True or false questions
            are handled are COUNT. This dictionary also contains conditions of 
            the request.
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
    

    def process(self, input_string):
        dm.chatbot.submit(input_string)
        chunked = self.chk.chunk(input_string)
        
        result = []
            
        if self.expect:
            response = self._response(chunked)
            if response:
                result.append(response) 

        for x in chunked:
            if isinstance(x, nltk.Tree):
                index = chunked.index(x)
                if x.node == "B-QUESTION":
                    request = self._parse_question(chunked,index)
                    if request:
                        result.append(request)
                    break
                elif x.node == "COMMAND":
                    next=chunked[index+1]
                    if isinstance(next, nltk.Tree):
                        next=next.leaves()[0]
                    all_leaves=chunked.leaves()
                    next_index = all_leaves.index(next)
                    keywords=self._search_keywords(all_leaves[next_index:])
                    if len(keywords)>0:
                        request=self._parse_pref(chunked, request=self._keyword2request(keywords[0]))
                        if request:
                            result.append(request)
                        break
                    #else: keywords not found, continue searching
            elif x[1]=="BYE":
                return {"command":dm.EXIT}
            elif x[1]=="RESTART":
                result.append({"command":dm.CLEAR})
                # Don't break here, there may be more preference
        else:
            preference=self._parse_pref(chunked)
            if preference:
                result.append(preference)
                
                    
        if len(result==0):
            result.append(self._off_topic(input_string))
            
    def _response(self, chuncked):
        """
        This method is called when user is supposed to answer a question
        Precondition: self.expect is not None    
        """
        if self.expect == "result_length":
            for node in chuncked:
                if isinstance(node, tuple) and node[1]=='CD':
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
            return self._parse_pref(chunked, request="person")
        elif qtype=="when":
            return self._parse_pref(chunked, request="year")
        elif qtype=="where":
            # FIXME Any other where question not about filming location? 
            return self._parse_pref(chunked, request="filming_loc")
        elif qtype=="how":
            # Handle "how many"
            if len(keywords>0):
                return self._parse_pref(chunked, request=dm.COUNT, of=self._keyword2request(keywords[0]))
        elif qtype=="what" or qtype=="which":
            # handle cases like which year, what genre, etc
            if len(keywords>0):
                return self._parse_pref(chunked, request=self._keyword2request(keywords[0]))
        # Haven't returned, return as preference
        return self._parse_pref(chunked)
    
    def _off_topic(self, input_string):
        return {'off_topic':input_string}
    
    def _search_keywords(self, list):
        """  
        Possible keywords are: KW_YEAR, KW_MOVIE, KW_MOVIES
        KW_DIRECTOR, KW_STAR, KW_PLOT, KW_GENRE, KW_COUNTRY,
        KW_LANGUAGE
        """
        keywords=[]
        for a in list:
            if a[1][0:2]=="KW":
                keywords.append(a[1])
        return keywords
    
    def _keyword2request(self, keyword):
        if keyword=="KW_MOVIE" or keyword=="KW_MOVIES":
            return "title"
        else:
            return keyword[3:].lower()
    
    def _parse_pref(self, chunked, **kargs):
        #TODO try to resolve pronoun locally
        #TODO add 'like' keyword
        negation = False
        all_pref={'request':dm.OPINION}
        all_pref.update(kargs)
        
    def _partition(self, chunked):
        """
        Partition a chunked sentence (tree) into several segments, 
        with each segment only have either positive opinion
        or negative opinion about one or more movie attributes,
        but not a mix
        Accepts: a chunked tree, example can be found at the
        bottom of chunker.py
        Returns: a list of lists, consists of leaves of chunked
        tree
        """
        
    def _decide_opinion(self, list):
        """
        Decide the user opinion in the current segment of sentence,
        represented by a list of tuples.
        Example input can be found by printing chunked.leaves(), with
        chunked being the return value of Chunker.chunk
        """
        