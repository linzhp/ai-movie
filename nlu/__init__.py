from os import path 
import sys
import re
import nltk
import dm

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

class NLUnderstanding:
    def __init__(self):
        self.expect = None

    def process(self, input_string):
        chunked = self.chk.chunk(input_string)
        
        result = []
            
        for x in chunked:
            if isinstance(x, nltk.Tree):
                if x.node == "B-QUESTION":
                    index = chunked.index(x)
                    request = self._parse_question(chunked,index)
                    if request:
                        result.append(request)
                    break
                elif x.node == "COMMAND":
                    #TODO implement it
                    break
            elif x[1]=="BYE":
                return {"command":dm.EXIT}
            elif x[1]=="RESTART":
                result.append({"command":dm.CLEAR})
                # Don't break here, there may be more preference
        else:
            preference=self._parse_PRP(chunked)
            if preference:
                #TODO implement it
                pass
                
                    
        if self.expect:
            response = self._response(chunked)
            if response:
                result.append(response) 

        if len(result==0):
            result.append(self._off_topic(input_string))
    """
    User is supposed to answer question
    Precondition: self.expect is not None    
    """
    def _response(self, chuncked):
        if self.expect == dm.HOW_MANY:
            for node in chuncked:
                if node[1]=='CD':
                    return {'response':int(node[0])}
            else:
                return None
        elif self.expect == dm.SEE_RESULT:
            for node in chuncked:
                if node[1]=='YES' or node[1]=='NO':
                    return {'response':node[1]}
        elif self.expect == dm.MORE_PREF:
            # TODO Modify _request not to merge with this dict
            return {'response': dm.MORE_PREF}
     

    def _parse_question(self, chunked, question_index):
        question_tree = chunked[question_index]
        qtype = question_tree[0][0].lower()
        keywords = self._search_keywords(question_tree)
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
        pass
    
    """  
    Possible keywords are: KW_YEAR, KW_MOVIE, KW_MOVIES
    KW_DIRECTOR, KW_STAR, KW_PLOT, KW_GENRE, KW_COUNTRY,
    KW_LANGUAGE
    """
    def _search_keywords(self, list):
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
        pass
