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
register(PARSE['APPLICATION_ID'], PARSE['REST_API_KEY'])

from flask import Flask, request, redirect
app = Flask(__name__)

class Subscriber(Object):
    pass

@app.route('/')
def hello_world():
    return 'Hello World!'

# All Twilio routing should be sent to /sms
@app.route("/sms", methods=['GET', 'POST'])
def sms():
    # Only continue if a POST request
    if request.method == 'POST':
        # Default reply message
        reply = 'Welcome to Bowery SMS. Text "Subscribe" to receive daily workouts.'

        # Remove whitespace, lowecase the inbound message
        message = request.form['Body'].strip().lower()
        # Sender's phone number. Save for later.
        phone = request.form['From']
        # Is the user a subscriber?
        subscriber_exist = Subscriber.Query.all().filter(phone=phone).limit(1)

        if message == 'subscribe':
            # If not, subscribe them
            if subscriber_exist.count() == 0:
                subscriber = Subscriber(phone=phone)
                subscriber.save()
                reply = 'You are now subscribed. Reply "Stop" to stop receiving updates.'
            else:
                # They already exist
                reply = 'You already subscribed!'

        # Todo: shouldn't work if the user hasn't subscribed
        elif message == 'stop':
            # Get subscriber object
            s = list(subscriber_exist)
            subscriber = s[0]

            # Unsubscribe
            subscriber.delete()
            reply = 'You\'ve unsubscribed.'

        print 'From: ', phone
        print 'Message: ', message
        print 'Response: ', reply

        # Create response object to send back
        resp = twilio.twiml.Response()
        resp.message(reply)
        return str(resp)
