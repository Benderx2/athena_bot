# ulc module
import os
import sys
import socket
import threading
import ast
import signal
import variables
import irc
def insert_string(string, new, pos):
	return string[:pos] + new + string[pos:]

def compile_ul(ulcode):
	output = "Output: "
	ulstack = ["NULL"]
	i = 0
	signal.alarm(10)
	while i < len(ulcode):
		if variables.time_counter - variables.init_counter > 0:
			irc.send_msg(variables.too_much_timer_err, variables.channel)
			signal.alarm(0)
			return "[NORESULT]"
		if ulcode[i] == '~':
			if len(ulstack) < 2:
				output = variables.bestack_2item_err
				return output
			a = ulstack.pop()
			b = ulstack.pop()
			ulstack.append(a)
			ulstack.append(b)
		elif ulcode[i] == ':':
			if len(ulstack) < 1:
				output = variables.bestack_1item_err
				return output
			a = ulstack.pop()
			ulstack.append(a)
			ulstack.append(a)
		elif ulcode[i] == '!':
			if len(ulstack) < 1:
				output = variables.bestack_1item_err
				return output
			ulstack.pop()
		elif ulcode[i] == '*':
			if len(ulstack) < 2:
				output = variables.bestack_2item_err
				return output
			a = ulstack.pop()
			b = ulstack.pop()
			ulstack.append(b+a)
		elif ulcode[i] == 'a':
			if len(ulstack) < 1:
				output = variables.bestack_1item_err
				return output
			a = ulstack.pop()
			ulstack.append("(" + a + ")")
		elif ulcode[i] == '^':
			if len(ulstack) < 1:
				output = variables.bestack_1item_err
				return output
			a = ulstack.pop()
			ulcode = insert_string(ulcode, a, i+1)
		elif ulcode[i] == 'S':
			if len(ulstack) < 1:
				output = variables.bestack_1item_err
				return output
			output = output + ulstack.pop()
		elif ulcode[i] == '(':
			a = ""
			level = 0
			i += 1
			level += 1
			while(level > 0):
				if i > len(ulcode):
					output = "Error! Unterminated parentheses."
					return output
				if ulcode[i] == '(':
					level += 1
				elif ulcode[i] == ')':
					level -= 1
				if level > 0:
					a += ulcode[i]
				i += 1
			i -= 1
			ulstack.append(a)
		i += 1
	signal.alarm(0)
	output = irc.process_output(output)
	return output
