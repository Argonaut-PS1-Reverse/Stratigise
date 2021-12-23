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
		
		# It seems like anything under 0x11 might be getting a value of that 
		# size.
		
		# 0x04 - Read a long value
		elif (op == 0x04):
			stack.append(Symbol("ReadInt32"))
			stack.append(strat.readInt32LE())
		
		# 0x05 to 0x11 - Read an opcode chars long string (???)
		elif (op == 0x08):
			stack.append(Symbol("ReadNString"))
			stack.append(strat.readBytes(op).decode('latin-1'))
		
		# 0x0C - Unknown but usually followed by string litral
		elif (op == 0x0C):
			stack.append(Symbol("String0C"))
			stack.append(strat.readString())
		
		# 0x0D - Unknown but usually followed by string literal
		elif (op == 0x0D):
			stack.append(Symbol("String0D"))
			stack.append(strat.readString())
		
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
			
			# It seems like 0x03 and 0x05 do the same thing
			# 0x03, 0x04, 0x05 - Long value (???)
			elif (pp == 0x03 or pp == 0x04 or pp == 0x05):
				stack.append(Symbol("ReadInt32"))
				stack.append(strat.readInt32LE())
			
			# 0x50 - Read int32 which is then shifted left 16 (0x10)
			elif (pp == 0x50):
				stack.append(Symbol("ReadInt32ShiftedLeft16"))
				stack.append(strat.readInt32LE() >> 0x10)
			
			# I did not actually check what exactly these do yet, since they
			# both seem to do the broing "load a 32-bit" integer routine
			# like most things here seem to do...
			elif (pp == 0x51 or pp == 0x8E):
				stack.append(Symbol("UnknownLongOperation1"))
				stack.append(strat.readInt32LE())
		
		# 0x23 - Check if higest bit on strat anim flags is set and decrement 
		# the stack pointer if so (seems very sepcific so not confident in this)
		# Flag32 referes to 32nd flag, not 32-bit integer
		elif (op == 0x23):
			stack.append(Symbol("CheckAnimFlag32"))
		
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
