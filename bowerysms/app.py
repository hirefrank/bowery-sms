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
    resp = twilio.twiml.Response()
    if request.method == 'POST':
        message = request.form['Body'].strip().lower()

        if request.form['Body'].strip().lower() == 'subscribe':
            phone = request.form['From']
            user_exist = User.Query.all().filter(phone=phone).limit(1)
            if not user_exist:
                u = User.signup(phone,"",phone=phone)
                resp.message('You are now subscribed. Reply "STOP" to stop receiving updates.')
            else:
                resp.message('You already subscribed!')
        else:
            resp.message('Welcome to Bowery SMS. Text "Subscribe" receive daily workouts.')
        return str(resp)

