import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from pymongo import MongoClient

class StoreManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Store Management System")
        self.root.geometry("400x300")

        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['store']
        self.users = self.db['users']

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.register_frame = tk.Frame(self.notebook)
        self.login_frame = tk.Frame(self.notebook)
        self.dashboard_frame = tk.Frame(self.notebook)

        self.notebook.add(self.register_frame, text="Register")
        self.notebook.add(self.login_frame, text="Login")
        self.notebook.add(self.dashboard_frame, text="Dashboard")

        self.create_registration_page()
        self.create_login_page()
        self.create_dashboard()

    def create_registration_page(self):
        self.username_label_reg = tk.Label(self.register_frame, text="Username:")
        self.username_entry_reg = tk.Entry(self.register_frame)
        self.password_label_reg = tk.Label(self.register_frame, text="Password:")
        self.password_entry_reg = tk.Entry(self.register_frame, show="*")
        self.register_button = tk.Button(self.register_frame, text="Register", command=self.register)

        self.username_label_reg.pack()
        self.username_entry_reg.pack()
        self.password_label_reg.pack()
        self.password_entry_reg.pack()
        self.register_button.pack()

    def create_login_page(self):
        self.username_label_log = tk.Label(self.login_frame, text="Username:")
        self.username_entry_log = tk.Entry(self.login_frame)
        self.password_label_log = tk.Label(self.login_frame, text="Password:")
        self.password_entry_log = tk.Entry(self.login_frame, show="*")
        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)

        self.username_label_log.pack()
        self.username_entry_log.pack()
        self.password_label_log.pack()
        self.password_entry_log.pack()
        self.login_button.pack()

    def create_dashboard(self):
        self.dashboard_label = tk.Label(self.dashboard_frame, text="Dashboard")
        self.dashboard_label.pack()
        self.logout_button = tk.Button(self.dashboard_frame, text="Logout", command=self.logout)
        self.logout_button.pack()

        self.menu_frame = tk.Frame(self.dashboard_frame)
        self.menu_frame.pack(side="left", fill="y")
        self.view_frame = tk.Frame(self.dashboard_frame)
        self.view_frame.pack(side="right", fill="both", expand=True)

        self.list_products_button = tk.Button(self.menu_frame, text="List Products", command=self.list_products)
        self.list_products_button.pack(pady=10)
        self.add_product_button = tk.Button(self.menu_frame, text="Add Product", command=self.add_product)
        self.add_product_button.pack(pady=10)

        # Initially disable the dashboard frame
        self.notebook.tab(2, state="disabled")

    def register(self):
        username = self.username_entry_reg.get()
        password = self.password_entry_reg.get()
        if username and password:
            user_data = {"username": username, "password": password}
            result = self.users.insert_one(user_data)
            if result:
                messagebox.showinfo("Success", "Registration successful!")
                self.notebook.select(self.login_frame)
            else:
                messagebox.showerror("Error", "Failed to register")
        else:
            messagebox.showerror("Error", "Please enter username and password")

    def login(self):
        username = self.username_entry_log.get()
        password = self.password_entry_log.get()
        if username and password:
            user_data = {"username": username, "password": password}
            if self.users.find_one(user_data):
                messagebox.showinfo("Success", "Login successful!")
                self.notebook.select(self.dashboard_frame)
                # Enable the dashboard frame after successful login
                self.notebook.tab(2, state="normal")
            else:
                messagebox.showerror("Error", "Invalid username or password")
        else:
            messagebox.showerror("Error", "Please enter username and password")

    def logout(self):
        self.notebook.select(self.login_frame)
        self.username_entry_log.delete(0, tk.END)
        self.password_entry_log.delete(0, tk.END)
        # Disable the dashboard frame after logout
        self.notebook.tab(2, state="disabled")

    def list_products(self):
        # Functionality to list products goes here
        pass

    def add_product(self):
        # Functionality to add product goes here
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = StoreManagementSystem(root)
    root.mainloop()
