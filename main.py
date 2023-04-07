from tmdb.tmdb import TMDb

#tmdb = TMDb()

#import pprint
#with open("log.txt", "w", encoding="utf-8") as f:
    #tv, seasons, episodes = tmdb.get_tv(1399)
    #pprint.pprint(tmdb.get_images([element['image_path'] for element in [tv] + seasons + episodes]))
    #pprint.pprint(tmdb.get_tv(1399), f)
    #pprint.pprint(tmdb.get_movie(550), f)
    #pprint.pprint(tmdb.search('thrones'), f)

from db.db import DB

db = DB('database.json')

ret1 = db.query('SELECT * FROM tmdb.movie;')
ret2 = db.query('SELECT * FROM tmdb.tv;')
print(ret1, ret2)
