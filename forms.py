from flask_wtf import Form
from wtforms import StringField, PasswordField, RadioField, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired, ValidationError
import sqlite3
from wtforms.widgets import TextArea
from flask import session
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename

class NetIDPasswordForm(Form):
	netID = StringField('NetID', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])

	def validate(self):
		# Makes sure that the netID they entered is in the database and that the password matches
		ret = Form.validate(self)
		if(not ret):
			return False
		netID = self.netID.data
		password = self.password.data
		conn = sqlite3.connect('/home/roommatepairup/mysite/roommates.db')
		cur = conn.cursor()
		query = 'SELECT Password FROM Student WHERE Net_ID = ?'
		cur.execute(query, (netID,))
		ret = cur.fetchone()
		conn.close()

		if(ret == None):
			self.netID.errors.append('Invalid NetID')
			return False
		elif(ret != None and ret[0] != password):
			self.password.errors.append('Invalid Password')
			return False

		return True


class SurveyForm(Form):
	outgoing = RadioField('outgoing', choices=[('1','Have a very shy personality'),('2','Usually keep to yourself in large groups'),('3','Enjoy being in group environments'), ('4','Socialize and make new friends often')])
	party = RadioField('party', choices=[('1','Never'),('2','Once a week'),('3','Two or three times a week'), ('4','More than three times a week')])
	guestOver = RadioField('guestOver', choices=[('1','Never'),('2','Once a week'),('3','Two or three times a week'), ('4','More than three times a week')])
	roomtime = RadioField('roomtime', choices=[('1','Stay in my room for most of the day'),('2','Tend to be in my room more than not'),('3','Usually outside of my room'), ('4','Almost always out and about throughout the day')])
	check_social = BooleanField("This category is important to me.")


	drinks = RadioField('drinks', choices=[('1','Never'),('2','Once a week'),('3','Two or three times a week'), ('4','More than three times a week')])
	smokes = RadioField('smokes', choices=[('1','Never'),('2','Very rarely'),('3','A few times a week'), ('4','Multiple times a day')])
	studyAmount = RadioField('studyAmount', choices=[('1','Less than an hour a day'),('2','One to three hours a day'),('3','Four to six hours a day'), ('4','More than six hours a day')])
	timeBed = RadioField('timeBed', choices=[('1','Before 10 p.m.'),('2','Between 10 p.m. to 12 a.m.'),('3','Between 12 a.m. to 2 a.m.'), ('4','After 2 a.m.')])
	check_habit = BooleanField("This category is important to me.")


	sports = RadioField('sports', choices=[('1','Have very little to no interest'),('2','Enjoy watching/playing sports occasionally'),('3','Watch/play sports multiple times a week'), ('4','Watch/play sports almost every day')])
	games = RadioField('games', choices=[('1','Have very little to no interest'),('2','Play occasionally'),('3','Play a few hours a week'), ('4','Play a multiple hours a day')])
	tv = RadioField('tv', choices=[('1','Hardly ever'),('2','A few hours a week'),('3','An hour a day'), ('4','Multiple hours a day')])
	cooking = RadioField('cooking', choices=[('1','Hardly ever'),('2','A few times a week'),('3','Once a day'), ('4','Multiple times a day')])
	check_interest = BooleanField("This category is important to me.")


	cleanliness = RadioField('cleanliness', choices=[('1','Very rarely clean each room of my place'),('2','Clean all the rooms a few times a month'),('3','Clean each room once a week'), ('4','Clean my living area almost every day')])
	roomTemp = RadioField('roomTemp', choices=[('1','Below 60 degrees F'),('2','Between 60 to 67 degrees F'),('3','Between 68 to 75 degrees F'), ('4','Above 75 degrees F')])
	pets = RadioField('pets', choices=[('1','No'),('2','Small caged pets'),('3','A large pet'), ('4','Multiple large pets')])
	sharing = RadioField('sharing', choices=[('1','Do not like sharing any items'),('2','Do not mind sharing certain items if asked first'),('3','Will share most things if asked'), ('4','Will sharing anything')])
	check_lifestyle = BooleanField("This category is important to me.")


