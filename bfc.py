import os
import sys
import socket
import threading
import ast
import signal
import irc
import variables

def compile_bf(bfcode):
	output = "Output: "
	bf_index = 0
	bfarr = [0] * 3000
	i = 0
	j = 0
	# build brace map i.e. return addresses
	bracestack, bracemap = [], {}
	while j < len(bfcode):
		if bfcode[j] == "[": bracestack.append(j)
		if bfcode[j] == "]":
			if len(bracestack) == 0:
				output = "Missing '['"
				return output
			start = bracestack.pop()
			bracemap[start] = j
			bracemap[j] = start
		j += 1
	if len(bracestack) != 0:
		output = "Missing ']'"
		return output
	signal.alarm(10)
	while i < len(bfcode):
		if variables.time_counter - variables.init_counter > 0:
			irc.send_msg(variables.too_much_timer_err, variables.channel)
			signal.alarm(0)
			return "[NORESULT]"
		if bfcode[i] == '<':
			if bf_index > 0:
				bf_index -= 1
			elif bf_index == 0:
				bf_index = 2999
		elif bfcode[i] == '>':
			if bf_index < 3000:
				bf_index += 1
			elif bf_index >= 2999:
				bf_index = 0
		elif bfcode[i] == '+':
			if bfarr[bf_index] == 255:
				bfarr[bf_index] = 0
			else:
				bfarr[bf_index] += 1
		elif bfcode[i] == '-':
			if bfarr[bf_index] == 0:
				bfarr[bf_index] = 255
			else:
				bfarr[bf_index] -= 1
		elif bfcode[i] == '.':
			if bfarr[bf_index] > 0 and bfarr[bf_index] < 255:
				output = output + chr(bfarr[bf_index])
			else:
				output = output + "[NON EXISTENT CHARACTER: " + str(bfarr[bf_index]) +"]"
		elif bfcode[i] == '[' and bfarr[bf_index] == 0:
			i = bracemap[i]
		elif bfcode[i] == ']' and bfarr[bf_index] != 0:
			i = bracemap[i]
		i += 1
	signal.alarm(0)
	output = irc.process_output(output)
	return output

