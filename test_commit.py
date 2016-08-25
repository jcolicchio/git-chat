#!/usr/local/bin/python

from subprocess import call
call(["touch", "dingus"])
call(["git", "add", "dingus"])
call(["git", "commit", "-m", "Test commit"])
call(["git", "push"])
