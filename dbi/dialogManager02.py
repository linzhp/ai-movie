import sys
sys.path.append("../dbi")
import dbi

import nltk
import imdb
import MySQLdb

choice = ("preference", "type", "typeInstance")
list = list()

conn = MySQLdb.connect(host = "localhost", user = "imdb", db = "imdb")
cursor = conn.cursor()
i =  imdb.IMDb('sql', uri='mysql://imdb@localhost/imdb')

def listGenerateKeyword(keyword):
   keyword = i.search_keyword(keyword)
   cursor.execute("""
   SELECT t.id 
   FROM title t, movie_keyword mk, keyword k 
   WHERE k.keyword = %s AND k.id = mk.keyword_id AND mk.id = t.id """, (keyword[0],))
   results = cursor.fetchall()
      
   listTemp = []
   for x in results:
      listTemp.append(x[0])
   return listTemp
   
while choice[0] != "quit":

   choiceZero = raw_input("Please input 'like' or 'dislike' or 'quit'\n")
   if choiceZero == "quit":
      print "Well fine, BE ThAT WAY!\n"
      break

   choiceOne = raw_input("\nNow please input query 'type':\n")
   choiceTwo = raw_input("\nLastly, input the instance of that type:\n")	
   choice = (choiceZero, choiceOne, choiceTwo)

   if choice[0] == "like" or choice[0] == "dislike":
      if choice[1] == "keyword":
         if not list:
            print "This list is empty"
            if choice[0] == "dislike":
         	   print "Don't generate a negative initial list!!!"
         	   continue
            list = listGenerateKeyword(choice[2])
         else:
            print "This list has stuff"
            oldList = list
            list = set(list) & set(listGenerateKeyword(choice[2]))
            if not list:
               print "\nREVERTING TO OLD LIST. CAPS FOR EMPHASIS OF COURSE\n"
               list = oldList

      if choice[1] == "actor":
         if not list:
            if choice[0] == "dislike":
               print "Don't generate a negative initial list!!!"
            else:
               actorID = dbi.get_id_person(choice[2])
               list = set(dbi.m_w_a(actorID))
         else:
            print "This list has stuff"
            actorID = dbi.get_id_person(choice[2])
            oldList = list
            if choice[0] == "like":
               list = (list).intersection(set(dbi.m_w_a(actorID)))
            if choice[0] == "dislike":
               list = (list).difference(set(dbi.m_w_a(actorID)))
            if not list:
               print "\nREVERTING TO OLD LIST. CAPS FOR EMPHASIS OF COURSE\n"
               list = oldList
               
      if choice[1] == "director":
         if not list:
            if choice[0] == "dislike":
               print "Don't generate a negative initial list!!!"
            else:
               directorID = dbi.get_id_person(choice[2])
               list = set(dbi.m_w_a(directorID))
         else:
            print "This list has stuff"
            directorID = dbi.get_id_person(choice[2])
            oldList = list
            if choice[0] == "like":
               list = (list).intersection(set(dbi.m_w_d(directorID)))
            if choice[0] == "dislike":
               list = (list).difference(set(dbi.m_w_d(directorID)))
            if not list:
               print "\nREVERTING TO OLD LIST. CAPS FOR EMPHASIS OF COURSE\n"
               list = oldList
               
   print "This is present choice -->"
   print choice
   print "\n"
   print "This is present list -->"
   print list
   print "\n"