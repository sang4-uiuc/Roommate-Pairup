import sqlite3, random
from generateSample import *
from flask import session

def hasTakenSurvey(netID):
	# @ desc searches one of the survey tables to see if their netid is in it, if it is then they
	# have taken the survey, otherwise they haven't
	# @ return boolean indicating whether they have taken the survey or not

	conn = sqlite3.connect('/home/roommatepairup/mysite/roommates.db')
	cur = conn.cursor()
	query = "SELECT * FROM Habits WHERE Net_ID = ?"
	cur.execute(query, (netID,))
	if(cur.fetchone() == None):
		conn.close()
		return False
	else:
		conn.close()
		return True



def insertUserIntoDatabase(data):
	# @ param data the form data, as a hashmap
	# @ return none
	conn = sqlite3.connect('/home/roommatepairup/mysite/roommates.db')
	cur = conn.cursor()
	query = "INSERT INTO Student(Net_ID, Password, Name, Age, Race, Gender, Major, Facebook, Twitter, Email, dormApt) VALUES (?, ?, ?, ?, ?, ? ,?, ?, ?, ?, ?)"

	params = (data["Net_ID"], data["Password"], data["Name"], data["Age"], data["Race"], data["Gender"], data["Major"], data["Facebook"], data["Twitter"], data["Email"], data["dormApt"])
	cur.execute(query, params)
	conn.commit()
	conn.close()

def insertSurveyIntoDatabase(data, Net_ID):
	# @ param data the form data, as a hashmap and their Net_ID
	# @ return none
	conn = sqlite3.connect('/home/roommatepairup/mysite/roommates.db')
	cur = conn.cursor()
	if(hasTakenSurvey(Net_ID)): # if they've already taken the survey, perform updates
		query = "UPDATE Misc SET cleanliness = ?, roomTemp = ?, pets = ?, sharing = ?, checked = ? WHERE Net_ID = ?"
		cur.execute(query, (data['cleanliness'], data['roomTemp'], data['pets'], data['sharing'], data['check_lifestyle'], Net_ID))

		query = "UPDATE Interests SET sports = ?, games = ?, tv = ?, cooking = ?, checked = ? WHERE Net_ID = ?"
		cur.execute(query, (data['sports'], data['games'], data['tv'], data['cooking'], data['check_interest'], Net_ID))

		query = "UPDATE Habits SET drinks = ?, smokes = ?, studyAmount = ?, timeBed = ?, checked = ? WHERE Net_ID = ?"
		cur.execute(query, (data['drinks'], data['smokes'], data['studyAmount'], data['timeBed'], data['check_habit'], Net_ID))

		query = "UPDATE Social SET outgoing = ?, party = ?, guestOver = ?, roomtime = ?, checked = ? WHERE Net_ID = ?"
		cur.execute(query, (data['outgoing'], data['party'], data['guestOver'], data['roomtime'], data['check_social'], Net_ID))




	else: #otherwise insert them for the first time

		query = "INSERT INTO Misc(Net_ID, cleanliness, roomTemp, pets, sharing, checked) VALUES (?, ?, ?, ?, ?, ?)"
		cur.execute(query, (Net_ID, data['cleanliness'], data['roomTemp'], data['pets'], data['sharing'], data['check_lifestyle']))

		query = "INSERT INTO Interests(Net_ID, sports, games, tv, cooking, checked) VALUES (?, ?, ?, ?, ?, ?)"
		cur.execute(query, (Net_ID, data['sports'], data['games'], data['tv'], data['cooking'], data['check_interest']))

		query = "INSERT INTO Habits(Net_ID, drinks, smokes, studyAmount, timeBed, checked) VALUES (?, ?, ?, ?, ?, ?)"
		cur.execute(query, (Net_ID, data['drinks'], data['smokes'], data['studyAmount'], data['timeBed'], data['check_habit']))

		query = "INSERT INTO Social(Net_ID, outgoing, party, guestOver, roomtime, checked) VALUES (?, ?, ?, ?, ?, ?)"
		cur.execute(query, (Net_ID, data['outgoing'], data['party'], data['guestOver'], data['roomtime'], data['check_social']))


	conn.commit()
	conn.close()

