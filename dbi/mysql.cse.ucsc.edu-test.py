#
# This file tests access to the MySQL IMDb database at mysql.cse.ucsc.edu
#

import imdb

i = imdb.IMDb('sql', uri='mysql://maw_imdb:pugOrz2u@mysql.cse.ucsc.edu/maw_imdb')

results = i.search_movie('the big lebowski')
for x in results: print x

