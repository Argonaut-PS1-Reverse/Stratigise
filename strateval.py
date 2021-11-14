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
"""

def Croc1Eval(strat):
	"""
	Croc 1 eval type handling
	"""
	
	op = strat.readInt8()
	
	# 0x13 - Load constant (?)
	if (op == 0x13):
		pp = strat.readInt8()
		
		# 0x01 - Long value
		if (pp == 0x01):
			return ("Lookup(" + str(strat.readInt32LE()) + ")")
		elif (pp == 0x03):
			return strat.readInt32LE()
	
	return 0

def Unknown(strat):
	"""
	Handler for unknown bytecodes
	"""
	
	return "[eval]"

"""
Table of eval functions
"""
EVAL_FUNC = {
	"croc1": Croc1Eval,
	"unknown": Unknown,
}
