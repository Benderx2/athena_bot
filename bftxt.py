# Implementation by JuEeHa: https://github.com/JuEeHa/bftextgen 
# -*- encoding: utf-8 -*-
from math import sqrt

# Parameters for the text gen
max_inrange = 10 # How big difference between a byte in tape and new byte can be for byte reusage

# ------------------------------------------------------------------
# Helper functions for genlogic()

class Bftextgen_exception(Exception):
	def __init__(self, value):
		self.value = value

class Bftextgen_invalid_IR(Bftextgen_exception):
	def __str__(self):
		return 'Invalid IR form: %s' % self.value

# Returns -1 on not found.
def locate_in_range(tape, byte):
	for i in range(len(tape)):
		if abs(tape[i] - byte) <= max_inrange:
			return i
	return -1

# ------------------------------------------------------------------

def genlogic(text):
	bytes = [ord(byte) for byte in text.encode('utf-8')] # Assume byte-based implementation using utf-8

	tape = [] # Keep track of what we already have stored
	program = []
	for i in range(len(bytes)):
		byte = bytes[i]

		tape_index = locate_in_range(tape, byte)

		if tape_index == -1: # Nothing found in range, create new cell
			tape_index = len(tape)

			# Generate code to create cell
			program.append(('set', tape_index, byte))

			# Update our tape
			tape.append(byte)
		else:
			change = byte - tape[tape_index]

			# Generate code to change cell
			program.append(('change', tape_index, change))

			# Update our tape
			tape[tape_index] = byte
		
		# Generate output
		program.append(('output', tape_index))
	
	return program

# Helper functions for genbf()

def move_tape_pointer(change):
	if change < 0:
		return '<' * -change
	else:
		return '>' * change

def change_cell(change):
	if change < 0:
		return '-' * -change
	else:
		return '+' * change

def set_cell(value):
	def factorize(value):
		factors = []
		rest = value
		while True:
			max_factor = int(sqrt(rest))

			i = 2 # Everything is divisible by 1 and nothing by 0
			while i <= max_factor:
				if rest%i == 0:
					factors.append(i)
					rest = rest / i
					break
				i += 1

			if i > max_factor: # No more factors to find anymore
				factors.append(rest)
				break

		return factors

	# Special case 1 and 0 as rest assumes only primes have one factor
	if value == 0:
		return ''
	elif value == 1:
		return '+'

	factors = factorize(value)
	if len(factors) == 1:
		# We don't want to have a huge string of '+'s
		# Fortunately prime - 1 is not a prime
		# Thus, we generate code for value - 1, then add 1
		return set_cell(value - 1) + '+' # Safe as it's guaranteed the value >= 2

	if len(factors) % 2 == 0: # Even number of factors means we must start at the cell above us, to end up at right cell
		start_cell = 1
	else:
		start_cell = 0

	program = move_tape_pointer(start_cell) + '+' * factors[0]
	cell_pointer = start_cell
	for factor in factors[1:]:
		move = (cell_pointer+1)%2 - cell_pointer # -1 if at 1, +1 if at 0
		# First, create a loop that does the multiplication, moving the result to the other cell
		program += '[' + move_tape_pointer(move) + '+' * factor + move_tape_pointer(-move) + '-' + ']'
		# Then, move to the other cell
		program += move_tape_pointer(move)

		cell_pointer += move

	return program

# ------------------------------------------------------------------

def genbf(logic):
	print logic #debg
	tape_pointer = 0

	program = ''
	for command in logic:
		if command[0] == 'output':
			if len(command) != 2:
				raise Bftextgen_invalid_IR(command)

			cell = command[1]
			program += move_tape_pointer(cell - tape_pointer)
			program += '.'

			tape_pointer = cell
		elif command[0] == 'set':
			if len(command) != 3:
				raise Bftextgen_invalid_IR(command)

			cell = command[1]
			value = command[2]
			program += move_tape_pointer(cell - tape_pointer)
			program += set_cell(value)

			tape_pointer = cell
		elif command[0] == 'change':
			if len(command) != 3:
				raise Bftextgen_invalid_IR(command)

			cell = command[1]
			change = command[2]
			program += move_tape_pointer(cell - tape_pointer)
			program += change_cell(change)

			tape_pointer = cell
		else:
			raise Bftextgen_invalid_IR(command)

	return program

def bf(text):
	return genbf(genlogic(text))

if __name__ == '__main__':
	while True:
		try:
			text = raw_input().decode('utf-8')
		except EOFError:
			break
		print bf(text)
