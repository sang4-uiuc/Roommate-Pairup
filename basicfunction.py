import sqlite3

def check(netID, RoommateNet_ID):
	netid = netID
	
	conn = sqlite3.connect('roommates.db')
	cur = conn.cursor()
	query = 'SELECT RoommateNet_ID FROM Feedback WHERE Net_ID = ?'
	cur.execute(query, (netid,))
	#fetches all roommate netIDs
	rows = cur.fetchall()
	conn.close()
	#have to make rmid into a tuple because fetchall returns a list of tuples
	rmid = ((RoommateNet_ID),)
	if(rmid in rows):
		return True
	else:
		return False


def basicfunction():

	netid = raw_input('Enter NetID: ')
	rmid = raw_input("Enter Roommate's NetID: ")
	score = raw_input("Enter your compatibility score: ")

	conn = sqlite3.connect("roommates.db")
	cur = conn.cursor()

	#cur.execute('''
	#CREATE TABLE IF NOT EXISTS Feedback (Net_ID TEXT, RoommateNet_ID TEXT, comp_score INT)''')
	

	if(check(netid, rmid) == False):
		cur.execute('''INSERT INTO Feedback (Net_ID, RoommateNet_ID, comp_score) VALUES (?, ?, ?)''', (netid, rmid, score))
		print("successfully inserted")
	elif(check(netid, rmid) == True):
		print("Roommate pair already exists in database")


	conn.commit()
	conn.close()

basicfunction()