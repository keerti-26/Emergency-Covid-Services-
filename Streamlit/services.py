import streamlit as st
import boto3, config
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr
import requests


# Function to display menu once logged in
def login_menu(username):
    st.sidebar.header(":gear:  Services")
    choice = st.sidebar.radio("Menu", ["Live Call Requests", "My Closed Requests"])
    if choice == "Live Call Requests":

        records = getcalls(False)
        st.table(records)

        for a in records:

            with st.beta_expander(a['ContactNumber']):
                col1, col2 = st.beta_columns(2)
                information = col1.text_input("Enter text", key="text_" + a['ContactId'])


                st.code("ContactID: " + a['ContactId'] + '\n' + "Contact Number: " + a[
                    'ContactNumber'] + '\n' + "Location: " + str(a['Location']) + '\n' + "Emergency Requirement: " + a[
                            'Emergency'])
                if st.button("Send Information", key="btn_" + a['ContactId']):
                    notify_entity(a['ContactNumber'],information)
                    print("notify done")
                    update_information(a['ContactId'], information)
                    update_assignee(a['ContactId'], username)
                    print("update assignee done!")
                    st.success("Notified " + a['ContactNumber'])

    elif choice == "My Closed Requests":
        records = getassigneecalls(True, username)
        if len(records) == 0:
            st.info("No Resolved Requests")
        else:
            st.table(records)

    # elif choice == "Analytics Dashboard":
    #     st.write("WIP")


# Function to pull calls which are pending from DynamoDB
def get_all_calls(value):
    dynamodb = boto3.resource('dynamodb', aws_access_key_id=config.aws["secret_id"],
                              aws_secret_access_key=config.aws["access_key"], region_name=config.aws["region"])

    try:
        table = dynamodb.Table('Covid-EMS-Master-Table')
        response = table.scan(
            TableName='Covid-EMS-Master-Table',
            FilterExpression=Attr('CallResolved').eq(value)
        )
    except ClientError as e:
        st.error(e.response['Error']['Message'])
    else:
        return response['Items']

# Function to pull calls which are pending from DynamoDB
def getcalls(value):
    dynamodb = boto3.resource('dynamodb', aws_access_key_id=config.aws["secret_id"],
                              aws_secret_access_key=config.aws["access_key"], region_name=config.aws["region"])

    try:
        table = dynamodb.Table('Covid-EMS-Master-Table')
        response = table.scan(
            TableName='Covid-EMS-Master-Table',
            FilterExpression=Attr('CallResolved').eq(value)

        )
    except ClientError as e:
        st.error(e.response['Error']['Message'])
    else:
        return response['Items']


# Function to get assignee closed requets
def getassigneecalls(value, assignee):
    dynamodb = boto3.resource('dynamodb', aws_access_key_id=config.aws["secret_id"],
                              aws_secret_access_key=config.aws["access_key"], region_name=config.aws["region"])

    try:
        table = dynamodb.Table('Covid-EMS-Master-Table')
        response = table.scan(
            TableName='Covid-EMS-Master-Table',
            FilterExpression=Attr('CallResolved').eq(value) & Attr("Assignee").eq(assignee)
        )
    except ClientError as e:
        st.error(e.response['Error']['Message'])
    else:
        return response['Items']


# Function to update assignee once resolved
def update_assignee(contactId, username):
    dynamodb = boto3.resource('dynamodb', aws_access_key_id=config.aws["secret_id"],
                              aws_secret_access_key=config.aws["access_key"], region_name=config.aws["region"])

    try:
        table = dynamodb.Table('Covid-EMS-Master-Table')
        response = table.update_item(
            Key={'ContactId': contactId},
            UpdateExpression="set Assignee = :u, CallResolved = :b",
            ExpressionAttributeValues={
                ':u': username,
                ':b': True,
            },
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as e:
        st.error(e.response['Error']['Message'])

def update_information(contactId, information):
    print("update info start")
    dynamodb = boto3.resource('dynamodb', aws_access_key_id=config.aws["secret_id"],
                                  aws_secret_access_key=config.aws["access_key"], region_name=config.aws["region"])

    try:
        table = dynamodb.Table('Covid-EMS-Master-Table')
        response = table.update_item(
            Key={'ContactId': contactId},
            UpdateExpression="set ReliefInfo = :u",
            ExpressionAttributeValues={
                 ':u': information
                  # ':b': True,
              },
              ReturnValues="UPDATED_NEW"
            )
    except ClientError as e:
        st.error(e.response['Error']['Message'])

def notify_entity(contactnumber,information):
    client=boto3.client('sns',aws_access_key_id=config.aws["secret_id"],
                                  aws_secret_access_key=config.aws["access_key"], region_name=config.aws["region"])

    response = client.subscribe(
        TopicArn='arn:aws:sns:us-east-1:355667032500:EmergencyCovidSewa',
        Protocol='SMS',
        Endpoint=contactnumber,
        ReturnSubscriptionArn=True
    )
    res = requests.get(f'https://8tia579ez2.execute-api.us-east-1.amazonaws.com/dev/notification?message={information}&number={contactnumber}')
    response_json = res.json()
    print(response_json)
    return res


