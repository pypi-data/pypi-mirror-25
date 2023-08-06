import sqlite3


class Connection:
    def __init__(self, db_file):
        self.db = sqlite3.connect(db_file)
        self.cursor = self.db.cursor()
        self.create_movies_table()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.commit()
        self.db.close()

    def create_movies_table(self):
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS movies(id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                                 title TEXT UNIQUE,
                                                 image TEXT,
                                                 info TEXT,
                                                 purchase_info TEXT,
                                                 purchase_link TEXT,
                                                 email_sent BOOLEAN)''')

    def insert_movie(self, movie):
        t = (None, movie.title, movie.image, movie.info, movie.purchase_info, movie.purchase_link, 'False',)
        if not self.movie_exists(movie.title):
            self.cursor.execute('''INSERT INTO movies VALUES (?,?,?,?,?,?,?)''', t)

    def movie_exists(self, movie_title):
        title_tuple = (movie_title,)
        query_answer = self.cursor.execute("SELECT count(*) FROM movies WHERE title=?", title_tuple)
        result = query_answer.fetchone()
        if result[0] == 0:
            return False
        return True

    def email_sent(self, movie):
        title_tuple = (movie.title,)
        self.cursor.execute("UPDATE movies SET email_sent='True' WHERE title=?", title_tuple)

    def get_not_notified_movies(self):
        return self.cursor.execute("SELECT * FROM movies WHERE email_sent='False' AND purchase_info NOT NULL")
