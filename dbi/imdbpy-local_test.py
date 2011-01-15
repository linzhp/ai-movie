#
# This file tests access to the local MySQL IMDb database
#

import imdb

i = imdb.IMDb('sql', uri='mysql://imdb@localhost/imdb')


print 'Searching for movie \'the big lebowski\''
results = i.search_movie('the big lebowski')
print results[0]


print 'Searching for actor \'samuel l. jackson\''
actor = i.search_person('samuel l. jackson')
print actor[0]


print 'Searching for movies with keyword \'apocalypse\''
kw = i.get_keyword('apocalypse')

for x in kw:
	print x 

print len(kw), 'results returned.'
raw_input("Press enter to continue")