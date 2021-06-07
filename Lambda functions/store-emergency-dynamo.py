import json
import boto3
from datetime import datetime,timezone
import requests
#from botocore.vendored import requests

def emergency_type(etype):
    
    if etype == '1':
        return "Hospital beds"
    elif etype == '2':
        return "Oxygen Cylinders"
    elif etype == '3':
        return "Plasma donor"
    elif etype == '4':
        return "Remdesivir injection"
    elif etype == '5':
        return "Blood bank"
    



def lambda_handler(event, context):
    # TODO implement
   
    a = emergency_type(event['Details']['ContactData']['Attributes']['emergencyType'])
    #IST = pytz.timezone('Asia/Kolkata')
    
    
    zipcode = event['Details']['ContactData']['Attributes']['pincode']
    key = 'API_KEY'
    response = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={zipcode}&region=in&key={key}")
    address = response.json()
    loc = address["results"][0]["formatted_address"]
    
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.put_item(TableName='Covid-EMS-Master-Table',Item={
                                             'ContactId': {'S': event['Details']['ContactData']['ContactId']},
                                             'ContactNumber': {'S': event['Details']['ContactData']['CustomerEndpoint']['Address']},
                                             'EmergencyType': {'N': event['Details']['ContactData']['Attributes']['emergencyType']},
                                             'Emergency': {'S': a},
                                             'Pincode': {'N': event['Details']['ContactData']['Attributes']['pincode']},
                                             'Location': {'S': loc},
                                             #'CallTimestamp': {'S': datetime.now(IST)},
                                             'CallResolved': {'BOOL': False},
                                             'Assignee': {'S': 'None'},
                                             'ReliefInfo': {'S': 'Pending'}
                                             
                                         }
                                         )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Call data loaded in table: Covid-EMS-Master-Table')
    }