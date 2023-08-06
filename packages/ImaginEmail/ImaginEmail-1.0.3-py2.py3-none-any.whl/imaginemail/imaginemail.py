import click

from .movie import Movie
from .scraper import Scraper


@click.group()
@click.version_option()
def cli():
    """ImaginEmail looks up for new films in the imaginbank webpage and registers them in a DB.
    After that, you can also notify a specific email if you want."""
    pass


@cli.command('notify', short_help='Notify an email.')
@click.option('--email', default='daniseijo12@gmail.com',
              help='The email that will receive the notification.')
def notify(email):
    """This script sends an email with new movies to an account provided."""
    Movie.notify_to_email(email)


@cli.command('check_web', short_help='Check for new movies.')
def check_web():
    """Check for new movies in the imaginbank web"""
    scraper = Scraper()
    scraper.check_and_save_new_movies()
