from flask import Flask, render_template, request
import random
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/setup')
def setup():
    return render_template('setup.html')

"------------------------------------------------------------------------"
# Creating some initiaters for the Signup and signin
class SS:
    def __init__(self):
        self.fname = ""
        self.lname = ""
        self.gmail = ""
        self.pswd = ""
    
rg = SS()
@app.route('/signup', methods = ["POST", "GET"])
# Signup module with required parameters
def signup():
    msg = None
    msg1 = None
    msg2 = None
    notify = None
    if request.method == "POST":
        rg.fname = request.form.get('fname')
        rg.lname = request.form.get('lname')
        mail = request.form.get('gmail')
        if (mail == rg.gmail):
            msg2 = "Account already exists"
        else:
            rg.gmail = mail
        p = request.form.get('p')
        if len(p) < 8:
            msg = "Password must contain 8 characters"
        rg.pswd = request.form.get('pswd')
        if rg.pswd != p:
            msg1 = "Password not matched"
        if rg.pswd == p:
            rg.pswd = p
        if (len(p) >= 8) and (rg.pswd == p) and (mail != rg.gmail):
            notify = "User account has created successfully"
    return render_template('signup.html', msg = msg, msg1 = msg1, 
                           notify = notify, msg2 = msg2)

# Account Profile module for testing
@app.route('/details', methods = ["GET", "POST"])
def details():
    if request.method == "GET":
        return render_template('details.html', fname = rg.fname,
                               lname = rg.lname, gmail = rg.gmail, pswd = rg.pswd)

# Signin Page module
@app.route('/signin', methods = ["POST", "GET"])
def signin():
    msg = None
    msg1 = None
    if request.method == "POST":
        s_gmail = request.form.get('s_gmail')            
        s_pswd = request.form.get('s_pswd')
        if (s_gmail != rg.gmail) or (s_pswd != rg.pswd):
            msg = "Enter mail or password is not matched"
        if (s_gmail == rg.gmail) and (s_pswd == rg.pswd):
            return index()
    return render_template('signin.html', msg = msg, msg1 = msg1)

# Forget Password Module
@app.route('/forget_password' , methods = ["POST", "GET"])
def forget_password():
    msg = None
    msg1 = None
    msg2 = None
    notify = None
    if request.method == "POST":
        f_gmail = request.form.get('f_gmail')
        if (f_gmail) != (rg.gmail):
            msg = "Please enter a valid mail-id"
        p = request.form.get('p')
        if len(p) < 8:
            msg1 = "Password must contain 8 character"
        f_pswd = request.form.get('f_pswd')
        if (f_pswd != p):
            msg2 = "Password not matched"
        if (f_gmail == rg.gmail) and (len(p) >= 8) and (f_pswd == p):
            rg.pswd = f_pswd
            notify = "Password changed successfully !"
    return render_template('forget_password.html', msg = msg, msg1 = msg1, 
                           msg2 = msg2, notify = notify)

"---------------------------------------------------------------------------------"

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
        self.acn = 0

gr = GORA()

# Account Creation Module
@app.route('/account_creation', methods = ["POST", "GET"])
def account_creation():
    msg = None
    msg1 = None
    msg2 = None
    msg3 = None
    msg4 = None
    if request.method == "POST":
        gr.name = request.form.get('name')
        gr.father_name = request.form.get('father_name')
        gr.dob = request.form.get('dob')
        gr.gender = request.form.get('gender')
        gr.mbno = request.form.get('mbno')
        b = random.randint(24620100014670, 29999999999999)
        gr.acn = b
        p = request.form.get('p')
        if len(p) != 6:
            msg = "Pin Should be in Six characters"
        gr.pin = request.form.get('pin')
        if gr.pin != p:
            msg1 = "Pin not matched with each other"
        gr.amount = int(request.form.get('amount'))
        if gr.amount < 1000:
            msg2 = "For account creation initial deposit amount is 1000"
        if (len(p) == 6) and (gr.pin == p) and (gr.amount >= 1000):
            msg3 = f"{gr.pin} is your account pin"
            msg4 = "Account has been created successfully"
    return render_template('account_creation.html', msg = msg, msg1 = msg1,
                           msg2=msg2, msg3 = msg3, msg4 = msg4)


