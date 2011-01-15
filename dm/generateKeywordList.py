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