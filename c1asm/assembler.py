"""
Creates assembled binary from tokens

While this does load specs, it only does so to make writing c1asm easier. It
cannot actually reassemble Croc 2 strats or anything else due to the other data
in those files.
"""

import common
from tokeniser import Token, TokenType
import exceptions

gSpec = None

def loadSpec(name):
	"""
	Load a spec and adapt it for the assembler
	"""
	
	global gSpec
	
	gSpec = common.loadModule(f"specs/{name}.py")
	
	# Swap opcode keys and values
	new_opcodes = {}
	
	for i in gSpec.opcodes:
		newlist = gSpec.opcodes[i].copy()
		newlist.pop(0)
		new_opcodes[gSpec.opcodes[i][0]] = [i,] + newlist
	
	gSpec.opcodes = new_opcodes

class Instruction:
	"""
	An instrusction
	"""
	
	def __init__(self, type, args):
		self.type = type
		self.args = args

class Label:
	"""
	A label
	"""
	
	def __init__(self, name, location):
		self.name = name
		self.location = location

class TokenList:
	"""
	Easier to manage list of tokens
	"""
	
	def __init__(self, tokens):
		self.tokens = tokens
		self.current = 0
	
	def match(self, kind):
		"""
		Check if a token matches a specific kind
		"""
		
		return (self.tokens[current].kind == kind)
	
	def matchData(self, kind, allowedValues):
		"""
		Check if there is a match with the token kind and any of the allowed
		data values
		"""
		
		return ((self.tokens[current].kind == kind) and (self.tokens[current].data in allowedValues))
	
	def next(self):
		"""
		Go to the next token, returning the current
		"""
		
		current += 1
		
		if (len(self.tokens) < self.current):
			raise Exception("Unexpected end of file - perhaps you forgot to include an argument on the last operation?")
		
		return self.tokens[current - 1]
	
	def expect(self, kind, message):
		"""
		Expect a certian kind of token and increment if found
		"""
		
		if (self.tokens[current].kind != kind):
			raise Exception(message)
		
		return self.next()
	
	def where(self):
		"""
		Return where the current token was in the source stream
		"""
		
		return self.tokens[current].location
	
	def done(self):
		"""
		Check if the token list is done
		"""
		
		return (len(self.tokens) <= self.current)

def assemble(tokens):
	"""
	Assemble the tokenised input to a binary
	"""
	
	tokens = TokenList(tokens)
	
	# We will need to keep track of the addresses to rewrite later
	rewrite_list = {}
	
	while (not tokens.done()):
		# Handle an instruction
		# It's not the nicest thing ever.
		if (tokens.matchData(TokenType.SYMBOL, gSpec.opcodes.keys())):
			op = tokens.next().kind
			
			i = 1
			
			while (i < len(gSpec.opcodes[op]))
				# Handle each type of argument
				match (gSpec.opcodes[op][i]):
					case 'int8':
						tokens.expect(TokenType.NUMBER, f"{op} expects a number (8 bit) for {i}th argument.")
					
					case 'address16', 'offset16':
						tokens.expect(TokenType.SYMBOL, f"{op} expects a label for {i}th argument.")
					
					case 'eval':
						gSpec.reevaluate(tokens)
		
		# Handle a label
		elif (tokens.match(TokenType.SYMBOL))
	
	return (instructions, labels)

if (__name__ == "__main__"):
	import sys
	from tokeniser import tokenise
	
	assemble(tokenise(sys.argv[1]))
