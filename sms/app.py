#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from settings_local import *
except ImportError as e:
    from settings import *

import twilio.twiml

from parse_rest.connection import register
from parse_rest.user import User
register(PARSE['APPLICATION_ID'], PARSE['REST_API_KEY'])

from flask import Flask, request, redirect
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route("/sms", methods=['GET', 'POST'])
def sms():
    if request.method == 'POST':
        # default reply
        reply = 'Welcome to Bowery SMS. Text "Subscribe" to receive daily workouts.'
        message = request.form['Body'].strip().lower()
        phone = request.form['From']

        resp = twilio.twiml.Response()
        resp.message(reply)
        return str(resp)