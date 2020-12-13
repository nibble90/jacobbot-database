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

from .index_db import jb_database

class AccessDatabase:
    def __init__(self, jblocation="databases/jacobbot.db", loginlocation="databases/jacobbot_logins.db"):
        self.ip_address = None
        self.uuid = None
        self.__jacobbot_database = jb_database(jblocation)

    def add_user(self):
        return self.__jacobbot_database.modify_user(uuid = self.uuid)

    def update_user(self, telegram_uuid=None, discord_uuid=None, username=None, password=None, superadmin=None):
        self.__jacobbot_database.modify_user(telegram_uuid=telegram_uuid, discord_uuid=discord_uuid, username=username, password=password, superadmin=superadmin)

    def login(self, username, password):
        attempt = self.__jacobbot_database.login_attempt(username=username, password=password, ip_address=self.ip_address)
        return attempt
