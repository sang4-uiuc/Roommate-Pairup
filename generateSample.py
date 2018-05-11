import random, csv
import numpy as np
from sklearn import linear_model
import sqlite3
from queries import *


def randomlyPopulate():
	maleNames = ["Brandon", "Matt", "Ryan", "Bryan", "James", "Robert", "Michael", "John", "Austin", "Spencer"]
	femaleNames = ["Mary", "Patricia", "Jennifer", "Elizabeth", "Linda", "Barbara", "Susan", "Lisa", "Kelly", "Kara", "Kayla"]
	lastNames = ["Smith", "Jones", "Johnson", "Williams", "Brown", "Davis", "Miller", "Wilson", "Moore", "Hardy", "Harambe"]
	majors = ["Aerospace", "Mechanical", "Industrial", "History", "Chemistry", "Biology", "Spanish", "CS", "Computer", "Nuclear"]
	races = ["Hispanic", "White", "Black", "Chinese", "Japenese"]

	conn = sqlite3.connect('/home/roommatepairup/mysite/roommates.db')
	cur = conn.cursor()
	netIDs = []
	n = 100
	for i in range(n):
		query = "INSERT INTO Student(Net_ID, Name, Age, Race, Gender, Major, isAvailable) VALUES (?, ?, ?, ?, ?, ?, ?)"

		if(random.uniform(0, 1) < 0.5):
			firstName = random.choice(maleNames)
			gender = "Male"
		else:
			firstName = random.choice(femaleNames)
			gender = "Female"

		lastName = random.choice(lastNames)
		name = firstName + " " + lastName
		netID = lastName.lower() + str(random.randint(0, n))

		while(netID in netIDs):
			netID = lastName.lower() + str(random.randint(0, n))
		netIDs.append(netID)

		print netID
		age = random.randint(18, 23)
		race = random.choice(races)
		major = random.choice(majors)
		isAvailable = 1
		cur.execute(query, (netID, name, age, race, gender, major, isAvailable))

		query = "INSERT INTO Social(Net_ID, outgoing, party, guestOver, roomtime) VALUES (?, ?, ?, ?, ?)"
		cur.execute(query, (netID, random.randint(1, 4), random.randint(1, 4), random.randint(1, 4), random.randint(1, 4)))

		query = "INSERT INTO Interests(Net_ID, sports, games, tv, cooking) VALUES (?, ?, ?, ?, ?)"
		cur.execute(query, (netID, random.randint(1, 4), random.randint(1, 4), random.randint(1, 4), random.randint(1, 4)))

		query = "INSERT INTO Habits(Net_ID, drinks, smokes, studyAmount, timeBed) VALUES (?, ?, ?, ?, ?)"
		cur.execute(query, (netID, random.randint(1, 4), random.randint(1, 4), random.randint(1, 4), random.randint(1, 4)))

		query = "INSERT INTO Misc(Net_ID, cleanliness, roomTemp, pets, sharing) VALUES (?, ?, ?, ?, ?)"
		cur.execute(query, (netID, random.randint(1, 4), random.randint(1, 4), random.randint(1, 4), random.randint(1, 4)))

	conn.commit()
	conn.close()
def getStudentHabits(Net_ID):
	# @ desc gets the student with Net_ID's responses for the habits category
	# @ param Net_ID the Net_ID of the student we want
	# @ return a list of the 4 responses

	conn = sqlite3.connect('/home/roommatepairup/mysite/roommates.db')
	cur = conn.cursor()
	query = "SELECT drinks, smokes, studyAmount, timeBed FROM Habits WHERE Net_ID = ?"
	cur.execute(query, (Net_ID,))
	habits = cur.fetchone()
	conn.close()
	return habits

def getStudentInterests(Net_ID):
	# @ desc gets the student with Net_ID's responses for the interests category
	# @ param Net_ID the Net_ID of the student we want
	# @ return a list of the 4 responses

	conn = sqlite3.connect('/home/roommatepairup/mysite/roommates.db')
	cur = conn.cursor()
	query = "SELECT sports, games, tv, cooking FROM Interests WHERE Net_ID = ?"
	cur.execute(query, (Net_ID,))
	interests = cur.fetchone()
	conn.close()
	return interests

