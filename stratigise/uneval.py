"""
Support functions for eval argument type

The "Eval" argument type for instructions is much more complex than most other
argument types, and is used the most often. It is basically a generic way to
access a value from almost anywhere, including constants, variables, globals and
other things.

Eval actually acts like its own bytecode interpreter itself. As an example of
this, it has its own stack that is used when evaluating arguments, and it forms
a sort of "bytecode" interpreter in itself with the switch-case interpreter
loop.

Eval is a bit less suited to being decompiled dynamicially, though: while we
could do a similar dynamic bytecode decompilation like we do for the strat
bytecode (that is, have bytecode profiles), it would probably require the use of
actual functions much more often. It seems a bit nicer to just deal with a table
of functions that can be used to interpret what exactly the bytecode means.

TODO: Allow for this to be loaded from external files (that is, the strat
bytecode config files).
"""

from stratigise.common import Symbol

def Croc1Eval(strat):
	"""
	Croc 1 eval type handling
	"""
	
	stack = []
	
	while (True):
		op = strat.readInt8()
		
		# So elif is consisent across opcodes
		if (False): pass
		
		# Assume that A and B are the top and second-to-top of the stack.
		
		# 0x01 - Get a PGVar (procedure global?)
		elif (op == 0x01):
			stack.append(Symbol("GetPGVar"))
			stack.append(strat.readInt16LE())
		
		# 0x02 - Get strat global value
		elif (op == 0x02):
			stack.append(Symbol("GetGVar"))
			stack.append(strat.readInt16LE())
		
		# 0x03 - Load alien var (?)
		elif (op == 0x03):
			stack.append(Symbol("GetAVar"))
			pp = strat.readInt16LE()
			stack.append(pp)
		
		# 0x04 - Read a long value
		elif (op == 0x04):
			stack.append(Symbol("ReadInt32"))
			stack.append(strat.readInt32LE())
		
		# 0x06 - Add between top values (A + B)
		elif (op == 0x06):
			stack.append(Symbol("Add"))
		
		# 0x07 - Subtract between top values (B - A)
		elif (op == 0x07):
			stack.append(Symbol("Subtract"))
		
		# 0x08 - Multiply between top values
		elif (op == 0x08):
			stack.append(Symbol("Multiply"))
		
		# 0x09 - Divide between top values
		elif (op == 0x09):
			stack.append(Symbol("Divide"))
		
		# 0x0A - Bitwise AND between top values
		elif (op == 0x0A):
			stack.append(Symbol("BitAnd"))
		
		# 0x0B - Bitwise OR between top values
		elif (op == 0x0B):
			stack.append(Symbol("BitOr"))
		
		# 0x0C - Unknown but usually followed by string litral
		elif (op == 0x0C):
			stack.append(Symbol("CmpEqual"))
		
		# 0x0D - Unknown but usually followed by string literal
		elif (op == 0x0D):
			stack.append(Symbol("CmpNotEuqal"))
		
		# 0x0E - Compare A < B
		elif (op == 0x0E):
			stack.append(Symbol("CmpTopLess"))
		
		# 0x0F - Compare B < A (A > B)
		elif (op == 0x0F):
			stack.append(Symbol("CmpTopGreater"))
		
		# 0x10 - Compare A < B then XOR 1
		elif (op == 0x10):
			stack.append(Symbol("CmpNotTopLess"))
		
		# 0x11 - Compare B < A then XOR 1 ((A > B) ^ 1)
		elif (op == 0x11):
			stack.append(Symbol("CmpNotTopGreater"))
		
		# 0x12 - Pop top stack value and return
		elif (op == 0x12):
			stack.append(Symbol("ReturnTop"))
			break
		
		# 0x13 - Load 32-bit constants with advanced operations
		elif (op == 0x13):
			stack.append(Symbol("LongOperation"))
			pp = strat.readInt8()
			
			# 0x01 - Long value with lookup
			if (pp == 0x01):
				stack.append(Symbol("SearchForWadEntry"))
				stack.append(strat.readInt32LE())
				strat.readInt8() # ignore value
				stack.append(strat.readString())
			
			# 0x03 - Load long value and then read a byte N and skip N bytes
			elif (pp == 0x03 or pp == 0x04 or pp == 0x05):
				stack.append(Symbol("ReadInt32AndSkip"))
				stack.append(strat.readInt32LE())
				sz = strat.readInt8()
				stack.append(strat.readBytes(sz).decode('latin-1'))
			
			# 0x50 - Read int32 which is then shifted left 16 (0x10)
			elif (pp == 0x50):
				stack.append(Symbol("ReadInt32ShiftedLeft16"))
				stack.append(strat.readInt32LE() >> 0x10)
				sz = strat.readInt8()
				stack.append(strat.readBytes(sz).decode('latin-1'))
			
			# I did not actually check what exactly these do yet, since they
			# both seem to do the broing "load a 32-bit" integer routine
			# like most things here seem to do...
			elif (pp == 0x51 or pp == 0x8E):
				stack.append(Symbol("UnknownLongOperation1"))
				stack.append(strat.readInt32LE())
		
		# 0x1E - Negate top value on the stack
		elif (op == 0x1E):
			stack.append(Symbol("Negate"))
		
		# 0x1F - Compare to zero, push 1 if is zero and 0 otherwise (A == 0)
		elif (op == 0x1F):
			stack.append(Symbol("CmpIsZero"))
		
		# 0x23 - Check if higest bit on strat anim flags is set and decrement 
		# the stack pointer if so (seems very sepcific so not confident in this)
		# Flag32 referes to 32nd flag, not 32-bit integer
		elif (op == 0x23):
			stack.append(Symbol("CheckAnimFlag32"))
		
		# 0x26 - Push zero and stop eval
		elif (op == 0x26):
			stack.append(Symbol("ReturnZero"))
			break
		
		# Unknown eval opcode
		else:
			break
	
	return stack

def Unknown(strat):
	"""
	Handler for unknown bytecodes
	"""
	
	return [Symbol("Eval code - strat decompiler output is now broken")]

"""
Table of eval functions
"""
EVAL_FUNC = {
	"croc1": Croc1Eval,
	"unknown": Unknown,
}
