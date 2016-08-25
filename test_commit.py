#!/usr/local/bin/python

from subprocess import call
from subprocess import check_output
import threading

def pollForUpdates():
	result = check_output(["git", "pull"])
	while(result.find("Already up-to-date.") != -1):
		result = check_output(["git", "pull"])
	print("GOT AN UPDATE")

t = threading.Thread(target=pollForUpdates, args=())
t.start()

while True:
	a = raw_input()
	call(["git", "commit", "-m", "Test commit", "--allow-empty"])
	call(["git", "push"])

