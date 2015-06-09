#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from settings_local import *
except ImportError as e:
    from settings import *

from workout import *
from smsuser import *
from timezone import *

from parse_rest.connection import register
from parse_rest.datatypes import Object
from twilio.rest import TwilioRestClient

if __name__ == '__main__':
    register(PARSE['APPLICATION_ID'], PARSE['REST_API_KEY'], master_key=PARSE['MASTER_KEY'])
    client = TwilioRestClient(TWILIO['ACCOUNT'], TWILIO['TOKEN'])

    body = "Whoops! Today's workout isn't an open gym. Sorry about that! \n\n"
    body += "Yesterday, Bowery CrossFit redesigned their website, and they no longer display upcoming WODs. As a result, I will be suspending the daily messages until I figure something else out. :/"

    # Get all users that subscribe
    users = SMSUser.Query.all().filter(subscriber=True)
    if users.count() > 0:
        for user in users:
            message = client.messages.create(to=user.phone, from_=TWILIO['NUMBER'], body=body)
