import csv
import math
from queries import *
import sqlite3
rows = []
def parse():
	lines = open("ResponsesForm.csv").read().splitlines()
	for i in range(2,len(lines)):
		rows.append(lines[i].split(','))
	print rows
	conn = sqlite3.connect("roommatePairup.db")
	cur = conn.cursor()

	for i in range(len(rows)):
		rows[i][18] = "regressionUser"+ str(i)
		rows[i][35] = "regressionUser"+ str(i+35)
		pairs = {"netid1": str(rows[i][18]), "netid2": str(rows[i][35]), "rating": str(rows[i][36]) }

		# insert into roommatepairs
		insertFeedback(pairs)

		varList = ['outgoing', 'party', 'guestOver','drinks', 'smokes', 'studyAmount','timeBed', 'roomtime','sports', 'games', 'tv', 'cooking', 'cleanliness', 'roomTemp', 'pets', 'sharing']
		Userdata1 = {}
		Userdata2= {}
		for j in range(16):
			Userdata1[varList[j]] = str(rows[i][j+2])
			Userdata2[varList[j]] =  str(rows[i][j+19])

		insertSurveyIntoDatabase(Userdata1, str(rows[i][18]))
		insertSurveyIntoDatabase(Userdata2, str(rows[i][35]))
	conn.commit()
	conn.close()


# parse()



