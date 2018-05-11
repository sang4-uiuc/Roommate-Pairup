from flask import render_template, redirect, flash, request, Flask, session
# from forms import NetIDPasswordForm, SurveyForm, signUpForm, updateProfileForm, searchForm
from forms import *
import sqlite3
from queries import *
import random

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'asdfjhaf;gjsgl;fjs;lfhjsdflasjdflk'
# app.config["WTF_CSRF_ENABLED"] = True



@app.route('/')
@app.route('/index')
def index():
	# session['takenSurvey'] = False
	return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
	loginForm = NetIDPasswordForm()
	netID = loginForm.data['netID']
	password = loginForm.data['password']
	if (loginForm.validate_on_submit()):
		session['username'] = netID
		session['logged_in'] = True
		session['takenSurvey'] = hasTakenSurvey(netID)
		print session['takenSurvey']

		return render_template('index.html')
	else:
		return render_template('login.html', title='Sign In', form= loginForm)

@app.route("/logout")
def logout():
	session['logged_in'] = False
	return render_template("index.html")



@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
	signupForm = signUpForm()
	if(signupForm.validate_on_submit()):
		print "DATA", signupForm.data
		session['username'] = signupForm.data['Net_ID']
		session['logged_in'] = True
		session['takenSurvey'] = hasTakenSurvey(signupForm.data['Net_ID'])

		insertUserIntoDatabase(signupForm.data)
		return render_template('index.html')
	else:
		return render_template('signUp.html', title='signUp', form = signupForm)

@app.route('/updateProfile', methods=['GET', 'POST'])
def updateProfile():
	updateprofileForm = updateProfileForm()
	if(updateprofileForm.validate_on_submit()):

		updateUserProfile(updateprofileForm.data)
		return render_template('index.html')
	else:
		return render_template('updateProfile.html', title='Update Profile', form = updateprofileForm)


@app.route('/survey', methods=['GET', 'POST'])
def survey():
	surveyForm = SurveyForm()
	if(surveyForm.validate_on_submit()):
		insertSurveyIntoDatabase(surveyForm.data, session['username'])
		session['takenSurvey'] = True
		return render_template('index.html')

	return render_template('survey.html', title='Survey', form = surveyForm)

@app.route('/matches', methods=['GET', 'POST'])
def matches():
	if(not session["logged_in"]):
		return render_template('index.html')

	else:

		checks = getUserChecks(session["username"])
		potentialMatches = bestMatches(checks[0], checks[1], checks[2], checks[3], session['username'])
		print "POTENTIAL MATCHES:",potentialMatches
# 		images = ["/static/images/pic03.jpg", "/static/images/dude4.jpg", "/static/images/pic03", "/static/images/pic03.jpg", "/static/images/pic03.jpg", "/static/images/pic03.jpg"]
# 		images = ["/static/images/dude4.jpg", "/static/images/dude3.jpg", "/static/images/dude2.jpg", "/static/images/pic03.jpg", "/static/images/pic05.jpg"]
# 		random.shuffle(images)
		return render_template('matches.html', title = 'Matches', matches = potentialMatches)

@app.route('/search', methods=['GET', 'POST'])
def search():
	search_form = searchForm()
	if(search_form.validate_on_submit()):
		searchFormData = {}
		for x in search_form.data:
			if(x != "csrf_token"):
				searchFormData[x] = int(search_form.data[x])

		exact_matches = exactMatches(session["username"], searchFormData)
		return render_template('matches.html', title = 'Matches', matches = exact_matches)

	return render_template('search.html', title = "Search", form = search_form)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback_view():
	feedback_form = feedback()
	if(feedback_form.validate_on_submit()):
		# verify = verifyNet_IDs(feedback_form.data)
		# if(verify):
		insertFeedback(feedback_form.data)
		return render_template('index.html', title = "Home")

	return render_template('feedback.html', title = "Feedback", form = feedback_form)








if(__name__ == "__main__"):
	app.run(debug = True)
