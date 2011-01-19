import sys
sys.path.append("../dbi")
import dbi

def trivia(list):
    include = set()
    exclude = set()
    genre_in = set()
    genre_ex = set()
    genre_set = set()

    tuple = list[2:]
    object = list[1]

    #print "\ntrivia input"
    #print list
    #print tuple

    for i,x in enumerate(tuple):

        if("actor" in x or "person" in x):
            #print "actor reached"
            #print dbi.get_id_person(tuple[i+1])
            #include.append(search_actor(tuple[id+1]))

            id_num = dbi.get_id_person(tuple[i+1])

            #print id_num
            #print type(id_num)
            #print dbi.get_name(id_num)
            #print dbi.m_w_a(id_num)
            #print dbi.m_w_a_id(id_num)

            #print dbi.m_w_a(id_num)

            """print x
            print id_num
            print type(id_num)
            print tuple[i+1]
            print type(tuple[i+1])"""

            #print"\n"
            #print dbi.m_w_a_id(id_num)
            #print"\n"

            if("!" in x):
                #exclude.append(dbi.m_w_a(id_num))

                #exclude = exclude.union(dbi.m_w_a(id_num))
                exclude = exclude.union(dbi.m_w_a_id(id_num))
                
            else:
                #include.append(dbi.m_w_a(id_num))

                #print dbi.m_w_a(id_num)

                if(include):
                    #print include
                    #print "printing ids of actor's movies"
                    #print dbi.m_w_a_id(id_num)

                    include = include & dbi.m_w_a_id(id_num)

                    #print include
                else:
                    include = include.union(dbi.m_w_a_id(id_num))

            #print "\nend of actor"
            #print include
            #print exclude
            #print "\n"

        elif("director" in x):
            id_num = dbi.get_id_person(tuple[i+1])

            if("!" in x):
                #exclude.append(dbi.m_w_a(id_num))

                exclude = exclude.union(dbi.m_w_d_id(id_num))
            else:
                #include.append(dbi.m_w_a(id_num))

                #print dbi.m_w_d(id_num)

                if(include):
                    include = include & dbi.m_w_d_id(id_num)
                else:
                    include = include.union(dbi.m_w_d_id(id_num))

            #print "\nend of director"
            #print include
            #print exclude
            #print "\n"

            #include.append(search_director(tuple[id+1]))
            #print x
            #print tuple[i+1]

        elif("title" in x):
            id_num = dbi.get_id_movie(tuple[i+1])

            #print id_num
            #print dbi.get_title(id_num)

            #set(id_num)
            #print id_num

            #include.append(search_title(tuple[id+1]))
            #print x
            #print tuple[i+1]

            #str = dbi.get_title(id_num)
            #title_set = set()
            #title_set.add(str)

            id_set = set()
            id_set.add(str(id_num))

            if("!" in x):
                #exclude.append(dbi.m_w_a(id_num))

                #exclude = exclude.union(title_set)
                exclude = exclude.union(id_set)
            else:
                #include.append(dbi.m_w_a(id_num))

                if(include):
                    #include = include & title_set
                    include = include & id_set
                else:
                    #include = include.union(title_set)
                    include = include.union(id_set)                    

            #print "\nend of title"
            #print include
            #print exclude
            #print "\n"

            #include.append(title_set)
            #include.append(dbi.get_title(id_num))

        elif("genre" in x):
            if("!" in x):
                genre_ex.add(tuple[i+1])
            else:
                genre_in.add(tuple[i+1])

            #print x
            #print tuple[i+1]

        elif("keyword" in x):
            #print "\nreached keyword"
            #print dbi.m_w_k(tuple[i+1])
            #print dbi.m_w_k_id(tuple[i+1])
            #print len(dbi.m_w_k_id(tuple[i+1]))
            #print tuple[i+1]
            #print x
            #print "printing include"
            #print include

            #print "\n printing union"
            #print include.union(dbi.m_w_k_id(tuple[i+1]))

            #for x in dbi.m_w_k_id(tuple[i+1]):
            #    print dbi.get_title(x)

            if("!" in x):
                #exclude.append(dbi.m_w_a(id_num))

                #exclude = exclude.union(dbi.m_w_a(id_num))

                exclude = exclude.union(dbi.m_w_k_id(tuple[i+1]))
                #print "\n printing exclude"
                #print exclude
                
            else:
                #print "\n positive keyword"
                #include.append(dbi.m_w_a(id_num))

                #print dbi.m_w_a(id_num

                if(include):
                    #print dbi.m_w_k_id(tuple[i+1])

                    include = include.intersection(dbi.m_w_k_id(tuple[i+1]))

                    #print include & dbi.m_w_k_id(tuple[i+1])
                    #print "\n printing include 1"
                    #print include
                else:
                    #print dbi.m_w_k_id(tuple[i+1])
                    #print dbi.get_title(567875)

                    include = include.union(dbi.m_w_k_id(tuple[i+1]))

                    #print "\n printing include 1"
                    #print include

        elif("year" in x):
            if("!" in x):
                #exclude.append(dbi.m_w_a(id_num))

                #exclude = exclude.union(dbi.m_w_a(id_num))

                exclude = exclude.union(dbi.m_w_y_id(tuple[i+1]))
                #print "\n printing exclude"
                #print exclude
                
            else:
                #include.append(dbi.m_w_a(id_num))

                #print dbi.m_w_a(id_num)

                if(include):
                    #print dbi.m_w_y_id(tuple[i+1])

                    include = include.intersection(dbi.m_w_y_id(tuple[i+1]))

                    #print  include & dbi.m_w_k_id(tuple[i+1]
                    #print "\n printing include 1"
                    #print include
                else:
                    include = include.union(dbi.m_w_y_id(tuple[i+1]))

    #print "\nfinal include exclude"
    #print include
    #print exclude
    #print "\nfinal genre sets"
    #print genre_in
    #print genre_ex
    #print "\ninclude - exclude"
    #print include - exclude
    #print len(include-exclude)
    #print "\n"

    final_include = include-exclude

    #for x in final_include:
        #print "trying to print titles"
        #print dbi.get_title(x)

    if(final_include):
        if(genre_in or genre_ex):
            for x in final_include:
                temp = dbi.genre_of_movie(x)

                if(genre_ex):

                    if(temp.isdisjoint(genre_ex)):

                        if(genre_in):

                            if(genre_in & temp):
                                genre_set.add(x)

                        else:
                            genre_set.add(x)
                elif(genre_in):

                    if(genre_in & temp):
                        genre_set.add(x)

        if(genre_set):
            final_include = genre_set

        #print genre_set
        #print len(genre_set)

        return_set = []

        if(object == "director"):
            for x in final_include:
                #print dbi.get_director(x)
                for y in dbi.get_director(x):
                    return_set.append(y)

                #return_set.add(dbi.get_director(x))
            return return_set
        elif(object == "actor"):
            for x in final_include:
                #print dbi.get_cast(x)
                for y in dbi.get_cast(x):
                    return_set.append(y)
            return return_set
        elif(object == "person"):
            for x in final_include:
                #print dbi.get_cast(x)
                for y in dbi.get_cast(x):
                    return_set.append(y)
            return return_set
        elif(object == "plot"):
            for x in final_include:
                #print dbi.get_plot(x)
                return_set.append(dbi.get_plot(x))
            return return_set
        elif(object == "genre"):
            for x in final_include:
                #print dbi.get_genre(x)
                for y in dbi.get_genre(x):
                    return_set.append(y)
            return return_set
        elif(object == "keyword"):
            for x in final_include:
                #print dbi.get_keywords(x)
                for y in dbi.get_keywords(x):
                    return_set.append(y)
        elif(object == "year"):
            for x in final_include:
                #print dbi.get_year(x)
                return_set.append(dbi.get_year(x))
            return return_set
        elif(object == "title"):
            for x in final_include:
                #print dbi.get_title(x)
                return_set.append(dbi.get_title(x))
            return return_set

    else:
        return final_include


