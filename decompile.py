#!/usr/bin/python

"""
Stratigise: Prototyping argounaut bytecode disassembler
"""

import struct
import sys
from strateval import EVAL_FUNC

def printUsageAndExit():
	print(f"Usage: {sys.argv[0]} [opcodes=OPCODEFILE] file1 file2 ...")
	print("\topcodes: Set the opcodes for all of the files after the file is set. Set to croc1 by default. Possible values:")
	print("\t\tcroc1, croc2")
	print("\tfiles: Any number of files to process.")
	
	sys.exit(127)

# The dynamic opcode table
OP_TABLE = None

def loadOpcodes(name = "croc1"):
	"""
	Load a set of opcodes
	"""
	
	global OP_TABLE
	
	f = open(name + '.py', 'r')
	OP_TABLE = eval(f.read())
	f.close()

################################################################################

class BinaryReadStream:
	"""
	A binary file stream supporting only needed operations.
	
	TODO: There is probably some more standardised way to do this that I still
	need to find out about.
	"""
	
	def __init__(self, path):
		"""
		Open the file at the given path
		"""
		self.file = open(path, "rb")
	
	def __del__(self):
		"""
		Close the file assocaited with the stream
		"""
		self.file.close()
	
	def getPos(self):
		"""
		Get the current file position
		"""
		
		return self.file.tell()
	
	def readByte(self):
		"""
		Read and return a byte from the stream.
		"""
		
		b = self.file.read(1)
		
		if (len(b) == 0):
			return None
		
		return b
	
	def readBytes(self, count):
		"""
		Read and return bytes from the stream.
		"""
		
		b = self.file.read(count)
		
		if (len(b) == 0):
			return None
		
		return b
	
	def readInt32LE(self):
		"""
		Read and return a 32-bit little-endian integer.
		"""
		
		b = self.file.read(4)
		
		if (len(b) != 4):
			return None
		
		return struct.unpack("<i", b)[0]
	
	def readInt32BE(self):
		"""
		Read and return a 32-bit big-endian integer.
		"""
		
		b = self.file.read(4)
		
		if (len(b) != 4):
			return None
		
		return struct.unpack(">i", b)[0]
	
	def readInt16LE(self):
		"""
		Read and return a 16-bit little-endian integer.
		"""
		
		b = self.file.read(2)
		
		if (len(b) != 2):
			return None
		
		return struct.unpack("<h", b)[0]
	
	def readInt16BE(self):
		"""
		Read and return a 16-bit big-endian integer.
		"""
		
		b = self.file.read(2)
		
		if (len(b) != 2):
			return None
		
		return struct.unpack(">h", b)[0]
	
	def readInt8(self):
		"""
		Read and return a 8-bit integer.
		"""
		
		b = self.file.read(1)
		
		if (len(b) != 1):
			return None
		
		return struct.unpack("B", b)[0]
	
	def readInt(self, size):
		"""
		Read an n byte integer (1, 2 or 4 bytes).
		"""
		
		if (size == 1):
			return self.readInt8()
		elif (size == 2):
			return self.readInt16LE()
		elif (size == 4):
			return self.readInt32LE()
	
	def readString(self):
		"""
		Read and return a NUL terminated string.
		"""
		
		string = ""
		last = None
		
		while (True):
			b = self.readByte()
			
			if (b != b'\x00'):
				string += b.decode('latin_1')
			else:
				break
		
		return string

################################################################################

def formathex(n):
	"""
	Format 32-bit integer as hexidecimal
	"""
	n = n if (n >= 0) else (-n) + (1 << 31)
	return "0x" + '{:08X}'.format(n)

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
		
		if (self.opcode in OP_TABLE):
			# Write opcode name
			string += str(OP_TABLE[self.opcode][0])
			
			# Parse opcode arguments
			arg = 0
			while (arg < len(OP_TABLE[self.opcode]) - 1):
				# Get the type of argument
				type = OP_TABLE[self.opcode][arg + 1]
				
				string += ' '
				
				# Based on the type, format the value appropraitely
				if (type == 'string'):  string += self.arguments[arg]
				elif (type == 'int32'): string += str(self.arguments[arg])
				elif (type == 'int16'): string += str(self.arguments[arg])
				else: string += str(self.arguments[arg])
				
				arg += 1
			
			string += f"    ; Location: {formathex(self.location)}"
		
		else:
			string += f"; Unknown opcode: {formathex(self.opcode)}"
		
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
		
		for s in self.stream:
			print(s.getString())
	
	def writeFile(self, path):
		"""
		Write the contents of an instruction stream to a file.
		"""
		
		f = open(path, "w")
		
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
	instructions.setPreamble(f"; Strat was {size} bytes long.\n; Second bytes were {formathex(secondint)}\n")
	
	# Read in opcodes
	while (True):
		start = strat.getPos()
		opcode = strat.readInt(OP_TABLE['InstructionSize'])
		
		# Break on EOF or incomplete opcode
		if (opcode == None):
			print("Warning: Incomplete opcode, probably just before EOF due to unrecognised instruction with variable length arguments.")
			break
		
		# Write opcode based on arguments in table
		else:
			args = []
			
			# Parse opcode arguments
			if (opcode in OP_TABLE):
				for arg in range(1, len(OP_TABLE[opcode])):
					type = OP_TABLE[opcode][arg]
					
					# Based on the type, format the next value in the
					# instruction stream appropraitely
					if (type == 'string'):
						args.append('"' + strat.readString() + '"')
					elif (type == 'int32'):
						args.append(str(strat.readInt32BE()))
					elif (type == 'int16'):
						args.append(str(strat.readInt16BE()))
					elif (type == 'eval'):
						print("Warning: Eval support is not complete!!")
						args.append(EVAL_FUNC[OP_TABLE["EvalType"]](strat))
					
					arg += 1
			
			# Add instruction to bytecode tokens
			instructions.addInstruction(Instruction(opcode, args, start))
	
	# Write disassembled file
	instructions.writeFile(output)

def main(params):
	"""
	Load default opcodes, then preform all commands
	"""
	
	if (len(params) == 0 or params[0] == "--help" or params[0] == "-h"):
		printUsageAndExit()
	
	loadOpcodes()
	
	for cmd in params:
		cmd = cmd.split('=')
		
		if (cmd[0] == 'opcodes'):
			print(f"Loading opcodes for {cmd[0]}...")
			loadOpcodes(cmd[1])
		else:
			print(f"Processing {cmd[0]}...")
			disassemble(cmd[0], cmd[0] + ".DIS")

if (__name__ == "__main__"):
	main(sys.argv[1:])
