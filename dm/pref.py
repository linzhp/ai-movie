import sys
sys.path.append("../")
from dbi import dbi
from nlu import nlu

N = nlu.NLU()

class Preference:
   def __init__(self):        
      self.recommendation = ["actor", "director", "person", "title", "genre", "keyword"]
      self.preferenceSet = set()
      self.triviaSet = set()
      self.flagRecommend = 0
      self.yesNoIrritation = 0
      self.hiFlag = 0

   def set_recommendation(self, tempList):
      self.recommendation = tempList
   def set_preferenceSet(self, tempSet):
      self.preferenceSet = tempSet
   def set_triviaSet(self, tempSet):
      self.triviaSet = tempSet
   def set_hiSelf(self, tempInt):
      self.hiFlag = tempInt
      
   def get_recommendation(self):
      return self.recommendation
   def get_preferenceSet(self):
      return self.preferenceSet
   def get_triviaSet(self):
      return self.triviaSet   
   def get_hiSelf(self):
      return self.hiFlag  
      
   def reset(self):
      self.recommendation = ["actor", "director", "person", "title", "genre", "keyword"]
      self.preferenceSet = set()
      self.triviaSet = set()
      
   def yesNo(self):
      tempString = "neither"
      while tempString:
         if self.yesNoIrritation < 5:
            input = raw_input("Yes, no? ")
         elif self.yesNoIrritation > 5:
            input = raw_input("... Yes, no? ")
         choice = N.process(input)
         if not choice:
            if self.yesNoIrritation == 0:
               print "This is your first 'yes/no' error, so I'll just presume you did this by accident."
            elif self.yesNoIrritation == 1:
               print "If you are having troule, a simple ''yes'' or ''no'' is alright. The NLU is parsing this though"
            elif self.yesNoIrritation == 2:
               print "I am starting to suspect you are messing with me, you won't like me angry!"
            elif self.yesNoIrritation >= 3:
               print "Sigh, really?"
            self.yesNoIrritation += 1
            choice = ["empty", "empty", "empty"]
         if choice[0] == "yes" or choice[0] == "no":
            return choice[0]
            
   def remove_recommendation(self, tempString):
      while self.recommendation.count(tempString) != 0:
         self.recommendation.remove(tempString)

   def ask_trivia(self, setTrivia):
      while self.recommendation.count(tempString) != 0:
         self.recommendation.remove(tempString)
         
   def ask_trueFalse(self, setTrivia):
      print "Do you want to see the first match we found? "
      tempString = self.yesNo()
      if (tempString == "yes"):
         return "Alright, here it is: " + str(dbi.get_title(setTrivia[0]))
      else:
         return "Ok, fine."
         
   def ask_hi(self):
      if self.hiFlag == 0:
         self.hiFlag = 2
         print "What a surprise! Someone with manners! I wonder if you went off the prompt? Such a paradox if you did!"         
      elif self.hiFlag == 1:
         print "Well, at least NOW you decided to finally say hi to me. Geez, what a rude punk."         
      elif self.hiFlag == 2:
         self.hiFlag = 3
         print "You already said hi, what are you trying to flatter me or something?."
      elif self.hiFlag == 3:
         print "... *sigh*, I get all of the ''special'' ones"      
               
   def ask_recommendation(self):
      if len(self.recommendation) == 0:
         if self.flagRecommend == 0:
            self.flagRecommend = 1
            return "Well that's a toughie... Not sure what advice to give you. Seems you've hit all of the parameters. You can however try parameters multiple times for further refinement..."
         if self.flagRecommend == 1:
            return "Do you want me to start repeating the query advice again?"
            tempString = self.yesNo()
            if (tempString == "yes"):
               self.recommendation = ["actor", "director", "person", "title", "genre", "keyword"]
            if (tempString == "no"):
               return "okey dokee, no more preference advice for now. " 
         if self.flagRecommend == 2:
            return ""
      else:
         import random
         tempString = self.recommendation[random.randint(0, len(self.recommendation)-1)]
         while self.recommendation.count(tempString) != 0:
            self.recommendation.remove(tempString)
         if tempString == "actor":
            return "Are there any actors you like or dislike? Perhaps specifying one will help you find your dream movie! "
         elif tempString == "director":
            return "Hmm... Do you have any favorite directors? Or directors you absolutely despise? We can parse the movie list by that too. "
         elif tempString == "person":
            return "Perhaps a more general person search might help quite a bit. Don't forget to capitalize the name, else I simply won't be able to determine whether you want a name or not! "
         elif tempString == "title":
            return "Do you have a favorite movie? You can ask for characteristics of a movie you like, then try a further search based on the found characteristics. Just don't forget to put quotations around the movie title, or else I won't be able to determine whether it is a movie or not. "
         elif tempString == "genre":
            return "Do you have a preference for a particular genre? Perhaps there is a genre you utterly despise? "
         elif tempString == "keyword":
            return "IMDb has a lot of plot related keywords going anywhere from 'licking-toilet-bowl' to 'sucking-toes.' Of course, there are more conventional ones like 'snake' and 'plane,' but what's the fun of that? "