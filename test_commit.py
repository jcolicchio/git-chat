#!/usr/local/bin/python

from subprocess import call
from subprocess import check_output
import threading

# get the most recent commit
updateMessage = ""
recentCommit = ""

def gitPull():
	check_output(["git", "pull"])

def mostRecentCommitHash():
	return check_output(["git", "log", "-1", "--oneline"])[:7]

def sendMessage(msg):
	global recentCommit
	gitPull()
	check_output(["git", "commit", "-m", msg, "--allow-empty"])
	recentCommit = mostRecentCommitHash()
	check_output(["git", "push"])

def pollForUpdates():
	global updateMessage
	global recentCommit
	recentCommit = check_output(["git", "log", "--oneline"]).split('\n')[0][:7]
	while True:
		result = check_output(["git", "pull"])
		while(result.find("Already up-to-date.") != -1):
			if len(updateMessage) > 0:
				sendMessage(updateMessage)
				updateMessage = ""
			result = check_output(["git", "pull"])
		allLogs = check_output(["git", "log", "--oneline"]).split('\n')
		i = 0
		while i < len(allLogs) and allLogs[i][:7] != recentCommit:
			print(allLogs[i][8:])
			i += 1
		recentCommit = allLogs[0][:7]

t = threading.Thread(target=pollForUpdates, args=())
t.start()

while True:
	updateMessage = raw_input()

