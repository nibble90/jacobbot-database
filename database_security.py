"""

TODO:
    [X] Grab IP address from application (mainly flask)
    [Y] Store IP address in seperate database with number of tries
    [X] If tries > 5 then block IP address
    [X] Super-Admin must unblock IP address
    [X] If username / password combination is correct before tries is up then
    tries is reset to 0 and user logged in

"""

from index_db import jb_db, login_db

class AccessDatabase:
    def __init__(self):
        self.ip_address = None
        self.uuid = None
        self.__jacobbot_database = jb_db("databases/jacobbot.db")
        self.__login_database = login_db("databases/jacobbot_logins.db")
    def check_access(self):
        attempts = int(self.attempts())
        if(attempts >= 5):
            return False
        else:
            return True
    def add_attempt(self):
        return self.__login_database.add_try(self.ip_address)
    def attempts(self):
        return self.__login_database.read_tries(self.ip_address)
    def reset_attempts(self):
        self.__login_database.reset_tries(self.ip_address)
        if(self.attempts() == 0):
            return True
        else:
            return False
    def uuid_check(self):
        return self.__jacobbot_database.check_for_uuid(uuid = self.uuid)

