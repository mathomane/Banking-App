import datetime
import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import PhotoImage


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
                return False, "Email already used!"
        
        new_user = [name, country, contact, email, password, ac_num, '0']
        data.append(new_user)
        self.write_data(data)
        return True, "Account created successfully."

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
                return True, record
        return False, "Account doesn't exist or wrong credentials."

class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x800")
        self.root.title("Pocket Bank")
        self.bank_system = BankSystem()
        self.logged_in_user = None
        
        self.create_login_screen()
        
    def create_login_screen(self):
        self.clear_screen()
        
        self.root.configure(bg='#fff')
        
        # Add an image (ensure the path is correct and the image exists)
        try:
            image = PhotoImage(file="images/banking-apps_meta_resized.png")
            image_label = tk.Label(self.root, image=image)
            image_label.image = image  # Keep a reference to the image to prevent garbage collection
            image_label.pack()
        except Exception as e:
            print(f"Error loading image: {e}")

        
        tk.Label(self.root, text="User Login", font="poppins").pack(pady=10)
        tk.Label(self.root, text="Email").pack()
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack()
        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show='*')
        self.password_entry.pack()
        
        tk.Button(self.root, text="Sign In", background="#8DD9CC", activebackground="orange", font="poppins", command=self.sign_in).pack(pady=10)
        tk.Button(self.root, text="Create an Account", background="#8DD9CC", activebackground="orange", font="poppins", borderwidth = 8, command=self.create_signup_screen).pack()
        
    def create_signup_screen(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Sign Up", font=("Arial", 18)).pack(pady=10)
        tk.Label(self.root, text="Name").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()
        tk.Label(self.root, text="Country").pack()
        self.country_entry = tk.Entry(self.root)
        self.country_entry.pack()
        tk.Label(self.root, text="Contact No").pack()
        self.contact_entry = tk.Entry(self.root)
        self.contact_entry.pack()
        tk.Label(self.root, text="Email").pack()
        self.email_signup_entry = tk.Entry(self.root)
        self.email_signup_entry.pack()
        tk.Label(self.root, text="Password").pack()
        self.password_signup_entry = tk.Entry(self.root, show='*')
        self.password_signup_entry.pack()
        
        tk.Button(self.root, text="Sign Up", command=self.sign_up).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_login_screen).pack()

    def create_main_menu(self):
        self.clear_screen()
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)

        tk.Label(self.root, text=f"Welcome Mr./Ms. {self.logged_in_user[0].upper()}", font=("poppins")).grid(row=0, column=1, pady=10, sticky='ew')
        tk.Label(self.root, text=f"A/C No.: {self.logged_in_user[5]}").grid(row=1, column=1, pady=5, sticky='ew')

        tk.Button(self.root, text="Check Balance", command=self.check_balance).grid(row=2, column=1, pady=5, sticky='ew')
        tk.Button(self.root, text="Add Money", command=self.add_money).grid(row=3, column=1, pady=5, sticky='ew')
        tk.Button(self.root, text="Withdraw Money", command=self.withdraw_money).grid(row=4, column=1, pady=5, sticky='ew')
        tk.Button(self.root, text="Sign Out", command=self.sign_out).grid(row=5, column=1, pady=20, sticky='ew')
    def sign_in(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        success, result = self.bank_system.sign_in(email, password)
        if success:
            self.logged_in_user = result
            self.create_main_menu()
        else:
            messagebox.showerror("Error", result)

    def sign_up(self):
        name = self.name_entry.get()
        country = self.country_entry.get()
        contact = self.contact_entry.get()
        email = self.email_signup_entry.get()
        password = self.password_signup_entry.get()
        
        success, message = self.bank_system.sign_up(name, country, contact, email, password)
        if success:
            messagebox.showinfo("Success", message)
            self.create_login_screen()
        else:
            messagebox.showerror("Error", message)
    
    def check_balance(self):
        balance = self.bank_system.check_bal(self.logged_in_user[5])
        messagebox.showinfo("Balance", f"Available balance: {balance}")

    def add_money(self):
        self.transaction_screen("Add Money", self.bank_system.add_money)

    def withdraw_money(self):
        self.transaction_screen("Withdraw Money", self.bank_system.withdraw)

    def transaction_screen(self, title, transaction_func):
        self.clear_screen()
        
        tk.Label(self.root, text=title, font=("poppins")).pack(pady=10)
        tk.Label(self.root, text="Amount").pack()
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack()
        
        def perform_transaction():
            amount = float(self.amount_entry.get())
            if transaction_func(self.logged_in_user[5], amount):
                messagebox.showinfo("Success", "Transaction Successful.")
                self.create_main_menu()
            else:
                messagebox.showerror("Error", "Transaction Failed.")
        
        tk.Button(self.root, text="Submit", command=perform_transaction).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_menu).pack()

    def sign_out(self):
        self.logged_in_user = None
        self.create_login_screen()
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()
