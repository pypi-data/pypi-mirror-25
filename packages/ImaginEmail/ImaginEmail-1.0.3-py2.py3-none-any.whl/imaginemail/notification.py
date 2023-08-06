import os
import smtplib
from email.mime.text import MIMEText

import click
from jinja2 import Environment, FileSystemLoader

from .connection import Connection


class EmailNotification:
    def __init__(self, template_dir='templates'):
        if os.path.isdir(template_dir):
            self.template_dir = template_dir
        else:
            self.template_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), template_dir)
        self.env = Environment(loader=FileSystemLoader(self.template_dir))
        click.echo(self.template_dir)
        self.db_name = os.environ.get('DB_NAME')

    def _mail_render(self, data, template):
        template = template + ".html"
        text = self.env.get_template(template)
        msg = text.render(data)
        return msg

    def send_email(self, email_to, movies):
        if len(movies) == 0:
            click.echo('No new movies to notify.')
            return

        click.echo('Sending email to: %s.' % email_to)
        msg_str = self._mail_render({'movies': movies}, 'template')

        msg = MIMEText(msg_str, 'html')
        server = smtplib.SMTP('smtp.gmail.com', 587)

        msg['Subject'] = "Nuevo preestreno con ImaginBank"
        msg['From'] = os.environ.get('EMAIL')
        msg['To'] = email_to

        server.starttls()
        server.login(os.environ.get('EMAIL'), os.environ.get('EMAIL_PASSWORD'))
        server.send_message(msg)
        for movie in movies:
            click.echo('Send email with new movie "%s".' % movie.title)
            self._update_sent_email(movie)
        server.quit()

    def _update_sent_email(self, movie):
        with Connection(self.db_name) as conn:
            conn.email_sent(movie)
