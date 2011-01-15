import nltk
import MySQLdb

conn = MySQLdb.connect (host = "localhost", user = "imdb", db = "imdb")

cursor = conn.cursor()
foo = "\"2006\""

sq = """SELECT t.id FROM title t WHERE t.production_year =  """ + foo + """ AND t.kind_id = "1" """

sql = sq
print sql

cursor.execute(sql)
results = set(cursor.fetchall())

for x in results:
	print x