#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from settings_local import *
except ImportError as e:
    from settings import *

import sendgrid

def email_admin(subject, body):
    sg = sendgrid.SendGridClient(SENDGRID['USERNAME'], SENDGRID['PASSWORD'])
    message = sendgrid.Mail()
    message.add_to(ADMIN_EMAIL)
    message.set_subject(subject)
    message.set_text(body)
    message.set_from('Bowery SMS')
    status, msg = sg.send(message)
