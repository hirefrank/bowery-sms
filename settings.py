#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

PARSE = {
    'APPLICATION_ID': os.environ['PARSE_APPLICATION_ID'],
    'REST_API_KEY': os.environ['PARSE_REST_API_KEY'],
    'MASTER_KEY': os.environ['PARSE_MASTER_KEY'],
}

TWILIO = {
    'ACCOUNT': os.environ['TWILIO_ACCOUNT'],
    'TOKEN': os.environ['TWILIO_TOKEN'],
}
