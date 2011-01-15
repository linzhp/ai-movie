import nltk
import MySQLdb
import sets

conn = MySQLdb.connect (host = "localhost", user = "imdb", db = "imdb")

cursor = conn.cursor()
foo = "\"1209025\""
sq = """SELECT t.title FROM title t, cast_info ci, name n WHERE ci.role_id = "1" AND t.kind_id = "1" AND t.id = ci.movie_id AND ci.person_id = n.id AND n.id = """ + foo + """ """
sql = sq
print sql
sq2 = """SELECT t.title FROM title t, cast_info ci, name n WHERE ci.role_id = "2" AND t.kind_id = "1" AND t.id = ci.movie_id AND ci.person_id = n.id AND n.id = """ + foo + """ """
sql2 = sq2
print sql2
cursor.execute(sql)
results = sets.Set(cursor.fetchall())
cursor.execute(sql2)
results2 = sets.Set(cursor.fetchall())

inter = results.union(results2)

for x in inter:
	print x