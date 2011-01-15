import nltk
import MySQLdb
import sets

conn = MySQLdb.connect (host = "localhost", user = "imdb", db = "imdb")

cursor = conn.cursor()
foo = "\"371934\""
sq = """SELECT t.title FROM title t, cast_info ci, name n WHERE  t.kind_id = "1" AND t.id = ci.movie_id AND ci.person_id = n.id AND n.id = """ + foo + """ """
sql = sq
print sql
cursor.execute(sql)
results = sets.Set(cursor.fetchall())
for x in results:
	print x