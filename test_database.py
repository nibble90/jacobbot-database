from index_db import jb_db
try:
    database = jb_db("jacobbot.db")
    database.create()
    database.read_full_users()
    database.add_user(uuid=12534)
    database.read_full_users()
    database.add_user(uuid=9687468, username="Steve", password="bob123", admin_user=True)
    database.read_full_users()
except Exception as e:
    print(e)
