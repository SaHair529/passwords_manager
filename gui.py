# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from db_manager import DBManager


class PasswordManagerApp:
    def __init__(self, root):
        self.db = DBManager()

        self.root = root
        self.root.title("Password Manager")

        # Поле поиска
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.update_search_results)
        self.search_entry = ttk.Entry(root, textvariable=self.search_var, width=50)
        self.search_entry.pack(pady=10)

        # Список результатов
        self.results_listbox = tk.Listbox(root, width=80, height=15)
        self.results_listbox.pack(pady=10)

        # Поля для ввода новых паролей
        self.website_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        ttk.Label(root, text="Website:").pack(pady=2)
        self.website_entry = ttk.Entry(root, textvariable=self.website_var, width=50)
        self.website_entry.pack(pady=2)

        ttk.Label(root, text="Username:").pack(pady=2)
        self.username_entry = ttk.Entry(root, textvariable=self.username_var, width=50)
        self.username_entry.pack(pady=2)

        ttk.Label(root, text="Password:").pack(pady=2)
        self.password_entry = ttk.Entry(root, textvariable=self.password_var, width=50)
        self.password_entry.pack(pady=2)

        # Кнопка добавления пароля
        self.add_button = ttk.Button(root, text="Add Password", command=self.add_password)
        self.add_button.pack(pady=10)

    def update_search_results(self, *args):
        query = self.search_var.get()
        results = self.db.search_password(query)
        self.results_listbox.delete(0, tk.END)
        for site, user, passw in results:
            self.results_listbox.insert(tk.END, f"Website: {site}, Username: {user}, Password: {passw}")

    def add_password(self):
        website = self.website_var.get()
        username = self.username_var.get()
        password = self.password_var.get()

        if website and username and password:
            self.db.add_password(website, username, password)
            self.website_var.set("")
            self.username_var.set("")
            self.password_var.set("")
            messagebox.showinfo("Success", "Password added successfully!")
            self.update_search_results()
        else:
            messagebox.showwarning("Input Error", "Please fill out all fields.")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    app.run()
