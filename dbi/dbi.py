import nltk
import MySQLdb
import imdb
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
i =  imdb.IMDb('sql', uri='mysql://%s:%s@%s:3306/%s'%(user_name,password,host,db_name))
conn = MySQLdb.connect (host = host, user = user_name, db = db_name, passwd = password)
#logfile = open('dbi.log', 'w')
logfile = 0

## select/cout object: all movie attributes
# conditions: all movie attributes, "keyword", "sort" (with the value of some movie attribute), "order" ("desc" or "asc")
# possible movie attributes are: "title", "year", "plot", "director", "actor", "genre", "country", "filming_loc" "award" and "language"
# TODO: award, gross
def query(wanted, known, count=False):
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
    fin_query = 'SELECT DISTINCT '

    if (count and not isinstance(count,list)):
        fin_query += 'COUNT( '
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
    if (wanted != 'cast' and wanted != 'keyword'):
        res_list = [item[0] for item in res_list]
    if (len(res_list)>10 and not count and not isinstance(count,list)):
        return query(wanted, known, 1) 
    if (count and not isinstance(count, list)): 
        return res_list.pop() # Returns int instead of [int]
    return res_list

# Get all films with a particular person.
# SELECT * FROM title t LEFT JOIN cast_info c ON (c.movie_id = t.id) LEFT JOIN name n ON (n.id = c.person_id) WHERE name="Family, Given" AND kind_id <> 7 LIMIT 0,100;    

def build_from(wanted, know):
    from_list = 'FROM '
    # Looking for movie title
    if (wanted == 'title' or wanted == 'year'):
        from_list += 'title t ' # Covers the year with production_year
        if (know.has_key('actor') or know.has_key('person') or know.has_key('role') or know.has_key('director')):
            from_list += 'LEFT JOIN cast_info c ON (c.movie_id = t.id) LEFT JOIN name n ON (n.id = c.person_id) '
            if (know.has_key('role') or know.has_key('director')):
                from_list += 'LEFT JOIN role_type rt ON (c.role_id = rt.id) '
        if (know.has_key('genre')): # Must have WHERE clause mi.info_type_id = 3
            from_list += 'LEFT JOIN movie_info mi ON (t.id = mi.movie_id) ' 
        if (wanted == 'keyword' or know.has_key('keyword')):
            from_list += 'LEFT JOIN movie_keyword mk ON (t.id = mk.movie_id) '
            from_list += 'LEFT JOIN keyword k ON (mk.keyword_id = k.id) '
    # Looking for actor
    elif (wanted == 'actor' or wanted == 'person' or wanted=='director'):
        from_list += 'name n LEFT JOIN cast_info c ON (n.id = c.person_id) '
        if (know.has_key('title') or know.has_key('year') or know.has_key('role') or know.has_key('genre')):
            from_list += 'LEFT JOIN title t ON (c.movie_id = t.id) '
            if (know.has_key('genre')):
                from_list += 'LEFT JOIN movie_info mi ON (t.id = mi.movie_id) '
        if (know.has_key('role') or know.has_key('director')):
            from_list += 'LEFT JOIN role_type rt ON (c.role_id = rt.id) '
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
    # To add keyword, link cast_info, title, and movie_keyword by movie_id, and keyword.id=movie_keyword.keyword_id     
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
        where_list = 'WHERE t.kind_id <> 7 '
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
    # Looking for movie title
    for key in know.keys():
        if (key == 'actor' or key == 'director' or key == 'person'): # Needs testing
            act = know.get(key)
            if (isinstance(act,list)): # TODO: Really a more complex case. Must Re-write SQL.
                for a in act:
                    # Need to invert the name if it doesn't contain a , here
                    where_list += 'AND n.name = "'+munge_name(a)+'" '
            else:
                # And here
                where_list += 'AND n.name = "'+munge_name(act)+'" '
        if (key == 'title'): 
            ele = know.get(key)
            if (isinstance(ele,list)): 
                first = 1
                where_list += 'AND ( '
                for k in ele:
                    if (first):
                        where_list += 't.title = "'+k+ '" '
                        first = 0
                    else:
                        where_list += 'OR t.title = "'+k+ '" '
                where_list += ' ) '
            else:
                where_list += 'AND t.title = "'+ele+'" '
        if (key == 'year'): 
            ele = know.get(key)
            if (isinstance(ele,list)): 
                for k in ele:
                    where_list += 'AND t.production_year = "'+k+'" '
            else:
                where_list += 'AND t.production_year = "'+ele+'" '

        if (key == 'genre'  or key == 'plot' or key == 'country' or key == 'filming_loc' or key == 'languages'):
            ele = know.get(key)
            if (isinstance(ele,list)): 
                for k in ele:
                    where_list += 'AND mi.info = "'+k+'" '
            else:
                where_list += 'AND mi.info = "'+ele+'" '
            
        if (key == 'keyword'): 
            ele = know.get(key)
            first = 1
            if (isinstance(key,list)): 
                for k in ele:
                    if (first):
                        where_list += 'AND k.keyword = "'+k+'" '
                        first = 0
                    else:
                        where_list += 'OR k.keyword = "'+k+'" '
            else:
                where_list += 'AND k.keyword = "'+ele+'" '
        if (key == '!keyword'): # REALLY WEIRD CASE. May not play well with others.
            ele = know.get(key)
            first = 1
            where_list += 'AND t.id NOT IN ( SELECT t.id FROM title t LEFT JOIN movie_keyword mk ON (t.id = mk.movie_id) LEFT JOIN keyword k ON (mk.keyword_id = k.id)  WHERE '
            if (isinstance(act,list)): 
                for k in ele:
                    if (first):
                        where_list += 'k.keyword = "'+k+'" '
                        first = 0
                    else:
                        where_list += 'OR k.keyword = "'+k+'" '
            else:
                where_list += 'k.keyword = "'+ele+'" '
            where_list += ') '
    return where_list

def commonality(title1, title2):
    q = 'SELECT COUNT(keyword_id) - COUNT(DISTINCT keyword_id)'
    q += 'FROM title t LEFT JOIN movie_keyword mk ON (t.id = mk.movie_id) '
    q += 'WHERE title="'+title1+'" OR title="'+title2+'" LIMIT 0,1000'

    conn.query(fin_query)
    result = conn.store_result()
    
    # Process result here

    return result

def munge_name(s):
    a=s.rsplit(' ', 1)
    a.reverse()
    return ', '.join(a)
   
"""
Get list of genres for a movie.
SELECT mi.info FROM title t LEFT JOIN movie_info mi ON (mi.movie_id = t.id) WHERE t.kind_id = "1" AND mi.info_type_id = 3 AND t.title = "A Scanner Darkly" LIMIT 100

"""

def check_person(name):
    debug_spellcheck = True 
    name_list = name.rsplit(' ', 1)
    family_name=name_list.pop()[:6]
    given_name =name_list.pop()[:4]
    name = munge_name(name)
    q = 'SELECT DISTINCT n.name FROM name n WHERE n.name = "' + str(name) + '" LIMIT 0,10'
    conn.query(q)
    result = conn.store_result()
    res_list = result.fetch_row(result.num_rows())
    res_list = [item[0] for item in res_list]
    while (len(res_list)==0 and len(family_name) > 3):
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

        family_name = family_name[:-2]
        if (len(given_name) > 2):
            given_name = given_name[:-2]
        elif (len(given_name) == 2):
            given_name = given_name[:-1]



    #Put word distance comparison here.
    return res_list


