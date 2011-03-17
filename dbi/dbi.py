import nltk
import MySQLdb
import logging
import ConfigParser
from os import path

config = ConfigParser.RawConfigParser()
config.read(path.dirname(__file__)+'/../movie.cfg')
user_name = config.get("database", "user_name")
password = config.get("database", "password")
host = config.get("database", "host")
db_name = config.get("database", "db_name")
#i =  imdb.IMDb('sql', uri='mysql://maw_imdb:pugOrz2u@mysql.cse.ucsc.edu/maw_imdb')
conn = MySQLdb.connect (host = host, user = user_name, db = db_name, passwd = password)
#logfile = open('dbi.log', 'w')
logfile = 0

#query_debug: Inserts 'EXPLAIN' before any query in order to help optimize the queries.
query_debug = False

## select/cout object: all movie attributes
# conditions: all movie attributes, "keyword", "sort" (with the value of some movie attribute), "order" ("desc" or "asc")
# possible movie attributes are: "title", "year", "plot", "director", "actor", "genre", "country", "filming_loc" "award" and "language"
# TODO: award, gross
def query(wanted, known, count=False):
    if not wanted:
        return 0
    logging.debug("wanted: "+wanted)
    logging.debug("known: "+str(known))
    if (logfile):
        logfile.write("Wanted: \"")
        logfile.write(str(wanted))
        logfile.write("\" Known: ")
        logfile.write(str(known)) 
        logfile.write('\n')
    fin_query = ''
    from_clause = build_from(wanted, known)
    if (query_debug):
        fin_query = 'EXPLAIN SELECT DISTINCT '
    else:
        fin_query = 'SELECT DISTINCT '

    if (count and not isinstance(count,list)):
        fin_query += 'COUNT( DISTINCT '
    if (wanted == 'title'):
        fin_query += 't.title '
    elif (wanted == 'actor' or wanted == 'person' or wanted == 'director'):
        fin_query += 'n.name '
    elif (wanted == 'cast'):
        fin_query += 'n.name, cn.name '
    elif (wanted == 'genre'  or wanted == 'plot' or wanted == 'country' or wanted == 'filming_loc' or wanted == 'languages'):
        fin_query += 'mi.info '
    elif (wanted == 'year'):
        fin_query += 't.production_year '
    elif (wanted == 'keyword'):
        fin_query += 'k.keyword '
    elif (wanted == 'character'):
        fin_query += 'cn.name '
    else:
        fin_query += 't.title, n.name, t.production_year '
        if (logfile):
            logfile.write('DBI: '+str(wanted)+' is unimpliment.\n')
        else: # Remove this block for final presentation
            print 'DBI: '+str(wanted)+' is unimpliment.'
    if (count and not isinstance(count,list)):
        fin_query += ') '

    fin_query += build_from(wanted, known) + build_where(wanted, known)
    if (known.has_key('sort')):
        sortby = known.get('sort')
        if (sortby == 'title'):
            fin_query += 'ORDER BY t.title '
        elif (sortby == 'actor' or sortby == 'director' or sortby == 'person'):
            fin_query += 'ORDER BY n.name '
        elif (sortby == 'year'):
            fin_query += 'ORDER BY t.production_year '
        elif (sortby == 'keyword'):
            fin_query += 'ORDER BY k.keyword '
    if (count and isinstance(count,list)):
        count.sort()
        count.reverse()
        fin_query += ' LIMIT ' + str(count.pop()) + ',' + str(count.pop())
    else:
        fin_query += ' LIMIT 0,11'

    if (logfile):
        logfile.write('Executing: '+fin_query+'\n')
        logfile.flush()
    else:
        print 'Executing: '+fin_query+'\n'
    conn.query(fin_query)
    result = conn.store_result()
    res_list = result.fetch_row(result.num_rows())
    if (wanted != 'cast'):
        res_list = [item[0] for item in res_list]
    if (len(res_list)>10 and not count and not isinstance(count,list)):
        return query(wanted, known, 1)
    if (count and not isinstance(count, list)): # Returns int instead of [int]
        if (isinstance(res_list,dict)):
            return [item[0] for item in res_list].pop()
        return res_list.pop() 
    return res_list

