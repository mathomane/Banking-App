import mysql.connector
import time

class DB:
    def __init__(self, server, user, pwd) -> None:
        self.server = server
        self.user = user
        self.pwd = pwd
        self.con = mysql.connector.connect(host=server, user=user, password=pwd)

    def createDB(self):
        query = "CREATE DATABASE IF NOT EXISTS bank;"
        c = self.con.cursor()
        c.execute(query)
        self.con.commit()
        c.close()
    
    def createTable(self, db):
        self.db = db 
        self.con = mysql.connector.connect(host=self.server, user=self.user, password=self.pwd, database=db)
        query1 = (
            "CREATE TABLE IF NOT EXISTS users ("
            "Name VARCHAR(30) UNIQUE NOT NULL, "
            "Country VARCHAR(15) NOT NULL, "
            "Contact VARCHAR(15) UNIQUE NOT NULL, "
            "Email VARCHAR(30) UNIQUE NOT NULL, "
            "Password VARCHAR(16) UNIQUE NOT NULL, "
            "AccountNo CHAR(16) UNIQUE NOT NULL, "
            "CurrentBalance FLOAT NOT NULL, "
            "PRIMARY KEY (AccountNo));"
        )
        c = self.con.cursor()
        c.execute(query1)
        self.con.commit()
        c.close()
        self.con.close()

print("Install MySQL server from https://mysql.com and set up the user account.")
try:
    inp = input("Enter 'DONE' if you've already installed MySQL server or press enter to exit: ")
    if inp.upper() == "DONE":
        # Connect to localhost using username and pwd
        print("Login to connect to the server")
        username = input("\tEnter username: ")
        password = input("\tEnter password: ")
        print("Please Wait! Connecting to the server", end="")
        for i in "...":
            print(i, end="", flush=True)
            time.sleep(1)
        time.sleep(2)
        print()
        try:
            database = DB("localhost", username, password)
            print("Successfully connected to the server!")
            time.sleep(2)
            print("Setting up the database. Please wait", end="")
            for i in "...":
                print(i, end="", flush=True)
                time.sleep(2)
            time.sleep(1)
            print()
            database.createDB()
            database.createTable("bank")
            print("Database successfully created. You can now use Minibank System")
            for i in "Have a nice day:)":
                print(i, end="", flush=True)
                time.sleep(0.05)
            input()
        except mysql.connector.Error as err:
            print(f"Oops! Can't connect to the server! Error: {err}\nPlease check the login credentials and re-run the program.")
            for i in "Have a nice day:)":
                print(i, end="", flush=True)
                time.sleep(0.05)
            print()
            input()
            exit()
    else:
        print("Install the required file from https://mysql.com and re-run the program.")
        for i in "Have a nice day:)":
            print(i, end="", flush=True)
            time.sleep(0.05)
        print()
        input()
except Exception as e:
    print(f"Oops! An error occurred! Exiting the program. Error: {e}")
    for i in "Have a nice day:)":
        print(i, end="", flush=True)
        time.sleep(0.05)
    print()
    input()
    exit()
# this is the end of the app