from cryptography.fernet import Fernet


def load_key(key_file):
    try:
        with open(key_file, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open(key_file, 'wb') as file:
            file.write(key)
        return key


class Encryptor:
    def __init__(self, key_file='key.key'):
        self.key = load_key(key_file)
        self.cipher = Fernet(self.key)

    def encrypt(self, data):
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, data):
        return self.cipher.decrypt(data.encode()).decode()
