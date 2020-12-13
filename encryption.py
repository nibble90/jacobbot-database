import hashlib
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSS
from os import getenv
from dotenv import load_dotenv


class Encrypt:
    def __init__(self, string):
        self.target = string
    def encrypt(self):
        hashed = hashlib.sha512()
        hashed.update(self.target.encode())
        return hashed.hexdigest()
    def tokenise(self):
        inst = TJWSS(RandomData.secret_data())
        tokenised = inst.dumps(self.target)
        return tokenised

class RandomData:
    @staticmethod
    def secret_data():
        load_dotenv()
        return getenv("SECRET_KEY")