# Get all films with a particular person.
# SELECT * FROM title t LEFT JOIN cast_info c ON (c.movie_id = t.id) LEFT JOIN name n ON (n.id = c.person_id) WHERE name="Family, Given" AND kind_id <> 7 LIMIT 0,100;

def build_from(wanted, know):
    from_list = 'FROM '
    # Looking for movie title
    if (wanted == 'title' or wanted == 'year'):
        from_list += 'title t ' # Covers the year with production_year
        if (know.has_key('actor') or know.has_key('person') or know.has_key('role') or know.has_key('director') or know.has_key('character')):
            actors = know.get('actor')
            people = know.get('person')
            direct = know.get('director')
            total_people = 0
            if (actors):
                if (isinstance(actors, list)):
                    total_people += len(actors)
                else:
                    total_people += 1
            if (direct):
                if (isinstance(direct, list)):
                    total_people += len(direct)
                else:
                    total_people += 1
            if (people):
                if (isinstance(people, list)):
                    total_people += len(people)
                else:
                    total_people += 1                                     
                    
            #len(know.has_key('actor')) + len(know.has_key('person')) + len(know.has_key('director'))
            from_list += 'LEFT JOIN cast_info c ON (c.movie_id = t.id) LEFT JOIN name n ON (n.id = c.person_id) '
            if (total_people > 1):
                for i in range (2, total_people + 1):
                    from_list += 'LEFT JOIN cast_info c' + str(i) + ' ON (c.movie_id = t.id) ' 
                    from_list += 'LEFT JOIN name n' + str(i) + ' ON (n' + str(i) 
                    from_list += '.id = c' + str(i) + '.person_id) '
                
            if (know.has_key('role') or know.has_key('director')):
                from_list += 'LEFT JOIN role_type rt ON (c.role_id = rt.id) '
            if (know.has_key('character')):
                from_list += 'LEFT JOIN char_name cn ON (c.person_role_id = cn.id) '
                
        if (know.has_key('genre')): # Must have WHERE clause mi.info_type_id = 3
            from_list += 'LEFT JOIN movie_info mi ON (t.id = mi.movie_id) ' 
        if (know.has_key('keyword')):
            from_list += 'LEFT JOIN movie_keyword mk ON (t.id = mk.movie_id) '
            from_list += 'LEFT JOIN keyword k ON (mk.keyword_id = k.id) '   
        
            
    # Looking for actor             #TODO: New FROM Statements for multiple titles.
    elif (wanted == 'actor' or wanted == 'person' or wanted=='director'):
        from_list += 'name n LEFT JOIN cast_info c ON (n.id = c.person_id) '
        if (know.has_key('title') or know.has_key('year') or know.has_key('role') or know.has_key('genre')):
            from_list += 'LEFT JOIN title t ON (c.movie_id = t.id) '
            if (know.has_key('genre')):
                from_list += 'LEFT JOIN movie_info mi ON (t.id = mi.movie_id) '
        if (know.has_key('role') or know.has_key('director')):
            from_list += 'LEFT JOIN role_type rt ON (c.role_id = rt.id) '
        if (know.has_key('character')):
            from_list += 'LEFT JOIN char_name cn ON (c.person_role_id = cn.id) '
            
            
            
    elif (wanted == 'genre'  or wanted == 'country' or wanted == 'filming_loc' or wanted == 'languages' or wanted == 'plot' or wanted == 'keyword'):
        from_list += 'title t LEFT JOIN movie_info mi ON (t.id = mi.movie_id) '
        if (know.has_key('person') or know.has_key('actor') or know.has_key('director')):
            from_list += 'LEFT JOIN cast_info c ON (c.movie_id = t.id) LEFT JOIN name n ON (n.id = c.person_id) '
        if (wanted == 'keyword' or know.has_key('keyword')):
            from_list += 'LEFT JOIN movie_keyword mk ON (t.id = mk.movie_id) '
            from_list += 'LEFT JOIN keyword k ON (mk.keyword_id = k.id) '
        if (know.has_key('genre')): # Must have WHERE clause mi.info_type_id = 3
            from_list += 'LEFT JOIN movie_info mi ON (t.id = mi.movie_id) ' 
    elif (wanted == 'cast'): # This is used for CAST query, but is a pretty good set for most queries that happen to fall through the cracks.
        from_list += 'title t LEFT JOIN cast_info c ON (c.movie_id = t.id) LEFT JOIN name n ON (c.person_id = n.id) '
        from_list += 'LEFT JOIN role_type rt ON (c.role_id = rt.id) '
        from_list += 'LEFT JOIN char_name cn ON (c.person_role_id = cn.id) '
        if (know.has_key('plot') or know.has_key('genre')):
            from_list += 'LEFT JOIN movie_info mi ON (c.movie_id = mi.movie_id) '
    elif (wanted == 'character'):
        from_list += 'FROM cast_info c LEFT JOIN char_name cn ON (c.person_role_id = cn.id) '
        if (know.has_key('title') or know.has_key('year')):
            from_list += 'LEFT JOIN title t ON (c.movie_id = t.id) '
        if (know.has_key('person') or know.has_key('actor') or know.has_key('director')):
            from_list += 'LEFT JOIN name n ON (c.person_id = n.id) '
            if (know.has_key('role') or know.has_key('director')):
                from_list += 'LEFT JOIN role_type rt ON (c.role_id = rt.id) '
    else:
        if (logfile):
            logfile.write('WARNING: DBi: Could not identify desired info: "'+ str(wanted) +'"\n')
            logfile.write('Making a generic guess... results could be slow as a result.\n')
        else:
            print 'WARNING: DBi: Could not identify desired info: "'+ str(wanted) +'"\n'
            print 'Making a generic guess... results could be slow as a result.\n'
        from_list += 'title t LEFT JOIN cast_info c ON (c.movie_id = t.id) LEFT JOIN name n ON (c.person_id = n.id) '
        from_list += 'LEFT JOIN role_type rt ON (c.role_id = rt.id) '
        from_list += 'LEFT JOIN char_name cn ON (c.person_role_id = cn.id) '
        from_list += 'LEFT JOIN movie_info mi ON (c.movie_id = mi.movie_id) '
        from_list += 'LEFT JOIN info_type it ON (mi.info_type_id = it.id) '
        from_list += 'LEFT JOIN movie_keyword mk ON (t.id = mk.movie_id) LEFT JOIN keyword k ON (mk.keyword_id = k.id)'
    return from_list

