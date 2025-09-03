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



@tasks.route("/get/<int:taskID>")
def getTaskByID(taskID):
    return "getting a task by for task ID " + str(taskID)

@tasks.route("/update/<int:taskID>")
def updateTask(taskID):
    return "updating task " + str(taskID)

@tasks.route("/updateStatus/<int:taskID>", methods = ["post"])
def updateStatus(taskID):
    
    db = DatabaseHandler()
    userID = session["userID"]
    formData = request.form
    status = formData.get("status")

    if status == "incomplete":
        newStatus = "complete"
    else:
        newStatus = "incomplete"

    success = db.updateStatus(taskID, userID, newStatus)


    if not success:
        flash("task not updated successfully")

    return redirect(url_for("pages.dashboard"))

@tasks.route("/delete/<int:taskID>", methods = ["post"])
def deleteTask(taskID):

    db = DatabaseHandler()
    userID = session["userID"]
    success = db.deleteTask(taskID,userID)

    if not success:
        flash("Task not deleted")
    else: 
        flash("task deleted succesfully")

    return redirect(url_for("pages.dashboard"))