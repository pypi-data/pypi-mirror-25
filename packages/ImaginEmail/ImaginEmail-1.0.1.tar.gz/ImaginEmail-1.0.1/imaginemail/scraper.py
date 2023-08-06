import re

import click
import requests
from bs4 import BeautifulSoup

from .movie import Movie


class Scraper:
    BASE_URL = 'https://www.imaginbank.com'
    movies = []

    def check_and_save_new_movies(self):
        soup = self.get_soup_from_web('/descuentos/experiencias_es.html')

        for discount in soup.find_all("li", class_="descuento"):
            if not self.exists_movie(discount):
                detail_view = self.get_detail_view(discount)
                self.compose_and_save_movie(detail_view)

    @staticmethod
    def exists_movie(discount: BeautifulSoup):
        title_str = discount.find(class_="informacion-top").h2.text
        return Movie.exists_movie(title_str)

    def compose_and_save_movie(self, detail_view: BeautifulSoup):
        image_str = str(self.BASE_URL + detail_view.find(class_="imagen-descuento").img.get('src'))
        title_str = str(detail_view.find(class_="informacion-top").h1.text)

        event_info = detail_view.find(class_="informacion-bottom")
        event_info.p['class'] = 'lead'

        info_str = str(event_info.p)

        madrid_info = detail_view.find(class_="popup_informacion").find(string=re.compile("Madrid"))

        if not madrid_info:
            purchase_info_str = None
            purchase_link_str = None
        else:
            purchase_info_str = str(madrid_info.next_element)
            purchase_info_str = ' '.join(purchase_info_str.replace('\n\r', '').split())
            purchase_link_str = str(madrid_info.find_next('a').get('href'))

        movie = Movie(title_str, image_str, info_str, purchase_info_str, purchase_link_str)
        movie.register_movie()

    def get_detail_view(self, discount):
        detail_url = discount.find(title='Ir a la oferta').get('href')
        return self.get_soup_from_web(detail_url)

    def get_soup_from_web(self, web):
        click.echo('Parsing web: "%s".' % (self.BASE_URL + web))
        resp = requests.get(self.BASE_URL + web)
        if resp.ok:
            resp.encoding = 'utf-8'
            return BeautifulSoup(resp.text, 'html.parser')
        else:
            click.echo('Error parsing web.')
            raise Exception('Error {code}: {msg}'.format(code=resp.status_code, msg=resp.text))
