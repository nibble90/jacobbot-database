"""

TODO:
    [X] Grab IP address from application (mainly flask)
    [Y] Store IP address in seperate database with number of tries
    [Y] If tries > 5 then block IP address
    [X] Super-Admin must unblock IP address
    [X] If username / password combination is correct before tries is up then
    tries is reset to 0 and user logged in
    [X] Add try excepts to everything in jb_db to detect is theres an error

"""

from index_db import jb_db, login_db

class AccessDatabase:
    def __init__(self, jblocation="databases/jacobbot.db", loginlocation="databases/jacobbot_logins.db"):
        self.ip_address = None
        self.uuid = None
        self.__jacobbot_database = jb_db(jblocation)
        self.__login_database = login_db(loginlocation)
    def check_access(self):
        attempts = int(self.attempts())
        if(attempts >= 5):
            return False
        else:
            return True
    def add_attempt(self):
        self.block_user()
        result = self.__login_database.add_try(self.ip_address)
        return result
    def attempts(self):
        return self.__login_database.read_tries(self.ip_address)
    def reset_attempts(self):
        self.__login_database.reset_tries(self.ip_address)
        if(self.attempts() == 0):
            return True
        else:
            return False
    def add_user(self):
        return self.__jacobbot_database.add_user(uuid = self.uuid)
    def uuid_check(self):
        return self.__jacobbot_database.check_for_uuid(uuid = self.uuid)
    def update_user(self, admin_user=False, superadmin_user=False, username=None, password=None):
        uid = self.uuid
        self.__jacobbot_database.update_user(uid, admin_user, superadmin_user, username, password)
    def block_user(self):
        access = self.check_access()
        if(access is not True):
            self.__login_database.block_ip(self.ip_address)
        else:
            pass
    def unblock_user(self):
        self.__login_database.unblock_ip(self.ip_address)
        if(self.check_block_status == False):
            return True
        else:
            return False
    def check_block_status(self):
        status = self.__login_database.check_for_blocked(self.ip_address)
        status = bool(status == True)
        if(status):
            return True
        else:
            return False
    def login(self, username, password):
        pass
