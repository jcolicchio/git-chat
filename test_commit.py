#!/usr/local/bin/python

from subprocess import call
from subprocess import check_output
import threading
import subprocess
import os

# get the most recent commit
updateMessage = ""
recentCommit = ""

def gitPull():
	with open(os.devnull, 'w') as devnull:
		result = check_output(["git", "pull"], stderr=devnull)
	return result

def logArray():
	with open(os.devnull, 'w') as devnull:
		result = check_output(["git", "log", "--pretty=format:%h %an: %s"], stderr=devnull).split('\n')
	return result

def mostRecentCommitHash():
	with open(os.devnull, 'w') as devnull:
		result = check_output(["git", "log", "-1", "--oneline"], stderr=devnull)[:7]
	return result

def gitPush():
	with open(os.devnull, 'w') as devnull:
		check_output(["git", "push"], stderr=devnull)

def gitCommitMessage(msg):
	with open(os.devnull, 'w') as devnull:
		check_output(["git", "commit", "-m", msg, "--allow-empty"], stderr=devnull)

def sendMessage(msg):
	global recentCommit
	gitPull()
	gitCommitMessage(msg)
	recentCommit = mostRecentCommitHash()
	gitPush()

def getHistory(num):
        with open(os.devnull, 'w') as devnull:
            result = check_output(["git", "log", "--reverse","--pretty=format:%an: %s", "-"+str(num)], stderr=devnull)
        return result;

def pollForUpdates():
	global updateMessage
	global recentCommit
	recentCommit = mostRecentCommitHash()
	while True:
		result = gitPull()
		while(result.find("Already up-to-date.") != -1):
			if len(updateMessage) > 0:
				sendMessage(updateMessage)
				updateMessage = ""
			result = gitPull()
		allLogs = logArray()
		i = 0
		while i < len(allLogs) and allLogs[i][:7] != recentCommit:
			print(allLogs[i][8:])
			i += 1
		recentCommit = allLogs[0][:7]

print getHistory(5)
t = threading.Thread(target=pollForUpdates, args=())
t.start()

while True:
	updateMessage = raw_input()
