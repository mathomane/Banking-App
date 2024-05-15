import mysql.connector
import datetime
import time

class BankSystem:
    
    # Constructor
    def __init__(self, server, user, pwd, db) -> None:
        self.server = server
        self.user = user
        self.pwd = pwd
        self.db = db
        self.con = mysql.connector.connect(host=server, user=user, password=pwd, database=db)
    
    # Current Date and Time (timestamp)
    def time_stamp(self):
        timeStamp = datetime.datetime.now()
        return timeStamp

    # Wait for user input to return
    def go_back(self):
        input("Press ENTER to return")
        print()

    # Function to generate an account number for user
    def generate_ac_no(self, name, country):
        name_char_vals = [ord(i) for i in name]
        sum_name_char_vals = sum(name_char_vals)
        base_num = 90036900100000
        ac_no = country[0:2].upper() + str(base_num + sum_name_char_vals)
        return ac_no

    # Function for creating a new account
    def sign_up(self):
        name = input("Enter your name: ")
        country = input("Enter your country name: ")
        contact = input("Enter your contact no.: ")
        email = input("Enter your email address: ")
        password = input("Enter your password: ")
        ac_num = self.generate_ac_no(name, country)
        
        query1 = f"SELECT * FROM users WHERE Email = '{email}'"
        c = self.con.cursor()
        c.execute(query1)
        found = [i for i in c]
        if len(found) == 0:
            query2 = f"INSERT INTO users (Name, Country, Contact, Email, Password, AccountNo, CurrentBalance) VALUES ('{name}', '{country}', '{contact}', '{email}', '{password}', '{ac_num}', 0);"
            c.execute(query2)
            self.con.commit()

            # Create table for handling transaction details for an account
            query3 = f"CREATE TABLE {ac_num} (SNo INT AUTO_INCREMENT, Credit FLOAT DEFAULT 0, Debit FLOAT DEFAULT 0, Balance FLOAT NOT NULL, Remarks VARCHAR(30) DEFAULT 'None', TransactionTime DATETIME, PRIMARY KEY(SNo));"
            c.execute(query3)
            self.con.commit()
            c.close()
            print("Account created successfully.")
            self.go_back()
        else:
            print("Email already used!")
            self.go_back()

    # Function for checking current account balance
    def check_bal(self, ac_no):
        query1 = f"SELECT CurrentBalance FROM users WHERE AccountNo='{ac_no}';"
        c = self.con.cursor()
        c.execute(query1)
        balance = 0
        for i in c:
            balance = float(i[0])
        c.close()
        return balance

    # Function for adding money into the account
    def add_money(self, ac_no, balance, amount):
        try:
            query1 = f"INSERT INTO {ac_no} (Credit, Balance, TransactionTime) VALUES ({amount}, {balance + amount}, '{self.time_stamp()}');"
            query2 = f"UPDATE users SET CurrentBalance={balance + amount} WHERE AccountNo='{ac_no}';"
            c = self.con.cursor()
            c.execute(query1)
            self.con.commit()
            c.execute(query2)
            self.con.commit()
            c.close()
            return True
        except Exception as e:
            print(f"Invalid value! Error: {e}")
            return False

    # Function for withdrawing money from the account
    def withdraw(self, ac_no, balance, amount):
        try:
            if balance > amount:
                query1 = f"INSERT INTO {ac_no} (Debit, Balance, TransactionTime) VALUES ({amount}, {balance - amount}, '{self.time_stamp()}');"
                query2 = f"UPDATE users SET CurrentBalance={balance - amount} WHERE AccountNo='{ac_no}';"
                c = self.con.cursor()
                c.execute(query1)
                self.con.commit()
                c.execute(query2)
                self.con.commit()
                c.close()
                return True
            else:
                print("Oops! Insufficient balance.")
                return False
        except Exception as e:
            print(f"Invalid value! Error: {e}")
            return False

    # Function for viewing transaction details
    def view_transactions(self, ac_no):
        query1 = f"DESCRIBE {ac_no};"
        query2 = f"SELECT * FROM {ac_no} ORDER BY TransactionTime DESC;"
        c = self.con.cursor()
        c.execute(query1)
        for i in c:
            print(i[0], end=" ")
        print()
        c.execute(query2)
        for i in c:
            print(i[0], i[1], i[2], i[3], i[4], i[5], sep=" | ")
        c.close()

    # Function for resetting user account password
    def reset_pwd(self, ac_no):
        current_pwd = input("Enter your current password: ")
        query1 = f"SELECT * FROM users WHERE AccountNo = '{ac_no}';"
        c = self.con.cursor()
        c.execute(query1)
        found = [i for i in c]
        if current_pwd == found[0][4]:
            new_pwd = input("Enter new password: ")
            confirm_pwd = input("Confirm password: ")
            if new_pwd == confirm_pwd:
                query2 = f"UPDATE users SET Password= '{new_pwd}' WHERE AccountNo = '{ac_no}'"
                c.execute(query2)
                self.con.commit()
                print("Password Changed Successfully!")
            else:
                print("Passwords do not match. Try Again.")
        else:
            print("Incorrect current password.")
        c.close()

    # Function for sending money to another account
    def send_money(self, ac_no, balance, amount):
        if amount <= balance:
            print("1. Via Contact Number\n2. Via Account Number")
            try:
                inp = int(input("Enter your choice: "))
                if inp == 1:
                    receiver_contact = input("Enter receiver's contact number: ")
                    query1 = f"SELECT * FROM users WHERE Contact='{receiver_contact}';"
                    c = self.con.cursor()
                    c.execute(query1)
                    found = [i for i in c]
                    if len(found) == 1:
                        receiver_ac = found[0][5]
                        receiver_bal = float(found[0][6])
                        confirm = input(f"Type 'CONFIRM' to send {amount} to {found[0][0]}: ")
                        if confirm.upper() == "CONFIRM":
                            if self.withdraw(ac_no, balance, amount):
                                query2 = f"UPDATE {ac_no} SET Remarks='TFR to {found[0][0]}' WHERE Balance={self.check_bal(ac_no)};"
                                c.execute(query2)
                                self.con.commit()
                                self.add_money(receiver_ac, receiver_bal, amount)
                                query3 = f"UPDATE {receiver_ac} SET Remarks='Recv From {ac_no}' WHERE Balance={self.check_bal(receiver_ac)};"
                                c.execute(query3)
                                self.con.commit()
                                print("Transaction Successful.")
                            else:
                                print("Transaction Failed!")
                    else:
                        print("Receiver not found.")
                    
                elif inp == 2:
                    receiver_ac_no = input("Enter receiver's account number: ")
                    query1 = f"SELECT * FROM users WHERE AccountNo='{receiver_ac_no}';"
                    c = self.con.cursor()
                    c.execute(query1)
                    found = [i for i in c]
                    if len(found) == 1:
                        receiver_ac = found[0][5]
                        receiver_bal = float(found[0][6])
                        confirm = input(f"Type 'CONFIRM' to send {amount} to {found[0][0]}: ")
                        if confirm.upper() == "CONFIRM":
                            if self.withdraw(ac_no, balance, amount):
                                query2 = f"UPDATE {ac_no} SET Remarks='TFR to {found[0][0]}' WHERE Balance={self.check_bal(ac_no)};"
                                c.execute(query2)
                                self.con.commit()
                                self.add_money(receiver_ac, receiver_bal, amount)
                                query3 = f"UPDATE {receiver_ac} SET Remarks='Recv From {ac_no}' WHERE Balance={self.check_bal(receiver_ac)};"
                                c.execute(query3)
                                self.con.commit()
                                print("Transaction Successful.")
                            else:
                                print("Transaction Failed!")
                    else:
                        print("Receiver not found.")
                else:
                    print("Invalid input!")
            except Exception as e:
                print(f"Invalid value! Error: {e}")
        else:
            print("Oops! Insufficient balance.")

    # Function for getting access to the user account
    def sign_in(self):
        c = self.con.cursor()
        email = input("Enter your email: ")
        # Easter egg
        if email.lower() == "iamaqib":
            query = f"SELECT * FROM users;"
            c.execute(query)
            for data in c:
                print(data)
            self.go_back()
        else:
            password = input("Enter your password: ")
            query1 = f"SELECT * FROM users WHERE Email='{email}' AND Password='{password}';"
            c.execute(query1)
            found = [i for i in c]
            if len(found) != 0:
                while True:
                    print(f"Welcome Mr. {found[0][0].upper()}")
                    ac_no = found[0][5]
                    print(f"A/C No.: {ac_no}")
                    print("="*30)
                    print("1. Check Balance\n2. Add money\n3. Withdraw money\n4. Send money\n5. View Transaction Details\n6. Reset Password\n7. Sign Out")
                    try:
                        op = int(input("Enter your choice: "))
                        balance = self.check_bal(ac_no)
                        if op == 1:
                            print(f"Available balance: {balance}")
                            self.go_back()
                        elif op == 2:
                            try:
                                amount = float(input("Enter amount to add: "))
                                if self.add_money(ac_no, balance, amount):
                                    print("Transaction Successful.")
                                    self.go_back()
                            except:
                                print("Invalid value!")
                                self.go_back()
                        elif op == 3:
                            try:
                                amount = float(input("Enter amount to withdraw: "))
                                if self.withdraw(ac_no, balance, amount):
                                    print("Transaction Successful.")
                                    self.go_back()
                                else:
                                    print("Oops! Insufficient balance.")
                                    self.go_back()
                            except:
                                print("Invalid value!")
                                self.go_back()
                        elif op == 4:
                            try:
                                amount = float(input("Enter amount: "))
                                self.send_money(ac_no, balance, amount)
                                self.go_back()
                            except:
                                print("Invalid value!")
                                self.go_back()
                        elif op == 5:
                            self.view_transactions(ac_no)
                            self.go_back()
                        elif op == 6:
                            self.reset_pwd(ac_no)
                            self.go_back()
                        elif op == 7:
                            print("Signed out.")
                            self.go_back()
                            break
                        else:
                            print("Invalid value!")
                            self.go_back()
                    except:
                        print("Invalid value!")
                        self.go_back()
            else:
                print("Account doesn't exist!")
                print("\n1. Create new account\n2. Main menu")
                new_acc = int(input("Enter your choice: "))
                if new_acc == 1:
                    self.sign_up()
                elif new_acc == 2:
                    pass
                else:
                    print("Invalid value!")
                    self.go_back()

    # Close connection
    def close_connection(self):
        self.con.close()

