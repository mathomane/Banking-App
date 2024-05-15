import datetime
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

class BankSystem:
    def __init__(self, data_file='users.txt'):
        self.data_file = data_file

    def generate_ac_no(self, name, country):
        name_char_vals = [ord(i) for i in name]
        sum_name_char_vals = sum(name_char_vals)
        base_num = 90036900100000
        ac_no = country[0:2].upper() + str(base_num + sum_name_char_vals)
        return ac_no

    def read_data(self):
        if not os.path.exists(self.data_file):
            return []
        with open(self.data_file, 'r') as file:
            data = file.readlines()
        return [line.strip().split('|') for line in data]

    def write_data(self, data):
        with open(self.data_file, 'w') as file:
            for record in data:
                file.write('|'.join(record) + '\n')

    def sign_up(self, name, country, contact, email, password):
        ac_num = self.generate_ac_no(name, country)
        data = self.read_data()
        for record in data:
            if record[3] == email:
                messagebox.showerror("Error", "Email already used!")
                return False
        
        new_user = [name, country, contact, email, password, ac_num, '0']
        data.append(new_user)
        self.write_data(data)
        messagebox.showinfo("Success", "Account created successfully.")
        return True

    def check_bal(self, ac_no):
        data = self.read_data()
        for record in data:
            if record[5] == ac_no:
                return float(record[6])
        return 0.0

    def update_balance(self, ac_no, new_balance):
        data = self.read_data()
        for record in data:
            if record[5] == ac_no:
                record[6] = str(new_balance)
        self.write_data(data)

    def add_money(self, ac_no, amount):
        balance = self.check_bal(ac_no)
        new_balance = balance + amount
        self.update_balance(ac_no, new_balance)
        return True

    def withdraw(self, ac_no, amount):
        balance = self.check_bal(ac_no)
        if balance >= amount:
            new_balance = balance - amount
            self.update_balance(ac_no, new_balance)
            return True
        return False

    def sign_in(self, email, password):
        data = self.read_data()
        for record in data:
            if record[3] == email and record[4] == password:
                return record
        return None


class App:
    def __init__(self, root):
        self.bank_system = BankSystem()
        self.root = root
        self.root.title("Mini Bank System")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20)

        self.login_screen()

    def login_screen(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="User Login", font=('Arial', 16)).pack(pady=10)
        tk.Label(self.main_frame, text="Username").pack()
        self.username_entry = tk.Entry(self.main_frame)
        self.username_entry.pack()

        tk.Label(self.main_frame, text="Password").pack()
        self.password_entry = tk.Entry(self.main_frame, show="*")
        self.password_entry.pack()

        tk.Button(self.main_frame, text="Login", command=self.login).pack(pady=5)
        tk.Button(self.main_frame, text="Create Account", command=self.create_account_screen).pack(pady=5)

    def create_account_screen(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Create Account", font=('Arial', 16)).pack(pady=10)
        
        tk.Label(self.main_frame, text="Name").pack()
        self.name_entry = tk.Entry(self.main_frame)
        self.name_entry.pack()

        tk.Label(self.main_frame, text="Country").pack()
        self.country_entry = tk.Entry(self.main_frame)
        self.country_entry.pack()

        tk.Label(self.main_frame, text="Contact").pack()
        self.contact_entry = tk.Entry(self.main_frame)
        self.contact_entry.pack()

        tk.Label(self.main_frame, text="Email").pack()
        self.email_entry = tk.Entry(self.main_frame)
        self.email_entry.pack()

        tk.Label(self.main_frame, text="Password").pack()
        self.password_entry_create = tk.Entry(self.main_frame, show="*")
        self.password_entry_create.pack()

        tk.Button(self.main_frame, text="Sign Up", command=self.create_account).pack(pady=5)
        tk.Button(self.main_frame, text="Back to Login", command=self.login_screen).pack(pady=5)

    def create_account(self):
        name = self.name_entry.get()
        country = self.country_entry.get()
        contact = self.contact_entry.get()
        email = self.email_entry.get()
        password = self.password_entry_create.get()

        if not name or not country or not contact or not email or not password:
            messagebox.showerror("Error", "All fields are required")
            return
        
        if self.bank_system.sign_up(name, country, contact, email, password):
            self.login_screen()

    def login(self):
        email = self.username_entry.get()
        password = self.password_entry.get()

        user = self.bank_system.sign_in(email, password)
        if user:
            self.user_dashboard(user)
        else:
            messagebox.showerror("Error", "Invalid login credentials")

    def user_dashboard(self, user):
        self.clear_frame()
        self.current_user = user
        tk.Label(self.main_frame, text=f"Welcome Mr. {user[0].upper()}", font=('Arial', 16)).pack(pady=10)
        tk.Label(self.main_frame, text=f"A/C No.: {user[5]}").pack()

        tk.Button(self.main_frame, text="Check Balance", command=self.check_balance).pack(pady=5)
        tk.Button(self.main_frame, text="Add Money", command=self.add_money).pack(pady=5)
        tk.Button(self.main_frame, text="Withdraw Money", command=self.withdraw_money).pack(pady=5)
        tk.Button(self.main_frame, text="Sign Out", command=self.login_screen).pack(pady=5)

    def check_balance(self):
        balance = self.bank_system.check_bal(self.current_user[5])
        messagebox.showinfo("Balance", f"Available balance: {balance}")

    def add_money(self):
        amount = simpledialog.askfloat("Add Money", "Enter amount to add:")
        if amount is not None:
            self.bank_system.add_money(self.current_user[5], amount)
            messagebox.showinfo("Success", "Transaction Successful")

    def withdraw_money(self):
        amount = simpledialog.askfloat("Withdraw Money", "Enter amount to withdraw:")
        if amount is not None:
            if self.bank_system.withdraw(self.current_user[5], amount):
                messagebox.showinfo("Success", "Transaction Successful")
            else:
                messagebox.showerror("Error", "Insufficient balance")

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

# this is the end of the app
