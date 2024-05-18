"""
Partially generic argonaut bytecode dissassemlber
"""

from pathlib import Path
from stratigise.common import BinaryReadStream, Symbol, SectionInfo, formatHex, loadModule, getLabelString

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
			
			# Call spec post function
			if (hasattr(gSpec, "after")):
				string += gSpec.after(self.opcode)
		
		else:
			string += f"; !!! Unknown opcode: {hex(self.opcode)} !!!"
		
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
		self.labels = []
	
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
	
	def addLabel(self, addr):
		"""
		Add a label to be marked in the output
		"""
		
		self.labels.append(addr)
	
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
			if (s.location in self.labels):
				f.write("\n" + getLabelString(s.location) + ":\n")
			
			f.write("\t" + s.getString() + "\n")
		
		f.close()

def disassemble(path, strat, section_info, instructions):
	"""
	Does disassembly for code segments
	"""
	
	# File header
	header = f"; disassembly using stratigise\n\n"
	
	for k, v in section_info.params.items():
		header += f"@{k} {v}\n"
	
	instructions.setPreamble(header)
	
	# Read in opcodes
	while (True):
		start = strat.getPos()
		opcode = gSpec.readOpcode(strat)
		
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
					
					# Break at end of section
					if (strat.getPos() > (section_info.start + section_info.length)):
						break
					
					# Based on the type, get the next value from the instruction stream appropraitely
					if (type == 'string'):
						args.append(strat.readString())
					elif (type == 'int32'):
						args.append(strat.readInt32LE())
					elif (type == 'offset32'):
						address = strat.readInt32LE() + strat.getPos()
						instructions.addLabel(address)
						args.append(Symbol(getLabelString(address)))
					elif (type == 'int16'):
						args.append(strat.readInt16LE())
					elif (type == 'offset16'):
						address = strat.readInt16LE() + strat.getPos()
						instructions.addLabel(address)
						args.append(Symbol(getLabelString(address)))
					elif (type == 'address16'):
						address = (strat.readInt16LE() or 1) + 0x4 # HACK
						instructions.addLabel(address)
						args.append(Symbol(getLabelString(address)))
					elif (type == 'int8'):
						args.append(strat.readInt8())
					elif (type == 'eval'):
						args.append(gSpec.unevaluate(strat))
					elif (type == 'varargs'):
						args += gSpec.varargs(strat, opcode, args, instructions)
					elif (type == 'placeholder64'):
						strat.readBytes(8)
					else:
						pass
			
			# Break at end of section
			if (strat.getPos() > (section_info.start + section_info.length)):
				break
			
			# Add instruction to bytecode tokens
			instructions.addInstruction(Instruction(opcode, args, start))
	
	instructions.writeFile(path + section_info.extension)

def handle_data(path, strat, section_info, instructions):
	Path(path + section_info.extension).write_bytes(strat.readBytes(section_info.length) or b"")

SECTION_HANDLERS = {
	"code": disassemble,
	"data": handle_data,
}

def process(path):
	"""
	Process a strat
	"""
	
	# Create a binary read stream
	strat = BinaryReadStream(path)
	
	# HACK Create instructions list
	# For now I've moved this here so we can create labels from the processSections function
	instructions = StratInstructionList()
	
	# Read strat headers and get sections
	sections = []
	
	if (hasattr(gSpec, "processSections")):
		sections += gSpec.processSections(strat, instructions)
	else:
		print("Error: Spec must have processSections in order to disassemble and read data.")
		return
	
	for s in sections:
		strat.setPos(s.start)
		(SECTION_HANDLERS[s.type])(path, strat, s, instructions)
