import nltk
import imdb
import MySQLdb

conn = MySQLdb.connect(host = "localhost", user = "imdb", db = "imdb")
cursor = conn.cursor()
i =  imdb.IMDb('sql', uri='mysql://imdb@localhost/imdb')

#i.get_keyword
#search_keyword(u'alabama')

keyword = raw_input("please input keyword: ")

cursor.execute("""
SELECT t.id 
FROM title t, movie_keyword mk, keyword k 
WHERE k.keyword = %s AND k.id = mk.keyword_id AND mk.id = t.id """, (keyword,))

results = cursor.fetchall()
raw_input ("Press key to see results")

count = 0;
if len(results) > 5:
	listLength = 5
else:
	listLength = len(results)
if listLength == 0:
	raw_input("Sorry dude, returned an empty list")
	exit()
	
while count < listLength:
	var01 = results[count]
	print var01
	var02 = i.get_movie(var01[0])
	print var02
	count = count + 1
exit()