import bs4
from bs4 import BeautifulSoup
import urllib.request

reviews = 'https://www.metal.de/reviews'

class MetaldeParser():
    """
    A html-parser for metal.de
    """
    def get_html_page(self, url):
        """
        Opens a given url.

        Returns: A BeautifulSoup object of the given page.
        """
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        return BeautifulSoup(response.read(), 'html.parser')
 
    def __init__(self):
        pass

    def text_filter(self, text):
        return lambda t: t.text == text

    def filter(self, attr, val):
        """
        Returns a filter function that can be passed to the find_all
        function of Beautiful Soup.

        The function matches html tags, which have an attribute
        attr with value val.
        """
        return lambda t: t.has_attr(attr) and t[attr] == val


    def get_review_page_nums(self):
        """
        Counts the number of pages containing links to reviews.
        """
        soup = self.get_html_page(reviews)
        tags = soup.find_all(self.filter('class', ['page-numbers']))
        return int(tags[-1].text.replace('.',''))

    def get_links_to_reviews(self, page_num):
        """
        Returns a list of links to all the reviews contained on a page.
        """
        soup = self.get_html_page(reviews+'/page/'+str(page_num))
        tags = soup.find_all(self.filter('data-category', 'Rubrik Reviews'))
        return [tag['href'] for tag in tags]

    # todo: check parsing of comment text
    def parse_comments(self, url):
        """
        Parses the comments on a metal.de page

        Parameters:
        - url : url of the metal.de page

        Returns:
        - A list of dictionaries, each corresponding to a comment. Dicts 
        contain keys 'date', 'author' and 'text' 
        """
        comment_list = []
        soup = self.get_html_page(url)
        com_tag = soup.find(self.filter('class', ['comment-list']))
        com_li = [tag for tag in com_tag.children if type(tag) == bs4.element.Tag]
        
        for i in range(len(com_li)):
            comment = {}
            date = com_li[i].find(self.filter('class',['comment-meta', 'commentmetadata'])).text
            date = ''.join([i if (ord(i)< 123 and ord(i) > 31) else '' for i in date])
            comment['date'] = date
            text = com_li[i].find('p').text
            comment['text'] = text
            author = com_li[i].find(self.filter('class', ['fn'])).text
            comment['author'] = author
            comment_list.append(comment)
        return comment_list

    # wip
    def parse_review(self, url):
        data = {}
        soup = self.get_html_page(url)
        publish_date = soup.find(self.filter('class',['date']))
        if publish_date:
            data['publish_date'] = publish_date.text
        else:
            data['publish_date'] = '-'
        author = soup.find(self.filter('itemprop', 'author'))
        if author:
            data['author'] = author.text
        else:
            data['author'] = '-'
        item = soup.find(self.filter('itemprop','itemReviewed'))
        if item:
            data['item'] = item.text
        else:
            data['item'] = '-'
        rating = soup.find(self.filter('itemprop','ratingValue'))
        if rating:
            data['rating'] = rating.text
        else:
            data['rating'] = '-'
        genre_tag = soup.find(self.text_filter('Stile'))
        if genre_tag:
            genre_tag = genre_tag.next_sibling
            genres = [tag.text for tag in genre_tag.find_all('a')]
            data['genres'] = genres
        else:
            data['genres'] = []
        pre_num_songs = soup.find(self.text_filter('Anzahl Songs'))
        num_songs = pre_num_songs.next_sibling.text
        data['num_songs'] = num_songs
        pre_duration = soup.find(self.text_filter('Spieldauer'))
        duration = pre_duration.next_sibling.text
        data['duration'] = duration
        pre_release_date = soup.find(self.text_filter('Release'))
        release_date = pre_release_date.next_sibling.text
        data['release_date'] = release_date
        pre_label = soup.find(self.text_filter('Label'))
        label = pre_label.next_sibling.text
        data['label'] = label
        comments = self.parse_comments(url)
        data['comments'] = comments 
        
        return data

        

    
if __name__ == '__main__':
    parser = MetaldeParser()
    data = parser.parse_review('https://www.metal.de/reviews/moetley-cruee-the-dirt-soundtrack-371224/')
    print(data)
    