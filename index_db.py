import sqlite3
from sys import argv
from .encryption import Encrypt
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
            admin = bool(admin_user, )
            superadmin = bool(superadmin_user, )
            user = str(username, )
            if password != None:
                passwrd = str(Encrypt(password).encrypt(), )
            else:
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
            return bool(result)
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
        passwd = str(Encrypt(password).encrypt(), )
        c.execute("UPDATE users SET admin_user=?, superadmin_user=?, username=?, password=? WHERE uuid=?", (admin, superadmin, user, passwd, uid))
        connection.commit()
        connection.close()

    def login_attempt(self, username, password_given):
        connection = sqlite3.connect(self.db_name)
        c = connection.cursor()
        user = str(username, )
        c.execute("SELECT password FROM users WHERE username=?", (user, ))
        result = c.fetchall()
        print(repr(result))
        connection.commit()
        connection.close()
        if(result != None):
            password_hash = Encrypt(password_given).encrypt()
            password = result[0][0]
            if(password_hash == password):
                return True
        else:
            return False

class login_db:
    def __init__(self, database_filename):
        self.db_name = database_filename
        self.__create()

    def connect(self):
        connection = sqlite3.connect(self.db_name)
        c = connection.cursor()
        return (connection, c)

    def disconnect(self, connection):
        connection.commit()
        connection.close()

    def __create(self):
        connection, c = self.connect()
        c.execute('''CREATE TABLE IF NOT EXISTS logins
             (ip_address text, tries integer, blocked boolean)''')
        self.disconnect(connection)

    def add_try(self, ip_address):
        if(not self.check_for_ip(ip_address)):
            connection, c = self.connect()
            ip = str(ip_address, )
            num_tries = int(1, )
            c.execute("INSERT INTO logins VALUES(?, ?, ?)", (ip, num_tries, bool(False)))
            self.disconnect(connection)
            return False
        else:
            connection, c = self.connect()
            ip = str(ip_address, )
            num_tries = self.read_tries(ip_address)
            num_tries += 1
            tries = int(num_tries, )
            c.execute("UPDATE logins SET tries=? WHERE ip_address=?", (tries, ip))
            self.disconnect(connection)
            return True

    def read_full_tries(self):
        connection, c = self.connect()
        c.execute("SELECT * FROM logins")
        print(c.fetchall())
        self.disconnect(connection)

    def read_tries(self, ip_address):
        connection, c = self.connect()
        ip = str(ip_address, )
        c.execute("SELECT tries FROM logins WHERE ip_address=?", (ip, ))
        result = c.fetchone()
        result = result[0]
        self.disconnect(connection)
        return result

    def reset_tries(self, ip_address):
        connection, c = self.connect()
        ip = str(ip_address, )
        tries = int(0, )
        c.execute("UPDATE logins SET tries=? WHERE ip_address=?", (tries, ip))
        self.disconnect(connection)

    def check_for_ip(self, ip_address):
        connection, c = self.connect()
        ip = str(ip_address, )
        c.execute("SELECT * FROM logins WHERE ip_address=?", (ip, ))
        result = c.fetchall()
        self.disconnect(connection)
        if len(result) > 0:
            return True
        else:
            return False

    def block_ip(self, ip_address):
        connection, c = self.connect()
        ip = str(ip_address, )
        c.execute("UPDATE logins SET blocked=1 WHERE ip_address=?", (ip, ))
        self.disconnect(connection)

    def check_for_blocked(self, ip_address):
        connection, c = self.connect()
        ip = str(ip_address, )
        c.execute("SELECT blocked FROM logins WHERE ip_address=?", (ip, ))
        result = c.fetchall()
        self.disconnect(connection)
        return bool(result[0][0])

    def unblock_ip(self, ip_address):
        connection, c = self.connect()
        ip = str(ip_address, )
        c.execute("UPDATE logins SET blocked=0 WHERE ip_address=?", (ip, ))
        self.disconnect(connection)

if __name__ == "__main__":
    #command = command_line()
    #command.identify()
    jb_db('/home/ubuntu/jacobbot/database/databases/jacobbot.db').read_full_users()
    print('*'*8)
    login_db('/home/ubuntu/jacobbot/database/databases/jacobbot_logins.db').read_full_tries()
    print('*'*8)
    login_db('/home/ubuntu/jacobbot/database/databases/jacobbot_logins.db').read_tries("192.168.0.0")
