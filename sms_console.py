#!/usr/bin/env python

# This application is a UAT testing dashboard for managing communications with Testers via sms and email.
# To use this an SMS service is required.
# Import contacts from contacts spreadsheet
from flask import Flask, request, render_template, flash, redirect
from flask_script import Manager
import time
import sys
import openpyxl
import string
from colours import colour
import os
from textmagic.rest import TextmagicRestClient
from twilio.rest import TwilioRestClient



app = Flask(__name__)
manager = Manager(app)
spreadsheetPath = "/Users/benwillett/Desktop/ITWork/DET/UAT/"
spreadsheet = "contacts.xlsx"
y = dict()

try:
    message = "importing contacts from spreadsheet"
    print (message)
    time.sleep(1)
    wb = openpyxl.load_workbook(spreadsheetPath + spreadsheet)
    print"loaded"
    sheet = wb.get_sheet_by_name("Sheet 1")
    print"sheet 1"
except:
    message = "could not import contacts from spreadsheet"
    time.sleep(1)
    sys.exit('operation completed')
#
rowCount = 0
columnA = sheet.columns[0]
columnB = sheet.columns[1]
columnC = sheet.columns[2]
columnD = sheet.columns[3]

y['testers'] = []
y['mobile'] = []
y['email'] = []
y['app'] = []
y['status'] = []
y['messageSent'] = []
y['emailSent'] = []
y['messageFailed'] = []


for i in range(0,sheet.max_row):
    if (str(columnA[rowCount].value)) == "None":
        cell = False
    else:
        cell = True
    if cell == True:
        nameTester = (str(columnA[rowCount].value))
        y['testers'].append(nameTester)
        print(y['testers'])

        mobileNum = (str(columnB[rowCount].value))
        y['mobile'].append(mobileNum)
        print(y['mobile'])

        emailAddress = (str(columnC[rowCount].value))
        y['email'].append(emailAddress)
        print(y['email'])

        appResponse = (str(columnD[rowCount].value))
        y['app'].append(appResponse)
        print(y['app'])

        print(y['status'])
    else:
        pass
    rowCount += 1

username = "benwillett"
token = "WD2ND1LXRHziVNew87dsoSrVsXnrSy"
client = TextmagicRestClient(username, token)

# ACCOUNT_SID = "ACee88997b173e176435f49f1667200b0b"
# AUTH_TOKEN = "2f3b730562cffae50135f6a8caa6a815"
# client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)


@app.route('/uat' , methods=['GET','POST'])
def uat():
    global y
    return render_template('uat.html', Y=y,)

@app.route('/message' , methods=['POST'])
def message():
    print(y["status"])
    sms = request.form['message']

    checkedSms = request.form.getlist('SMS')
    print(checkedSms)
    smsList = list(set(checkedSms))
    print("ok 1")
    print(smsList)

    try:
        smsList.remove("None")
    except:
        pass

    checkedEmail = request.form.getlist('EMAIL')
    emailList = list(set(checkedEmail))
    print("ok list 2")
    try:
        emailList.remove("None")
    except:
        pass


    for each in smsList:
        try:
            print("Sending SMS to " + each + " MESSAGE:" + sms)
            client.messages.create(phones=each, text=sms)
            print("SMS sent successfully to" + each)
            y['messageSent'].append(each)


        except:
            print("could not connect to SMS provider, SMS not sent to " + each)
            y['messageFailed'].append(each)
            print("Message failed list")
            print(y['messageFailed'])
            pass

    for each in emailList:
        try:
            print("Sending EMAIL to " + each + " MESSAGE:" + sms)
            # client.messages.create(phones=each, text=sms)
            print("EMAIL sent successfully to" + each)
            y['emailSent'].append(each)

        except:
            print("could not connect to SMTP Server, EMAIL not sent to " + each)
            pass

    checkedStatus = request.form.getlist('STATUS')
    print(checkedStatus)

    try:
        print("got this far")
        status = list(set(checkedStatus))
        k = y['status'] + status
        y['status'] = k
        print(k)

    except:
        print("problem adding status")
    print(y['status'])


    print("redirecting")
    return redirect('/uat')




if __name__ == '__main__':
    manager.run()
    app.run(debug=True)