class signUpForm(Form):
	Net_ID = StringField('NetID', validators=[DataRequired()])
	Password = PasswordField('Password', validators=[DataRequired()])
	rePassword = PasswordField('rePassword', validators=[DataRequired()])
	Name = StringField('Name', validators=[DataRequired()])
	Age = SelectField('Age', choices = [ ('', '- Age -'), ('18','18'),('19','19'),('20','20'), ('21','21'), ('22','22'), ('23','23'), ('24','24'), ('25','25'), ('26','26')], validators=[DataRequired()])
	Gender = SelectField('Gender', choices = [('', '- Gender -'), ('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
	Major = StringField('NetID', validators = [DataRequired()])
	Race = SelectField('Race', choices = [('', '- Race -'), ('1','White'),('2','African American'),('3','Native American'), ('4','Indian'), ('5', 'Chinese'), ('6', 'Japanese'), ('7', 'Korean'), ('8', 'Vietnamese'),
										  ('9', 'Other Asian'), ('10', 'Native Hawaiian'), ('11', 'Filipino'), ('12', 'Other Pacific Islander'), ('13', 'Hispanic or Latino'), ('14', 'Some other race')])
	Email = StringField('Email', validators=[DataRequired()])
	Twitter = StringField('Twitter', validators=[DataRequired()])
	Facebook = StringField('Facebook', validators=[DataRequired()])
	dormApt = RadioField('DormApt', choices=[("Dorm", "Dorm"), ("Apartment", "Apartment")], validators=[DataRequired()])
	# ADD PROFILE PICTURE UPLOAD OPTIONS HERE

	def validate(self):
		# makes sure that they pick a new username and that their passwords match
		ret = Form.validate(self)
		if(not ret):
			return False
		netID = self.Net_ID.data
		password = self.Password.data
		rePassword = self.rePassword.data

		conn = sqlite3.connect('/home/roommatepairup/mysite/roommates.db')
		cur = conn.cursor()
		query = 'SELECT Password FROM Student WHERE Net_ID = ?'
		cur.execute(query, (netID,))
		ret = cur.fetchone()
		conn.close()

		if(ret != None):
			self.Net_ID.errors.append('NetID already taken.')
			return False
		if(password != rePassword):
			self.rePassword.errors.append('Passwords don\'t match.')
			return False
		return True

class updateProfileForm(Form):
	oldPassword = PasswordField('Password', validators=[DataRequired()])

	# let them change password, email, twitter or facebook
	newPassword = PasswordField('newPassword')
	rePassword = PasswordField('rePassword')
	Email = StringField('Email')
	delete = BooleanField("I want to delete my profile")


	def validate(self):
		# makes sure that they pick a new username and that their passwords match
		ret = Form.validate(self)
		if(not ret):
			return False
		netID = session['username']
		oldPassword = self.oldPassword.data

		newPassword = self.newPassword.data
		rePassword = self.rePassword.data

		conn = sqlite3.connect('/home/roommatepairup/mysite/roommates.db')
		cur = conn.cursor()
		query = 'SELECT Password FROM Student WHERE Net_ID = ?'
		cur.execute(query, (netID,))
		ret = cur.fetchone()
		conn.close()

		if(ret[0] != oldPassword):
			self.oldPassword.errors.append("Incorrect password")
			return False
		if(newPassword != rePassword):
			self.rePassword.errors.append("Your new password doesn't match")
			return False
		return True


class searchForm(Form):
	outgoing = RadioField('outgoing', choices=[('0', 'This does not matter to me'), ('1','Have a very shy personality'),('2','Usually keep to yourself in large groups'),('3','Enjoy being in group environments'), ('4','Socialize and make new friends often')], default = "0")
	party = RadioField('party', choices=[('0', 'This does not matter to me'), ('1','Never'),('2','Once a week'),('3','Two or three times a week'), ('4','More than three times a week')], default = "0")
	guestOver = RadioField('guestOver', choices=[('0', 'This does not matter to me'), ('1','Never'),('2','Once a week'),('3','Two or three times a week'), ('4','More than three times a week')], default = "0")
	roomtime = RadioField('roomtime', choices=[('0', 'This does not matter to me'), ('1','Stays in their room for most of the day'),('2','Tend to be in their room more than not'),('3','Usually outside of their room'), ('4','Almost always out and about throughout the day')], default = "0")


	drinks = RadioField('drinks', choices=[('0', 'This does not matter to me'), ('1','Never'),('2','Once a week'),('3','Two or three times a week'), ('4','More than three times a week')], default = "0")
	smokes = RadioField('smokes', choices=[('0', 'This does not matter to me'), ('1','Never'),('2','Very rarely'),('3','A few times a week'), ('4','Multiple times a day')], default = "0")
	studyAmount = RadioField('studyAmount', choices=[('0', 'This does not matter to me'), ('1','Less than an hour a day'),('2','One to three hours a day'),('3','Four to six hours a day'), ('4','More than six hours a day')], default = "0")
	timeBed = RadioField('timeBed', choices=[('0', 'This does not matter to me'), ('1','Before 10 p.m.'),('2','Between 10 p.m. to 12 a.m.'),('3','Between 12 a.m. to 2 a.m.'), ('4','After 2 a.m.')], default = "0")


	sports = RadioField('sports', choices=[('0', 'This does not matter to me'), ('1','Have very little to no interest'),('2','Enjoy watching/playing sports occasionally'),('3','Watch/play sports multiple times a week'), ('4','Watch/play sports almost every day')], default = "0")
	games = RadioField('games', choices=[('0', 'This does not matter to me'), ('1','Have very little to no interest'),('2','Play occasionally'),('3','Play a few hours a week'), ('4','Play a multiple hours a day')], default = "0")
	tv = RadioField('tv', choices=[('0', 'This does not matter to me'), ('1','Hardly ever'),('2','A few hours a week'),('3','An hour a day'), ('4','Multiple hours a day')], default = "0")
	cooking = RadioField('cooking', choices=[('0', 'This does not matter to me'), ('1','Hardly ever'),('2','A few times a week'),('3','Once a day'), ('4','Multiple times a day')], default = "0")


	cleanliness = RadioField('cleanliness', choices=[('0', 'This does not matter to me'), ('1','Very rarely clean each room of their place'),('2','Clean all the rooms a few times a month'),('3','Clean each room once a week'), ('4','Clean their living area almost every day')], default = "0")
	roomTemp = RadioField('roomTemp', choices=[('0', 'This does not matter to them'), ('1','Below 60 degrees F'),('2','Between 60 to 67 degrees F'),('3','Between 68 to 75 degrees F'), ('4','Above 75 degrees F')], default = "0")
	pets = RadioField('pets', choices=[('0', 'This does not matter to me'), ('1','No pets'),('2','Small caged pets'),('3','A large pet'), ('4','Multiple large pets')], default = "0")
	sharing = RadioField('sharing', choices=[('0', 'This does not matter to me'), ('1','Do not like sharing any items'),('2','Do not mind sharing certain items if asked first'),('3','Will share most things if asked'), ('4','Will sharing anything')], default = "0")



class feedback(Form):
	netid1 = StringField("Your NetID")
	netid2 = StringField("Your roommate's NetID")
	rating = SelectField("Roommate Rating", choices = [('', '- Roommate Compatibility Rating -'), ('1','1'),('2','2'),('3','3'), ('4','4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')])

	def validate(self):
		# makes sure that they pick a new username and that their passwords match
		ret = Form.validate(self)
		if(not ret):
			return False

		conn = sqlite3.connect('/home/roommatepairup/mysite/roommates.db')
		cur = conn.cursor()
		netid1 = self.netid1.data
		netid2 = self.netid2.data

		query = "SELECT Net_ID FROM Student" # get all student's netids
		cur.execute(query)
		students = [Net_ID[0] for Net_ID in cur.fetchall()]

		if(netid1 not in students): # make sure they both exist
			self.netid1.errors.append("We do not have that user in our database")
			conn.close()
			return False

		if(netid2 not in students): # make sure they both exist
			self.netid2.errors.append("We do not have that user in our database")
			conn.close()
			return False


		query = "SELECT Student1_Net_ID, Student2_Net_ID FROM roommatePairs"
		cur.execute(query)
		allRoommatePairs = cur.fetchall() # list of pairs of roommates
		for pair in allRoommatePairs:
			if( sorted(pair) == sorted([netid1, netid2]) ): # if this pair has already left feedback
				conn.close()
				self.netid1.errors.append("We already have feedback for this pair")
				return False
		conn.close()
		return True


