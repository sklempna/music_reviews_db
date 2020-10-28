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

reviews = []
page_nums = parser.get_review_page_nums()
for i in range(page_nums):
    reviews.append(parser.get_links_to_reviews(i+1))

L.log(str(len(reviews))+' reviews discovered')
if len(reviews) != 0:
    L.set_last_review(reviews[0])

for review in reviews:
    print('reading review '+ review)
    try:
        review_data = parser.parse_review(review)
        mysqltools.insert_review_in_db(review_data)
        L.log('parsed review '+ review)
    except:
        L.log('Error parsing '+ review)
    
