from flask import Flask, redirect, render_template, request, url_for
from database import DatabaseHandler
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")
        
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/auth/createuser", methods = ["POST"])
def createuser():
    formDetails = request.form
    username = formDetails.get("username")
    password = formDetails.get("password")
    repassword = formDetails.get("repassword")

    if len(username) > 2 and len(password) > 7 and len(repassword) > 7 and password == repassword:
        db = DatabaseHandler()
        success = db.createUser(username, password)
        if success:

            return redirect(url_for("dashboard")) 

    return redirect(url_for("signup"))




app.run(debug = True)