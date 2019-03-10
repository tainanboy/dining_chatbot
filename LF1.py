from __future__ import print_function
import time
import os
import logging
import dateutil.parser
import math
import boto3
import json

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#yelp api client ID: "Yo0svsZwE29SvjnXko25OA"
#yelp api key: "3IJu8H3FvrID96O5L9fclsftlRjbrRYB3jyTwITHwU1XHECY7EjDXtGMr0YOMone2iTKO4eBY7sT723kvPEYL1xuu6AyYHDxGqQ6ZztcQw3mXHHq3MC3_6T7g0Z8XHYx"
""" --- Helpers top get result from YELP --- """
import argparse
import json
import pprint
from botocore.vendored import requests
import sys
import urllib
from datetime import datetime
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
API_KEY= 'X-yHBjZ6bMpwjTvCu8hFUWZ8MPnu1YqgPCZ-cvzcdafxIbeEIOnBWUuwm5KWaq3UDPXJoVGj09WTW-_TrUr0t-LqyiFHVjv6h7TfA53wTzYJMmspWSzhAdq2gyiEXHYx'
# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.

# Defaults for our simple example.
DEFAULT_TERM = 'breakfast'
DEFAULT_LOCATION = 'San Diego, CA'
DEFAULT_CATEGORY = 'Japanese'
# DEFAULT_OPEN = False
DEFAULT_DATE = datetime.now()
SEARCH_LIMIT = 3

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
    # print("response=",response.json())
    return response.json()


def search(api_key, term, location,category):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'category': category.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, api_key)


def query_api(term, location, category):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(API_KEY, term, location, category)

    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location, category))
        return

    #print(str(len(businesses))+' businesses found, querying business info ')

 
    # business_id = businesses[0]['id']
    res = []
    for ind in range(len(businesses)):
    	response = get_business(API_KEY, businesses[ind]['id'])
    	res.append((response['name'], str(response['location']['address1'])))
    return res

def searchYelp(location, cuisine, dining_date, dining_time, num_people, term = DEFAULT_TERM):
	try:
		return query_api(cuisine, location, term)
	except HTTPError as error:
		sys.exit(
		    'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
		        error.code,
		        error.url,
		        error.read(),
		    )
		)

""" --- Helpers to build responses which match the structure of the necessary dialog actions --- """
def get_slots(intent_request):
    return intent_request['currentIntent']['slots']

def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }

def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }
    return response

def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }

""" --- Helper Functions --- """
def try_ex(func):
    """
    Call passed in function in try block. If KeyError is encountered return None.
    This function is intended to be used to safely access dictionary.
    Note that this function would have negative impact on performance.
    """
    try:
        return func()
    except KeyError:
        return None

def parse_int(n):
    try:
        return int(n)
    except ValueError:
        return float('nan')

def safe_int(n):
    """
    Safely convert n value to int.
    """
    if n is not None:
        return int(n)
    return n

def build_validation_result(is_valid, violated_slot, message_content):
    if message_content is None:
        return {
            "isValid": is_valid,
            "violatedSlot": violated_slot,
        }

    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }

def isvalid_date(date):
    try:
        dateutil.parser.parse(date)
        return True
    except ValueError:
        return False

# To-do
def validate_dining(slots):
    location = try_ex(lambda: slots['Location'])
    cuisine = try_ex(lambda: slots['Cuisine'])
    dining_date = (try_ex(lambda: slots['​DiningDate']))
    dining_time = (try_ex(lambda: slots['DiningTime']))
    num_people = safe_int(try_ex(lambda: slots['NumPeople']))
    #
    valid_cities = ['new york', 'los angeles', 'chicago', 'san francisco', 'seattle', 'washington dc', 'boston']
    if location is not None and location.lower() not in valid_cities:
        return build_validation_result(False,
                                       'Location',
                                       '{} is not a valid destination. Could you try a different city?'.format(location))

    if dining_date is not None:
        if not isvalid_date(dining_date):
            return build_validation_result(False, 'DiningDate', 'I did not understand that, what date would you like to have the cuisine?')

    if dining_time is not None:
        if len(dining_time) != 5:
            # Not a valid time; use a prompt defined on the build-time model.
            return build_validation_result(False, 'DiningTime', 'I am sorry that it is not a valid time. Please enter a valid time.')
        hour, minute = dining_time.split(':')
        hour = parse_int(hour)
        minute = parse_int(minute)
        if math.isnan(hour) or math.isnan(minute):
            # Not a valid time; use a prompt defined on the build-time model.
            return build_validation_result(False, 'DiningTime', 'I am sorry that it is not a valid time. Please enter a valid time.')
        if hour < 0 or hour > 24:
            # Outside of business hours
            return build_validation_result(False, 'DiningTime', 'I am sorry that it is not a valid time. Please enter a valid time.')
    
    if num_people is not None and (num_people < 1):
        return build_validation_result(
            False,
            'NumPeople',
            'The minimum number of people is 1. How many people do you have?'
        )

    return {'isValid': True}

""" --- Functions that control the bot's behavior --- """
# To-do
def Dining_Suggestions(intent_request):
    # get info
    location = try_ex(lambda: intent_request['currentIntent']['slots']['Location'])
    cuisine = try_ex(lambda: intent_request['currentIntent']['slots']['Cuisine'])
    dining_date =  try_ex(lambda: intent_request['currentIntent']['slots']['DiningDate'])    
    dining_time = try_ex(lambda: intent_request['currentIntent']['slots']['DiningTime'])
    num_people = safe_int(try_ex(lambda: intent_request['currentIntent']['slots']['NumPeople']))
    #
    if intent_request['invocationSource'] == 'DialogCodeHook':
        # Validate any slots which have been specified.  If any are invalid, re-elicit for their value
        validation_result = validate_dining(intent_request['currentIntent']['slots'])
        #
        if not validation_result['isValid']:
            slots = intent_request['currentIntent']['slots']
            slots[validation_result['violatedSlot']] = None

            return elicit_slot(
                intent_request['sessionAttributes'],
                intent_request['currentIntent']['name'],
                slots,
                validation_result['violatedSlot'],
                validation_result['message']
            )
        session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        return delegate(session_attributes, get_slots(intent_request))
    # Order the restaurant, and rely on the goodbye message of the bot to define the message to the end user.
    # In a real bot, this would likely involve a call to a backend service.
    # to-do: searhc yelp and get restaurant suggestions
    suggest_res = searchYelp(location, cuisine, dining_date, dining_time, num_people)
    res_str = ""
    for i, r in enumerate(suggest_res):
        res_str+= str(i+1)+". "+r[0]+" located at "+r[1]+". "
    res_st = 'My {} place suggestions for {} people on {} at {} in {}: '.format(cuisine, num_people, dining_date, dining_time, location)
    res_end = ' Enjoy your meal!'
    res_msg = res_st + res_str + res_end
    # 
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': res_msg})

def Greeting(intent_request):
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'Hi there, how can I help you?'
        }
    )

def Thank_You(intent_request):
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'You are welcome! Thanks for using the service. See you next time!'
        }
    )

""" --- Intents --- """
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """
    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))
    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'GreetingIntent':
        return Greeting(intent_request)
    elif intent_name == "DiningSuggestionsIntent":
        return Dining_Suggestions(intent_request)
    elif intent_name == "ThankYouIntent":
        return Thank_You(intent_request)
    raise Exception('Intent with name ' + intent_name + ' not supported')

""" --- Main handler --- """
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    return dispatch(event)