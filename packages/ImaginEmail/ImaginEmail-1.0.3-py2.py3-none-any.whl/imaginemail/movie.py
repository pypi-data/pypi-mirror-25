import os

import click

from .connection import Connection
from .notification import EmailNotification
from .tmdb import TMDBInfo


class Movie:
    def __init__(self, title, image, info, purchase_info, purchase_link):
        self.title = title
        self.image = image
        self.info = info
        self.purchase_info = purchase_info
        self.purchase_link = purchase_link

        self.db_name = os.environ.get('DB_NAME')

    def register_movie(self):
        click.echo('Registering movie "%s" on database.' % self.title)
        with Connection(self.db_name) as conn:
            conn.insert_movie(self)

    def _get_tmdb_info(self):
        info = TMDBInfo(title=self.title)

        self.title = info.get_title()
        self.overview = info.get_overview()
        self.image = info.get_image()

    @staticmethod
    def exists_movie(movie_title):
        with Connection(os.environ.get('DB_NAME')) as conn:
            if conn.movie_exists(movie_title):
                return True
        return False

    @staticmethod
    def notify_to_email(to_email):
        movies = []
        with Connection(os.environ.get('DB_NAME')) as conn:
            query = conn.get_not_notified_movies()
            for row in query:
                m = Movie(row[1], row[2], row[3], row[4], row[5])
                movies.append(m)

        en = EmailNotification()

        en.send_email(to_email, movies)