def trueFalse(tuple):
    include = set()
    exclude = set()
    genre_in = set()
    genre_ex = set()
    genre_set = set()
    #key_in = set()
    #key_ex = set()
    #year_in = set()
    #year_ex = set()
 
    #print "\ntreu_false input"
    #print tuple

    for i,x in enumerate(tuple):

        if("actor" in x or "person" in x):
            #include.append(search_actor(tuple[id+1]))

            id_num = dbi.get_id_person(tuple[i+1])

            #print id_num

            #print dbi.m_w_a(id_num)

            """print x
            print id_num
            print type(id_num)
            print tuple[i+1]
            print type(tuple[i+1])"""

            #print"\n"
            #print dbi.m_w_a_id(id_num)
            #print"\n"

            if("!" in x):
                #exclude.append(dbi.m_w_a(id_num))

                #exclude = exclude.union(dbi.m_w_a(id_num))
                exclude = exclude.union(dbi.m_w_a_id(id_num))
                
            else:
                #include.append(dbi.m_w_a(id_num))

                #print dbi.m_w_a(id_num)

                if(include):
                    include = include & dbi.m_w_a_id(id_num)
                else:
                    include = include.union(dbi.m_w_a_id(id_num))

            #print "\nend of actor"
            #print include
            #print exclude
            #print "\n"

        elif("director" in x):
            id_num = dbi.get_id_person(tuple[i+1])

            if("!" in x):
                #exclude.append(dbi.m_w_a(id_num))

                exclude = exclude.union(dbi.m_w_d_id(id_num))
            else:
                #include.append(dbi.m_w_a(id_num))

                #print dbi.m_w_d(id_num)

                if(include):
                    include = include & dbi.m_w_d_id(id_num)
                else:
                    include = include.union(dbi.m_w_d_id(id_num))

            #print "\nend of director"
            #print include
            #print exclude
            #print "\n"

            #include.append(search_director(tuple[id+1]))
            #print x
            #print tuple[i+1]

        elif("title" in x):
            id_num = dbi.get_id_movie(tuple[i+1])

            #print id_num
            #print dbi.get_title(id_num)

            #set(id_num)
            #print id_num

            #include.append(search_title(tuple[id+1]))
            #print x
            #print tuple[i+1]

            #str = dbi.get_title(id_num)
            #title_set = set()
            #title_set.add(str)

            id_set = set()
            id_set.add(str(id_num))

            if("!" in x):
                #exclude.append(dbi.m_w_a(id_num))

                #exclude = exclude.union(title_set)
                exclude = exclude.union(id_set)
            else:
                #include.append(dbi.m_w_a(id_num))

                if(include):
                    #include = include & title_set
                    include = include & id_set
                else:
                    #include = include.union(title_set)
                    include = include.union(id_set)                    

            #print "\nend of title"
            #print include
            #print exclude
            #print "\n"

            #include.append(title_set)
            #include.append(dbi.get_title(id_num))

        elif("genre" in x):
            if("!" in x):
                genre_ex.add(tuple[i+1])
            else:
                genre_in.add(tuple[i+1])

            #print x
            #print tuple[i+1]

        elif("keyword" in x):
            #print "\nreached keyword"
            #print dbi.m_w_k(tuple[i+1])
            #print dbi.m_w_k_id(tuple[i+1])
            #print len(dbi.m_w_k_id(tuple[i+1]))
            #print tuple[i+1]
            #print x
            #print "printing include"
            #print include

            #print "\n printing union"
            #print include.union(dbi.m_w_k_id(tuple[i+1]))

            #for x in dbi.m_w_k_id(tuple[i+1]):
            #    print dbi.get_title(x)

            if("!" in x):
                #exclude.append(dbi.m_w_a(id_num))

                #exclude = exclude.union(dbi.m_w_a(id_num))

                exclude = exclude.union(dbi.m_w_k_id(tuple[i+1]))
                #print "\n printing exclude"
                #print exclude
                
            else:
                #include.append(dbi.m_w_a(id_num))

                #print dbi.m_w_a(id_num)

                if(include):
                    #print dbi.m_w_k_id(tuple[i+1])

                    include = include.intersection(dbi.m_w_k_id(tuple[i+1]))

                    #print  include & dbi.m_w_k_id(tuple[i+1])
                    #print "\n printing include 1"
                    #print include
                else:
                    include = include.union(dbi.m_w_k_id(tuple[i+1]))

                    #print "\n printing include 2"
                    #print include

            """if("!" in x):
                key_ex.add(tuple[i+1])
            else:
                key_in.add(tuple[i+1])"""            

            #include.append(search_keyword(tuple[id+1]))
            #print x
            #print tuple[i+1]



        elif("year" in x):
            if("!" in x):
                #exclude.append(dbi.m_w_a(id_num))

                #exclude = exclude.union(dbi.m_w_a(id_num))

                exclude = exclude.union(dbi.m_w_y_id(tuple[i+1]))
                #print "\n printing exclude"
                #print exclude
                
            else:
                #include.append(dbi.m_w_a(id_num))

                #print dbi.m_w_a(id_num)

                if(include):
                    #print dbi.m_w_y_id(tuple[i+1])

                    include = include.intersection(dbi.m_w_y_id(tuple[i+1]))

                    #print  include & dbi.m_w_k_id(tuple[i+1]
                    #print "\n printing include 1"
                    #print include
                else:
                    include = include.union(dbi.m_w_y_id(tuple[i+1]))

            #print "\n printing include"
            #print include
            #print len(include)
            #include.append(search_year(tuple[id+1]))
            #print x
            #print tuple[i+1]

    #print include

    #print "\nfinal include and exclude"
    #print include
    #print exclude
    #print "\nfinal genre sets"
    #print genre_in
    #print genre_ex
    #print "\ninclude - exclude"
    #print include - exclude
    #print len(include-exclude)
    #print "\n"

    final_include = include-exclude

    #for x in include-exclude:
        #print dbi.get_title(x)

    if(final_include):
        if(genre_in or genre_ex):
            for x in final_include:
                temp = dbi.genre_of_movie(x)

                if(genre_ex):

                    if(temp.isdisjoint(genre_ex)):

                        if(genre_in):

                            if(genre_in & temp):
                                genre_set.add(x)

                        else:
                            genre_set.add(x)
                elif(genre_in):

                    if(genre_in & temp):
                        genre_set.add(x)

        if(genre_set):
            final_include = genre_set


        #print genre_set
        #print len(genre_set)
        #print "true"
        
        return final_include
    else:
        #print "false"

        return final_include

questions = list()
preferences = list()
true_false = list()

def input(string):

    if(string[0] == "trivia"):
        questions.append(string)
        trivia(string)

    elif(string[0] == "like" or string[0] == "dislike"):
        preferences.append(string)

    elif(string[0] == "true_false"):
        true_false.append(string)
        trueFalse(string)

    #print questions
    #print preferences
    #print true_false
    #print "\n"

q1 = ("trivia", "title", "keyword", "skynet", "actor", "linda hamilton")
p1 = ("like", "title", "heat")
p2 = ("dislike", "actor", "carrot top")
tf1 = ["true_false", "!year", "2006", "keyword", "snake", "actor", "samuel l jackson"]
tf2 = ["true_false", "title", "die hard", "genre", "Action"]

input(q1)
#input(p1)
#input(p2)
#input(tf1)
print "\n"
#input(tf2)
