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
	while(i < len(dfcode)):
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
	return output