def updateUserProfile(data):
	# @ desc updates the user's record in the database to match what they just entereed
	# @ param data the form data, as a hashmap
	# @ return none

	conn = sqlite3.connect('/home/roommatepairup/mysite/roommates.db')
	cur = conn.cursor()

	if(data["newPassword"] != ""):
		query = "UPDATE Student SET Password = ? WHERE Net_ID = ?"
		cur.execute(query, (data["newPassword"], session["username"]) )
		conn.commit()

	if(data["Email"] != ""):
		query = "UPDATE Student SET Email = ? WHERE Net_ID = ?"
		cur.execute(query, (data["Email"], session["username"]) )
		conn.commit()
	print data["delete"]

	if(data["delete"] == True):
		query = "DELETE FROM Student WHERE Net_ID = ?"
		cur.execute(query, (session["username"],))

		query = "DELETE FROM Habits WHERE Net_ID = ?"
		cur.execute(query, (session["username"],))

		query = "DELETE FROM Interests WHERE Net_ID = ?"
		cur.execute(query, (session["username"],))

		query = "DELETE FROM Misc WHERE Net_ID = ?"
		cur.execute(query, (session["username"],))

		query = "DELETE FROM Social WHERE Net_ID = ?"
		cur.execute(query, (session["username"],))

		session["logged_in"] = False
		conn.commit()

	conn.close()



