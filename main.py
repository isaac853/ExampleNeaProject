from flask import Flask, redirect, render_template, request, url_for, session
from scripts.isauthorised import isAuthorised
from database import DatabaseHandler
from blueprints.pages import pages
from blueprints.auth import auth

SECRET_KEY = "thisisabadsecret"

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.register_blueprint(pages)
app.register_blueprint(auth)

db = DatabaseHandler()
db.createTables()

app.run(debug = True)