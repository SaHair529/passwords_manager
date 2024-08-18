from gui import PasswordManagerApp
import tkinter as tk


def main():
    root = tk.Tk()
    app = PasswordManagerApp(root)
    app.run()


if __name__ == '__main__':
    main()
