from cryptography.fernet import Fernet
import os.path


class local_encryption():
    def __init__(self):

        if os.path.exists('secret.dll'):
            print("File exists")
            with open('key.key', 'rb') as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open("key.key", "wb") as f:
                f.write(self.key)

    def encrypt(self):
        f = Fernet(self.key)
        with open("secret.dll", "rb") as file:
            file_data = file.read()
        encrypted_data = f.encrypt(file_data)
        with open("secret.dll", "wb") as file:
            file.write(encrypted_data)

    def decryptlogins(self):
        f = Fernet(self.key)
        with open("secret.dll", "rb") as file:
            encrypted_data = file.read()
        return f.decrypt(encrypted_data).decode("utf-8")


if __name__ == "__main__":
    s = local_encryption()
    print(s.decryptlogins())
