import boto3, config
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb', aws_access_key_id=config.aws["secret_id"],
                                    aws_secret_access_key=config.aws["access_key"], region_name=config.aws["region"])

try:
    table = dynamodb.Table('Covid-EMS-Master-Table')
    response = table.scan(
        TableName='Covid-EMS-Master-Table',
        FilterExpression = Attr('Emergency').eq('Plasma donor') #& Key('title').between(title_range[0], title_range[1])
    )
except ClientError as e:
    print(e.response['Error']['Message'])
else:
    print(response['Items'])
