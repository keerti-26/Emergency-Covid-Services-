import json
import boto3


def lambda_handler(event, context):
    sns = boto3.client("sns",region_name="us-east-1",aws_access_key_id="API KEY",aws_secret_access_key="SECRET KEY")

    print(event)
    sns.publish(PhoneNumber=event['params']['querystring']['number'],
                     Message=event['params']['querystring']['message'],
                     Subject="Emergency Services Help")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
