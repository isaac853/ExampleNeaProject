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
                results = conn.execute("SELECT password FROM users WHERE username = ?", (username,))
                stored_hash = results.fetchone()
                print()
                if userDetails != None:
                    return True
                return False
        
        except:
            return False