#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from settings_local import *
except ImportError as e:
    from settings import *

import sys
import twilio.twiml
import random

from workout import *
from smsuser import *
from strings import *
from timezone import *

from parse_rest.connection import register
from parse_rest.datatypes import Object, ACL, Pointer
register(PARSE['APPLICATION_ID'], PARSE['REST_API_KEY'], master_key=PARSE['MASTER_KEY'])

from flask import Flask, request, redirect
app = Flask(__name__)

# User's PRs
class PRLog(Object):
    pass

# User's workout results
class WorkoutLog(Object):
    pass

# SMS logs
class SMSLog(Object):
    pass

def list_of_commands():
    content = ''
    for key in commands:
        content += key + '\n # ' + commands[key] + '\n\n'
    return content

@app.route('/')
def hello_world():
    return 'Hello World!'

# All Twilio routing should be sent to /sms
@app.route("/sms", methods=['GET', 'POST'])
def sms():
    # Only continue if a POST request
    if request.method == 'POST':

        # Remove whitespace
        message = request.form['Body'].strip()

        # Sender's phone number. Save for later.
        phone = request.form['From']

        # Does user exist?
        user_exist = SMSUser.Query.all().filter(phone=phone).limit(1)
        if user_exist.count() == 0:
            new_user = SMSUser(name=message, phone=phone, admin=False, subscriber=False, ACL=ACL({}))
            new_user.save()
            u = new_user

            # Welcome reply message
            reply = 'Hi ' + message + '! Welcome to Bowery SMS. Text any of the commands below to get started.\n\n'
            reply += list_of_commands()
        else:
            # Lowercase the inbound message
            message = message.lower()

            user_object = list(user_exist)
            u = user_object[0]

            # Subscribe to daily wod reminders
            if message == 'subscribe':
                # Has the user subscribed?
                if u.subscriber is False:
                    u.subscriber = True
                    u.save()
                    reply = 'You are now subscribed. Reply "Stop" to stop receiving updates.'
                else:
                    # They already exist
                    reply = 'You already subscribed!'

            # Get today's wod
            # Todo: Should return "open gym" for Sundays
            elif message == 'wod':
                if day_of_the_week == "Sunday":
                    reply = "Open gym!"
                else:
                    reply = latest_workout()

            # Get a list of commands
            elif message == 'help':
                reply = 'Commands:\n' + list_of_commands()

            # Log today's workout
            elif message[0] == '+':
                result = message[1:].strip()
                w = latest_workout_obj()

                # Does workout log exist?
                workout_log_exist = WorkoutLog.Query.all().filter(SMSUser=u).filter(Workout=w).limit(1)
                if workout_log_exist.count() == 0:
                    workout_log = WorkoutLog(result=result, ACL=ACL({}))
                    workout_log.SMSUser = Pointer(u)
                    workout_log.Workout = Pointer(w)
                    workout_log.save()
                    reply = random.choice(salutations) + " We've recorded " + result + " for today's workout."

                else:
                    workout_log.result = result
                    workout_log.save()
                    reply = random.choice(salutations) + " We've updated your workout result to " + result + "."

            # Search for a movement
            elif message[0] == '?':
                reply = 'Search not yet implemented.'

            # Log a particular movement
            elif len(message.split(":")) > 1:
                activity = message.split(":")[0]
                result = message.split(":")[1]

                pr_log = PRLog(activity=activity, result=result, ACL=ACL({}))
                pr_log.SMSUser = Pointer(u)
                pr_log.save()
                reply = random.choice(salutations) + " We've recorded " + result + " for " + activity + "."

            elif message == 'stop':
                # Is the user subscribed?
                if u.subscriber is True:
                    u.subscriber = False
                    u.save()
                    reply = 'You\'ve unsubscribed.'
                else:
                    reply = 'You haven\'t subscribed.'
            else:
                reply = "Say what? Text 'Help' for a list of commands."

        # Log SMS exchange
        print 'From:', phone
        print 'Message:', message
        print 'Response:', reply

        sms_log = SMSLog(message=message, response=reply, ACL=ACL({}))
        sms_log.SMSUser = Pointer(u)
        sms_log.save()

        # Create response object to send back
        resp = twilio.twiml.Response()
        resp.message(reply)
        return str(resp)