# possible movie attributes are: "title", "year", "plot", "director", "actor", "genre", "country", "filming_loc" "award" and "language"


def build_where(wanted, know):
    if (wanted == 'title'):
        if (know.has_key('expand')): # TODO: Check this is good keyword to use.
            where_list = 'WHERE t.kind_id <> 7 ' 
        else: # If expansion is off, only look at movie titles.
            where_list = 'WHERE t.kind_id = 1 '            
    elif (wanted == 'plot'):
        where_list = 'WHERE mi.info_type_id = 98 '
    elif (wanted == 'genre'):
        where_list = 'WHERE mi.info_type_id = 3 '
    elif (wanted == 'country'):
        where_list = 'WHERE mi.info_type_id = 8 '
    elif (wanted == 'filming_loc'):
        where_list = 'WHERE mi.info_type_id = 18 '
    elif (wanted == 'languages'):
        where_list = 'WHERE mi.info_type_id = 4 '
    elif (wanted == 'actor'):
        where_list = 'WHERE c.role_id < 3 '
    elif (wanted == 'director'):
        where_list = 'WHERE c.role_id = 8 '
    else:
        where_list = 'WHERE 1=1 '

    where_list += where_person(know) # Supports actor, director, and person 
    where_list += where_title(know)
    where_list += where_year(know)
    where_list += where_info(know)   # Supports genre, plot, country, filming_loc, and languages
    where_list += where_keyword(know) 
    where_list += where_character(know)

    return where_list

