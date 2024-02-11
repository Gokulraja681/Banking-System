from flask import *
import random
import pymongo

app = Flask(__name__)

mongocon = pymongo.MongoClient('mongodb://localhost:27017')
mydb = mongocon['Banking']
mycol = mydb['Data']



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
        temp_mail = request.form['gmail']
        existing_user = mycol.find_one({'gmail': temp_mail})
        if existing_user:
            msg2 = 'Account already exists'
        else:
            rg.gmail = temp_mail
            p = request.form['p']
            if len(p) < 8:
                msg = 'Password must contain 8 characters'
            else:
                rg.pswd = request.form['pswd']
                if rg.pswd != p:
                    msg1 = 'password not matched with each other'
                else:
                    rg.pswd = p
                    mydoc = {
                        'fname': rg.fname,
                        'lname': rg.lname,
                        'gmail': rg.gmail,
                        'pswd' : rg.pswd
                    }
                    mycol.insert_one(mydoc)
                    return redirect(url_for('signin'))
    return render_template('signup.html', msg=msg, msg1=msg1, notify=notify, msg2=msg2)

# Account Profile module for testing
@app.route('/details', methods = ["GET", "POST"])
def details():
    if request.method == "GET":
        all_details = mycol.find()
        return render_template('details.html', all_details = all_details)

# Signin Page module
@app.route('/signin', methods = ["POST", "GET"])
def signin():
    msg = None
    msg1 = None
    if request.method == "POST":
        s_gmail = request.form.get('s_gmail')            
        s_pswd = request.form.get('s_pswd')
        user = mycol.find_one({'gmail': s_gmail})
        if user and user['pswd'] == s_pswd:
            session['user_data'] = user
            return redirect(url_for('index'))
        else:
            msg = "Enter mail or password is not matched"
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
        user = mycol.find_one({'gmail': f_gmail})
        if user:
            p = request.form['p']
            if len(p) < 8:
                msg1 = "Password must contain 8 character"
            else:
                f_pswd = request.form['f_pswd']
            if (f_pswd != p):
                msg2 = "Password not matched"
            else:
                rg.pswd = f_pswd
                mycol.update_one({'gmail': f_gmail}, {'$set':{
                    'pswd': f_pswd
                }})
                return redirect(url_for('signin'))
        else:
            msg = "Please enter a valid mail-id"
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
        self.bmail = ""
        self.amount = 0
        self.acn = 0

gr = GORA()

# Account Creation Module
# Account Creation Module
@app.route('/account_creation', methods = ["POST", "GET"])
def account_creation():
    msg = None
    msg1 = None
    msg2 = None
    msg3 = None
    msg4 = None
    if request.method == "POST":
        print(request.form)  # Add this line to check form data
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
        else:
            gr.pin = request.form.get('pin')
            if gr.pin != p:
                msg1 = "Pin not matched with each other"
            else:
                gr.bmail = request.form['b_mail']  # Check here
                user = mycol.find_one({'gmail': gr.bmail})
                if user:
                    gr.amount = int(request.form.get('amount'))
                    if gr.amount < 1000:
                        msg2 = "For account creation initial deposit amount is 1000"
                    else:
                        msg3 = f"{gr.pin} is your account pin"
                        msg4 = "Account has been created successfully"
                    mydoc={
                        'Name': gr.name,
                        'Father_Name': gr.father_name,
                        'DOB': gr.dob,
                        'Gender': gr.gender,
                        'Mbno': gr.mbno,
                        'Account_Number': gr.acn,
                        'Pin': gr.pin,
                        'Amount': gr.amount
                    }
                    mycol.update_one({'gmail': gr.bmail}, {'$set': mydoc})
    return render_template('account_creation.html', msg=msg, msg1=msg1,
                           msg2=msg2, msg3=msg3, msg4=msg4)


# Account Holder's Profile Module
@app.route('/profile', methods = ["GET"])
def profile():
    if request.method == 'GET':
        user_data = session.get('user_data')
        return render_template('profile.html', user_data=user_data)


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