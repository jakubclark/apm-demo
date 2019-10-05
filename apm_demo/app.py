import logging
import json
from random import choice
from time import sleep

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from ddtrace import tracer
from redis import StrictRedis
from requests import Session

log = logging.getLogger(__name__)

http_client = Session()
redis_client = StrictRedis(host="127.0.0.1", port=6379)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_private_db.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
def index():
    return ('Welcome to the Datadog APM Demo Application!'
            'Consider hitting one of the following endpoints:\n'
            '\n'.join(['/sql', '/redis', '/http', '/all'])
            )


@app.route('/sql')
def sql_endpoint():
    return get_sql_data()


@app.route('/redis')
def redis_endpoint():
    return get_redis_data()


@app.route('/http')
def http_endpoint():
    return get_http_data()


@app.route('/all')
def all_endpoint():
    status = choice([200, 400, 500])
    return str(
        (
            get_redis_data(),
            get_sql_data(),
            get_http_data()
        )
    ), status


def get_sql_data():
    return User.query.all()


def get_redis_data():
    return redis_client.get('randomnumber')


@tracer.wrap(name='expensive_http_call', service='http_backend')
def get_http_data():
    status = choice([200, 400, 500])
    url = f'https://httpbin.org/status/{status}'
    res = http_client.get(url)
    res.raise_for_status()
    return res.text
