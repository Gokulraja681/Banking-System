from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/account_creation')
def account_creation():
    return render_template('account_creation.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/withdrawal')
def withdrawal():
    return render_template('withdrawal.html')

@app.route('/deposit')
def deposit():
    return render_template('deposit.html')

@app.route('/balance_enquiry')
def balance_enquiry():
    return render_template('balance_enquiry.html')

if __name__ == "__main__":
    app.run(debug=True)