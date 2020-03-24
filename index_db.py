import sqlite3
from sys import argv
class command_line:
    def __init__(self):
        self.arguments = argv

    def unix(self):
        pass

    def gnu(self):
        pass

    def windows(self):
        pass

    def identify(self):
        dash = 0
        slash = 0
        for character in self.arguments[1]:
            if(character == "-"):
                dash += 1
            elif(character == "/"):
                slash += 1
        if(dash == 1):
            print("UNIX")
            print(*self.arguments)
        elif(dash == 2):
            print("GNU")
            print(*self.arguments)
        elif(slash == 1):
            print("WINDOWS")
            print(*self.arguments)
        else:
            print("Error, found {} dashes and {} slashes".format(dash, slash))
            print(*self.arguments)
        self.strip()
        print(*self.arguments)

    def strip(self):
        temp_argv = []
        for element in self.arguments:
            if(element[0] == "-" or element[0] == "/"):
                if(element[1] == "-"):
                    temp_argv.append(element[2:])
                else:
                    temp_argv.append(element[1:])
            else:
                temp_argv.append(element)
        self.arguments = temp_argv
    
class jb_db:
    def __init__(self, database_filename):
        self.db_name = database_filename
        self.__create()

    def __create(self):
        connection = sqlite3.connect(self.db_name)
        c = connection.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
             (uuid text, admin_user boolean, username text, password text)''')

    def add_user(self, uuid, admin_user=False, username=None, password=None):
        if(not self.check_for_uuid(uuid)):
            connection = sqlite3.connect(self.db_name)
            c = connection.cursor()
            u = str(uuid, )
            a = str(admin_user, )
            us = str(username, )
            p = str(password, )
            c.execute("INSERT INTO users VALUES(?, ?, ?, ?)", (u, a, us, p))
            connection.commit()
            connection.close()
            return False
        else:
            return True

    def read_full_users(self):
        connection = sqlite3.connect(self.db_name)
        c = connection.cursor()
        c.execute("SELECT * FROM users")
        print(c.fetchall())
        connection.commit()
        connection.close()

    def check_for_uuid(self, uuid):
        connection = sqlite3.connect(self.db_name)
        c = connection.cursor()
        u = str(uuid, )
        c.execute("SELECT * FROM users WHERE uuid=?", (u, ))
        result = c.fetchall()
        connection.commit()
        connection.close()
        if len(result) > 0:
            return True
        else:
            return False

    def permissions_check(self, uuid):
        uuid_exists = self.add_user(uuid=uuid)
        if(uuid_exists):
            connection = sqlite3.connect(self.db_name)
            c = connection.cursor()
            u = str(uuid, )
            c.execute("SELECT admin_user FROM users WHERE uuid=?", (u, ))
            result = c.fetchall()
            connection.commit()
            connection.close()
            result = str(result[0][0])
            return bool(True == result)
        else:
            return False

if __name__ == "__main__":
    #command = command_line()
    #command.identify()
    jb_db('jacobbot.db').create()