def bestMatches(social, interests, habits, misc, Net_ID):
	# @ desc finds the closest matches for the roommate depending on their responses
	# @ param social, 0 if they checked the box, 1 if they didn't
	# @ param interests, 0 if they checked the box, 1 if they didn't
	# @ param habits, 0 if they checked the box, 1 if they didn't
	# @ param misc, 0 if they checked the box, 1 if they didn't
	# @ param Net_ID, the Net_ID of the user searching for roommates
	# @ return a list of [Name, Age, Major, Email] for each match, up to 5

	total = social + interests + habits + misc
	if(total == 0):
		social = 1
		interests = 1
		habits = 1
		misc = 1
		total = 4

	conn = sqlite3.connect('/home/roommatepairup/mysite/roommates.db')
	cur = conn.cursor()
	query = "SELECT Gender, dormApt FROM Student WHERE Net_ID = ?"
	cur.execute(query, (Net_ID,))
	results = cur.fetchone()
	gender = results[0]
	dormApt = results[1]

	params = []

	for coef in getCoefs(social, interests, habits, misc):
		params.append(coef)
		params.append(Net_ID)
	params.append(Net_ID)
	params.append(gender)
	# params.append(dormApt)

	params = tuple(params)



	view_string = 'CREATE TEMP VIEW Joined_Attributes AS\n'
	view_string = view_string + 'SELECT '
	first_cat = 1
	paramlist = [social,interests,habits,misc]
	view_string += 'Student.*,'

	if (social == 1):
		view_string = view_string + 'SOCIAL.*'
		first_cat = 0

	if interests == 1:
		if first_cat == 1:
			view_string = view_string + 'Interests.*'
			first_cat = 0
		else:
			view_string = view_string + ', Interests.*'
	if habits == 1:
                if first_cat == 1:
                        view_string = view_string + 'Habits.*'
                        first_cat = 0
                else:
                        view_string = view_string + ', Habits.*'
	if misc == 1:
                if first_cat == 1:
                        view_string = view_string + 'Misc.*'
                        first_cat = 0
                else:
                        view_string = view_string + ', Misc.*'

	view_string+= '\nFROM '
	first_cat = 1
	last_one = 0
	if (social == 1):
                view_string = view_string + 'Social\n'
                first_cat = 0
                last_one = 1
        if interests == 1:
                if first_cat == 1:
                        view_string = view_string + 'Interests'
                        first_cat = 0
                else:
                        view_string = view_string + '\tINNER JOIN Interests\n\t ON Interests.Net_ID = Social.Net_ID\n'
                last_one = 2
        if habits == 1:
                if first_cat == 1:
                        view_string = view_string + 'Habits\n'
                        first_cat = 0
                elif (first_cat == 0 and paramlist[1] == 1):
                        view_string = view_string + '\tINNER JOIN Habits\n\t ON Habits.Net_ID = Interests.Net_ID\n'
		else:
			view_string = view_string + '\tINNER JOIN Habits\n\t ON Habits.Net_ID = Social.Net_ID\n'
			last_one = 3
        if misc == 1:
                if first_cat == 1:
                        view_string = view_string + 'Misc\n'
                        first_cat = 0
                elif first_cat == 0 and paramlist[2] == 1:
                        view_string = view_string + '\tINNER JOIN Misc\n\t ON Misc.Net_ID = Habits.Net_ID\n'
                elif first_cat == 0 and paramlist[1] == 1:
                        view_string = view_string + '\tINNER JOIN Misc\n\t ON Misc.Net_ID = Interests.Net_ID\n'
		else:
			view_string = view_string + '\tINNER JOIN Misc\n\t ON Misc.Net_ID = Social.Net_ID\n'
		last_one = 4
	if last_one == 4:
		view_string += '\tINNER JOIN Student\n\t ON Student.Net_ID = Misc.Net_ID\n'
	if last_one == 3:
                view_string += '\tINNER JOIN Student\n\t ON Student.Net_ID = Habits.Net_ID\n'
	if last_one == 2:
                view_string += '\tINNER JOIN Student\n\t ON Student.Net_ID = Interests.Net_ID\n'
	if last_one == 1:
                view_string += '\tINNER JOIN Student\n\t ON Student.Net_ID = Social.Net_ID\n'

	view_string = view_string[:-1]
	sel_string = 'SELECT Net_ID,'
	if (social == 1):
		sel_string = sel_string + '(? * ABS(outgoing - (SELECT outgoing FROM Joined_Attributes WHERE Net_ID = ?))) +\n'
		sel_string+= '(? * ABS(party - (SELECT party FROM Joined_Attributes WHERE Net_ID = ?))) + \n'
		sel_string+= '(? * ABS(guestOver - (SELECT guestOver FROM Joined_Attributes WHERE Net_ID = ?))) + \n'
		sel_string+=    '(? * ABS(roomtime - (SELECT roomtime FROM Joined_Attributes WHERE Net_ID = ?)))\n'
		first_cat = 0
	if misc == 1:
		if first_cat ==0:
			sel_string+= '+ '
		sel_string+= '(? * ABS(cleanliness - (SELECT cleanliness FROM Joined_Attributes WHERE Net_ID = ?))) +\n'
		sel_string+= '(? * ABS(roomTemp - (SELECT roomTemp FROM Joined_Attributes WHERE Net_ID = ?))) +\n'
		sel_string+= '(? * ABS(pets - (SELECT pets FROM Joined_Attributes WHERE Net_ID = ?))) +\n'
		sel_string+= '(? * ABS(sharing - (SELECT sharing FROM Joined_Attributes WHERE Net_ID = ?)))\n'
		first_cat = 0
	if interests == 1:
		if first_cat == 0:
			sel_string += '+ '
		sel_string+= '(? * ABS(sports - (SELECT sports FROM Joined_Attributes WHERE Net_ID = ?))) +\n'
		sel_string+=    '(? * ABS(games - (SELECT games FROM Joined_Attributes WHERE Net_ID = ?))) +\n'
		sel_string+=    '(? * ABS(tv - (SELECT tv FROM Joined_Attributes WHERE Net_ID = ?))) +\n'
		sel_string+=    '(? * ABS(cooking - (SELECT cooking FROM Joined_Attributes WHERE Net_ID = ?)))\n'
		first_cat = 0
	if habits == 1:
		if first_cat == 0:
			sel_string+= '+ '
		sel_string += '(? * ABS(drinks - (SELECT drinks FROM Joined_Attributes WHERE Net_ID = ?))) +\n'
		sel_string += ' (? * ABS(smokes - (SELECT smokes FROM Joined_Attributes WHERE Net_ID = ?))) +\n'
		sel_string += '(? * ABS(studyAmount - (SELECT studyAmount FROM Joined_Attributes WHERE Net_ID = ?))) +\n'
		sel_string += '(? * ABS(timeBed - (SELECT timeBed FROM Joined_Attributes WHERE Net_ID = ?)))'
	sel_string+= 'AS total FROM Joined_Attributes WHERE Net_ID != ? AND Gender = ? ORDER BY total DESC LIMIT 4'
	print(view_string)
	cur.execute(view_string)
	print sel_string
	cur.execute(sel_string, params)
	results = cur.fetchall()
	ret = []


	for result in results:
		query = "SELECT Name, Age, Major, Email FROM Student WHERE Net_ID = ?"
		cur.execute(query, (result[0],))
		ret.append(cur.fetchone())
	conn.close()
	return ret


# print userSelect(1, 1, 1, 1, "miller13")


# def findMatches(netID):

# 	conn = sqlite3.connect("roommates.db")
# 	cur = conn.cursor()
# 	params = []

