import nltk
import MySQLdb

conn = MySQLdb.connect (host = "localhost", user = "root", db = "imdb")

cursor = conn.cursor()

foo = "\"479849\""
sq = """SELECT mi.info FROM title t, movie_info mi WHERE t.kind_id = "1" AND mi.movie_id = t.id AND mi.info_type_id = 3 AND t.id = """ + foo + """ """

sql = sq
print sql

cursor.execute(sql)
results = set(cursor.fetchall())

for x in results:
        print x