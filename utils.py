import os
import sys
import socket
import threading
import ast
import signal
import irc
import variables

from datetime import datetime
from datetime import date
from pytz import timezone
from random import randint

import pytz

import operator as op

operators = { 	ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor, ast.USub: op.neg, 
	 	ast.BitOr: op.or_, ast.LShift: op.lshift, ast.RShift: op.rshift, ast.Mod: op.mod, ast.BitAnd: op.and_, ast.Invert: op.invert,
		ast.Eq: op.eq, ast.Lt: op.lt, ast.LtE: op.le, ast.NotEq: op.ne, ast.Gt: op.gt, ast.GtE: op.ge,  }
def eval_expr(expr):
	try:
		a = eval_(ast.parse(expr, mode='eval').body)
		return a
	except (RuntimeError, TypeError, NameError, KeyError, SyntaxError, ZeroDivisionError):
		irc.send_msg(variables.eval_op_error_str, channel)

def eval_(node):
	# clear any previous errors
	if isinstance(node, ast.Num):
		return node.n
	elif isinstance(node, ast.BinOp):
		return operators[type(node.op)](eval_(node.left), eval_(node.right))
	elif isinstance(node, ast.UnaryOp):
		return operators[type(node.op)](eval_(node.operand))
	else:
		eval_op_error = True
		return 0

def evaluate_expression(myexpr):
	myexpr = myexpr.replace(".eval", "")
	myexpr = myexpr.replace(" ", "")
	myexpr = myexpr.replace("C_PI", "3.14159265")
	myexpr = myexpr.replace("C_E", "2.7182818")
	return str(eval_expr(myexpr))

def decimal_to_hex(arg):
	arg = (arg.replace(".d2h", "")).replace(" ", "")					
	try:
		irc.send_msg("Output: " + hex(int(arg)), variables.channel)
	except (TypeError, ValueError):
		irc.send_msg("Error while converting decimal to hex!", variables.channel)
def hex_to_decimal(arg):
	arg = (arg.replace(".h2d", "")).replace(" ", "")					
	try:
		arg = arg.replace("A", "a").replace("B", "b").replace("C", "c").replace("D", "d").replace("E", "e").replace("F", "f")
		arg = arg.replace("0x", "").replace("0X", "")
		arg = arg.replace("X", "").replace("x", "")
		irc.send_msg("Output: " + str(int(arg, 16)), variables.channel)
	except (TypeError, ValueError):
		irc.send_msg("Error while converting hex to int!", variables.channel)
def decimal_to_bin(arg):
	arg = (arg.replace(".d2b", "")).replace(" ", "")					
	try:
		irc.send_msg("Output: " + bin(int(arg)), variables.channel)
	except (TypeError, ValueError):
		irc.send_msg("Error while converting decimal to bin", variables.channel)
def hex_to_bin(arg):
	arg = (arg.replace(".h2b", "")).replace(" ", "")
	arg = arg.replace("A", "a").replace("B", "b").replace("C", "c").replace("D", "d").replace("E", "e").replace("F", "f")
	arg = arg.replace("0x", "").replace("0X", "")
	arg = arg.replace("X", "").replace("x", "")					
	try:
		irc.send_msg("Output: " + bin(int((arg),16)), variables.channel)
	except (TypeError, ValueError):
		irc.send_msg("Error while converting hex to bin", variables.channel)
def bin_to_hex(arg):
	arg = (arg.replace(".b2h", "")).replace(" ", "")
	arg = arg.replace("0B", "").replace("0b", "")
	arg = arg.replace("B", "").replace("b", "")					
	try:
		irc.send_msg("Output: " + hex(int(arg,2)), variables.channel)
	except (TypeError, ValueError):
		irc.send_msg("Error while converting bin to hex", variables.channel)
def bin_to_decimal(arg):
	arg = (arg.replace(".b2d", "")).replace(" ", "")
	arg = arg.replace("0B", "").replace("0b", "")
	arg = arg.replace("B", "").replace("b", "")					
	try:
		irc.send_msg("Output: " + str(int((arg), 2)), variables.channel)
	except (TypeError, ValueError):
		irc.send_msg("Error while converting bin to decimal", variables.channel)
def get_time(arg):
	try:
		arg = arg.replace(".time", "").replace(" ", "")
		mytimezone = timezone(arg)
		the_time = datetime.now(mytimezone)
		irc.send_msg("Output: Time (In " + arg + ") " + the_time.strftime('%Y/%m/%d - %H:%M:%S') + ": UTC " + pytz.timezone(arg).localize(datetime(date.today().year,date.today().month,date.today().day)).strftime('%z'), variables.channel)
	except (pytz.exceptions.UnknownTimeZoneError):
		irc.send_msg("Unknown Time zone.", variables.channel)
def test():
	irc.send_msg("Acknowledge.", variables.channel)