# 	for weight in getWeights(4):
# 		params.append(weight)
# 		params.append(netID)
# 	params.append(netID)
# 	params = tuple(params)

# 	cur.execute('''
# 	CREATE TEMP VIEW Joined_Attributes AS
# 	SELECT Social.*, Interests.*, Habits.*, Misc.*
# 	FROM Social
# 	    INNER JOIN Interests
# 	        ON Interests.Net_ID = Social.Net_ID
# 	    INNER JOIN Habits
# 	        ON Habits.Net_ID = Interests.Net_ID
# 	    INNER JOIN Misc
# 	        ON Misc.Net_ID = Habits.Net_ID''')


# 	cur.execute('''
# 	SELECT Net_ID,  (? * ABS(outgoing - (SELECT outgoing FROM Joined_Attributes WHERE Net_ID = ?))) +
# 	            (? * ABS(party - (SELECT party FROM Joined_Attributes WHERE Net_ID = ?))) +
# 	            (? * ABS(guestOver - (SELECT guestOver FROM Joined_Attributes WHERE Net_ID = ?))) +
# 	            (? * ABS(roomtime - (SELECT roomtime FROM Joined_Attributes WHERE Net_ID = ?))) +
# 	            (? * ABS(cleanliness - (SELECT cleanliness FROM Joined_Attributes WHERE Net_ID = ?))) +
# 	            (? * ABS(roomTemp - (SELECT roomTemp FROM Joined_Attributes WHERE Net_ID = ?))) +
# 	            (? * ABS(pets - (SELECT pets FROM Joined_Attributes WHERE Net_ID = ?))) +
# 	            (? * ABS(sharing - (SELECT sharing FROM Joined_Attributes WHERE Net_ID = ?))) +
# 	            (? * ABS(sports - (SELECT sports FROM Joined_Attributes WHERE Net_ID = ?))) +
# 	            (? * ABS(games - (SELECT games FROM Joined_Attributes WHERE Net_ID = ?))) +
# 	            (? * ABS(tv - (SELECT tv FROM Joined_Attributes WHERE Net_ID = ?))) +
# 	            (? * ABS(cooking - (SELECT cooking FROM Joined_Attributes WHERE Net_ID = ?))) +
# 	            (? * ABS(drinks - (SELECT drinks FROM Joined_Attributes WHERE Net_ID = ?))) +
# 	            (? * ABS(smokes - (SELECT smokes FROM Joined_Attributes WHERE Net_ID = ?))) +
# 	            (? * ABS(studyAmount - (SELECT studyAmount FROM Joined_Attributes WHERE Net_ID = ?))) +
# 	            (? * ABS(timeBed - (SELECT timeBed FROM Joined_Attributes WHERE Net_ID = ?))) AS total
# 	FROM Joined_Attributes WHERE Net_ID != ? ORDER BY total DESC LIMIT 5''', params)

# 	results = cur.fetchall()

# 	ret = []
# 	for result in results:
# 		query = "SELECT Name, Age, Major, Email FROM Student WHERE Net_ID = ?"
# 		cur.execute(query, (result[0],))
# 		ret.append(cur.fetchone())
# 	return ret
# print findMatches("miller13")

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

#def exactMatches(Net_ID, responseHash):
	# @ desc takes in a net_id and the responses for their ideal roommate, searches the database for all exact matches and returns a list of them
	# @ param Net_ID, the Net_ID of the user who is searching
	# @ param responseHash, the hash of "question": "answer" for all questions
	# @ return a list of the matching roommates
#	pass
#	return [[1, 2, 3], [1, 2, 3], [1, 2, 3]]

def getUserChecks(Net_ID):
	# @ desc gets the categories that the user marked as important to him (social, interests, misc, habits)
	# @ desc so that we can pass that information to get potentialMatches()
	# @ param Net_ID the Net_ID of the user searching
	# @ return [social, interests, misc, habits] where each is 0 or 1 depending on whether that's important to the user or not
	ret = []
	conn = sqlite3.connect('/home/roommatepairup/mysite/roommates.db')
	cur = conn.cursor()



	query = "SELECT checked FROM Social WHERE Net_ID = ?"
	cur.execute(query, (Net_ID,))
	ret.append(cur.fetchone()[0])

	query = "SELECT checked FROM Interests WHERE Net_ID = ?"
	cur.execute(query, (Net_ID,))
	ret.append(cur.fetchone()[0])

	query = "SELECT checked FROM Habits WHERE Net_ID = ?"
	cur.execute(query, (Net_ID,))
	ret.append(cur.fetchone()[0])

	query = "SELECT checked FROM Misc WHERE Net_ID = ?"
	cur.execute(query, (Net_ID,))
	ret.append(cur.fetchone()[0])


	conn.close()
	return ret

