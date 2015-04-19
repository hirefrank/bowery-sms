#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from settings_local import *
except ImportError as e:
    from settings import *

import sys
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

        print '***********************'
        print 'From: ', phone
        print 'Message: ', message

        user_exist = User.Query.all().filter(phone=phone).limit(1)
        print len(user_exist)

        #if message == 'subscribe':
            #try:
            #    u = User.signup(phone,"",phone=phone)
            #user_exist = User.Query.all().filter(phone=phone).limit(1)
            #print len(user_exist)
            #if phone in users:
            #    print "blah"
            #else:
            #    print "boo"


            #numbers =
            #if(numbers.indexOf(phone) !== -1) {
            #user_exist = User.Query.all().filter(phone=phone).limit(1)
            #try:
            #    user_exist = User.Query.all().filter(phone=phone).limit(1)
            #print user_exist
            #if user_exist[0]:
            #   print "empty"
            #else:
            #    print "not empty"
            #if len(user_exist) == 0:
            #    u = User.signup(phone,"",phone=phone)
            #    reply = 'You are now subscribed. Reply "Stop" to stop receiving updates.'
            #else:
            #    reply = 'You already subscribed!'

        return ''
        #resp = twilio.twiml.Response()
        #resp.message(reply)
        #return str(resp)
