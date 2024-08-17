import sqlite3
from encryptor import Encryptor


class DBManager:
    def __init__(self, db_file='passwords.db'):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.encryptor = Encryptor()

        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
        ''')
        self.connection.commit()

    def add_password(self, website, username, password):
        encrypted_password = self.encryptor.encrypt(password)
        self.cursor.execute('''
        INSERT INTO passwords (website, username, password)
        VALUES (?, ?, ?)
        ''', (website, username, encrypted_password))
        self.connection.commit()

    def search_password(self, query):
        query = f"%{query}%"
        self.cursor.execute('''
        SELECT website, username, password FROM passwords
        WHERE website LIKE ? OR username LIKE ? OR password LIKE ?
        ''', (query, query, query))
        results = self.cursor.fetchall()
        return [(site, user, self.encryptor.decrypt(passw)) for site, user, passw in results]

    def close(self):
        self.connection.close()
