# irc module

import os
import sys
import socket
import threading
import ast
import signal
import variables

def ping():
	variables.ircsock.send("PONG :pingis\n")

def send_msg(message, chan):
	variables.ircsock.send("PRIVMSG " + chan + " :" + message + "\n")
	
def join_channel(chan):
	variables.ircsock.send("JOIN " + chan + "\n")

def leave_channel(chan):
	variables.ircsock.send("PART " + chan + "\n")

def process_output(output):
	global channel
	i = 0
	while i < len(output):
		if output[i] == '\n' or output[i] == '\r' or output[i] == u'\n' or output[i] == u'\r':
			send_msg("WARNING: Output contains newline (0x0A).", channel)
			return output.replace("\n", "").replace("\r", "")
		i += 1
	return output

def parse_msg(s):
    prefix = ''
    trailing = []
    if not s:
       raise IRCBadMessage("Empty line.")
    if s[0] == ':':
        prefix, s = s[1:].split(' ', 1)
    if s.find(' :') != -1:
        s, trailing = s.split(' :', 1)
        args = s.split()
        args.append(trailing)
    else:
        args = s.split()
    command = args.pop(0)
    return { 'PREFIX':prefix, 'COMMAND':command, 'ARGS':args }

