import db
import json
import random
import smtplib
from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)

otp = 0
email_address = "ghostdetectorteam@gmail.com"
email_password = "kamalkrisna"

@app.route('/', methods = ['GET', 'POST'])
def home():
    return 'Hello World'

@app.route("/otp", methods = ['GET', 'POST'])
def otp():
    global otp

    if request.method == "POST":
        otp = random.randint(100000, 999999)
        email = request.form['email']
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=email_address, password=email_password)
            connection.sendmail(
                from_addr=email_address,
                to_addrs=email,
                msg=f"subject:Your signup OTP \n\n {otp}")
    else:   
        pass
    
    return 'OTP'
    

@app.route('/signin', methods = ['GET', 'POST'])
def signin():
    status, username = db.check_user()
    
    data = {
        "username": username,
        "status": status
    }
    
    return json.dumps(data)

@app.route('/register', method = ['GET', 'POST'])
def register():
    status = db.insert_data()
    return json.dumps(status)


@app.route('/forgetpassword', methods = ['GET', 'POST'])
def forgetpass():
    username = db.check_user()

    if request.method == "POST":
        email = request.form['email']
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=email_address, password=email_password)
            connection.sendmail(
                from_addr=email_address,
                to_addrs=email,
                msg=f"subject:Forget pass? \n\n ")
            update = db.insert_data()
    else:   
        return 'EMAIL NOT FOUND!'

if __name__ == "__main__":
    app.run(debug=True)