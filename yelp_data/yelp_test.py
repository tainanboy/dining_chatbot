# -*- coding: utf-8 -*-
"""
Yelp Fusion API code sample.

This program demonstrates the capability of the Yelp Fusion API
by using the Search API to query for businesses by a search term and location,
and the Business API to query additional information about the top result
from the search query.

Please refer to http://www.yelp.com/developers/v3/documentation for the API
documentation.

This program requires the Python requests library, which you can install via:
`pip install -r requirements.txt`.

Sample usage of the program:
`python sample.py --term="bars" --location="San Francisco, CA"`
"""
from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib
from datetime import datetime
import csv

# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode

# Yelp Fusion no longer uses OAuth as of December 7, 2017.
# You no longer need to provide Client ID to fetch Data
# It now uses private keys to authenticate requests (API Key)
# You can find it on
# https://www.yelp.com/developers/v3/manage_app
#API_KEY= "3IJu8H3FvrID96O5L9fclsftlRjbrRYB3jyTwITHwU1XHECY7EjDXtGMr0YOMone2iTKO4eBY7sT723kvPEYL1xuu6AyYHDxGqQ6ZztcQw3mXHHq3MC3_6T7g0Z8XHYx"
API_KEY= 'X-yHBjZ6bMpwjTvCu8hFUWZ8MPnu1YqgPCZ-cvzcdafxIbeEIOnBWUuwm5KWaq3UDPXJoVGj09WTW-_TrUr0t-LqyiFHVjv6h7TfA53wTzYJMmspWSzhAdq2gyiEXHYx'
# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.

# Defaults for our simple example.
DEFAULT_TERM = 'Chinese'
DEFAULT_LOCATION = 'New York, NY'
DEFAULT_CATEGORY = 'Food'
DEFAULT_DATE = datetime.now()
SEARCH_LIMIT = 50


def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    #print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, term, location, category, url_params):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """
    return request(API_HOST, SEARCH_PATH, api_key, url_params)


def get_business(api_key, business_id):
    """Query the Business API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, api_key)


def query_api(num_req, term, location, category):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    if num_req == 0:
        offset = 0
    else:
        offset = num_req*SEARCH_LIMIT+1
    print(num_req, offset)
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'category': category.replace(' ', '+'),
        'limit': SEARCH_LIMIT,
        'offset': offset
    }
    response = search(API_KEY, term, location, category, url_params)

    businesses = response.get('businesses')
    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location, category))
        return

    res = []
    for ind in range(len(businesses)):
        try:
            response = get_business(API_KEY, businesses[ind]['id'])
            res.append((response['id'], response['name'], str(response['location']['address1']), response['coordinates'], response['review_count'], response['rating'], response['location']['zip_code']))
        except:
            pass
    return res

def searchYelp(num_req, term = DEFAULT_TERM, location = DEFAULT_LOCATION, category = DEFAULT_CATEGORY):
    try:
        data = query_api(num_req, term, location, category)
        print(num_req, len(data))
        filename = 'yelp_'+term+'.csv'
        with open(filename,'a') as out:
            csv_out=csv.writer(out)
            if num_req == 0:
                csv_out.writerow(['Business_ID', 'Name', 'Address', 'Coordinates', 'Num_of_Reviews', 'Rating', 'Zip_Code'])
            for row in data:
                csv_out.writerow(row)
    except HTTPError as error:
        print(error)
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
    )

import time, threading
if __name__ == '__main__':
    #terms = ['chinese', 'italian', 'indian','mexican','american', 'sushi']
    terms = ['sushi']
    for term in terms:
        # each req limit =  50
        i = 0
        while(i<24):
            searchYelp(i, term = term)
            time.sleep(10)   
            print(time.ctime(), i)         
            i += 1

            
