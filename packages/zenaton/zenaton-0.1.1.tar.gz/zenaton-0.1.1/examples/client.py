from __future__ import absolute_import, print_function, unicode_literals

import os

from zenaton import Client


APP_ID = os.environ['ZENATON_APP_ID']
API_TOKEN = os.environ['ZENATON_API_TOKEN']
APP_ENV = os.environ['ZENATON_APP_ENV']
BASE_URL = os.getenv('ZENATON_BASE_URL')

client = Client(APP_ID, API_TOKEN, APP_ENV, BASE_URL)
