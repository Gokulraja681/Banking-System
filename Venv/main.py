from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html')

#Creating Some initiaters for the datas
class GORA:
    def __init__(self):
        self.name = ""
        self.father_name = ""
        self.dob = ""
        self.gender = ""
        self.mbno = ""
        self.pin = ""
        self.amount = 0

gr = GORA()

# Account Creation Module
@app.route('/account_creation', methods = ["POST", "GET"])
def account_creation():
    msg = None
    a = None
    if request.method == "POST":
        gr.name = request.form.get('name')
        gr.father_name = request.form.get('father_name')
        gr.dob = request.form.get('dob')
        gr.gender = request.form.get('gender')
        gr.mbno = request.form.get('mbno')
        p = request.form.get('p')
        while len(p) != 6:
            a = "! Your Should be in Six characters !"
            p = request.form.get('p')
        gr.pin = request.form.get('pin')
        while gr.pin != p:
            a = "! Your Pin not matched with each other !"
            gr.pin = request.form.get('pin')
        if gr.pin == p:
            a = "! Your Pin has been generated successfully !"
        gr.amount = int(request.form.get('amount'))
        if gr.amount > 500:
            msg = "Account has been created Successfully !"
    return render_template('account_creation.html', msg = msg, a = a)


# Account Holder's Profile Module
@app.route('/profile', methods = ["GET"])
def profile():   
    return render_template('profile.html', name = gr.name, father_name = gr.father_name,
                           dob = gr.dob, gender = gr.gender, mbno = gr.mbno,
                           pin = gr.pin, amount = gr.amount)

# Account Profile Module
@app.route('/withdrawal', methods = ["POST", "GET"])
def withdrawal():
    amt = 0
    total = 0
    msg = None
    if request.method == "POST":
        amt  = int(request.form.get('amt'))
        total = gr.amount - amt
        gr.amount = total
        msg = "Amount Withdrawal is Successful !"
    return render_template('withdrawal.html', msg = msg, name = gr.name)

# Amount Deposit Module
@app.route('/deposit', methods = ["POST", "GET"])
def deposit():
    amt = 0
    total = 0
    msg = None
    if request.method == "POST":
        amt = int(request.form.get('amt'))
        total = gr.amount + amt
        gr.amount = total
        msg = "Amount Deposited Successfully !"
    return render_template('deposit.html', name = gr.name, msg = msg)

# Balance Enquiry Module
@app.route('/balance_enquiry', methods = ["GET", "POST"])
def balance_enquiry():
    msg = None
    if request.method == "GET":
        msg = "Your Account Current Balance Details"
    return render_template('balance_enquiry.html', msg = msg, name = gr.name,
                           amount = gr.amount)

if __name__ == "__main__":
    app.run(debug=True)