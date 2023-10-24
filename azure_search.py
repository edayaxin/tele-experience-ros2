
#Copyright (c) Microsoft Corporation. All rights reserved.
#Licensed under the MIT License.

# -*- coding: utf-8 -*-

import json
import os 
from pprint import pprint
import requests

'''
This sample makes a call to the Bing Web Search API with a query and returns relevant web search.
Documentation: https://docs.microsoft.com/en-us/bing/search-apis/bing-web-search/overview
'''


BASE_URI = 'https://api.bing.microsoft.com/bing/v7.0/images/visualsearch'
SUBSCRIPTION_KEY = '214b957930bf4db68ea56cd71b348914'
imagePath = 'tmp.jpg'

HEADERS = {'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY}
file = {'image' : ('myfile', open(imagePath, 'rb'))}
def print_json(obj):
    """Print the object as json"""
    print(json.dumps(obj, sort_keys=True, indent=2, separators=(',', ': ')))

try:
    response = requests.post(BASE_URI, headers=HEADERS, files=file)
    response.raise_for_status()
    print_json(response.json())
    
except Exception as ex:
    # raise ex
    print(ex)


# Add your Bing Search V7 subscription key and endpoint to your environment variables.
subscription_key = '214b957930bf4db68ea56cd71b348914'
endpoint = "https://api.bing.microsoft.com/bing/v7.0/search"

# Query term(s) to search for. 
query = "Hello test"

# Construct a request
mkt = 'en-US'
params = { 'q': query, 'mkt': mkt }
headers = { 'Ocp-Apim-Subscription-Key': subscription_key }

# Call the API
try:
    response = requests.get(endpoint, headers=headers, params=params)
    response.raise_for_status()

    print("Headers:")
    print(response.headers)

    print("JSON Response:")
    pprint(response.json())
except Exception as ex:
    raise ex
    