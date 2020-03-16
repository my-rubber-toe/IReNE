import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
irene = myclient["IReNE"]

collab = irene["Collaborators"]
admin = irene["Admin"]
session = irene["Session"]
doc = irene["Document"]
taglist = irene["TagList"]
infra = irene["Infrastructure"]
damage = irene["Damage"]

#print ("server_info():", myclient.server_info())

# db = myclient["IReNE"]
# try: db.command("serverStatus")
# except Exception as e: print(e)
# else: print("You are connected!")
# myclient.close()