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

    def setup_db(self):
        try:
            self.db.createDB()
            self.db.createTable()
            messagebox.showinfo("Setup Complete", "Database and table setup successfully.")
        except Exception as e:
            messagebox.showerror("Setup Failed", f"Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    db = DB("bank_system.txt")
    app = DBApp(root, db)
    root.mainloop()
