import metalde
import time
from log_tools import Logger


filename = 'review_links.txt'
parser = metalde.MetaldeParser()
L = Logger()

reviews = []
page_nums = parser.get_review_page_nums()
for i in range(page_nums):
    while True:
        print('reading page '+str(i+1))
        new_reviews = parser.get_links_to_reviews(i+1)
        #time.sleep(0.5)
        if new_reviews:
            break
    reviews += new_reviews

L.log(str(len(reviews))+' reviews discovered')
if len(reviews) != 0:
    L.set_last_review(reviews[0])

f = open(filename, 'a')
for review in reviews:
   f.write(review+'\n') 
f.close()
