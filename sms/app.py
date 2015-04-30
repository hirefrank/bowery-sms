#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from settings_local import *
except ImportError as e:
    from settings import *

import sys
import twilio.twiml
import string
import random

from parse_rest.connection import register
from parse_rest.datatypes import Object
from parse_rest.user import User
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

        # Does user exist?
        user_exist = User.Query.all().filter(phone=phone).limit(1)

        if user_exist.count() == 0:
            random_pwd = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(20))
            new_user = User.signup(phone, random_pwd, phone=phone, admin=False, subscriber=False)
            u = new_user[0]
        else:
            user_object = list(user_exist)
            u = user_object[0]

        print 'user object: ', u

        if message == 'subscribe':
            # Has the user subscribed?
            if u.subscriber is not True:
                u.subscriber = True
                u.save()
                reply = 'You are now subscribed. Reply "Stop" to stop receiving updates.'
            else:
                # They already exist
                reply = 'You already subscribed!'

        elif message == 'stop':
            # Is the user subscribed?
            if u.subscriber is True:
                u.subscriber = False
                u.save()
                reply = 'You\'ve unsubscribed.'
            else:
                reply = 'You haven\'t subscribed.'

        print 'From: ', phone
        print 'Message: ', message
        print 'Response: ', reply

        # Create response object to send back
        resp = twilio.twiml.Response()
        resp.message(reply)
        return str(resp)
