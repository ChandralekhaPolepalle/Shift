import os
import threading
import json
import logging
from flask import Flask, render_template, request, redirect, url_for
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
from flask import Flask, request, jsonify
import httpx
import smtplib
from flask_mail import Mail, Message
# from dotenv import load_dotenv

app = Flask(__name__)

# load_dotenv()

HUBSPOT_ACCESS_TOKEN = "pat-na1-2fcd038b-0c6d-4d85-9d15-f1134485bc2a"

SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/contacts']

# Configuring Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tech@shiftgroup.ca'
app.config['MAIL_PASSWORD'] = 'rddh vikr ojtc sboz'
app.config['MAIL_DEBUG'] = True
app.config['DEBUG'] = True

mail = Mail(app)

# Load Google credentials from environment variable
try:
    google_credentials = os.getenv('GOOGLE_CREDENTIALS')

    if google_credentials is None:
        raise ValueError("GOOGLE_CREDENTIALS environment variable is not set.")
    credentials_info = json.loads(google_credentials)
    credentials = Credentials.from_service_account_info(credentials_info, scopes=SCOPES)


except Exception as e:
    raise ValueError("Failed to load Google credentials. Ensure the environment variable is set correctly.") from e

# Google Sheets API setup
SPREADSHEET_ID = '1VGBJr6zFSilCvF7jCv_0ejlUR2CcST_QHCR4bZDXkwE'
RANGE_NAME = 'SHIFT Subscriptions!A2:F2'
service = build('sheets', 'v4', credentials=credentials)
people_service = build('people', 'v1', credentials=credentials)
sheet = service.spreadsheets()

# GOOGLE_CREDENTIALS = os.getenv('GOOGLE_CREDENTIALS')
# credentials_info = json.loads(GOOGLE_CREDENTIALS)
# credentials = Credentials.from_service_account_info(credentials_info, scopes=SCOPES)
# service = build('sheets', 'v4', credentials=credentials)
# sheet = service.spreadsheets()
# # SERVICE_ACCOUNT_FILE = 'credentials.json'
#
#

#
#
# # credentials = Credentials.from_service_account_file(
# #     SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# # service = build('sheets', 'v4', credentials=credentials)
# # sheet = service.spreadsheets()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subscription_form', methods=['GET', 'POST'])
def subscription_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        company_name = request.form['companyName']
        company_website = request.form['companyWebsite']
        subscribe_check = 'Yes' if 'subscribeCheck' in request.form else 'No'
        interested_solutions = request.form.getlist('interestedSolution')
        fleet_size = request.form['fleetSize']
        interested_solutions_str = ', '.join(interested_solutions)

        values = [[name,email, company_name, company_website,subscribe_check,interested_solutions_str,fleet_size]]
        body = {'values': values}
        print("---------------------------")
        print(body)

        try:
            sheet.values().append(
                spreadsheetId=SPREADSHEET_ID,
                range=RANGE_NAME,
                valueInputOption='RAW',
                body=body
            ).execute()

            # Add to Google Contacts
            contact_body = {
                'names': [{'givenName': name}],
                'emailAddresses': [{'value': email}],
                'memberships': [{'contactGroupMembership': {'contactGroupResourceName': 'contactGroups/SHIFT Subscriptions'}}]
            }
            contact_response = people_service.people().createContact(body=contact_body).execute()
            logging.debug(f"Google Contacts response: {contact_response}")

            message = "Thank you for subscribing!"
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            message = f"An error occurred: {e}"
            message = "Please provide vaild details"

        url = "https://api.hubapi.com/crm/v3/objects/contacts"

        data = {
            "properties": {
                "firstname": name,
                "email": email,
                "company":company_name,
                "website":company_website,
                "subscription":subscribe_check,
                "interested_solution": interested_solutions_str,
                "fleet_size":fleet_size

            }
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {HUBSPOT_ACCESS_TOKEN}"
        }

        response = httpx.post(url, json=data, headers=headers)

        if response.status_code == 201:
            print("Contact added successfully")

        else:
            print(response.json())


    return render_template('index.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/nav')
def nav():
    return render_template('nav.html')
@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/productSuites')
def productSuites():
    return render_template('product_suites.html')

@app.route('/homeKeyFeatures')
def homeKeyFeatures():
    return render_template('home_keyfeatures.html')

@app.route('/business')
def business():
    return render_template('business.html')

@app.route('/productAdminPortal')
def pAdminPortal():
    return render_template('p_admin_portal.html')

@app.route('/productCustomerApp')
def pCustomerApp():
    return render_template('p_customer_app.html')

@app.route('/navBar')
def navBar():
    return render_template('navbar.html')

@app.route('/fleetManagement')
def fleetManagement():
    return render_template('fleet_management.html')

@app.route('/comingSoon')
def comingSoon():
    return render_template('coming_soon.html')

@app.route('/home')
def Home():
    return render_template('home.html')

@app.route('/mobileNav')
def MobileNav():
    return render_template('mobile_nav.html')

@app.route('/mobileDesktopNav')
def MobileDesktopNav():
    return render_template('mobile_desktop_nav.html')

@app.route('/productDriverApp')
def pDriverApp():
    return render_template('p_driver_app.html')

@app.route('/productAgentOperationalApp')
def pOperationalApp():
    return render_template('p_operational_app.html')

@app.route('/productEldReport')
def pEldReport():
    return render_template('p_eld_report.html')

@app.route('/productAIDashCam')
def pAiDashCam():
    return render_template('p_ai_dash_cam.html')

@app.route('/productTracking')
def pTracking():
    return render_template('p_tracking.html')

@app.route('/productDigitalKey')
def pDigitalKey():
    return render_template('p_digital_key.html')

def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")
            logging.error(f"Error sending email: {e}")

@app.route('/contactUs', methods=['GET', 'POST'])
def contactUs():
    if request.method == 'POST':
        print("TEST")
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        msg = Message('SHIFT Contact Us Form Submission', sender='tech@shiftgroup.ca', recipients=['tech@shiftgroup.ca'])
        msg.body = f"Name: {name}\nEmail: {email}\nSubject: {subject}\nMessage: {message}"

        thread = threading.Thread(target=send_async_email, args=(app, msg))
        thread.start()

        # try:
        #     mail.send(msg)
        #     print("Email sent successfully!")
        # except Exception as e:
        #     print(f"Failed to send email: {e}")
        #     logging.error(f"Error sending email: {e}")

    return render_template('contactUs.html')

if __name__ == '__main__':
    app.run(debug=True)
