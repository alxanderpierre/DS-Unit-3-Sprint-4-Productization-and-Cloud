from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import requests
import openaq
import seaborn
import matplotlib
import json
import openaq

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(app)


@app.route('/')
def root():
    """Base view."""
    return 'Hello'


@app.route('/openaq')
def openaq_data():
    api = openaq.OpenAQ()
    status, body = api.cities()
    return body


@app.route('/la')
def la_air_q():
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    return body


@app.route('/date')
def date():
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    a = []
    response = body['results']
    for i in response:
        x = response[0]
        d = str(i['date']['utc'])
        v = str(i['value'])
        a.append(d + ', '  + v)
    return ', '.join(a)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)


def __repr__(self):
    return "< Record {} >".format(self.name)


@app.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    return "Database Reset Success"


@app.route('/enterdata')
def fill_db():
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    response = body['results']
    DB.session.add(Record(datetime='data', id='city', value='value'))
    DB.session.commit()
    return 'Data refreshed!'


if __name__ == '__main__':
    app.run()
