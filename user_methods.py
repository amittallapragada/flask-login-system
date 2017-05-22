from pymongo import MongoClient
# import pprint

client = MongoClient()

db = client.Users

collection = db.test_collection

posts = db.posts


def signupchecker(username, password):
	requirements = []
	if str(db.posts.find_one({"username": username})) != 'None':
		requirements.append("Your username is taken.")
	if len(password) < 4:
		requirements.append("Your password is too short.")
	return requirements



def loginchecker(username, password):
 	if db.posts.find_one({ "$and": [ { "username" : username }, { "password" : password } ] }):
 		return 1
 	elif str(db.posts.find_one({ "$and": [ { "username" : username }, { "password" : password } ] })) == 'None':
 		print "true"
 		return 0
 	else:
 		return 0


