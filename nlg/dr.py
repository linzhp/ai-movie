import sys
sys.path.append("../dbi")
sys.path.append("../dm")
import dbi
import pref

#get_name(ID)

def dialogueResolution(choice, memory, memoryTrivia, Movee):

   stringTemp = ""
   
   if choice[0] == "trivia":
      listTrivia = list(memoryTrivia)
      if len(listTrivia) == 1:
         stringTemp += "You asked about " + choice[1] + " and we found one instance: " + (listTrivia[0])
      elif len(listTrivia) > 1:
         print "We received " + str(len(listTrivia)) + " results. How many do you want?"
         tempInt = int(raw_input())
         if type(tempInt) == int:
            if tempInt >= len(listTrivia):
               tempInt = len(listTrivia) - 1
            for n in range(0, tempInt):
               stringTemp += listTrivia[n]
               stringTemp += "\n"
         else:
            stringTemp += "not an int"
      else:
         stringTemp += "The query you asked returned false. "

   if choice[0] == "True_False":
      listTrivia = list(memoryTrivia)
      if choice[1] == "actor":
         stringTemp += "I am in actor"
         if not memoryTrivia:
            stringTemp += "No"
         else:
            stringTemp += "Yep!"
            stringTemp += Movee.ask_trueFalse(listTrivia)
      if choice[1] == "person":
         if not memoryTrivia:
            stringTemp += "No"
         else:
            stringTemp += "Yep!"
            stringTemp += Movee.ask_trueFalse(listTrivia)
      if choice[1] == "director":
         if not memoryTrivia:
            stringTemp += "No"
         else:
            stringTemp += "Yep!"
            stringTemp += Movee.ask_trueFalse(listTrivia)
      if choice[1] == "title":
         if not memoryTrivia:
            stringTemp += "No"
         else:
            stringTemp += "Yep!"
            stringTemp += Movee.ask_trueFalse(listTrivia)
      if choice[1] == "genre":
         if not memoryTrivia:
            stringTemp += "No"
         else:
            stringTemp += "Yep!"
            stringTemp += Movee.ask_trueFalse(listTrivia)
      if choice[1] == "keyword":
         if not memoryTrivia:
            stringTemp += "No"
         else:
            stringTemp += "Yep!"
            stringTemp += Movee.ask_trueFalse(listTrivia)
      if choice[1] == "year":
         if not memoryTrivia:
            stringTemp += "No"
         else:
            stringTemp += "Yep!"
            stringTemp += Movee.ask_trueFalse(listTrivia)
              
   if choice[0] == "like" or choice[0] == "dislike":
      listMem = list(memory)
      tempString = "This is present movie list: "
      if len(listMem) < 5:
         stringTemp += "Present list size = " + str(len(memory))
         for x in listMem:
            tempString += dbi.get_title(x)
            tempString += " "
         stringTemp += tempString
      else:
         stringTemp += "Present list size = " + str(len(memory))
         stringTemp += Movee.ask_recommendation()
         Movee.remove_recommendation(choice[1])
         
   print stringTemp + "\n"
   return stringTemp