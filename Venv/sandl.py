from flask import Flask, render_template, request
app = Flask(__name__)

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
    notify = None
    if request.method == "POST":
        rg.fname = request.form.get('fname')
        rg.lname = request.form.get('lname')
        rg.gmail = request.form.get('gmail')
        p = request.form.get('p')
        if len(p) < 8:
            msg = "Password must contain 8 characters"
        rg.pswd = request.form.get('pswd')
        if rg.pswd != p:
            msg1 = "Password not matched"
        if rg.pswd == p:
            rg.pswd = p
        if (len(p) >= 8) and (rg.pswd == p):
            notify = "User account has created successfully"
    return render_template('signup.html', msg = msg, msg1 = msg1, notify = notify)

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
            msg1 = "Login Successfully"
            return render_template('index.html')
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

if (__name__) == ("__main__"):
    app.run(debug=True)