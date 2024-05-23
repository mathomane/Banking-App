import time
import tkinter as tk
from tkinter import messagebox, simpledialog
import os

class DB:
    def __init__(self, db_file) -> None:
        self.db_file = db_file
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as db:
                db.write("Name,Country,Contact,Email,Password,AccountNo,CurrentBalance\n")

    def createDB(self):
        with open(self.db_file, 'w') as db:
            db.write("Name,Country,Contact,Email,Password,AccountNo,CurrentBalance\n")

    def createTable(self):
        # In text file implementation, table creation is handled in createDB
        pass

    def read_data(self):
        if not os.path.exists(self.db_file):
            return []
        with open(self.db_file, 'r') as file:
            data = file.readlines()
        return [line.strip().split(',') for line in data][1:]  # Exclude header

    def write_data(self, data):
        with open(self.db_file, 'w') as file:
            file.write("Name,Country,Contact,Email,Password,AccountNo,CurrentBalance\n")
            for record in data:
                file.write(','.join(record) + '\n')

    def update_balance(self, ac_no, new_balance):
        data = self.read_data()
        for record in data:
            if record[5] == ac_no:
                record[6] = str(new_balance)
        self.write_data(data)

    def check_bal(self, ac_no):
        data = self.read_data()
        for record in data:
            if record[5] == ac_no:
                return float(record[6])
        return 0.0

# Tkinter GUI Implementation
class DBApp:
    def __init__(self, root, db):
        self.db = db
        self.root = root
        self.root.title("Pocket Bank Setup")
        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.lbl_welcome = tk.Label(self.frame, text="Welcome to Pocket Bank Setup")
        self.lbl_welcome.pack()

        self.btn_setup = tk.Button(self.frame, text="Setup Database", command=self.setup_db)
        self.btn_setup.pack()

        self.btn_transaction = tk.Button(self.frame, text="Make a Transaction", command=self.transaction_prompt)
        self.btn_transaction.pack()

    def setup_db(self):
        try:
            self.db.createDB()
            self.db.createTable()
            messagebox.showinfo("Setup Complete", "Database and table setup successfully.")
        except Exception as e:
            messagebox.showerror("Setup Failed", f"Error: {e}")

    def transaction_prompt(self):
        ac_no = simpledialog.askstring("Account Number", "Enter your Account Number:")
        if not ac_no:
            return

        balance = self.db.check_bal(ac_no)
        if balance == 0.0:
            messagebox.showerror("Error", "Account not found.")
            return

        if messagebox.askyesno("Transaction", "Would you like to make a transaction?"):
            if messagebox.askyesno("Transaction Type", "Would you like to make a deposit? (No for withdrawal)"):
                self.transaction_screen(balance, "Deposit", self.db.update_balance, True)
            else:
                self.transaction_screen(balance, "Withdraw", self.db.update_balance, False)
        else:
            messagebox.showinfo("Info", "Transaction canceled.")

    def transaction_screen(self, balance, transaction_type, transaction_func, is_deposit):
        self.clear_screen()

        tk.Label(self.root, text=f"Current Balance: {balance}", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(self.root, text="Amount").pack()
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack()
        
        def perform_transaction():
            try:
                amount = float(self.amount_entry.get())
                if amount <= 0:
                    raise ValueError("Amount must be greater than zero.")
                
                if is_deposit:
                    new_balance = balance + amount
                else:
                    if amount > balance:
                        messagebox.showerror("Error", "Insufficient funds for withdrawal.")
                        return
                    new_balance = balance - amount

                transaction_func(ac_no, new_balance)
                messagebox.showinfo("Success", f"{transaction_type} successful. New balance: {new_balance}")
            except ValueError:
                messagebox.showerror("Error", "You provided an invalid input.")
            self.create_widgets()
        
        tk.Button(self.root, text="Submit", command=perform_transaction).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_widgets).pack()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    db = DB("bank_system.txt")
    app = DBApp(root, db)
    root.mainloop()
