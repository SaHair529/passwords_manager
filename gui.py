# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from db_manager import DBManager


def select_all(event):
    event.widget.select_range(0, tk.END)
    event.widget.icursor(tk.END)
    return "break"


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
        self.search_entry.bind("<Control-a>", select_all)  # Привязка Ctrl+A
        self.search_entry.bind("<Control-Shift-C>", self.copy_password_if_one_result)  # Привязка Ctrl+Shift+C
        self.search_entry.focus_set()

        # Список результатов
        self.results_listbox = tk.Listbox(root, width=80, height=15)
        self.results_listbox.pack(pady=10)
        self.results_listbox.bind("<<ListboxSelect>>", self.on_select)

        # Поля для ввода/редактирования паролей
        self.website_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        ttk.Label(root, text="Website:").pack(pady=2)
        self.website_entry = ttk.Entry(root, textvariable=self.website_var, width=50)
        self.website_entry.pack(pady=2)
        self.website_entry.bind("<Control-a>", select_all)  # Привязка Ctrl+A

        ttk.Label(root, text="Username:").pack(pady=2)
        self.username_entry = ttk.Entry(root, textvariable=self.username_var, width=50)
        self.username_entry.pack(pady=2)
        self.username_entry.bind("<Control-a>", select_all)  # Привязка Ctrl+A

        ttk.Label(root, text="Password:").pack(pady=2)
        self.password_entry = ttk.Entry(root, textvariable=self.password_var, width=50)
        self.password_entry.pack(pady=2)
        self.password_entry.bind("<Control-a>", select_all)  # Привязка Ctrl+A

        # Кнопки для добавления, редактирования и удаления паролей
        self.add_button = ttk.Button(root, text="Add Password", command=self.add_password)
        self.add_button.pack(pady=5)

        self.update_button = ttk.Button(root, text="Update Password", command=self.update_password)
        self.update_button.pack(pady=5)

        self.delete_button = ttk.Button(root, text="Delete Password", command=self.delete_password)
        self.delete_button.pack(pady=5)

        # Кнопка для копирования пароля в буфер обмена
        self.copy_button = ttk.Button(root, text="Copy Password", command=self.copy_password)
        self.copy_button.pack(pady=5)

        self.selected_record = None

    def update_search_results(self, *args):
        query = self.search_var.get()
        results = self.db.search_passwords(query)
        self.results_listbox.delete(0, tk.END)
        for site, user, passw in results:
            self.results_listbox.insert(tk.END, f"Website: {site}, Username: {user}, Password: {passw}")
        self.current_results = results

    def on_select(self, event):
        try:
            index = self.results_listbox.curselection()[0]
            selected_text = self.results_listbox.get(index)
            site, user, passw = selected_text.split(", ")
            self.website_var.set(site.split(": ")[1])
            self.username_var.set(user.split(": ")[1])
            self.password_var.set(passw.split(": ")[1])
            self.selected_record = (site.split(": ")[1], user.split(": ")[1])
        except IndexError:
            pass

    def add_password(self):
        website = self.website_var.get()
        username = self.username_var.get()
        password = self.password_var.get()

        if website and username and password:
            self.db.add_password(website, username, password)
            self.clear_fields()
            messagebox.showinfo("Success", "Password added successfully!")
            self.update_search_results()
        else:
            messagebox.showwarning("Input Error", "Please fill out all fields.")

    def update_password(self):
        if self.selected_record:
            website = self.website_var.get()
            username = self.username_var.get()
            password = self.password_var.get()

            if website and username and password:
                old_site, old_user = self.selected_record
                self.db.update_password(old_site, old_user, website, username, password)
                self.clear_fields()
                messagebox.showinfo("Success", "Password updated successfully!")
                self.update_search_results()
            else:
                messagebox.showwarning("Input Error", "Please fill out all fields.")
        else:
            messagebox.showwarning("Selection Error", "Please select a record to update.")

    def delete_password(self):
        if self.selected_record:
            old_site, old_user = self.selected_record
            self.db.delete_password(old_site, old_user)
            self.clear_fields()
            messagebox.showinfo("Success", "Password deleted successfully!")
            self.update_search_results()
        else:
            messagebox.showwarning("Selection Error", "Please select a record to delete.")

    def copy_password(self):
        if self.selected_record:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.password_var.get())
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Selection Error", "Please select a record to copy.")

    def copy_password_if_one_result(self, event):
        if len(self.current_results) == 1:
            site, user, passw = self.current_results[0]
            self.root.clipboard_clear()
            self.root.clipboard_append(passw)
            messagebox.showinfo("Success", f"Password for {site} copied to clipboard!")
            self.root.quit()
        else:
            messagebox.showwarning("Search Error", "Please narrow down your search to one result.")
        return "break"

    def clear_fields(self):
        self.website_var.set("")
        self.username_var.set("")
        self.password_var.set("")
        self.selected_record = None

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    app.run()
