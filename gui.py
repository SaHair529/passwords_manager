import tkinter as tk
from tkinter import ttk
from db_manager import DBManager


class PasswordManagerApp:
    def __init__(self, rooot):
        self.db = DBManager()

        self.root = rooot
        self.root.title("Password Manager")

        # Поле поиска
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.update_search_results)
        self.search_entry = ttk.Entry(rooot, textvariable=self.search_var, width=50)
        self.search_entry.pack(pady=10)

        # Список результатов
        self.results_listbox = tk.Listbox(rooot, width=80, height=20)
        self.results_listbox.pack(pady=10)

    def update_search_results(self, *args):
        query = self.search_var.get()
        results = self.db.search_password(query)
        self.results_listbox.delete(0, tk.END)
        for site, user, passw in results:
            self.results_listbox.insert(tk.END, f"{site} - {user} - {passw}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    app.run()
