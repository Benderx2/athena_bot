# deadfish module

import os
import sys
import socket
import threading
import ast
import signal
import irc
import variables

def compile_df(dfcode):
	accumulator = 0
	i = 0
	output = ""
	signal.alarm(10)
	while(i < len(dfcode)):
		if variables.time_counter - variables.init_counter > 0:
				signal.alarm(0)
				irc.send_msg(variables.too_much_time_err, variables.channel)
				return "[NORESULT]"
		if dfcode[i] == 'x' or dfcode[i] == 'i':
			accumulator += 1
		elif dfcode[i] == 'd':
			accumulator -= 1
		elif dfcode[i] == 's' or dfcode[i] == 'k':
			accumulator *= accumulator
		elif dfcode[i] == 'o' or dfcode[i] == 'c':
			if accumulator == 0 or accumulator == 256:
				output += "0 "
			else:
				output += str(accumulator) + " "
		i += 1
	signal.alarm(0)
	output = irc.process_output(output)
	return output
