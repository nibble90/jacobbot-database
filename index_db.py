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
             (uuid text, admin_user boolean, superadmin_user boolean, username text, password text)''')

    def add_user(self, uuid, admin_user=False, superadmin_user=False, username=None, password=None):
        if(not self.check_for_uuid(uuid)):
            connection = sqlite3.connect(self.db_name)
            c = connection.cursor()
            uid = str(uuid, )
            admin = str(admin_user, )
            superadmin = str(superadmin_user, )
            user = str(username, )
            passwrd = str(password, )
            c.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?)", (uid, admin, superadmin, user, passwrd))
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
            return bool('True' == result)
        else:
            return False

    def filter_permissions_check(self):
        connection = sqlite3.connect(self.db_name)
        c = connection.cursor()
        c.execute("SELECT uuid FROM users WHERE admin_user='True'")
        result = c.fetchall()
        connection.commit()
        connection.close()
        return result

    def update_user(self, uuid, admin_user=False, superadmin_user=False, username=None, password=None):
        connection = sqlite3.connect(self.db_name)
        c = connection.cursor()
        uid = str(uuid, )
        admin = bool(admin_user, )
        superadmin = bool(superadmin_user, )
        user = str(username, )
        passwd = str(password, )
        c.execute("UPDATE users SET admin_user=?, superadmin_user=?, username=?, password=? WHERE uuid=?", (admin, superadmin, user, passwd, uid))
        connection.commit()
        connection.close()

class login_db:
    def __init__(self, database_filename):
        self.db_name = database_filename
        self.__create()

    def __create(self):
        connection = sqlite3.connect(self.db_name)
        c = connection.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS logins
             (ip_address text, tries integer, blocked boolean)''')

    def add_try(self, ip_address):
        if(not self.check_for_ip(ip_address)):
            connection = sqlite3.connect(self.db_name)
            c = connection.cursor()
            ip = str(ip_address, )
            num_tries = int(1, )
            c.execute("INSERT INTO logins VALUES(?, ?, ?)", (ip, num_tries, False))
            connection.commit()
            connection.close()
            return False
        else:
            connection = sqlite3.connect(self.db_name)
            c = connection.cursor()
            ip = str(ip_address, )
            num_tries = self.read_tries(ip_address)
            num_tries += 1
            tries = int(num_tries, )
            c.execute("UPDATE logins SET tries=? WHERE ip_address=?", (tries, ip))
            connection.commit()
            connection.close()
            return True

    def read_full_tries(self):
        connection = sqlite3.connect(self.db_name)
        c = connection.cursor()
        c.execute("SELECT * FROM logins")
        print(c.fetchall())
        connection.commit()
        connection.close()

    def read_tries(self, ip_address):
        connection = sqlite3.connect(self.db_name)
        c = connection.cursor()
        ip = str(ip_address, )
        c.execute("SELECT tries FROM logins WHERE ip_address=?", (ip, ))
        result = c.fetchone()
        result = result[0]
        connection.commit()
        connection.close()
        return result

    def reset_tries(self, ip_address):
        connection = sqlite3.connect(self.db_name)
        c = connection.cursor()
        ip = str(ip_address, )
        tries = int(0, )
        c.execute("UPDATE logins SET tries=? WHERE ip_address=?", (tries, ip))
        connection.commit()
        connection.close()

    def check_for_ip(self, ip_address):
        connection = sqlite3.connect(self.db_name)
        c = connection.cursor()
        ip = str(ip_address, )
        c.execute("SELECT * FROM logins WHERE ip_address=?", (ip, ))
        result = c.fetchall()
        connection.commit()
        connection.close()
        if len(result) > 0:
            return True
        else:
            return False

    def block_ip(self, ip_address):
        connection = sqlite3.connect(self.db_name)
        c = connection.cursor()
        ip = str(ip_address, )
        c.execute("UPDATE logins SET blocked=? WHERE ip_address=?", (True, ip))
        connection.commit()
        connection.close()

    def check_for_blocked()

if __name__ == "__main__":
    #command = command_line()
    #command.identify()
    jb_db('databases/jacobbot.db').read_full_users()
    login_db('databases/jacobbot_logins.db').read_full_tries()
