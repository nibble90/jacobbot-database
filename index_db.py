import sqlite3
from sys import argv
class command_line:
    def __init__(self):
        self.arguments = argv[]
    def unix(self):
        pass
    def gnu(self):
        pass
    def windows(self):
        pass
    def identify(self):
        dash = 0
        slash = 0
        for character in argv[1]:
            if(character == "-"):
                dash += 1
            elif(character == "/"):
                slash += 1
        if(dash = 1):
            print("UNIX")
        elif(dash = 2):
            print("GNU")
        elif(slash = 1):
            print("WINDOWS")
        else:
            print("Error, found {} dashes and {} slashes".format(dash, slash))
    
class jb_db:
    def __init__(self, ):
        pass
    def create():
        connection = sqlite3.connect('jacobbot_database.db')
        c = connection.cursor()
        c.execute('''CREATE TABLE users
             (date text, trans text, symbol text, qty real, price real)''')
if __name__ == "__main__":
    command_line.identify()
    #database = jb_db()
