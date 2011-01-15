import nltk
import imdb
i =  imdb.IMDb('sql', uri='mysql://imdb@localhost/imdb')

def find_movie(fn_input):
    result = i.search_movie(fn_input)
    if len(result) > 0:
        length = len(result)
        count = 0
        max_count = min(length,5)
        while count < max_count:
            print count + 1, '->', result[count]['long imdb title']
            count = count + 1
        user_input = raw_input("Want any of these(1-5)?  ")
        movie = result[int(user_input) - 1]        
        i.update(movie)
        #print movie['title']
        print movie.summary()
    else:
        print 'No movie, sorry.'

def find_person(fn_input):
    result = i.search_person(fn_input)
    if len(result) > 0:
        length = len(result)
        count = 0
        max_count = min(length,5)
        while count < max_count:
            print count + 1, '->', result[count]['name']
            count = count + 1
        user_input = raw_input("Want any of these(1-5)?  ")
        person = result[int(user_input) - 1]
        i.update(person)
        #print person['name']
        print person.summary()
    else:
        print 'No movie, sorry.'

def find_keyword(fn_input):
    result = i.get_keyword(fn_input)
    if len(result) > 0:
        length = len(result)
        count = 0
        max_count = min(length,5)
        while count < max_count:
            print count + 1, '->', result[count]['long imdb title']
            count = count + 1
        user_input = raw_input("Want any of these(1-5)?  ")
        movie = result[int(user_input) - 1]
        i.update(movie)
        #print movie['title']
        print movie.summary()


def actor_keyword():
    person_input = raw_input("Give me an actor!  ")
    people = i.search_person(person_input)
    person = people[0]
    i.update(person)
    list1 = person['actor']
    print list1
    key_input = raw_input("Give me a keyword!  ")
    list2 = i.get_keyword(key_input)
    print list2
    set1 = set(list1)
    set2 = set(list2)
    set3 = set1 & set2
    list3 = list(set3)
    print ""
    print "size of actor movie list: ", len(list1)
    print "size of keyword movie list: ", len(list2)
    print list3

count = 1;
while count is count:
    print ""
    choice = raw_input("#1-4 // 1. Find Movie, 2. Find Person, 3. Find Keyword, 4.Actor & Keyword Search: ")
    if choice is '1':
        name = raw_input("Title?  ")
        find_movie(name)
    if choice is '2':
        name = raw_input("Name?  ")
        find_person(name)
    if choice is '3':
        name = raw_input("Keyword?  ")
        find_keyword(name)
    if choice is '4':
        actor_keyword()




