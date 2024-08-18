# db_manager.py
import sqlite3
from encryptor import Encryptor


class DBManager:
    def __init__(self, db_file='passwords.db'):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.encryptor = Encryptor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS passwords (
                                website TEXT,
                                username TEXT,
                                password TEXT)''')
        self.conn.commit()

    def add_password(self, website, username, password):
        encrypted_password = self.encryptor.encrypt(password)
        self.cursor.execute("INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)",
                            (website, username, encrypted_password))
        self.conn.commit()

    def search_passwords(self, query):
        query = f"%{query}%"
        self.cursor.execute("SELECT website, username, password FROM passwords WHERE website LIKE ? OR username LIKE ?",
                            (query, query))
        results = self.cursor.fetchall()
        return [(site, user, self.encryptor.decrypt(passw)) for site, user, passw in results]

    def update_password(self, old_site, old_user, new_site, new_user, new_password):
        encrypted_password = self.encryptor.encrypt(new_password)
        self.cursor.execute(
            "UPDATE passwords SET website = ?, username = ?, password = ? WHERE website = ? AND username = ?",
            (new_site, new_user, encrypted_password, old_site, old_user))
        self.conn.commit()

    def delete_password(self, site, user):
        self.cursor.execute("DELETE FROM passwords WHERE website = ? AND username = ?", (site, user))
        self.conn.commit()

    def close(self):
        self.conn.close()
