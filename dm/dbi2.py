import nltk
import MySQLdb
import imdb
i =  imdb.IMDb('sql', uri='mysql://imdb@localhost/imdb')
conn = MySQLdb.connect (host = "localhost", user = "imdb", db = "imdb")

#Takes in movie title(string), returns movie ID.
def get_id_movie(fn_input):
    results = i.search_movie(fn_input)
    size = len(results)
    if (size <= 0):
        return 'none'
    temp = results[0]['title']
    count = 0
    movie_list = list()
    for movie in results:
        if movie['title'] == temp:
            movie_list.append(movie)
    size = len(movie_list)
    if (size < 1):
        return 'error'
    elif (size == 1):
        return movie_list[0].movieID
    out = movie_list[0]
    votes = 0
    for movie in movie_list:
        temp = movie
        i.update(temp)
        if 'votes' in temp.keys():
            if temp['votes'] > votes:
               votes = int(temp['votes'])
               out = movie
    return out.movieID

#Takes in person title(string), returns movie ID.
def get_id_person(fn_input):
    results = i.search_person(fn_input)
    size = len(results)
    if (size <= 0):
        return 'none'
    temp = results[0]['name']
    count = 0
    person_list = list()
    for person in results:
        if person['name'] == temp:
            person_list.append(person)
    size = len(person_list)
    if (size < 1):
        return 'none'
    elif (size == 1):
        return person_list[0].personID
    out = person_list[0]
    for person in person_list:
        if '(I)' in person['long imdb name']:
            out = person
    return out.personID

#Takes in movie ID, returns cast (List of Strings).
def get_cast(movie_id):
    movie = i.get_movie(movie_id)
    if 'cast' in movie.keys():
        result = movie['cast']
        cast = list()
        for person in result:
            temp = list()
            temp.append(person['name'])
            temp.append(" as ")
            temp.append(unicode(person.currentRole))
            temp = "".join(temp)
            temp = str(temp)
            cast.append(temp)
        return cast
    return 'none'

#Takes in movie ID, returns directors (List of Strings).
def get_director(movie_id):
    movie = i.get_movie(movie_id)
    if 'director' in movie.keys():
        result = movie['director']
        director = list()
        for person in result:
            director.append(str(person['name']))
        return director
    return 'none'

#Takes in movie ID, returns genres (List of Strings).
def get_genre(movie_id):
    movie = i.get_movie(movie_id)
    if 'genres' in movie.keys():
        result = movie['genres']
        result = str(result)
        return result
    return 'none'

#Takes in movie ID, returns plot (String).
def get_plot(movie_id):
    movie = i.get_movie(movie_id)
    if 'plot' in movie.keys():
        result = movie['plot']
        if len(result) >= 1:
            return str(result[0])
    return 'none'

#Takes in movie ID, returns cast (List of Strings).
def get_rating(movie_id):
    movie = i.get_movie(movie_id)
    if 'rating' in movie.keys():
        result = movie['rating']
        return str(result)
    return 'none'

#Takes in movie ID, returns runtime (String).
def get_runtimes(movie_id):
    movie = i.get_movie(movie_id)
    if 'runtimes' in movie.keys():
        result = movie['runtimes']
        return str(result[0])
    return 'none'

#Takes in movie ID, returns year (String).
def get_year(movie_id):
    movie = i.get_movie(movie_id)
    if 'year' in movie.keys():
        result = movie['year']
        return str(result)
    return 'none'

#Takes in movie ID, returns movie's keywords (List of Strings).
def get_keywords(movie_id):
    movie = i.get_movie(movie_id)
    if 'keywords' in movie.keys():
        result = movie['keywords']
        key = list()
        for w in result:
            key.append(str(key))
        return key
    return 'none'

#Takes in movie ID, returns production companies (List of Strings).
def get_production(movie_id):
    movie = i.get_movie(movie_id)
    if 'production companies' in movie.keys():
        result = movie['production companies']
        company = list()
        for item in result:
            company.append(str(item['name']))
        return company
    return 'none'

#Takes in movie ID, returns title (String).
def get_title(movie_id):
    movie = i.get_movie(movie_id)
    if 'long imdb title' in movie.keys():
        result = movie['title']
        return str(result)
    return 'none'

#Takes in person ID, returns biography (String).
def get_biography(person_id):
    person = i.get_person(person_id)
    if 'mini biography' in person.keys():
        result = person['mini biography']
        return str(result)
    return 'none'

#Takes in person ID, returns movies they directed (List of Strings).
def get_movies_directed(person_id):
    person = i.get_person(person_id)
    if 'director' in person.keys():
        result = person['director']
        movie = list()
        for item in result:
            movie.append(str(item['title']))
        return movie
    return 'none'

#Takes in person ID, returns name (String).
def get_name(person_id):
    person = i.get_person(person_id)
    if 'name' in person.keys():
        result = person['name']
        return str(result)
    return 'none'

#Takes in person ID, returns movies they acted in (List of Strings).
def get_movies_acted(person_id):
    person = i.get_person(person_id)
    if 'actor' in person.keys():
        result = person['actor']
        movie = list()
        for item in result:
            movie.append(item['title'])
        return movie
    return 'none'

#Takes in person ID, returns their "other" works (List of Strings).
def get_other_works(person_id):
    person = i.get_person(person_id)
    if 'other works' in person.keys():
        result = person['other works']
        other = list()
        for w in result:
            other.append(str(w))
        return result
    return 'none'

