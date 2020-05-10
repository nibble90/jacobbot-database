from index_db import jb_db, login_db
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
