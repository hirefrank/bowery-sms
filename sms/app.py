#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from settings_local import *
except ImportError as e:
    from settings import *

import sys
import twilio.twiml

from parse_rest.connection import register
from parse_rest.datatypes import Object
#from parse_rest.user import User
register(PARSE['APPLICATION_ID'], PARSE['REST_API_KEY'])

from flask import Flask, request, redirect
app = Flask(__name__)

class Subscriber(Object):
    pass

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
        subscriber_exist = Subscriber.Query.all().filter(phone=phone).limit(1)

        if message == 'subscribe':
            if subscriber_exist.count() == 0:
                subscriber = Subscriber(phone=phone)
                subscriber.save()
                reply = 'You are now subscribed. Reply "Stop" to stop receiving updates.'
            else:
                reply = 'You already subscribed!'

        elif message == 'stop':
            subscriber.delete()
            reply = 'You\'ve unsubscribed.'

        print 'From: ', phone
        print 'Message: ', message
        print 'Response: ', reply

        #resp = twilio.twiml.Response()
        #resp.message(reply)
        #return str(resp)
