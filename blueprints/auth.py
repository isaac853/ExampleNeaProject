from flask import Blueprint, flash, redirect, request, session, url_for

from database import DatabaseHandler

auth = Blueprint("auth", __name__, url_prefix="/auth")

@auth.route("/authoriseUser", methods = ["POST"])
def authoriseUser():
    formDetails = request.form
    username = formDetails.get("username")
    password = formDetails.get("password")

    db = DatabaseHandler()
    success, userID = db.authoriseUser(username, password)
    if success:
        session["currentUser"] = username
        session["userID"] = userID
        return redirect(url_for("pages.dashboard")) 
    
    return redirect(url_for("pages.signin"))


@auth.route("/createuser", methods = ["POST"])
def createuser():
    formDetails = request.form
    username = formDetails.get("username")
    password = formDetails.get("password")
    repassword = formDetails.get("repassword")
    errors = False

    if password != repassword:
        flash("passwords do not match")
        errors = True

    if len(password) < 8:
        flash("password needs to be over 8 characters")
        errors = True

    if len (username) < 3:
        flash("username must be 3 or more characters")
        errors = True

    if errors:
        return redirect(url_for("pages.signup"))



    db = DatabaseHandler()
    success, errorType = db.createUser(username, password)
    if success:

        return redirect(url_for("pages.dashboard")) 

    if errorType == "inetgrity-error":
        flash("invalid data has been entered, please try again")

    elif errorType == "unique-error":
        flash("Username taken, please use another.")

    else:
        flash("an unkown error has occured")
    return redirect(url_for("pages.signup"))

@auth.route("/signout")
def signOut():
    session.clear()
    return redirect(url_for("pages.signin"))