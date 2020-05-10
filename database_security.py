"""

TODO:
    - Grab IP address from application (mainly flask)
    - Store IP address in seperate database with number of tries
    - If tries > 5 then block IP address
    - Super-Admin must unblock IP address
    - If username / password combination is correct before tries is up then
    tries is reset to 0 and user logged in

"""

from index_db import jb_db, login_db

class AccessDatabase:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.__jacobbot_database = jb_db("databases/jacobbot.db")
        self.__login_database = login_db("databases/jacobbot_logins.db")
    def add_attempt(self):
        return self.__login_database.add_try(self.ip_address)
    def attempts(self):
        return self.__login_database.read_tries(self.ip_address)