def getStudentSocial(Net_ID):
	# @ desc gets the student with Net_ID's responses for the social category
	# @ param Net_ID the Net_ID of the student we want
	# @ return a list of the 4 responses

	conn = sqlite3.connect('/home/roommatepairup/mysite/roommates.db')
	cur = conn.cursor()
	query = "SELECT outgoing, party, guestOver, roomtime FROM Social WHERE Net_ID = ?"
	cur.execute(query, (Net_ID,))
	social = cur.fetchone()
	conn.close()
	return social

def getStudentMisc(Net_ID):
	# @ desc gets the student with Net_ID's responses for the misc category
	# @ param Net_ID the Net_ID of the student we want
	# @ return a list of the 4 responses

	conn = sqlite3.connect('/home/roommatepairup/mysite/roommates.db')
	cur = conn.cursor()
	query = "SELECT cleanliness, roomTemp, pets, sharing FROM Misc WHERE Net_ID = ?"
	cur.execute(query, (Net_ID,))
	misc = cur.fetchone()
	conn.close()
	return misc





def generateRoommatePairs():
	stud1 = 1
	stud2 = 2
	conn = sqlite3.connect('/home/roommatepairup/mysite/roommates.db')
	cur = conn.cursor()

	query = "SELECT Net_ID FROM Student"
	cur.execute(query)
	allNetIDS = [netID[0] for netID in cur.fetchall()]
	for i in range(1000):
		randomPair = random.sample(allNetIDS, 2)
		query = "INSERT INTO roommatePairs(Student1_Net_ID, Student2_Net_ID, success) VALUES(?, ?, ?)"
		randSuccess = random.randint(1, 10)
		cur.execute(query, (randomPair[0], randomPair[1], randSuccess))
	conn.commit()
	conn.close()
	return "Completed Inserting Random Data"



# print generateRoommatePairs()

# SOURCE: http://stackoverflow.com/questions/1147906
# 4/multiple-linear-regression-in-python

def listDiff(list1, list2):
	# @ desc takes two lists of integers and subtracts them using absolute value
	# @ param list1 the first list
	# @ param list2 the second list
	# @ return ret
	print list1, list2
	assert(len(list1) == len(list2))
	ret = []
	for i in range(len(list1)):
		ret.append( abs(list1[i] - list2[i]) )
	return ret

def getCoefs(habits, interests, misc, social):
	all_xs = []
	ys = []

	conn = sqlite3.connect('/home/roommatepairup/mysite/roommates.db')
	cur = conn.cursor()
	query = "SELECT Student1_Net_ID, Student2_Net_ID, success FROM roommatePairs"
	cur.execute(query)
	pairs = cur.fetchall()

	for pair in pairs:
		xs = []
		s1_id = pair[0]
		s2_id = pair[1]
		success = pair[2]
		if(habits):
			s1_habits = getStudentHabits(s1_id)
			s2_habits = getStudentHabits(s2_id)
			print s1_id, s2_id, s1_habits, s2_habits
			diff_habits = listDiff(s1_habits, s2_habits)
			xs += diff_habits

		if(interests):
			s1_interests = getStudentInterests(s1_id)
			s2_interests = getStudentInterests(s2_id)
			diff_interests = listDiff(s1_interests, s2_interests)
			xs += diff_interests

		if(misc):
			s1_misc = getStudentMisc(s1_id)
			s2_misc = getStudentMisc(s2_id)
			diff_misc = listDiff(s1_misc, s2_misc)
			xs += diff_misc

		if(social):
			s1_social = getStudentSocial(s1_id)
			s2_social = getStudentSocial(s2_id)
			diff_social = listDiff(s1_social, s2_social)
			xs += diff_social
		all_xs.append(xs)
		ys.append(success)
	conn.close()
	clf = linear_model.LinearRegression()
	clf.fit(all_xs, ys)
	return clf.coef_

print np.dot(getCoefs(1, 1, 1, 1), [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1])
# print getWeights(4)