def where_title(know): #TODO: Insert new code
    titles = know.get('title')
    not_titles = know.get('!title')
    tw = '' # title where 
    if (titles):
        if (isinstance(titles, list)):
            first = 1
            tw += 'AND ( '
            for k in titles:
                if (first):
                    tw += 't.title = "' + k + '" '
                    first = 0
                else:
                    tw += 'OR t.title = "' + k + '" '
            
            tw += ' ) '
        else:
            tw += 'AND t.title = "' + titles + '" '
    if (not_titles):
        tw += 'AND t.id NOT IN ( SELECT t.id FROM title t WHERE t.title = '
        if (isinstance(not_titles, list)):
            tw += str(not_titles.pop()) + ' '
            for k in not_titles:
                tw += 'OR t.title = ' + k + ' '
        else:
            tw += not_titles + ' '
        tw += ') '
    if (tw == None):
        return ''
    return tw

def where_person(know): #TODO: Insert new code
    q = ''
    actor = know.get('actor')
    director = know.get('director')
    person = know.get('person')
    not_actor = know.get('!actor')
    not_director = know.get('!director')
    not_person = know.get('!person')
    
    # Positive cases: Desired query follows.
    # TODO: Make changes in build_from so this code gets used.
    # SELECT t.title 
    #FROM cast_info c LEFT JOIN title t ON (c.movie_id = t.id) LEFT JOIN name n ON (c.person_id = n.id),
    #cast_info c2 LEFT JOIN name n2 ON (c2.person_id = n2.id)
    #WHERE n.name = "Tilly, Jennifer" AND n2.name = "Gershon, Gina" AND kind_id = 1 AND c1.movie_id = c2.movie_id
    
    idx = 0 # Index of which person we are on.
    if (actor):
        if (isinstance(actor,list)): # TODO: Add support for this in build_from AND check roll.
            for a in actor:
                idx += 1
                if (idx == 1):
                    q += 'AND n.name = "' + family_first(a) + '" '
                else:
                    q += 'AND n' + str(idx) + '.name = "' + family_first(a) + '" '
        else:
            q += 'AND n.name = "' + family_first(actor) + '" '
        q += 'AND c.role_id < 3 '
    if (person):
        if (isinstance(person,list)): # TODO: Add support for this in build_from AND check roll.
            for p in person:
                idx += 1
                if (idx == 1):
                    q += 'AND n.name = "' + family_first(p) + '" '
                else:
                    q += 'AND n' + str(idx) + '.name = "' + family_first(p) + '" '
        else:
            q += 'AND n.name = "' + family_first(person) + '" '
    if (director):
        if (isinstance(director,list)): # TODO: Add support for this in build_from AND check roll.
            for d in director:
                idx += 1
                if (idx == 1):
                    q += 'AND n.name = "' + family_first(d) + '" '
                else:
                    q += 'AND n' + str(idx) + '.name = "' + family_first(d) + '" '
        else:
            q += 'AND n.name = "' + family_first(director) + '" '
            q += 'AND c.role_id = 8 ' # Enforce that they directed.
    
    if (idx > 1):
        q += 'AND c.movie_id = c2.movie_id '
        if (idx > 2):
            for i in range(2,idx+1): 
                q += 'AND c.movie_id = c' + str(i) + '.movie_id '
        
    # Negative cases

    if (not_actor): 
        q += 'AND t.id NOT IN ( '  
        q += '  SELECT DISTINCT c.movie_id FROM cast_info c LEFT JOIN name n ON (c.person_id = n.id) '
        q += '  WHERE n.name = "'
        if (isinstance(not_actor, list)):
            q += str(not_actor.pop()) + '" '
            for na in not_actor:
                 q += 'OR n.name = ' + na +' '
        else:
            q += str(not_actor) + '" '
        q += 'AND c.role_id < 3 ) ' 
    if (not_director): 
        q += 'AND t.id NOT IN ( '  
        q += '  SELECT DISTINCT c.movie_id FROM cast_info c LEFT JOIN name n ON (c.person_id = n.id) '
        q += '  WHERE n.name = "'        
        if (isinstance(not_director, list)):
            q += str(not_director.pop()) + '" '
            for nd in not_director:
                 q += 'OR n.name = ' + nd +' '
        else:
            q += str(not_actor) + '" '
        q += 'AND c.role_id = 8 ) '
    if (not_person): 
        q += 'AND t.id NOT IN ( '  
        q += '  SELECT DISTINCT c.movie_id FROM cast_info c LEFT JOIN name n ON (c.person_id = n.id) '
        q += '  WHERE n.name = "'        
        if (isinstance(not_person, list)):
            q += str(not_person.pop()) + '" '
            for np in not_person:
                 q += 'OR n.name = ' + np +' '
        else:
            q += str(not_actor) + '" ) '
    if (q == None):
        return ''
    return q

