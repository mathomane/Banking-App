import mysql.connector
import datetime
import time

class BankSystem:
    
    #constructor
    def _init_(self,server,user,pwd,db) -> None:
        self.server = server
        self.user = user
        self.pwd = pwd
        self.db = db
        self.con = mysql.connector.connect(host = server, username = user, password  = pwd, database = db)
        
        # Current Date and Time(timestamp)
        def time_stamp(self):
            timeStamp = datetime.datetime.now()
            return timeStamp
        
        #Wait for user input to return
        def go_back(self):
            back = input("Press ENTER to return")
            print()
            
            #thus is a commet
        

