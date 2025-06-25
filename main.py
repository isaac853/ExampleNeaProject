from flask import Flask, redirect, render_template, request, url_for, session
from database import DatabaseHandler

SECRET_KEY = "thisisabadsecret"



app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route("/")
def home():
    return render_template("home.html")
        
@app.route("/dashboard")
def dashboard():
    currentUser = session["currentUser"]
    return render_template("dashboard.html", currentUser = currentUser)

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/auth/authoriseUser", methods = ["POST"])
def authoriseUser():
    formDetails = request.form
    username = formDetails.get("username")
    password = formDetails.get("password")

    db = DatabaseHandler()
    success = db.authoriseUser(username, password)
    if success:
        session["currentUser"] = username
        return redirect(url_for("dashboard")) 
    
    return redirect(url_for("signin"))


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

@app.route("/auth/signout")
def signOut():
    session.clear()
    return redirect(url_for("signin"))

app.run(debug = True)