#Takes in person ID, returns their birthdate (String).
def get_birthdate(person_id):
    person = i.get_person(person_id)
    if 'birth date' in person.keys():
        result = person['birth date']
        return str(result)
    return 'none'

#Takes in person ID, returns movies they acted in (Set of Strings).
def m_w_a(actorID):
    cursor = conn.cursor()
    foo = actorID
    foo = str(foo)
    sq = """SELECT t.title FROM title t, cast_info ci, name n WHERE ci.role_id = "1" AND t.kind_id = "1" AND t.id = ci.movie_id AND ci.person_id = n.id AND n.id = """ + foo + """ """
    sql = sq
    sq2 = """SELECT t.title FROM title t, cast_info ci, name n WHERE ci.role_id = "2" AND t.kind_id = "1" AND t.id = ci.movie_id AND ci.person_id = n.id AND n.id = """ + foo + """ """
    sql2 = sq2
    cursor.execute(sql)
    results = cursor.fetchall()
    list1 = list()
    for w in results:
        list1.append(str(w[0]))
    cursor.execute(sql2)
    results2 = cursor.fetchall()
    list2 = list()
    for w in results:
        list2.append(str(w[0]))
    set1 = set(list1)
    set2 = set(list2)
    inter = set1 | set2
    return inter

#Takes in person ID, returns movies associated with them (Set of Strings).
def m_w_p(personID):
    cursor = conn.cursor()
    foo = personID
    foo = str(foo)
    sq = """SELECT t.title FROM title t, cast_info ci, name n WHERE  t.kind_id = "1" AND t.id = ci.movie_id AND ci.person_id = n.id AND n.id = """ + foo + """ """
    sql = sq
    cursor.execute(sql)
    results = cursor.fetchall()
    list1 = list()
    for w in results:
        list1.append(str(w[0]))
    return set(list1)

#Takes in genre, returns movies with that genre (Set of Strings).
#Make sure it is an actual genre on SQL
def m_w_g(genre):
    cursor = conn.cursor()
    foo = genre
    sq = """SELECT t.title FROM title t, movie_info mi WHERE t.kind_id = "1" AND mi.movie_id = t.id AND mi.info_type_id = 3 AND mi.info = """ + foo + """ """
    sql = sq
    cursor.execute(sql)
    results = cursor.fetchall()
    list1 = list()
    for w in results:
        list1.append(str(w[0]))
    return set(list1)

#Takes in person ID, returns movies they directed (Set of Strings).
def m_w_d(directorID):
    cursor = conn.cursor()
    foo = directorID
    foo = str(foo)
    sq = """SELECT t.title FROM title t, cast_info ci, name n WHERE ci.role_id = "8" AND t.kind_id = "1" AND t.id = ci.movie_id AND ci.person_id = n.id AND n.id = """ + foo + """ """
    sql = sq
    cursor.execute(sql)
    results = cursor.fetchall()
    list1 = list()
    for w in results:
        list1.append(str(w[0]))
    return set(list1)

#Takes in person ID, returns ids of movies with given actor  (Set of Strings).
def m_w_a_id(actorID):
    cursor = conn.cursor()
    foo = actorID
    foo = str(foo)
    sq = """SELECT t.id FROM title t, cast_info ci, name n WHERE ci.role_id = "1" AND t.kind_id = "1" AND t.id = ci.movie_id AND ci.person_id = n.id AND n.id = """ + foo + """ """
    sql = sq
    sq2 = """SELECT t.id FROM title t, cast_info ci, name n WHERE ci.role_id = "2" AND t.kind_id = "1" AND t.id = ci.movie_id AND ci.person_id = n.id AND n.id = """ + foo + """ """
    sql2 = sq2
    cursor.execute(sql)
    results = cursor.fetchall()
    list1 = list()
    for w in results:
        list1.append(str(w[0]))
    cursor.execute(sql2)
    results2 = cursor.fetchall()
    list2 = list()
    for w in results:
        list2.append(str(w[0]))
    set1 = set(list1)
    set2 = set(list2)
    inter = set1 | set2
    return inter

#Takes in movie ID, returns genres of movies (Set of Strings).
def genre_of_movie(movieID):
    cursor = conn.cursor()
    foo = "\"479849\""
    sq = """SELECT mi.info FROM title t, movie_info mi WHERE t.kind_id = "1" AND mi.movie_id = t.id AND mi.info_type_id = 3 AND t.id = """ + foo + """ """
    sql = sq
    cursor.execute(sql)
    results = cursor.fetchall()
    list1 = list()
    for w in results:
        list1.append(str(w[0]))
    return set(list1)

#Takes in a keyword, returns movies associated with given keyword (Set of Strings).
def m_w_k(keyword):
   keyword = i.search_keyword(keyword)
   cursor.execute("""
   SELECT t.id 
   FROM title t, movie_keyword mk, keyword k 
   WHERE k.keyword = %s AND k.id = mk.keyword_id AND mk.id = t.id AND t.kind_id = "1" """, (keyword[0],))
   results = cursor.fetchall()
   listTemp = []
   for x in results:
      listTemp.append(x[0])
   return set(listTemp)

"""id1 = get_id_person("John Travolta")
id2 = get_id_person("SameuL L Jackson")
set1 = m_w_a(id1)
list2 = get_movies_acted(id2)
set2 = set(list2)
print set1
print set2
set3 = set1 & set2
print set3
qwe = m_w_a_id(id1)
print qwe
qwe = m_w_k("snake")
print qwe"""
