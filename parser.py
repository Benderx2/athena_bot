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

from datetime import datetime
from datetime import date
from pytz import timezone
from random import randint

import pytz

import operator as op

def check_if_unicode(string):
	try:
		string.decode('utf-8')
   		return True
	except UnicodeError:
    		return False

def unicode_len(string):
	return len(string.decode('utf-8'))

def imports():
    for name, val in globals().items():
        if isinstance(val, types.ModuleType):
            yield val.__name__

def parse_ath_message(mycode, mystr):
		if mycode.startswith(".bf", 0, 3) == True:
			mycode = mycode.replace(".bf ", "")
			irc.send_msg(bfc.compile_bf(mycode), variables.channel)
			signal.alarm(0)
		elif mycode.startswith(".be", 0, 3) == True:
			mycode = mycode.replace(".be ", "")
			irc.send_msg(bec.compile_be(mycode), variables.channel)
			signal.alarm(0)
		elif mycode.startswith(".ul", 0, 3) == True:
			print mycode
			mycode = mycode.replace(".ul ", "")
			irc.send_msg(ulc.compile_ul(mycode), variables.channel)
			signal.alarm(0)
		elif mycode.startswith(".test", 0, 5) == True:
			utils.test()
		elif mycode.startswith(".eval", 0, 5) == True:
			output = "Result: " + utils.evaluate_expression(mycode)
			irc.send_msg(output, variables.channel)
		elif mycode.startswith(".d2h", 0, 4) == True:
			utils.decimal_to_hex(mycode)
		elif mycode.startswith(".h2d", 0, 4) == True:
			utils.hex_to_decimal(mycode)
		elif mycode.startswith(".d2b", 0, 4) == True:
			utils.decimal_to_bin(mycode)
		elif mycode.startswith(".h2b", 0, 4) == True:
			utils.hex_to_bin(mycode)
		elif mycode.startswith(".b2h", 0, 4) == True:
			utils.bin_to_hex(mycode)
		elif mycode.startswith(".b2d", 0, 4) == True:
			utils.bin_to_decimal(mycode)
		elif mycode.startswith(".join", 0, 5) == True:
			user = mystr['PREFIX']
			user = user.split('!')
			if user[0] != variables.head_user:
				irc.send_msg("You need to be: " + variables.head_user + " to make me join a channel", variables.channel)	
			else:
				mychan = mycode.replace(".join", "")
				mychan = mychan.replace(" ", "")
				if mychan == "0":
					irc.send_msg(variables.i_hate_you, variables.channel)
				else:
					irc.join_channel(mychan)

		elif mycode.startswith(".leave", 0, 6):
			user = mystr['PREFIX']
			user = user.split('!')
			if user[0] != variables.head_user:
				irc.send_msg("You need to be: " + variables.head_user + " to make me leave a channel", variables.channel)	
			else:
				mychan = mycode.replace(".leave", "")
				mychan = mychan.replace(" ", "")
				if mychan == "0":
					irc.send_msg(variables.i_hate_you, variables.channel)
				else:
					irc.leave_channel(mychan)
		elif mycode.startswith(".time", 0, 5) == True:
			utils.get_time(mycode)
		elif mycode.startswith(".ccount ", 0, 8) == True:
			mycode = mycode.replace(".ccount ", "")
			length = 0
			if check_if_unicode(mycode) == True:
				length = unicode_len(mycode)
			else:
				length = len(mycode)
			irc.send_msg("Length: " + str(length), variables.channel)
		elif mycode.startswith(".help", 0, 5) == True:
			irc.send_msg(help.athena_help, variables.channel)
		elif mycode.startswith(".list", 0, 5):
			irc.send_msg("List of modules: " + str(list(imports())), variables.channel)	
		elif mycode.startswith(".source", 0, 7):
			irc.send_msg("https://github.com/Benderx2/athena_bot", variables.channel)
