"""
Creates assembled binary from tokens

While this does load specs, it only does so to make writing c1asm easier. It
cannot actually reassemble Croc 2 strats or anything else due to the other data
in those files.
"""

import common
from tokeniser import Token, TokenType

gSpec = None

def loadSpec(name):
	"""
	Load a spec and adapt it for the assembler
	"""
	
	global gSpec
	
	gSpec = common.loadModule(f"../specs/{name}.py")
	
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
		
		return (self.tokens[self.current].kind == kind)
	
	def matchData(self, kind, allowedValues):
		"""
		Check if there is a match with the token kind and any of the allowed
		data values
		"""
		
		return ((self.tokens[self.current].kind == kind) and (self.tokens[self.current].data in allowedValues))
	
	def next(self):
		"""
		Go to the next token, returning the current
		"""
		
		self.current += 1
		
		if (len(self.tokens) < self.current):
			raise Exception("Unexpected end of file - perhaps you forgot to include an argument on the last operation?")
		
		return self.tokens[self.current - 1]
	
	def expect(self, kind, message = "Expected a different type of token from the one that was found."):
		"""
		Expect a certian kind of token and increment if found
		"""
		
		if (self.tokens[self.current].kind != kind):
			raise Exception(f"Syntax Error: {self.tokens[self.current]}: {message}")
		
		return self.next()
	
	def where(self):
		"""
		Return where the current token was in the source stream
		"""
		
		return self.tokens[self.current].location
	
	def done(self):
		"""
		Check if the token list is done
		"""
		
		return (len(self.tokens) <= self.current)

def assemble(strat, tokens):
	"""
	Assemble the tokenised input to bytecode. This only does the body, not headers
	(or in the case of Croc 1) audio data.
	
	strat: The input file
	tokens: The tokens of the strat
	"""
	
	tokens = TokenList(tokens)
	
	# We will need to keep track of the addresses to rewrite later
	rewrite_list = []
	
	# To make things easier we will also keep track of where labels are
	label_locations = {}
	
	# Also we should read attributes :)
	attributes = {}
	
	###############################
	# First Pass - Assemble strat
	###############################
	
	while (not tokens.done()):
		# Handle an instruction
		# It's not the nicest thing ever.
		if (tokens.matchData(TokenType.SYMBOL, gSpec.opcodes.keys())):
			# Get the opcode name string
			op = tokens.next().data
			
			# print(op)
			
			# Get the opcode 
			op_num = gSpec.opcodes[op][0]
			
			# Write the opcode
			if (hasattr(gSpec, "writeOpcode")):
				gSpec.writeOpcode(strat, op_num)
			else:
				strat.writeInt8(op_num)
			
			# Write opcode arguments, and handle any errors related to them.
			i = 1
			
			while (i < len(gSpec.opcodes[op])):
				arg_type = gSpec.opcodes[op][i]
				
				# print(f"\t{arg_type}")
				
				match (arg_type):
					case 'int8' | 'int16' | 'int32':
						number = tokens.expect(TokenType.NUMBER, f"{op} expects a number ({arg_type}) for {i}th argument.")
						
						if (type(number.data) == float):
							# 20.12 and 4.12 fixed point number encode
							number = int(number.data * 4096.0)
						else:
							number = int(number.data)
						
						match (arg_type):
							case 'int8' : strat.writeInt8(number)
							case 'int16': strat.writeInt16LE(number)
							case 'int32': strat.writeInt32LE(number)
					
					case 'address16' | 'offset16':
						label = tokens.expect(TokenType.SYMBOL, f"{op} expects a label for {i}th argument.")
						
						# Add to patch table
						rewrite_list.append({
							"pos": strat.getPos(),
							"label": label,
							"relative": (True if (arg_type == "offset16") else False)
						})
						
						# Just write zero for now
						strat.writeInt16LE(0)
					
					case 'varargs':
						# Needs to be handled by spec
						gSpec.revarargs(strat, tokens)
					
					case 'eval':
						# This will be handled by the spec
						gSpec.reevaluate(strat, tokens)
				
				i += 1
		
		# Handle a label
		elif (tokens.match(TokenType.SYMBOL)):
			label = tokens.next()
			
			tokens.expect(TokenType.COLON, f"Expected colon after label by name '{label.data}'. (Maybe you misspelled an instruction?)")
			
			label_locations[label.data] = strat.getPos()
		
		# Handle an attirbute e.g. @ <symbol> <string|int>
		elif (tokens.match(TokenType.ATTRIBUTE)):
			tokens.next()
			
			# Expect the attribute name
			attr_name = tokens.expect(TokenType.SYMBOL, "Did not find symbol after attribute.").data
			
			# Get the attribute value
			attributes[attr_name] = tokens.next().data
		
		# Error condition
		else:
			# tokens.expect(TokenType.INVALID, "Don't know what is happening right now.")
			print(f"Don't know what is happening right now. {tokens.next()}")
	
	end_pos = strat.getPos()
	
	###############################
	# Second Pass - Patch missing addresses
	###############################
	
	for r in rewrite_list:
		strat.setPos(r["pos"])
		strat.writeInt16LE((label_locations[r["label"]] - r["pos"]) if (r["relative"]) else (label_locations[r["label"]]))
	
	return end_pos

if (__name__ == "__main__"):
	import sys
	from tokeniser import tokenise
	
	loadSpec("croc1")
	assemble(common.BinaryWriteStream("testfile.bin"), tokenise(sys.argv[1]))
