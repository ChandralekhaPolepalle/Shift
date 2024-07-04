import os
import json
from flask import Flask, render_template, request, redirect, url_for
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials.json'
SPREADSHEET_ID = '1VGBJr6zFSilCvF7jCv_0ejlUR2CcST_QHCR4bZDXkwE'
RANGE_NAME = 'Sheet1!A2:D2'


credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subscription_form', methods=['GET', 'POST'])
def subscription_form():
    if request.method == 'POST':
        email = request.form['email']
        business_type = request.form['businessType']
        first_name = request.form['firstName']
        services = request.form['services']
        subscribe_check = 'Yes' if 'subscribeCheck' in request.form else 'No'

        values = [[email, business_type, first_name, services, subscribe_check]]
        body = {'values': values}

        try:
            sheet.values().append(
                spreadsheetId=SPREADSHEET_ID,
                range=RANGE_NAME,
                valueInputOption='RAW',
                body=body
            ).execute()
            message = "Thank you for subscribing!"
        except Exception as e:
            message = "Please provide vaild details"

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

if __name__ == '__main__':
    app.run(debug=True)
