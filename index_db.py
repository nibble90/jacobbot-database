import sqlite3
import pyotp
import base64
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

    def __disconnect(self, connection):
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
        if((discord_uuid == "None") and (telegram_uuid != "None")):
            c.execute('''SELECT uuid FROM users WHERE telegram_uuid=?''', (telegram_uuid, ))
        elif ((telegram_uuid == "None") and (discord_uuid != "None")):
            c.execute('''SELECT uuid FROM users WHERE discord_uuid=?''', (discord_uuid, ))
        else:
            c.execute('''SELECT uuid FROM users WHERE telegram_uuid=? AND discord_uuid=?''', (telegram_uuid, discord_uuid))
        result = c.fetchall()
        self.__disconnect(connection)
        return result
    
    def __login_details(self, uuid=None, username=None):
        uuid = str(uuid, )
        username = str(username, )
        connection, c = self.__connect()
        if uuid != "None":
            c.execute('''SELECT username, password, superadmin FROM login_details WHERE uuid=?''', (uuid, ))
        else:
            c.execute('''SELECT username, password, superadmin FROM login_details WHERE username=?''', (username, ))
        result = c.fetchall()
        self.__disconnect(connection)
        if(len(result) > 0):
            return result[0]
        return False
        # result = result[0]
        # return result

    def __login_exists(self, uuid):
        result = self.__login_details(uuid)
        if not result:
            return False
        return True

    def __update_login(self, uuid, username, password):
        uuid = str(uuid, )
        username = str(username, )
        password = str(Encrypt(password).encrypt(), )
        connection, c = self.__connect()
        if(self.__login_exists(uuid)):
            c.execute('''UPDATE login_details SET username=?, password=? WHERE uuid=?''', (username, password, uuid))
        else:
            c.execute('''INSERT INTO login_details (uuid, superadmin, username, password) VALUES (?, ?, ?, ?)''', (uuid, bool(False), username, password))
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
        self.__disconnect(connection)
        if(len(result) > 0):
            return result[0]
        else:
            return False

    def __add_attempt(self, ip_address):
        ip_address = str(ip_address, )
        connection, c = self.__connect()
        attempts = self.__check_attempts(ip_address)
        if(attempts == False):
            c.execute('''INSERT INTO login_attempts (ip_address, tries, blocked) VALUES (?, 1, ?)''', (ip_address, bool(False)))
        else:
            attempts = int(attempts[0]) + 1
            c.execute('''UPDATE login_attempts SET tries=? WHERE ip_address=?''', (attempts, ip_address))
        self.__disconnect(connection)

    def __reset_attempts(self, ip_address):
        connection, c = self.__connect()
        c.execute('''UPDATE login_attempts SET tries=0 WHERE ip_address=?''', (ip_address, ))
        self.__disconnect(connection)
 
    def __block_ip_address(self, ip_address):
        ip_address = str(ip_address, )
        connection, c = self.__connect()
        c.execute('''UPDATE login_attempts SET blocked=? WHERE ip_address=?''', (bool(True), ip_address))
        self.__disconnect(connection)

    def __blocked_check(self, ip_address, override=False):
        if not override:
            self.__add_attempt(ip_address)
        ip_address = str(ip_address, )
        connection, c = self.__connect()
        c.execute('''SELECT tries, blocked FROM login_attempts WHERE ip_address=?''', (ip_address, ))
        result = c.fetchall()
        self.__disconnect(connection)
        if(len(result) == 0):
            return False
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

    def __add_twitter_tokens(self, uuid, twitter_oauth, twitter_oauth_secret):
        uuid = str(uuid, )
        twitter_oauth = str(twitter_oauth, )
        twitter_oauth_secret = str(twitter_oauth_secret, )
        exists = self.__extensions_uuid_exists(uuid)
        connection, c = self.__connect()
        if not exists:
            c.execute('''INSERT INTO user_extensions (uuid, twitter_oauth, twitter_oauth_secret) VALUES(?, ?, ?)''', (uuid, twitter_oauth, twitter_oauth_secret))
        else:
            c.execute('''UPDATE user_extensions SET twitter_oauth=?, twitter_oauth_secret=? WHERE uuid=?''', (twitter_oauth, twitter_oauth_secret, uuid))
        self.__disconnect(connection)

    def __get_twitter_tokens(self, uuid):
        uuid = str(uuid, )
        connection, c = self.__connect()
        c.execute('''SELECT twitter_oauth, twitter_oauth_secret FROM user_extensions WHERE uuid=?''', (uuid, ))
        results = c.fetchall()
        self.__disconnect(connection)
        if(len(results) > 0):
            return results[0][0], results[0][1]
        return False

    def __extensions_uuid_exists(self, uuid):
        uuid = str(uuid, )
        connection, c = self.__connect()
        c.execute('''SELECT * FROM user_extensions WHERE uuid=?''', (uuid, ))
        results = c.fetchall()
        self.__disconnect(connection)
        if(len(results) > 0):
            return True
        return False
    
    def __default_weather(self, uuid):
        uuid = str(uuid, )
        connection, c = self.__connect()
        c.execute('''SELECT default_weather FROM user_extensions WHERE uuid=?''', (uuid, ))
        results = c.fetchall()
        self.__disconnect(connection)
        if((results[0] == None ) or (len(results[0]) == 0)):
            return False
        return results[0]

    def __remove_twitter_tokens(self, uuid):
        uuid = str(uuid, )
        default_weather_set = self.__default_weather(uuid)
        connection, c = self.__connect()
        if default_weather_set == False:
            c.execute('''DELETE FROM user_extensions WHERE uuid=?''', (uuid, ))
        else:
            c.execute('''UPDATE user_extensions SET twitter_oauth=?, twitter_oauth_secret=? WHERE uuid=?''', (None, None, uuid))
        self.__disconnect(connection)

    def __two_factor_authentication_secret(self, username):
        try:
            username, password, superadmin = self.__login_details(username=username)
            if((username == "None") or (password == "None") or (superadmin == "None")):
                return False, False
            else:
                seckey = password[:15].encode("UTF-8")
                encoded_seckey = base64.b32encode(seckey)
                return encoded_seckey, username
        except TypeError:
            return False, False
        except Exception as e:
            return False, False

    def __verify_two_factor_authentication(self, username, code):
        encoded_seckey, username = self.__two_factor_authentication_secret(username)
        if((encoded_seckey == False) and (username == False)):
            return False
        instance = pyotp.TOTP(encoded_seckey)
        code = str(code)
        verified = instance.verify(code)
        return verified

    def __register_two_factor_authentication(self, username):
        encoded_seckey, username = self.__two_factor_authentication_secret(username)
        instance = pyotp.totp.TOTP(encoded_seckey).provisioning_uri(name=username, issuer_name='JacobBot Admin Panel')
        return instance

    def modify_user(self, uuid=None, telegram_uuid=None, discord_uuid=None, username=None, password=None, superadmin=None):
        if((username == None) and (password == None) and (superadmin == None)):
            if(not self.__user_exists(telegram_uuid, discord_uuid)):
                self.__add_user(telegram_uuid, discord_uuid)
        elif((username != None) and (password != None)):
            uuid = self.__find_uuid(telegram_uuid, discord_uuid)
            uuid = uuid[0][0]
            self.__update_login(uuid, username, password)
        else:
            #raise error if superadmin is none
            pass
        if(superadmin != None):
            self.__update_superadmin(uuid, superadmin)

    def check_superadmin(self, username):
        result = self.__login_details()
        if(not result):
            return bool(result[2])
        return False
        
    def login_attempt(self, username, given_password, ip_address):
        if(not self.__blocked_check(ip_address)):
            try:
                user, password, superadmin = self.__login_details(username=username)
                given_password = Encrypt(given_password).encrypt()
                if given_password == password:
                    self.__reset_attempts(ip_address)
                    return True
                return False
            except TypeError:
                return False
        return False

    def unblock_ip_address(self, ip_address):
        self.__unblock_ip_address(ip_address)
        self.__reset_attempts(ip_address)

    def check_user(self, username, ip_address, override=False):
        if(not self.__blocked_check(ip_address, override)):
            try:
                user, password, superadmin = self.__login_details(username=username)
                return True
            except TypeError:
                return False
        else:
            return False
            
    def twitter_tokens(self, uuid):
        result = self.__get_twitter_tokens(uuid)
        if not result:
            return False
        else:
            return result[0], result[1]

    def insert_twitter_token(self, uuid, twitter_oauth, twitter_oauth_secret):
        if self.__get_twitter_tokens(uuid):
            return False
        self.__add_twitter_tokens(uuid, twitter_oauth, twitter_oauth_secret)

    def remove_twitter_token(self, uuid):
        self.__remove_twitter_tokens(uuid)

    def verify_two_factor(self, username, code):
        return self.__verify_two_factor_authentication(username, code)

    def register_two_factor_authentication(self, username):
        return self.__register_two_factor_authentication(username)

if __name__ == "__main__":
    inst = jb_database("/home/ubuntu/jacobbot/database/databases/jacobbot.db")
    # inst.two_factor("admin")
    # inst.modify_user(telegram_uuid="123456", discord_uuid="12458")
    # inst.modify_user(discord_uuid="12458", username="admin", password="admin")
    # inst.twitter_tokens("123")
    # inst.insert_twitter_token("123", "abcdefg", "gfedcba")
    # inst.twitter_tokens("123")