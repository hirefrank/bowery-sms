#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from sms.app import app

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)