# MAIN
heading = "========== Mini Bank System =========="
for i in heading:
    print(i, end="", flush=True)
    time.sleep(0.05)
time.sleep(1)
print("\nUSER LOGIN")
username = input("\tEnter username: ")
password = input("\tEnter password: ")
print("Please Wait! Connecting to DATABASE", end="")
for i in "...":
    print(i, end="", flush=True)
    time.sleep(0.5)
time.sleep(0.5)
print()
try:
    BankSys = BankSystem("localhost", username, password, "bank")
    print("Successfully Connected!")
    while True:
        print("="*10 + " Welcome to Mini Bank " + "="*10)
        try:
            print("1. Sign in\n2. Create an account\n3. Exit")
            ch = int(input("Enter your choice: "))
            if ch == 1:
                BankSys.sign_in()
            elif ch == 2:
                BankSys.sign_up()
            elif ch == 3:
                BankSys.close_connection()
                break
            else:
                print("Invalid choice.")
                BankSys.go_back()
        except Exception as e:
            print(f"Invalid value. Error: {e}")
            BankSys.go_back()
    print("Thanks for using this program.")
    input("Press ENTER ")
except Exception as e:
    print(f"Oops! An error occurred. Check login credentials. Error: {e}")
    input("Press ENTER ")


            
        

