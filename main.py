from cryptography.fernet import Fernet
import os.path
import os
from kamarapi import *


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

    def encrypt(self, file_data):
        f = Fernet(self.key)
        encrypted_data = f.encrypt(file_data)
        with open("secret.dll", "wb") as file:
            file.write(encrypted_data)

    def decryptlogins(self):
        f = Fernet(self.key)
        with open("secret.dll", "rb") as file:
            encrypted_data = file.read()
        return f.decrypt(encrypted_data).decode("utf-8")


if __name__ == "__main__":
    cryt = local_encryption()
    while True:
        if input("New user? [y/n]") == "y":
            temp1 = input("what school u goto? \n").lower() + "\n"
            for i in range(0, 50):
                print("")
            temp1 += input("username : \n").lower() + "\n"
            for i in range(0, 50):
                print("")
            temp1 += input("password : \n")
            for i in range(0, 50):
                print("")
            cryt.encrypt(temp1.encode("utf-8"))
            break
        else:
            with open("secret.dll", "wb") as file:
                file.write(
                    b"gAAAAABjD9uqq5hAe6_bgLyH7j-GZ-h6rcw8aRmhaXpGWKVLg-vAn-p8gTOdP-dOcgMsVyHkENnUqzF2CY2g7ZcHTZYejUrEYG579TgegzKroBOHjWMXU9Y=")
            break

    cred_details = cryt.decryptlogins().split("\n")
    k = kamar_api(cred_details[0], cred_details[1], cred_details[2])
    results = k.getresults()
    print("Youre Rank score is : ", results)
