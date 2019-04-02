import json
import boto3

# LF2 as a queue worker
# Whenever it is invoked by the CloudWatch event trigger that runs every minute:
# 1. pulls a message from the SQS queue, 
# 2. gets a random restaurant recommendation for the cuisine collected through conversation from ElasticSearch and DynamoDB, 
# 3. formats them and 
# 4. sends them over text message to the phone number included in the SQS message, using SNS

def lambda_handler(event, context):
    # TODO implement
    print("Testing CloudWatch: Call LF2 every minute.")
    # pulls a message from the SQS queue
    # Create SQS client 
    sqs = boto3.client('sqs')
    # Get URL for SQS queue
    response = sqs.get_queue_url(QueueName='chatbot_slots')
    queue_url = response['QueueUrl']
    print(queue_url)
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
    except:
        print("SQS queue is now empty")
    # gets a random restaurant recommendation for the cuisine collected through conversation from ElasticSearch

    # get more information from DynamoDB

    # format the message

    # send the message using SNS
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
