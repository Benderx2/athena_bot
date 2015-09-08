# -*- coding: utf-8 -*-

import os
import sys
import socket
import threading
import ast
import signal
import types

# user modules

import irc
import variables
import bfc
import bec
import ulc
import utils
import help
import parser

from datetime import datetime
from datetime import date
from pytz import timezone
from random import randint

import pytz

import operator as op

def ten_sec_handler(signum, frame):
	variables.time_counter += 1

import types
def imports():
    for name, val in globals().items():
        if isinstance(val, types.ModuleType):
            yield val.__name__
def restart_bot():
	python = sys.executable
	os.execl(python, python, * sys.argv)

def quit_bot():
	variables.ircsock.send("QUIT :User Quit\n\r")
	sys.exit("bot exit")

def main_loop():
	while 1:
		irc_message = variables.ircsock.recv(8192)
		irc_message = irc_message.strip('\n\r')
		signal.alarm(0)
		variables.time_counter = 0
		print(irc_message)
		output = "Output: "
		mystr = irc.parse_msg(irc_message)
		if mystr['COMMAND'] == "PRIVMSG":
				if len(mystr['ARGS']) == 0:
					variables.channel = "#rxvm"
				else:
					variables.channel = mystr['ARGS'][0]
				if variables.channel == variables.botnick:
					variables.channel = variables.old_channel
				else:
					variables.old_channel = mystr['ARGS'][0]
				myinput = ""
				if mystr['ARGS'][1].startswith("ath", 0, len("ath")) == True:
					mycode = mystr['ARGS'][1].replace("ath", "")
					if mycode.startswith(".reload", 0, 7):
						mycode = mycode.replace(".reload", "").replace(" ", "")
						user = mystr['PREFIX']
						user = user.split('!')
						if user[0] != variables.head_user:
							irc.send_msg("You need to be: " + variables.head_user + " to make me reload a module", variables.channel)	
						else:
							try:
								reload(sys.modules[mycode])
								irc.send_msg("Reloaded module: " + mycode, variables.channel)
							except (KeyError):
								irc.send_msg("Module not found", variables.channel)
					else:
						parser.parse_ath_message(mycode, mystr)
							
		if irc_message.find("PING :") != -1:
			irc.ping()
	return 0

print sys.argv
print len(sys.argv)
if len(sys.argv) != 4:
	print "I expect the following arguments: python bot.py [your nick] [channel to join] [bot nick]"
	sys.exit("less/too many arguments given")
else:
	variables.head_user = sys.argv[1]
	variables.channel = sys.argv[2]
	variables.botnick = sys.argv[3]
reload(sys)
sys.setdefaultencoding('utf-8')
variables.ircsock.connect((variables.server, variables.port))
variables.ircsock.send("USER "+ variables.botnick + " " + variables.botnick +" "+ variables.botnick +" :MOTHERLAND_BOT\n")
variables.ircsock.send("NICK " + variables.botnick + "\n")
irc.join_channel(variables.channel)
signal.signal(signal.SIGALRM, ten_sec_handler)
try:
	main_loop()
except:
	err = sys.exc_info()
	exception = sys.exc_info()[0]
	if exception == KeyboardInterrupt:
		quit_bot()
	irc.send_msg("Error! INFO: " + str(err), variables.head_user)
	irc.send_msg("An error has been reported to the head user. Further details would be disclosed to the public in future. [RESTARTING]", variables.channel)
	variables.ircsock.send("QUIT :Restarting bot after error\n\r")
	restart_bot()
	