import os
import sys
import socket
import threading
import ast
import signal
import irc
import variables


def compile_be(becode):
		output = "Output: "
		bestack = [0]
		pc_dir = variables.right
		i = 0
		signal.alarm(10)
		while becode[i] != '@':
			if variables.time_counter - variables.init_counter > 0:
				signal.alarm(0)
				irc.send_msg(variables.too_much_time_err, variables.channel)
				return "[NORESULT]"
			if becode[i] == '+' or becode[i] == '-' or becode[i] == '/' or becode[i] == '*' or becode[i] == '%':
				if len(bestack) < 2:
					output = variables.bestack_2item_err
					return output
				else:
					a = bestack.pop()
					b = bestack.pop()
					if becode[i] == '+':
						bestack.append(a+b)
					elif becode[i] == '-':
						bestack.append(b-a)
					elif becode[i] == '*':
						bestack.append(a*b)
					elif becode[i] == '/':
						bestack.append(b/a)
					elif becode[i] == '%':
						bestack.append(b%a)
					else:
						output = variables.bestack_2item_err
						return output
			elif becode[i] == '!':
				if len(bestack) < 1:
					output = bestack_1item_err
					return output
				else:
					a = bestack.pop()
					if a == 0:
						bestack.append(1)
					else:
						bestack.append(0)
			elif becode[i] == '`':
				if len(bestack) < 2:
					output = variables.bestack_2item_err
					return output
				else:
					a = bestack.pop()
					b = bestack.pop()
					if(b > a):
						bestack.append(1)
					else:
						bestack.append(0)
			elif becode[i] == '<':
				pc_dir = variables.left
			elif becode[i] == '>':
				pc_dir = variables.right
			elif becode[i] == '?':
				pc_dir = randint(variables.left,variables.right)
			elif becode[i] == '_':
				if len(bestack) < 1:
					output = variables.bestack_1item_err
					return output
				else:
					a = bestack.pop()
					if a == 0:
						pc_dir = variables.right
					else:
						pc_dir = variables.left
			elif becode[i] == '|':
				if len(bestack) < 1:
					output = variables.bestack_1item_err
					return output
				else:
					a = bestack.pop()
					if a == 0:
						pc_dir = variables.down
					else:
						pc_dir = variables.up
			elif becode[i] == '"':
				j = i+1
				mark_found = False
				while j < len(becode):
					if becode[j] == '"':
						mark_found = True
						break
					else:			
						try:	
							bestack.append(ord(becode[j]))
						except (TypeError):
							bestack.append(ord(' '))
					j += 1
				if mark_found == False:
					output = variables.be_string_err
					return output
				i = j
			elif becode[i] == ':':
				if len(bestack) < 1:
					output = variables.bestack_1item_err
					return output
				else:
					a = bestack.pop()
					bestack.append(a)
					bestack.append(a)
			elif becode[i] == '\\':
				if len(bestack) < 2:
					output = variables.bestack_2item_err
					return output
				else:
					a = bestack.pop()
					b = bestack.pop()
					bestack.append(a)
					bestack.append(b)
			elif becode[i] == '.':
				if len(bestack) < 1:
					output = variables.bestack_1item_err
					return output
				else:
					a = bestack.pop()
					output = output + str(a)
			elif becode[i] == ',':
				if len(bestack) < 1:
					output = variables.bestack_1item_err
					return output
				else:
					a = bestack.pop()
					if (a) > 0 and (a) < 255:
						output = output + chr((a))
					else:
						output = output + "[NON-ASCII CHAR: " + str(a) + "]"
			elif becode[i] == '#':
				if pc_dir == variables.right:
					i += 1
				elif pc_dir == variables.left:
					i -= 1
				else: 
					output = variables.be_internal_err
					return output
			elif becode[i] == '$':
				if len(becode) < 1:
					output = "Stack underflow error!"
					return output
				else:
					bestack.pop()
			elif becode[i] == 'g':
				if len(bestack) < 2:
					output = variables.bestack_2item_err
					return output
				y_pos = bestack.pop()
				x_pos = bestack.pop()
				array_pos = x_pos
				if array_pos < 0 or array_pos > len(becode):
					bestack.append(0)
				else:
					bestack.append(ord(becode[array_pos]))
			elif becode[i] == '0' or becode[i] == '1' or becode[i] == '2' or becode[i] == '3' or becode[i] == '4' or becode[i] == '5' or becode[i] == '6' or becode[i] == '7' or becode[i] == '8' or becode[i] == '9':
				bestack.append(int(becode[i]))
			if pc_dir == variables.right:
				i += 1
			elif pc_dir == variables.left:
				i -= 1
			else:
				output = variables.be_internal_err
				return output
			if i < 0 or i >= len(becode):
				output = variables.be_oerflow_err
				return output
		signal.alarm(0)
		output = irc.process_output(output)
		return output