def where_year(know):
    year = know.get('year')
    not_year = know.get('!year')
    ret = ''
    if (year):
        if (isinstance(year,list)):
            ret += 'AND t.production_year = "' + str(year.pop()) + '" ' 
            for y in year:
                ret += 'OR t.production_year = "'+y+'" '
        else:
            ret += 'AND t.production_year = "'+year+'" '
    if (not_year):
        if (isinstance(not_year, list)):
            ret += 'AND NOT ( t.production_year = "' + str(year.pop()) + '" ' 
            for y in year:
                ret += 'OR t.production_year = "'+y+'" '
            ret += ') '
        else:
            ret += 'AND NOT t.production_year = "'+year+'" ' 
    if (ret == None):
        return ''
    return ret

def where_info(know): # Handles Genre, Plot, Country, Filming Location, and Languages. 
    # TODO: Put in new query code. Merge genres on items within type on OR, between type AND
    ele = []
    genre = know.get('genre')
    country = know.get('country')
    languages = know.get('languages')
    film_loc = know.get('filming_loc')
    
    if(genre):
        if (isinstance(genre, list)):
            ele += genre
        else:
            ele += [genre]
    if(country):
        if (isinstance(country, list)):
            ele += country
        else:
            ele += [country]
    if(languages):
        if (isinstance(languages, list)):
            ele += languages
        else:
            ele += [languages]
    if(film_loc):
        if (isinstance(film_loc, list)):   
            ele += film_loc
        else:
            ele += [film_loc]
    ret = ''
    if (isinstance(ele,list)): 
        for k in ele:
            ret += 'AND mi.info = "'+k+'" '
    else:
        ret += 'AND mi.info = "'+ele+'" '
    ele = []
    if(know.get('!genre')):
        ele += know.get('!genre')
    if(know.get('!country')):
        ele += know.get('!country')
    if(know.get('!languages')):
        ele += know.get('!languages')
    if(know.get('!filming_loc')):
        ele += know.get('!filming_loc')
        
    if (isinstance(ele,list)): 
        for k in ele:
            ret += 'AND NOT mi.info = "'+k+'" '
    else:
        ret += 'AND NOT mi.info = "'+ele+'" '
    if (ret == None):
        return ''
    return ret

# Assumes looking for title, but could work in other cases.         
def where_keyword(know): 
        ele = know.get('keyword')
        if (not ele):
            return ''
        where_list = ''
        first = 1
        if (isinstance(ele,list)): 
            for k in ele:
                if (first):
                    where_list += 'AND ( k.keyword = "'+k+'" '
                    first = 0
                else:
                    where_list += 'OR k.keyword = "'+k+'" '
            where_list += ') '
        else:
            where_list += 'AND k.keyword = "'+ele+'" '
        ele = know.get('!keyword')
        first = 1
        where_list += 'AND t.id NOT IN ( SELECT t.id FROM title t LEFT JOIN movie_keyword mk ON (t.id = mk.movie_id) LEFT JOIN keyword k ON (mk.keyword_id = k.id)  WHERE '
        if (isinstance(ele,list)): 
            for k in ele:
                if (first):
                    where_list += 'k.keyword = "'+k+'" '
                    first = 0
                else:
                    where_list += 'OR k.keyword = "'+k+'" '
        else:
            where_list += 'k.keyword = "'+ele+'" '
        where_list += ') '  
        if (where_list == None):
            return ''
        return where_list   
    
