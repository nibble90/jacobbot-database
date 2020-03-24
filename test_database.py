from index_db import jb_db
def read_db():
    print("-"*6, "BEGIN DATABASE READ", "-"*6)
    database.read_full_users()
    print("-"*6, "END DATABASE READ", "-"*6)
try:
    database = jb_db("jacobbot.db")
    #database.create()
    read_db()
    print(database.add_user(uuid=12534))
    read_db()
    print(database.add_user(uuid=9687468, username="Steve", password="bob123", admin_user=True))
    read_db()
    print(database.add_user(uuid=9687468))
    read_db()
except Exception as e:
    print(e)
