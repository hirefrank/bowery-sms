#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from settings_local import *
except ImportError as e:
    from settings import *

from twilio.rest import TwilioRestClient
from twilio import twiml
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/sms')
def sms():
    #print TWILIO['ACCOUNT']
    #return TWILIO['TOKEN']
    #client = TwilioRestClient(, TWILIO['TOKEN'])
    #return client
    #resp = twiml.Response()
    #return resp

if __name__ == '__main__':
    app.run()
