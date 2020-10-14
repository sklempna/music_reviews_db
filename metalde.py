import bs4
from bs4 import BeautifulSoup
import urllib

reviews = 'https://www.metal.de/reviews'

"""
A html-parser for metal.de
"""
class MetaldeParser():
    """
    Opens a given url.

    Returns: A BeautifulSoup object of the given page.
    """
    def get_html_page(self, url):
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        return BeautifulSoup(response.read(), 'html.parser')
 
    def __init__(self):
        pass

    
    """
    Returns a filter function that can be passed to the find_all
    function of Beautiful Soup.

    The function matches html tags, which have an attribute
    attr with value val.
    """
    def filter(self, attr, val):
        return lambda t: t.has_attr(attr) and t[attr] == val


    """
    Counts the number of pages containing links to reviews.
    """
    def get_review_page_nums(self):
        soup = self.get_html_page(reviews)
        tags = soup.find_all(self.filter('class', ['page-numbers']))
        return int(tags[-1].text.replace('.',''))

    """
    Returns a list of links to all the reviews contained on a page.
    """
    def get_links_to_reviews(self, page_num):
        soup = self.get_html_page(reviews+'/page/'+str(page_num))
        tags = soup.find_all(self.filter('data-category', 'Rubrik Reviews'))
        return [tag['href'] for tag in tags]

    # wip 
    def parse_comments(self, url):
        comment_list = []
        soup = self.get_html_page(url)
        com_tag = soup.find(self.filter('class', ['comment-list']))
        com_li = [tag for tag in com_tag.children if type(tag) == bs4.element.Tag]
        return com_li

    # wip
    def parse_review(self, url):
        data = {}
        soup = self.get_html_page(url)
        publish_date = soup.find(self.filter('class',['date'])).text
        data['publish_date'] = publish_date
        author = soup.find(self.filter('itemprop', 'author')).text
        data['author'] = author
        item = soup.find(self.filter('itemprop','itemReviewed')).text
        data['item'] = item
        rating = int(soup.find(self.filter('itemprop','ratingValue')).text)
        data['rating'] = rating
        return data

        

    
if __name__ == '__main__':
    parser = MetaldeParser()
    data = parser.parse_comments('https://www.metal.de/specials/666-antifaschistische-black-metal-bands-409505/')
    print(len(data))
    