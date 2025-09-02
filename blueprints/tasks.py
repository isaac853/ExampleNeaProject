#CRUD - create, retrieve, update, delete

from flask import Blueprint, flash, redirect, request, session, url_for

from database import DatabaseHandler

tasks = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks.route("/create", methods = ["post"] )
def createTask():

    #get the task name and description from the form
    formDetails = request.form
    taskName = formDetails.get("taskName")
    description = formDetails.get("description")

    #also need a user ID - session data
    userID = session["userID"]
    errors = False

    #validate allat
    if len(taskName) < 3:
        errors = True
        flash("invalid task name")

    if len(description) < 1:
        errors = True
        flash("invalid task description")

    if errors:
        return redirect(url_for("pages.createTask"))
    
    #if it is valid add it to the database
    db = DatabaseHandler()
    success, errorType = db.createTask(taskName, description, userID)
    
    if success:
        return redirect(url_for("pages.dashboard")) 

    #handle errors and redirect appropriately
    flash("an error occured making the task")
    return redirect(url_for("pages.createTask"))


# @tasks.route("/get")
# def getTasks():
#     return "getting all tasks"

@tasks.route("/get/<int:taskID>")
def getTaskByID(taskID):
    return "getting a task by for task ID " + str(taskID)

@tasks.route("/update/<int:taskID>")
def updateTask(taskID):
    return "updating task " + str(taskID)

@tasks.route("/delete/<int:taskID>")
def deleteTask(taskID):
    return "deleting task " + str(taskID)