import json

# LF2 as a queue worker
# Whenever it is invoked by the CloudWatch event trigger that runs every minute:
# 1. pulls a message from the SQS queue, 
# 2. gets a random restaurant recommendation for the cuisine collected through conversation from ElasticSearch and DynamoDB, 
# 3. formats them and 
# 4. sends them over text message to the phone number included in the SQS message, using SNS

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
