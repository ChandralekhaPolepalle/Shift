from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subscription_form')
def subscription_form():
    return render_template('subscription_form.html')

@app.route('/products')
def products():
    return render_template('products.html')

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


if __name__ == '__main__':
    app.run(debug=True)
