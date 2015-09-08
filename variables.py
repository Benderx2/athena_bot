import os
import sys
import socket
import threading
import ast
import signal

server = "irc.freenode.net"
port = 6667
channel = ""
botnick = ""
head_user = ""

time_counter = 0
init_counter = 0

too_much_timer_err = "10 seconds passed since execution. Maximum time limit reached."

left = 0
right = 1

bestack_1item_err = "Error! Attempt to commit operation on non-existent values on stack!"
bestack_2item_err = "Error! Attempt to commit operation on two non-existent values on stack!"
be_internal_err = "Internal interpreter error! Please contact bender| @ irc.freenode.net or https://github.com/Benderx2!"
be_string_err = "Error! Unterminated string."
be_invalid_op_err = "Error! Invalid opcode found!"
be_oerflow_err = "Error! Program has no end. Forgot '@'?"
i_hate_you = "Can't join channel: '0'"
eval_op_error_str = "Error! Error evaluating expression."



ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
