import mysql.connector
import metalde

user = 'pi_db'
host = 'localhost'

def convert_date(date_str):
    """
    Convert a date_str in the format 'DD.MM.YYYY' into mysql
    format 'YYYY-MM-DD'.
    """
    date_li = date_str.split('.')
    return '-'.join(reversed(date_li))

def create_reviews_db():
    """
    Creates a database 'metal_reviews_db' with an empty table 
    'metalde'.
    """
    db = mysql.connector.connect(host=host, user=user)
    cursor = db.cursor()
    db_create_str = "CREATE DATABASE IF NOT EXISTS metal_reviews_db"
    cursor.execute(db_create_str)
    cursor.execute('USE metal_reviews_db')
    tb_create_str = """
        CREATE TABLE IF NOT EXISTS metalde (
            text MEDIUMTEXT,
            publish_date DATE,
            author VARCHAR(255),
            item VARCHAR(255),
            rating SMALLINT,
            genres VARCHAR(255),
            num_songs SMALLINT,
            duration VARCHAR(255),
            release_date DATE,
            label VARCHAR(255),
            comments MEDIUMTEXT
        )
    """
    cursor.execute(tb_create_str)
    #cursor.execute('DESCRIBE metalde')
    #for x in cursor:
    #    print(x)

def remove_reviews_db():
    """
    Remove metal_reviews_db database from server.
    """
    db = mysql.connector.connect(host=host, user=user)
    cursor = db.cursor()
    cursor.execute('DROP DATABASE metal_reviews_db')

def insert_review_in_db(review):
    db = mysql.connector.connect(host=host, user=user, database='metal_reviews_db')
    cursor = db.cursor()
    text = review['text']
    publish_date = convert_date(review['publish_date'])
    author = review['author']
    item = review['item']
    if review['rating'].isdigit():
        rating = int(review['rating'])
    else:
        rating = 'NULL'
    genres = ', '.join(review['genres'])
    if review['num_songs'].isdigit():
        num_songs = int(review['num_songs'])
    else:
        num_songs = 'NULL'
    duration = review['duration']
    release_date = convert_date(review['release_date'])
    label = review['label']
    if review['comments'] == []:
        comments = 'NULL'
    else:
        comments = '"' + str(review['comments']) + '"'

    command_str = """INSERT INTO metalde (
            text, 
            publish_date, 
            author, 
            item, 
            rating, 
            genres, 
            num_songs, 
            duration, 
            release_date, 
            label, 
            comments
        ) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})""".format(
            '"' + text + '"', 
            '"' + publish_date + '"', 
            '"' + author + '"', 
            '"' + item + '"', 
            rating, 
            '"' + genres + '"', 
            num_songs, 
            '"' + duration + '"', 
            '"' + release_date + '"', 
            '"' + label + '"', 
            comments
        )

    cursor.execute(command_str)
    db.commit()


    

if __name__ == "__main__":
    remove_reviews_db()
    create_reviews_db()

    parser = metalde.MetaldeParser()
    review_list = parser.get_links_to_reviews(1)[:5]
    for review_page in review_list:
        review = parser.parse_review(review_page)
        insert_review_in_db(review)

    #review = parser.parse_review('https://www.metal.de/reviews/moetley-cruee-the-dirt-soundtrack-371224/')
    #insert_review_in_db(review)
    #print(data)
    #remove_reviews_db()
    