def verifyNet_IDs(data):
	# @ desc takes in two net_ids and makes sure they aren't already in the database as leaving feedback and that they are valid
	# @ param data a hash map {netid1: value, netid2: value, rating: value}
	# @ return true if valid, false otherwise

	conn = sqlite3.connect('/home/roommatepairup/mysite/roommates.db')
	cur = conn.cursor()
	netid1 = data["netid1"]
	netid2 = data["netid2"]

	query = "SELECT Net_ID FROM Student" # get all student's netids
	cur.execute(query)
	students = [Net_ID[0] for Net_ID in cur.fetchall()]
	if(netid1 not in students or netid2 not in students): # make sure they both exist
		conn.close()
		return False

	query = "SELECT Student1_Net_ID, Student2_Net_ID FROM roommatePairs"
	cur.execute(query)
	allRoommatePairs = cur.fetchall() # list of pairs of roommates
	for pair in allRoommatePairs:
		if( sorted(pair) == sorted([netid1, netid2]) ): # if this pair has already left feedback
			conn.close()
			return False
	conn.close()
	return True

def insertFeedback(data):
	 # @ desc inserts the feedback into the roommatePairs table
	 # @ param data a hash map {netid1: value, netid2: value, rating: value}
	 # @ return None

	 conn = sqlite3.connect('/home/roommatepairup/mysite/roommates.db')
	 cur = conn.cursor()
	 print data
	 query = "INSERT INTO roommatePairs(Student1_Net_ID, Student2_Net_ID, success) VALUES(?, ?, ?)"
	 cur.execute(query, (data["netid1"], data["netid2"], data["rating"]))
	 conn.commit()
	 conn.close()
	 return


