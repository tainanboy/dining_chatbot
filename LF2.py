import json
import boto3
from botocore.vendored import requests
from boto3.dynamodb.conditions import Key, Attr

# LF2 as a queue worker
# Whenever it is invoked by the CloudWatch event trigger that runs every minute:
# 1. pulls a message from the SQS queue, 
# 2. gets a random restaurant recommendation for the cuisine collected through conversation from ElasticSearch and DynamoDB, 
# 3. formats them and 
# 4. sends them over text message to the phone number included in the SQS message, using SNS

# choose the elasticsearch index: "restaurants" is the easier version, "predictions" is with the ML service
#search_index = "restaurants"
search_index = "predictions"


def lambda_handler(event, context):
    # TODO implement
    print("Testing CloudWatch: Call LF2 every minute.")
    # 1. pulls a message from the SQS queue
    # Create SQS client 
    sqs = boto3.client('sqs')
    # Get URL for SQS queue
    response = sqs.get_queue_url(QueueName='chatbot_slots')
    queue_url = response['QueueUrl']
    print(queue_url)
    message = None
    # Receive a message from SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    try:
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        # Delete received message from queue
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        print('Received and deleted message: %s' % message)
        # 2. gets a random restaurant recommendation for the cuisine collected through conversation from ElasticSearch
        print(message['Body'])
        # all information stored in sqs queue
        location = message['MessageAttributes']['location']['StringValue']
        cuisine = message['MessageAttributes']['cuisine']['StringValue']
        dining_date =  message['MessageAttributes']['dining_date']['StringValue']
        dining_time = message['MessageAttributes']['dining_time']['StringValue']
        num_people = message['MessageAttributes']['num_people']['StringValue']
        phone =  message['MessageAttributes']['phone']['StringValue']
        print(location, cuisine, dining_date, dining_time, num_people, phone)
        # use http request to search ElasticSearch index: restaurant
        sendMessage = None
        if search_index == "restaurants":
            # pick a restaurant randomly, get the business_ID (always pick first one here, need further work)
            r = requests.get('https://search-restaurants-cozvshffzyeezzf7wcfsnab45u.us-east-1.es.amazonaws.com/restaurants/_search?q='+str(cuisine))
            data = r.json()
            Business_ID = data['hits']['hits'][0]['_source']['Business_ID']
            print(Business_ID)
            # 3. get more information from DynamoDB
            # search DynamoDB using Business_ID
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('yelp-restaurant')
            response = table.query(
                KeyConditionExpression=Key('Business_ID').eq(Business_ID)
            )
            # 4. format the message
            name = response['Items'][0]['Name']
            address = response['Items'][0]['Address']
            num_reviews = response['Items'][0]['Num_of_Reviews']
            rating = response['Items'][0]['Rating']
            sendMessage = "Hello! For {}, we recommend the {} {} restaurant on {}. The place has {} of reviews and an average score of {} on Yelp. Enjoy!".format(location, name, cuisine, address, num_reviews, rating)
            print(sendMessage)
        else:
            # pick a restaurant randomly, get the business_ID (always pick first one here, need further work)
            r = requests.get('https://search-predictions-nxhiwrjp3ljnqsel5gr6sbxsau.us-east-1.es.amazonaws.com/predictions/_search?q='+str(cuisine))
            data = r.json()
            Business_ID = data['hits']['hits'][0]['_source']['Business_ID']
            print(Business_ID)
            # 3. get more information from DynamoDB
            # search DynamoDB using Business_ID
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('yelp-restaurant')
            response = table.query(
                KeyConditionExpression=Key('Business_ID').eq(Business_ID)
            )
            # 4. format the message
            name = response['Items'][0]['Name']
            address = response['Items'][0]['Address']
            num_reviews = response['Items'][0]['Num_of_Reviews']
            rating = response['Items'][0]['Rating']
            sendMessage = "Hello! For {}, we recommend the {} {} restaurant on {}. The place has {} of reviews and an average score of {} on Yelp. Enjoy!".format(location, name, cuisine, address, num_reviews, rating)
            print(sendMessage)
        # 5. send the message using SNS
        # Create SQS client
        sns = boto3.client('sns')
        # send message
        sns.publish(
            PhoneNumber = '+1'+phone,
            Message = sendMessage
        )
    except:
        print("SQS queue is now empty")
    # return 
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda LF2!')
    }
