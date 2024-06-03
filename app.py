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

if __name__ == '__main__':
    app.run(debug=True)
