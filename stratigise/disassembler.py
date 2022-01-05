"""
Partially generic argonaut bytecode dissassemlber
"""

from stratigise.common import BinaryReadStream, Symbol, formatHex, loadModule

# Opcode table
gSpec = None

def loadSpec(name = "croc1"):
	"""
	Load a spec for a game format
	"""
	
	global gSpec
	
	gSpec = loadModule("specs/" + name + ".py")

def formatOperationArgs(arguments):
	"""
	Format an array of operation arguments as a string
	"""
	
	string = ""
	arg = 0
	
	while (arg < len(arguments)):
		string += ' '
		
		# format string argument
		if (type(arguments[arg]) == str):
			string += "\"" + arguments[arg] + "\""
		# format array of arguments
		elif (type(arguments[arg]) == type([])):
			string += "{"
			string += formatOperationArgs(arguments[arg])
			string += " }"
		# format literal symbol (string without quotes)
		elif (type(arguments[arg]) == Symbol):
			string += arguments[arg].value
		# format other values
		else:
			string += format(arguments[arg])
		
		arg += 1
	
	return string

class Instruction:
	"""
	An instruction from the bytecode
	"""
	
	def __init__(self, opcode, arguments = [], location = -1):
		"""
		Initialise an instruction, given its name, arguments and location.
		"""
		
		self.opcode = opcode
		self.arguments = arguments
		self.location = location
	
	def getString(self):
		"""
		Convert the instruction to a representation as a string.
		"""
		
		string = ""
		
		if (self.opcode in gSpec.opcodes):
			# Write opcode name
			string += str(gSpec.opcodes[self.opcode][0])
			
			# Parse opcode arguments
			string += formatOperationArgs(self.arguments)
			
			string += f"\t\t\t; Location: {formatHex(self.location)}"
		
		else:
			string += f"; Unknown opcode: {formatHex(self.opcode)}"
		
		return string

class StratInstructionList:
	"""
	A class containing each instruction as one entry in an arry with arguments.
	"""
	
	def __init__(self, preamble = None):
		"""
		Initialise the instruction list.
		"""
		
		self.preamble = "" if type(preamble) != str else preamble
		self.stream = []
	
	def setPreamble(self, preamble):
		"""
		Set the preamble (i.e. starting comment, usually containg other info)
		"""
		
		self.preamble = preamble
	
	def addInstruction(self, instruction):
		"""
		Add an instruction to the stream.
		"""
		
		self.stream.append(instruction)
	
	def writePrint(self):
		"""
		Print the contents of an instruction stream.
		"""
		
		print(self.preamble)
		
		for s in self.stream:
			print(s.getString())
	
	def writeFile(self, path):
		"""
		Write the contents of an instruction stream to a file.
		"""
		
		f = open(path, "w")
		
		f.write(self.preamble)
		
		for s in self.stream:
			f.write(s.getString() + "\n")
		
		f.close()

def disassemble(path, output):
	"""
	Disassemble a strat
	"""
	
	strat = BinaryReadStream(path)
	instructions = StratInstructionList()
	
	# Read strat header
	size = strat.readInt32LE()
	secondint = strat.readInt32BE()
	
	# Set starting comment
	instructions.setPreamble(f"; Strat was {size} bytes long.\n; Second bytes were {formatHex(secondint)}\n")
	
	# Read in opcodes
	while (True):
		start = strat.getPos()
		opcode = strat.readInt(gSpec.instructionSize)
		
		# Break on EOF or incomplete opcode
		if (opcode == None):
			break
		
		# Write opcode based on arguments in table
		else:
			args = []
			
			# Parse opcode arguments
			if (opcode in gSpec.opcodes):
				for arg in range(1, len(gSpec.opcodes[opcode])):
					type = gSpec.opcodes[opcode][arg]
					
					# Based on the type, get the next value from the instruction stream appropraitely
					if (type == 'string'):
						args.append(strat.readString())
					elif (type == 'int32'):
						args.append(strat.readInt32LE())
					elif (type == 'int16'):
						args.append(strat.readInt16LE())
					elif (type == 'int8'):
						args.append(strat.readInt8())
					elif (type == 'eval'):
						args.append(gSpec.unevalute(strat))
					else:
						pass
			
			# Add instruction to bytecode tokens
			instructions.addInstruction(Instruction(opcode, args, start))
	
	# Write disassembled file
	instructions.writeFile(output)
