import sys
sys.path.append("../dbi")
sys.path.append("../nlu")
import nlu
import dbi
import dmp
import dm
import dr
import pref
import time
from datetime import date

def generate_session_id():
	session_id = str(date.today()) + str(time.time())
	return session_id

Movee = pref.Preference()
choice = ["empty", "empty", "empty"]
#choice = Movee.get_recommendation()
memory = Movee.get_preferenceSet()
memoryTrivia = Movee.get_triviaSet()

N = nlu.NLU()

with open('./session2.log', 'a') as logfile:

	id = generate_session_id()
	logfile.write("\n*\n*  Session id: " + id + "\n*\n")
	print "\n\n Your session id is:", id, "\n\n"

	outstr = "Welcome to the Dialogue Manager! My name is Movee, a highly original name conceived by the most brilliant of the team that designed me. The core functionalities I fascillitate are movie list generation based off of preference, basic trivia, and true/false trivia resolution."

	logfile.write("BOT:" + outstr + "\n")
	print outstr + "\n"
	

	#raw_input()
	#outstr = "Oh yeah, I'm supposed to help you right?"
	#logfile.write("BOT:" + outstr + "\n")
	#print outstr + "\n"
   
	while choice[0] != "bye":

		outstr = "\n\n Alright, how may I help you? "
		logfile.write("BOT:" + outstr + "\n")
		print outstr + "\n"
	
		input = raw_input()
		logfile.write("USER:" + input + "\n")

		choice = N.process(input)
		logfile.write("#NLU: " + str(choice))
		if not choice:
			choice = ["nothing", "nothing", "nothing"]
			outstr = "Sorry, that inquiry is too vague. Can you elaborate please?"
			logfile.write("BOT:" + outstr + "\n")
			print outstr + "\n"
			continue

		if choice[0] == "bye":
			exit()
      
		if choice[0] == "hi":
			Movee.ask_hi()
	      
		if choice[0] == "reset":
			logfile.write("\n*\n*  Session id: " + generate_session_id() + "\n*\n")
			memory = Movee.get_preferenceSet()
	
		#print choice
	   
		if choice[0] == "like" or choice[0] == "dislike":
			if len(choice) < 3:
				outstr = "Sorry, that inquiry is too vague. Can you elaborate please?"
				logfile.write("BOT:" + outstr + "\n")
				print outstr + "\n"
				continue
			memory = dmp.generateMoviePreferenceList(choice, memory)
		if choice[0] == "trivia":
			memoryTrivia = dm.trivia(choice)
		if choice[0] == "True_False":
			memoryTrivia = dm.trueFalse(choice)
	      
		#print "choice is = ", choice
	                           
		outstr = dr.dialogueResolution(choice, memory, memoryTrivia, Movee)
		logfile.write("BOT:" + outstr + "\n")
		print outstr + "\n"

		if Movee.get_hiSelf() == 0:
			Movee.set_hiSelf(1)

logfile.closed

	      	
