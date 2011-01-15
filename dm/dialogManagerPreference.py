import sys
sys.path.append("../dbi")
import dbi


def generateMoviePreferenceList(choice, memory):

   # Case Actor
   if choice[1] == "actor":
      if not memory:
         if choice[0] == "dislike":
         	print "What the hell is your problem!? All movies that lack a particular actor as a primary query? REALLY!?"
         else:
            id = dbi.get_id_person(choice[2])
            memory = dbi.m_w_a_id(id)
      else:
         print "This list has stuff"
         id = dbi.get_id_person(choice[2])
         oldmemory = memory
         if choice[0] == "like":
            memory = (memory).intersection(set(dbi.m_w_a_id(id)))
         if choice[0] == "dislike":
            memory = (memory).difference(set(dbi.m_w_a_id(id)))
         if not memory:
            print "\nThe cross of this list is empty yo. CAPS FOR EMPHASIS OF COURSE\n"
            memory = oldmemory
             
   # Case Director  
   if choice[1] == "director":
      if not memory:
         if choice[0] == "dislike":
            print "Don't generate a negative initial memory!!!"
         else:
            id = dbi.get_id_person(choice[2])
            memory = set(dbi.m_w_d_id(id))
      else:
         print "This memory has stuff"
         id = dbi.get_id_person(choice[2])
         oldmemory = memory
         if choice[0] == "like":
            memory = (memory).intersection(set(dbi.m_w_d_id(id)))
         if choice[0] == "dislike":
            memory = (memory).difference(set(dbi.m_w_d_id(id)))
         if not memory:
            print "\nREVERTING TO OLD list. CAPS FOR EMPHASIS OF COURSE\n"
            memory = oldmemory
            
   # Case Person   
   if choice[1] == "person":
      if not memory:
         if choice[0] == "dislike":
            print "Don't generate a negative initial memory!!!"
         else:
            id = dbi.get_id_person(choice[2])
            memory = set(dbi.m_w_p_id(id))
      else:
         print "This memory has stuff"
         id = dbi.get_id_person(choice[2])
         oldmemory = memory
         if choice[0] == "like":
            memory = (memory).intersection(set(dbi.m_w_p(id)))
         if choice[0] == "dislike":
            memory = (memory).difference(set(dbi.m_w_p(id)))
         if not memory:
            print "\nREVERTING TO OLD LIST. CAPS FOR EMPHASIS OF COURSE\n"
            memory = oldmemory
            
   # Case keyword  
   if choice[1] == "keyword":
      if not memory:
         if choice[0] == "dislike":
            print "Don't generate a negative initial memory!!!"
         else:
            memory = set(dbi.m_w_k_id(choice[2]))
      else:
         print "This memory has stuff"
         oldmemory = memory
         if choice[0] == "like":
            memory = (memory).intersection(set(dbi.m_w_k_id(choice[2])))
         if choice[0] == "dislike":
            memory = (memory).difference(set(dbi.m_w_k_id(choice[2])))
         if not memory:
            print "\nREVERTING TO OLD LIST. CAPS FOR EMPHASIS OF COURSE\n"
            memory = oldmemory
            
   # Case Genre
   if choice[1] == "genre":
      if not memory:
         if choice[0] == "dislike":
            print "I could do an initial 'negative' genre search, but this would take FOREVAR. So... Can you please try something else first? Sorry!"
         else:
            print "*sigh* this will take a while, this is a pretty broad category to start a search with."
            memory = set(dbi.m_w_g_id(choice[2]))
      else:
         print "This list has stuff"
         oldmemory = memory
            
         if choice[0] == "like":
            listTemp = list()
            for x in memory:
               listGenre = dbi.genre_of_movie(x)
               for y in listGenre:
                  if y == choice[2]:
                     listTemp.append(x)
            memory = set(listTemp)
            
         if choice[0] == "dislike":
            memory = list(memory)
            for x in memory:
               listGenre = dbi.genre_of_movie(x)
               for y in listGenre:
                  if y == choice[2]:
                     memory.remove(x)
            memory = set(memory)

         if not memory:
            print "\nREVERTING TO OLD LIST. CAPS FOR EMPHASIS OF COURSE\n"
            memory = oldmemory   
             
   # Case Title
   if choice[1] == "title":
      id = dbi.get_id_movie(choice[2])
      print "Far too vague, allow me to make some recommendations"

   # Case Other
   if choice[1] == "other":
      print "Sorry, but could you elaborate on what you meant by" + choice[2]
      
   return memory