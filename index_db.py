import sqlite3
from sys import argv
from .encryption import Encrypt

class jb_database:
    def __init__(self, database_filename):
        self.db_name = database_filename
        self.__create()

    def __connect(self):
        connection = sqlite3.connect(self.db_name)
        c = connection.cursor()
        return (connection, c)

    def __disconnect(self):
        connection.commit()
        connection.close()

    def __create(self):
        connection, c = self.__connect()
        c.execute('''CREATE TABLE IF NOT EXISTS users
            (uuid INTEGER PRIMARY KEY AUTOINCREMENT, telegram_uuid TEXT, 
            discord_uuid TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS login_details
            (uuid TEXT, superadmin BOOLEAN, username TEXT, password TEXT, FOREIGN KEY(uuid) REFERENCES posts(uuid))''')
        c.execute('''CREATE TABLE IF NOT EXISTS login_attempts
            (ip_address TEXT, tries INTEGER, blocked BOOLEAN)''')
        c.execute('''CREATE TABLE IF NOT EXISTS user_extensions
            (uuid TEXT, twitter_oauth TEXT, twitter_oauth_secret TEXT, default_weather TEXT, 
            FOREIGN KEY (uuid) REFERENCES users(uuid))''')
        self.__disconnect(connection)

    def __user_exists(self, telegram_uuid=None, discord_uuid=None):
        result = self.__find_uuid(telegram_uuid, discord_uuid)       
        if(len(result) > 0):
            return True
        return False

    def __add_user(self, telegram_uuid=None, discord_uuid=None):
        telegram_uuid = str(telegram_uuid, )
        discord_uuid = str(discord_uuid, )
        connection, c = self.__connect()
        if discord_uuid is None:
            c.execute('''INSERT INTO users (telegram_uuid) VALUES (?)''', (telegram_uuid, ))
        elif telegram_uuid is None:
            c.execute('''INSERT INTO users (discord_uuid) VALUES (?)''', (discord_uuid, ))
        else:
            c.execute('''INSERT INTO users (telegram_uuid, discord_uuid) VALUES (?, ?)''', (telegram_uuid, discord_uuid))
        result = c.fetchall()
        self.__disconnect(connection)        
        if(len(result) > 0):
            return True
        return False

    def __find_uuid(self, telegram_uuid=None, discord_uuid=None):
        telegram_uuid = str(telegram_uuid, )
        discord_uuid = str(discord_uuid, )
        connection, c = self.__connect()
        if discord_uuid is None:
            c.execute('''SELECT uuid FROM users WHERE telegram_uuid=?''', (telegram_uuid, ))
        elif telegram_uuid is None:
            c.execute('''SELECT uuid FROM users WHERE discord_uuid=?''', (discord_uuid, ))
        else:
            c.execute('''SELECT uuid FROM users WHERE telegram_uuid=? AND discord_uuid=?''', (telegram_uuid, discord_uuid))
        result = c.fetchall()
        self.__disconnect(connection)
        result = result[0]
        return result
    
    def __login_details(self, uuid=None, username=None):
        uuid = str(uuid, )
        username = str(username, )
        connection, c = self.__connect()
        if uuid != None:
            c.execute('''SELECT username, password, superadmin FROM login_details WHERE uuid=?''', (uuid, ))
        else:
            c.execute('''SELECT username, password, superadmin FROM login_details WHERE username=?''', (username, ))
        result = c.fetchall()
        self.__disconnect(connection)
        result = result[0]
        return result

    def __login_exists(self, uuid):
        result = self.__login_details(uuid)
        if(len(result) > 0):
            return True
        return False

    def __update_login(self, uuid, username, password):
        uuid = str(uuid, )
        username = str(username, )
        password = str(Encrypt(password).encrypt(), )
        connection, c = self.__connect()
        if(self.__login_exists(uuid)):
            c.execute('''UPDATE login_details SET username=?, password=? WHERE uuid=?''', (username, password, uuid))
        else:
            c.execute('''INSERT INTO login_details (uuid, username, password) VALUES (?, ?, ?)''', (uuid, username, password))
        self.__disconnect(connection)

    def __update_superadmin(self, uuid, superadmin):
        uuid = str(uuid, )
        superadmin = bool(superadmin, )
        connection, c = self.__connect()
        c.execute('''UPDATE login_details SET superadmin=?''', (superadmin, ))
        self.__disconnect(connection)

    def __check_attempts(self, ip_address):
        ip_address = str(ip_address, )
        connection, c = self.__connect()
        c.execute('''SELECT tries FROM login_attempts WHERE ip_address=?''', (ip_address, ))
        result = c.fetchall()
        self.__disconnect()
        if(len(result[0]) > 1):
            return result[0]
        else:
            return False

    def __add_attempt(self, ip_address):
        ip_address = str(ip_address, )
        connection, c = self.__connect()
        attempts = self.__check_attempts(ip_address)
        if(not attempts):
            c.execute('''INSERT INTO login_attempts (ip_address, tries) VALUES (?, 1)''', (ip_address, ))
        else:
            attempts = attempts + 1
            c.execute('''UPDATE login_attempts SET tries=? WHERE ip_address=?''', (attempts, ip_address))
        self.__disconnect(connection)

    def __reset_attempts(self, ip_address):
        connection, c = self.__connect()
        c.execute('''UPDATE login_details SET tries=0 WHERE ip_address=?''', (ip_address, ))
        self.__disconnect(connection)
 
    def __block_ip_address(self, ip_address):
        ip_address = str(ip_address, )
        connection, c = self.__connect()
        c.execute('''UPDATE login_attempts SET blocked=? WHERE ip_address=?''', (bool(True), ip_address))
        self.__disconnect(connection)

    def __blocked_check(self, ip_address):
        ip_address = str(ip_address, )
        connection, c = self.__connect()
        c.execute('''SELECT tries, blocked FROM login_attempts WHERE ip_address=?''', (ip_address, ))
        result = c.fetchall()
        self.__disconnect(connection)
        tries = result[0][0]
        blocked = result[0][1]
        if(bool(blocked)):
            return True
        elif(not bool(blocked) and tries >= 5):
            self.__block_ip_address(ip_address)
            return True
        elif(tries < 5):
            return False
        else:
            return True

    def __unblock_ip_address(self, ip_address):
        ip_address = str(ip_address, )
        connection, c = self.__connect()
        c.execute('''UPDATE login_attempts SET blocked=? WHERE ip_address=?''', (bool(False), ip_address))
        self.__disconnect(connection)

    def modify_user(self, uuid=None, telegram_uuid=None, discord_uuid=None, username=None, password=None, superadmin=None):
        if((username == None) and (password == None) and (superadmin == None)):
            if(not self.__user_exists(telegram_uuid, discord_uuid)):
                self.__add_user(telegram_uuid, discord_uuid)
        elif((username != None) and (password != None)):
            uuid = self.__find_uuid(telegram_uuid, discord_uuid)
            self.__update_login(uuid, username, password)
        else:
            #raise error if superadmin is none
            pass
        if(superadmin != None):
            self.__update_superadmin(uuid, superadmin)

    def check_superadmin(self, username):
        result = self.__login_details()
        return bool(result[2])

    def login_attempt(self, username, given_password, ip_address):
        if(not self.__blocked_check(ip_address)):
            user, password, superadmin = self.__login_details(username=username)
            given_password = Encrypt(given_password).encrypt()
            if given_password == password:
                self.__reset_attempts(ip_address)
                return True
            self.__add_attempt(ip_address)
            return False
        return False

    def unblock_ip_address(self, ip_address):
        self.__unblock_ip_address(ip_address)
        self.__reset_attempts(ip_address)

