from __future__ import print_function # In python 2.7
from flask import Flask, render_template, request
from pymongo import MongoClient
import sys
import user_methods 
from werkzeug import secure_filename


#create mongo client
client = MongoClient()
db = client.Users #go to Users database
posts = db.posts  #goes to posts collection


app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']







#login page
@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		result = request.form.copy()
		username = result['username']
		password = result['password']
		if user_methods.loginchecker(username,password) == 1:
			return render_template('user_home.html', username = username)
		else:
			return render_template('login.html', alerts = "you entered in an incorrect username or password. try again")
	else:
		return render_template('login.html')



@app.route('/', methods = ['GET', 'POST'])
#signup page
def signup():
	if request.method == 'POST':
		result = request.form.copy() #returns multidict
		user = result['username']
		passw = result['password']
		email = result['email']
		alerts = user_methods.signupchecker(user,passw)

		file = request.files['file']
    	# Check if the file is one of the allowed types/extensions

		filename = secure_filename(file.filename)



		#if there are no alerts we add user to db
		if len(alerts) == 0: 
			post_id = db.posts.insert_one(result).inserted_id
			if post_id != None:
				return render_template('signup.html', filename = file, alerts = post_id)
			else:
				return render_template('signup.html', alerts = alerts)
		#else we return the alerts to the user
		else:
			return render_template('signup.html', alerts = alerts)
	else:
		return render_template('signup.html')





if(__name__ == "__main__"):
	app.run(debug=True)