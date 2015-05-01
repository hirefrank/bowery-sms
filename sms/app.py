#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from settings_local import *
except ImportError as e:
    from settings import *

import sys
import twilio.twiml

from parse_rest.connection import register
from parse_rest.datatypes import Object, ACL, Pointer
register(PARSE['APPLICATION_ID'], PARSE['REST_API_KEY'], master_key=PARSE['MASTER_KEY'])

from flask import Flask, request, redirect
app = Flask(__name__)

class SMSLog(Object):
    pass

class SMSUser(Object):
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
        user_exist = SMSUser.Query.all().filter(phone=phone).limit(1)
        if user_exist.count() == 0:
            new_user = SMSUser(phone=phone, admin=False, active=False, ACL=ACL({}))
            new_user.save()
            u = new_user[0]
        else:
            user_object = list(user_exist)
            u = user_object[0]

        # subscribe to daily wod reminders
        if message == 'subscribe':
            # Has the user subscribed?
            if u.active is False:
                u.active = True
                u.save()
                reply = 'You are now subscribed. Reply "Stop" to stop receiving updates.'
            else:
                # They already exist
                reply = 'You already subscribed!'

        # get today's wod (latest wod that has been sent)
        elif message == 'wod':
            reply = message

        # get a list of commands
        elif message == 'help':
            reply = message

        # log today's workout
        elif message[0] == '+':
            reply = message

        # search for a movement
        elif message[0] == '?':
            reply = message

        # log a particular movement
        elif len(message.split(":")) > 2:
            reply = message

        elif message == 'stop':
            # Is the user subscribed?
            if u.active is True:
                u.active = False
                u.save()
                reply = 'You\'ve unsubscribed.'
            else:
                reply = 'You haven\'t subscribed.'
        else:
            reply = "what?"

        # Log SMS exchange
        print 'From:', phone, '[' + u.objectId + ']'
        print 'Message:', message
        print 'Response:', reply

        sms_log = SMSLog(message=message, response=reply, ACL=ACL({}))
        sms_log.SMSUser = Pointer(u)
        sms_log.save()

        # Create response object to send back
        resp = twilio.twiml.Response()
        resp.message(reply)
        return str(resp)
