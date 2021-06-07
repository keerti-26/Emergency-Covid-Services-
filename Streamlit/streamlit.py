import streamlit as st
import hashlib
import sqlite3
import services
import streamlit as st
import altair as alt
from os import listdir
from os.path import isfile, join
#from pydantic import BaseModel
import boto3
import json
import time
import pandas as pd
import numpy as np
import random
import string
from datetime import datetime
from datetime import date
import requests as requests
import pandas as pd
#import matplotlib.pyplot as plt
import streamlit as st

# Security

# passlib,hashlib,bcrypt,scrypt


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False


# DB Management

conn = sqlite3.connect('data.db')
c = conn.cursor()


# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)', (username, password))
    conn.commit()


def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data


def main():

    st.set_page_config(
        page_title="EmerygencyCallServices",
        page_icon=":phone:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("Emergency Call Services")

    # Sidebar
    st.sidebar.header(":gear: Navigation")
    menu = ["Home", "Login", "SignUp", "Logout"]
    choice = st.sidebar.selectbox(label="Menu", options=menu, index=0, help="Main Navigation Menu")

    if choice == "Login":

        ACCESS_KEY_ID = 'AKIA5CUSOFRV36GAHXEX'
        ACCESS_SECRET_KEY = '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'
        #st.sidebar.title('** Welcome to Team 3 CSYE !!!**')
        #st.sidebar.header('User Authentication')

        #st.sidebar.subheader('Please enter valid username password and Acess Token')

        usrName = st.sidebar.text_input('Username')
        usrPassword = st.sidebar.text_input('Password')
        acesstoken = st.sidebar.text_input('Enter your Token')

        OTP = usrName + usrPassword
        dynamodb = boto3.resource('dynamodb',
                                  aws_access_key_id=ACCESS_KEY_ID,
                                  aws_secret_access_key=ACCESS_SECRET_KEY,
                                  region_name='us-east-1')

        table = dynamodb.Table('users')

        response = table.scan()

        OTPD = response['Items']
        userlist = []
        toklist = []
        i = 0
        while i < len(OTPD):
            # print(OTP[i])
            x = OTPD[i]['login']
            y = OTPD[i]['acesstoken']
            # print(x)
            userlist.append(x)
            toklist.append(y)
            i = i + 1

        if OTP in userlist and acesstoken in toklist:
            verified = "True"
            result = "Congratulations User Verified!!"
            #page = st.sidebar.radio("Choose a page", )
            st.title(result)
            a, b = st.beta_columns([0.6, 10])
            a.image("support.png", width=60, caption=usrName)
            b.header("Welcome, {}!!".format(usrName))
            services.login_menu(usrName)

    # elif choice == "Login":
    #
    #     username = st.sidebar.text_input("User Name")
    #     password = st.sidebar.text_input("Password", type='password')
    #     if st.sidebar.checkbox("Login/Logout"):
    #
    #         create_usertable()
    #         hashed_pswd = make_hashes(password)
    #
    #         result = login_user(username, check_hashes(password, hashed_pswd))
    #         if result:
    #
    #             a, b = st.beta_columns([0.6,10])
    #             a.image("support.png", width=60, caption=username)
    #             b.header("Welcome, {}!!".format(username))
    #
    #             services.login_menu(username)
    #
    #         else:
    #             st.sidebar.error("Incorrect Username/Password")

    elif choice == "Logout":
        st.header("You are Logged Out")
        st.subheader("Please Go to Homepage to Login")
        st.balloons()

    elif choice == "Home":
        st.image("welcome.gif", use_column_width=True)

    elif choice == "SignUp":
        # st.subheader("Create New Account")
        # new_user = st.text_input("Username")
        # new_password = st.text_input("Password", type='password')

        signusrName = st.text_input('Username')
        signusrPassword = st.text_input('Password')
        signusrEmail = st.text_input('Email')

        userOPT = signusrName + signusrPassword

        ACCESS_KEY_ID = ACCESS-KEY
        ACCESS_SECRET_KEY = SECRET-KEY

        dynamodb = boto3.resource('dynamodb',
                                  aws_access_key_id=ACCESS_KEY_ID,
                                  aws_secret_access_key=ACCESS_SECRET_KEY,
                                  region_name='us-east-1')

        dynamoTable = dynamodb.Table('users')

        # Generating a Random Token for API Key
        letters = string.ascii_lowercase
        tok = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(40))

        # if st.button("Signup"):
        #     create_usertable()
        #     add_userdata(new_user, make_hashes(new_password))
        #     st.success("You have successfully created a valid Account")
        #     st.info("Go to Login Menu to login")

        # Code to Put the Item
        if signusrName == "" or signusrPassword == "" or signusrEmail == "":
            st.text('Please enter Valid Values')

        else:
            st.title('Congratulations, Your Account is created Successfully!')
            st.title('Your Unique Token from AWS Cognito is Sent Via Email: ')
            # st.title(tok)
            import smtplib

            conn = smtplib.SMTP('smtp.gmail.com', 587)

            conn.ehlo()

            conn.starttls()

            conn.login('emergencycovidrelif@gmail.com', 'Neu#2019')

            conn.sendmail('emergencycovidrelif@gmail.com', signusrEmail,
                          'Subject: This is Your Access Token for FAST Stock App \n\n Dear ' + signusrName + tok + '')

            conn.quit()

            dynamoTable.put_item(
                Item={
                    'login': userOPT,
                    'acesstoken': tok
                }
            )


if __name__ == '__main__':
    main()
