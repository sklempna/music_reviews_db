import mysql.connector

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
            publish_date DATE
        )
    """
    cursor.execute(tb_create_str)
    cursor.execute('DESCRIBE metalde')
    for x in cursor:
        print(x)

def remove_reviews_db():
    """
    Remove metal_reviews_db database from server.
    """
    db = mysql.connector.connect(host=host, user=user)
    cursor = db.cursor()
    cursor.execute('DROP DATABASE metal_reviews_db')

    

if __name__ == "__main__":
    create_reviews_db()
    remove_reviews_db()
    

