import sqlite3 as sql
from werkzeug.security import generate_password_hash, check_password_hash

class DatabaseHandler:
    def __init__(self, dbName = "appData.db"):
        self.dbName = dbName

    def connect(self):
        return sql.connect(self.dbName)
    
    def createTables(self):
        with self.connect() as conn:
            conn.execute(""" CREATE TABLE IF NOT EXISTS users(
                         userID INTEGER PRIMARY KEY AUTOINCREMENT,
                         username TEXT UNIQUE NOT NULL CHECK(length(username) > 2),
                         password TEXT NOT NULL CHECK(length(password) > 7)
                         );""")
            
            conn.execute("""CREATE TABLE IF NOT EXISTS tasks (
                         taskID INTEGER PRIMARY KEY AUTOINCREMENT,
                         userID INTEGER NOT NULL,
                         taskName TEXT NOT NULL CHECK(length(taskName) > 2),
                         taskDescription TEXT NOT NULL,
                         status TEXT DEFAULT "incomplete" CHECK(status IN ("incomplete", "complete")),
                         created TEXT DEFAULT CURRENT_TIMESTAMP,
                         FOREIGN KEY (userID) REFERENCES users(USERID) ON DELETE CASCADE
                         )""")


    def createUser(self, username, password):
        try:
            hashed_password = generate_password_hash(password)
            with self.connect() as conn:
                conn.execute("INSERT INTO users (username, password ) VALUES (?,?)", (username, hashed_password))
                conn.commit()
            return True, None
       
        except sql.IntegrityError as error:
            print(error)
            if "UNIQUE" in str(error):
                return False, "unique-error"
            else:
                return False, "inetgrity-error"
        
        except Exception as error:
            print(error)
            return False, "unknown error"

    def authoriseUser(self, username, password):
        try:
            with self.connect() as conn:
                results = conn.execute("SELECT password, userID FROM users WHERE username = ?", (username,))
                stored_hash, userID = results.fetchone()
                if check_password_hash(stored_hash, password):
                    return True, userID
                else:
                    return False,None

        except:
            return False
        
    def createTask(self, taskName, description, userID):
        try:
            with self.connect() as conn:
                conn.execute("""INSERT INTO tasks
                             (taskName, taskDescription, userID)
                             VALUES
                             (?,?,?)""",(taskName, description, userID))
                conn.commit()
                return True, None
        except:
            return False, "error-unknown"
      
        
    def fetchAllTasks(self, userID):
        try:
            with self.connect() as conn:
                results = conn.execute("""SELECT taskName, TaskDescription, status, created
                             FROM tasks
                             WHERE userID = ?""", (userID,))
                tasks = results.fetchall()
                print(tasks)
        except:
            print("an error occured")