def exactMatches(Net_ID, response):

	conn = sqlite3.connect('/home/roommatepairup/mysite/roommates.db')
	cur = conn.cursor()
	query = "SELECT Gender, dormApt FROM Student WHERE Net_ID = ?"
	cur.execute(query, (Net_ID,))
	results = cur.fetchone()
	print results
	gender = results[0]
	dormApt = results[1]

	social = 0
	interests = 0
	habits = 0
	misc = 0

	if response['outgoing'] + response['party'] + response['guestOver'] + response['roomtime'] != 0:
		social = 1

	if response['sports'] + response['games'] + response['tv'] + response['cooking'] != 0:
		interests = 1

	if response['drinks'] + response['smokes'] + response['studyAmount'] + response['timeBed'] != 0:
		habits = 1

	if response['cleanliness'] + response['roomTemp'] + response['pets'] + response['sharing'] != 0:
		misc = 1

	if social + interests + habits + misc == 0:
		bestMatches(social, interests, habits, misc, Net_ID)

	else:
		view_string = 'CREATE TEMP VIEW Joined_Attributes AS\n'
		view_string += 'SELECT '
		first_cat = 1
		paramlist = [social,interests,habits,misc]
		view_string += 'Student.*,'

		if social == 1:
			view_string += 'Social.*'
			first_cat = 0

		if interests == 1:
			if first_cat == 1:
				view_string += 'Interests.*'
				first_cat = 0
			else:
				view_string += ', Interests.*'
		if habits == 1:
			if first_cat == 1:
				view_string += 'Habits.*'
				first_cat = 0
			else:
				view_string += ', Habits.*'
		if misc == 1:
			if first_cat == 1:
				view_string += 'Misc.*'
				first_cat = 0
			else:
				view_string += ', Misc.*'


		view_string+= '\nFROM '
		first_cat = 1
		last_one = 0
		if social == 1:
			view_string = view_string + 'Social\n'
			first_cat = 0
			last_one = 1
		if interests == 1:
			if first_cat == 1:
				view_string = view_string + 'Interests'
				first_cat = 0
			else:
				view_string = view_string + '\tINNER JOIN Interests\n\t ON Interests.Net_ID = Social.Net_ID\n'
				last_one = 2
		if habits == 1:
			if first_cat == 1:
				view_string = view_string + 'Habits\n'
				first_cat = 0
			elif (first_cat == 0 and paramlist[1] == 1):
				view_string = view_string + '\tINNER JOIN Habits\n\t ON Habits.Net_ID = Interests.Net_ID\n'
			else:
				view_string = view_string + '\tINNER JOIN Habits\n\t ON Habits.Net_ID = Social.Net_ID\n'
				last_one = 3
		if misc == 1:
			if first_cat == 1:
				view_string = view_string + 'Misc\n'
				first_cat = 0
			elif first_cat == 0 and paramlist[2] == 1:
				view_string = view_string + '\tINNER JOIN Misc\n\t ON Misc.Net_ID = Habits.Net_ID\n'
			elif first_cat == 0 and paramlist[1] == 1:
				view_string = view_string + '\tINNER JOIN Misc\n\t ON Misc.Net_ID = Interests.Net_ID\n'
			else:
				view_string = view_string + '\tINNER JOIN Misc\n\t ON Misc.Net_ID = Social.Net_ID\n'
			last_one = 4
		if last_one == 4:
			view_string += '\tINNER JOIN Student\n\t ON Student.Net_ID = Misc.Net_ID\n'
		if last_one == 3:
			view_string += '\tINNER JOIN Student\n\t ON Student.Net_ID = Habits.Net_ID\n'
		if last_one == 2:
			view_string += '\tINNER JOIN Student\n\t ON Student.Net_ID = Interests.Net_ID\n'
		if last_one == 1:
			view_string += '\tINNER JOIN Student\n\t ON Student.Net_ID = Social.Net_ID\n'



		params = []
		params.append(gender)
		params.append(Net_ID)
		view_string = view_string[:-1]
		sel_string = 'SELECT Net_ID\nFROM Joined_Attributes\nWHERE gender = ? AND Net_ID != ?'
		if response['outgoing'] != 0:
			sel_string += ' AND outgoing = ?'
			params.append(response['outgoing'])
		if response['party'] != 0:
			sel_string += ' AND party = ?'
			params.append(response['party'])
		if response['guestOver'] != 0:
			sel_string += ' AND guestOver = ?'
			params.append(response['guestOver'])
		if response['roomtime'] != 0:
			sel_string += ' AND roomtime = ?'
			params.append(response['roomtime'])
		if response['sports'] != 0:
			sel_string += ' AND sports = ?'
			params.append(response['sports'])
		if response['games'] != 0:
			sel_string += ' AND games = ?'
			params.append(response['games'])
		if response['tv'] != 0:
			sel_string += ' AND tv = ?'
			params.append(response['tv'])
		if response['cooking'] != 0:
			sel_string += ' AND cooking = ?'
			params.append(response['cooking'])
		if response['drinks'] != 0:
			sel_string += ' AND drinks = ?'
			params.append(response['drinks'])
		if response['smokes'] != 0:
			sel_string += ' AND smokes = ?'
			params.append(response['smokes'])
		if response['studyAmount'] != 0:
			sel_string += 'AND studyAmount = ?'
			params.append(response['studyAmount'])
		if response['timeBed'] != 0:
			sel_string += ' AND timeBed = ?'
			params.append(response['timeBed'])
		if response['cleanliness'] != 0:
			sel_string += ' AND cleanliness = ?'
			params.append(response['cleanliness'])
		if response['roomTemp'] != 0:
			sel_string += ' AND roomTemp = ?'
			params.append(response['roomTemp'])
		if response['pets'] != 0:
			sel_string += ' AND pets = ?'
			params.append(response['pets'])
		if response['sharing'] != 0:
			sel_string += 'AND sharing = ?'
			params.append(response['sharing'])

		sel_string += 'LIMIT 4'
		params = tuple(params)
		print(view_string)
		cur.execute(view_string)
		print sel_string
		cur.execute(sel_string, params)
		results = cur.fetchall()
		ret = []

		for result in results:
			query = "SELECT Name, Age, Major, Email FROM Student WHERE Net_ID = ?"
			cur.execute(query, (result[0],))
			ret.append(cur.fetchone())
		conn.close()
		return ret

# response = {'outgoing' : 0, 'party' : 0, 'guestOver' : 0, 'roomtime' : 0, 'sports' : 0, 'games' : 0, 'tv' : 0, 'cooking' : 0, 'drinks' : 0, 'smokes' : 0, 'studyAmount': 0, 'timeBed' : 0, 'cleanliness' : 0, 'roomTemp' : 0, 'pets' : 0, 'sharing' : 3}
# mylist = exactMatches("miller13", response)
# print mylist[0][0]


