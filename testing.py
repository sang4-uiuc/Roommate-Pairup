from queries import *
from generateSample import *
import numpy as np


def test_getHabits():
	Net_ID = "miller13"
	habits = getStudentHabits(Net_ID)
	assert(habits[0] == 2 and habits[1] == 2 and habits[2] == 4 and habits[3] == 1)
	return "Passed test_getHabits()"

def test_getInterests():
	Net_ID = "miller13"
	interests = getStudentInterests(Net_ID)
	assert(interests[0] == 1 and interests[1] == 4 and interests[2] == 4 and interests[3] == 3)
	return "Passed test_getInterests()"


def test_getSocial():
	Net_ID = "miller13"
	social = getStudentSocial(Net_ID)
	assert(social[0] == 1 and social[1] == 2 and social[2] == 4 and social[3] == 2)
	return "Passed test_getSocial()"

def test_getMisc():
	Net_ID = "miller13"
	misc = getStudentMisc(Net_ID)
	assert(misc[0] == 1 and misc[1] == 1 and misc[2] == 2 and misc[3] == 3)
	return "Passed test_getMisc()"

def test_listDiff():
	list1 = [1, 1, 2, 3, 1]
	list2 = [1, 2, 1, 4, 1]

	assert(listDiff(list1, list2) == [0, 1, 1, 1, 0])



def test_getCoefs():
	all4 = getCoefs(1, 1, 1, 1)
	assert(len(all4) == 16)
	print all4
	return "Passed getCoefs"

def test_getSuccess():
	inputs = [0] * 13 + [1, 1, 1]
	coefs = getCoefs(1, 1, 1, 1)
	return np.dot(inputs, coefs)
	return "Passed getSuccess"


def test_getUserChecks():
	Net_ID = "miller13"
	results = getUserChecks(Net_ID)
	assert(results[0] == 1 and results[1] == 0 and results[2] == 0 and results[3] == 1)
	return "Passed getUserChecks"



print test_getHabits()
print test_getInterests()
print test_getSocial()
print test_getMisc()
print test_listDiff()
print test_getCoefs()
print test_getSuccess()
print test_getUserChecks()