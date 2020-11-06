import metalde
import mysqltools
from log_tools import Logger

parser = metalde.MetaldeParser()
L = Logger()
last_review = L.get_last_review()

review_links = []
page_nums = parser.get_review_page_nums()
for i in range(page_nums):
    print('reading page '+str(i))
    review_links += parser.get_links_to_reviews(i+1)
    if last_review in review_links:
        break


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
        mysqltools.insert_review_in_db(review_data, name='music_reviews_db_recent')
        L.log('parsed review '+ review)
    except:
        L.log('Error parsing '+ review)
    
