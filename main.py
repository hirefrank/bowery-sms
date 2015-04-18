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

@app.route("/sms")
def sms():
    resp = twiml.Response()
    print resp

if __name__ == '__main__':
    client = TwilioRestClient(TWILIO['ACCOUNT'], TWILIO['TOKEN'])
    app.run()