def where_character(know):
    chara = know.get('character')
    not_chara = know.get('!character')
    ret = ''
    if (chara):
        if (isinstance(chara,list)):
            ret += 'AND cn.name = "' + str(chara.pop()) + '" ' 
            for c in chara:
                ret += 'OR cn.name = "'+c+'" '
        else:
            ret += 'AND cn.name = "'+chara+'" '
    if (not_chara):
        first = 1
        ret += 'AND c.person_type_id NOT IN ( Snot_charaCT cn.id FROM char_name cn WHERE '
        if (isinstance(not_chara,list)): 
            for c in not_chara:
                if (first):
                    ret += 'cn.name = "'+c+'" '
                    first = 0
                else:
                    ret += 'OR cn.name = "'+c+'" '
        else:
            ret += 'cn.name = "'+not_chara+'" '
        ret += ') '  
    if (ret == None):
        return ''
    return ret   

# Find number of awards a person has recieved? Been niminated for? 
def awards(person):
    q = 'SELECT count(t.id) FROM cast_info c LEFT JOIN title t ON (c.movie_id = t.id) LEFT JOIN name n ON (c.person_id = n.id) '
    q += 'WHERE n.name="' + family_first(person) + '" AND t.title LIKE "%award%"'
    conn.query(q)
    result = conn.store_result()
    return result.pop()

# Find number of keywords in common between two movies.
def commonality(title1, title2):
    q = 'SELECT COUNT(keyword_id) - COUNT(DISTINCT keyword_id)'
    q += 'FROM title t LEFT JOIN movie_keyword mk ON (t.id = mk.movie_id) '
    q += 'WHERE title="'+title1+'" OR title="'+title2+'" LIMIT 0,1000'
    conn.query(q)
    result = conn.store_result()
    res_list = result.fetch_row(result.num_rows())
    res_list = [item[0] for item in res_list]
    if (res_list and isinstance(res_list,list)):
        return res_list.pop()
    return 0

def family_first(name):
    if (name.count(',')):
        return name
    return invert_name(name)
    
def given_first(name):
    if (name.count(',')):
        return invert_name(name)
    return name

# Take a name in the form Given1 Given2 GevenN FamilyName and return it as FamilyName, Given1 Given2 ...
def invert_name(s):
    if (s.count(',')):
        a=s.split(', ', 1)
    else:
        a=s.rsplit(' ', 1)
    a.reverse()
    return ', '.join(a)
  
# Naieve Name Spell-check. Pass in the name, and it will return a list with either the name, or a list of similar names.
def check_person(name):
    debug_spellcheck = False 
    if (name.count(' ')==0 or name == None or name == '' or len(name) < 3): # If this is an atomic name
        return [name] # TODO: Throw an exception.
    name = given_first(name)
    name_list = name.rsplit(' ', 1)
    family_name=name_list.pop()[:6]
    given_name =name_list.pop()[:4]
    name = invert_name(name)
    q = 'SELECT DISTINCT n.name FROM name n WHERE n.name = "' + str(name) + '" LIMIT 0,10'
    conn.query(q)
    result = conn.store_result()
    res_list = result.fetch_row(result.num_rows())
    res_list = [item[0] for item in res_list]
    failed = 0
    while (len(res_list)==0 and (failed < 2)):
        q = 'SELECT DISTINCT n.name FROM name n WHERE n.name LIKE "'
        q += family_name + '%, ' + given_name + '%" LIMIT 0,10'
        conn.query(q)
        result = conn.store_result()
        res_list = result.fetch_row(result.num_rows())
        res_list = [item[0] for item in res_list]

        if (debug_spellcheck):
            print 'Name: ' + family_name + ', ' + given_name + '\n'
            print 'Query: ' + q + '\n'
            print 'Results: ' + str(len(res_list)) + '\n'

        family_name = family_name[:-1]
        if (len(given_name) > 2):
            given_name = given_name[:-1]
        elif (len(given_name) == 2):
            given_name = given_name[:-1]
        if (len(family_name) < 4 or (len(family_name) < 5 and failed)): # Try an alternative method
            failed += 1
            name_list = name.rsplit(' ', 1)
            family_name = name_list.pop()[:9]
            family_name = family_name[:1]+'__'+family_name[3:]
            given_name = name_list.pop()[:6]
            given_name = given_name[:1]+'__'+given_name[3:]


    #Sort by word distance comparison here, if there is time.
    return res_list


