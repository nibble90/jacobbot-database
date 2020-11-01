from index_db import jb_db, login_db
from database_access_layer import AccessDatabase
"""
def read_db():
    print("-"*6, "BEGIN DATABASE READ", "-"*6)
    database1.read_full_users()
    database2.read_full_tries()
    print("-"*6, "END DATABASE READ", "-"*6)
try:
    database1 = jb_db("databases/jacobbot.db")
    database2 = login_db("databases/jacobbot_logins.db")
    #database.create()
    read_db()
    print(database1.add_user(uuid=12534))
    print(database2.add_try(ip_address="192.168.0.0"))
    read_db()
    print(database1.add_user(uuid=9687468, username="Steve", password="bob123", admin_user=True))
    print(database2.add_try(ip_address="192.168.0.0"))
    read_db()
    print(database1.add_user(uuid=9687468))
    print(database2.add_try(ip_address="192.168.0.0"))
    read_db()
except Exception as e:
    print(e)
"""
def test_security():
    ip_add = "192.168.0.0"
    securedb = AccessDatabase(ip_add)

    #Reset IP Address test
    print("Resetting {} from {} to 0".format(ip_add, securedb.attempts()))
    securedb.reset_attempts()
    if(securedb.attempts() == 0):
        print("------SUCCESS-----")
        print("IP Address reset successfully")
        print("\n")
    else:
        print("------FAILURE------")
        print("IP Address reset failed")
        print("\n")

    #Add try to IP Address test
    print("Attempting to add an attempt to IP Address {}".format(ip_add))
    securedb.add_attempt()
    if(securedb.attempts() == 1):
        print("------SUCCESS------")
        print("IP Address attempt increment success")
        print("\n")
    else:
        print("------FAILURE------")
        print("IP Address atmp increment failed")
        print("\n")

def add_user():
    database1 = jb_db("databases/jacobbot.db")
    database1.add_user(uuid=9687468, username="admin", password="admin", admin_user=True)

add_user()
#test_security() #
