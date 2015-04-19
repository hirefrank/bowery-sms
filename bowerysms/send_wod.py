#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from settings_local import *
except ImportError as e:
    from settings import *

from scraper import *
from twilio.rest import TwilioRestClient

message = client.messages.create(to="", from_=TWILIO['NUMBER'],
                                     body="Hello there!")
