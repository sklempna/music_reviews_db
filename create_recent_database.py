import mysqltools

name = 'music_reviews_db_recent'

try:
    mysqltools.create_reviews_db(name)
except:
    print('database already exists')
    
