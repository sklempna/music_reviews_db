import metalde
import mysqltools
from log_tools import Logger

#mysqltools.remove_reviews_db()

try:
    mysqltools.create_reviews_db()
except:
    print('database already exists')

parser = metalde.MetaldeParser()
L = Logger()

review_links = parser.get_links_to_reviews(1)
last_review = L.get_last_review()

new_reviews = []
for review in review_links:
    if review != last_review:
        new_reviews.append(review)
    else:
        break

if len(new_reviews) == 0:
    L.log('no new reviews discovered')
else:
    L.set_last_review(new_reviews[0])

for review in new_reviews:
    print('reading review '+ review)
    try:
        review_data = parser.parse_review(review)
        mysqltools.insert_review_in_db(review_data)
        L.log('parsed review '+ review)
    except:
        L.log('Error parsing '+ review)
    
