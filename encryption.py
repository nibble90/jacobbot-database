import hashlib


class Encrypt:
    def __init__(self, string):
        self.target = string
    def encrypt(self):
        hashed = hashlib.sha512()
        hashed.update(self.target.encode())
        return hashed.hexdigest()