# Account Holder's Profile Module
@app.route('/profile', methods = ["GET"])
def profile():   
    return render_template('profile.html', acn = gr.acn ,name = gr.name, father_name = gr.father_name,
                           dob = gr.dob, gender = gr.gender, mbno = gr.mbno,
                           pin = gr.pin, amount = gr.amount)

# Account Profile Module
@app.route('/withdrawal', methods = ["POST", "GET"])
def withdrawal():
    amt = 0
    total = 0
    msg = None
    msg1 = None
    msg2 = None
    msg3 = None
    notify = None
    if request.method == "POST":
        amt  = int(request.form.get('amt'))
        if amt < 500:
            msg = "Minimum Deposit Amount is 500"
        if amt > gr.amount:
            msg3 = "Doesn't have enough balance"
        pin = request.form.get('pin')
        if pin != gr.pin:
            msg1 = "Please enter your pin correctly"
        if (amt >= 500) and (amt <= gr.amount) and (pin == gr.pin):
            total = gr.amount - amt
            gr.amount = total
            notify = f"{amt} has been debited from your account !"
            msg2 = "Amount Withdrawal is Successful !"
    return render_template('withdrawal.html', msg = msg, name = gr.name, acn = gr.acn,
                           msg1 = msg1, msg2 = msg2, notify = notify, msg3 = msg3)

# Amount Deposit Module
@app.route('/deposit', methods = ["POST", "GET"])
def deposit():
    amt = 0
    total = 0
    msg = None
    msg1 = None
    msg2 = None
    notify = None
    if request.method == "POST":
        amt = int(request.form.get('amt'))
        if amt < 500:
            msg = "Minimum Deposit amount is 500"
        pin = request.form.get('pin')
        if pin != gr.pin:
            msg1 = "Please enter your Pin correctly"
        if (amt >= 500) and (pin == gr.pin):
            total = gr.amount + amt
            gr.amount = total
            notify = f"{amt} has been credited in Account"
            msg2 = "Amount Deposited Successfully !"
    return render_template('deposit.html', name = gr.name, msg = msg,
                           msg1 = msg1, msg2 = msg2, notify = notify, acn = gr.acn)

# Balance Enquiry Module
@app.route('/balance_enquiry', methods = ["GET", "POST"])
def balance_enquiry():
    msg = None
    if request.method == "GET":
        msg = "Your Account Current Balance Details"
    return render_template('balance_enquiry.html', msg = msg, name = gr.name,
                           amount = gr.amount, acn = gr.acn)

# Change the Pin
@app.route('/change_pin', methods = ["GET", "POST"])
def change_pin():
    msg = None
    msg1 = None
    msg2 = None
    msg3 = None
    msg4 = None
    if request.method == "POST":
        mbno = request.form.get('mbno')
        if mbno != gr.mbno:
            msg = "Entered Mobile number is not matched"
        acn  = int(request.form.get('acn'))
        if acn != gr.acn:
            msg1 = "Entered Account Number is not matched"
        re_pin = request.form.get('re_pin')
        if len(re_pin) != 6:
            msg2 = "Pin should contain 6 characters"
        pin = request.form.get('pin')
        if pin != re_pin:
            msg3 = "Pin not matched with each other"
        if (mbno == gr.mbno) and (acn == gr.acn) and (len(re_pin) == 6) and (re_pin == pin):
            gr.pin = pin
            msg4 = "Pin has been Changed Successfully"  
    return render_template('change_pin.html', msg = msg, msg1 = msg1, msg2 = msg2,
                           msg3 = msg3, msg4 = msg4)

@app.route('/logout')
def logout():
    return setup()

if __name__ == "__main__":
    app.run(debug=True)