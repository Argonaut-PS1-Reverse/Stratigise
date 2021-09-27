#!/usr/bin/python

import struct
import sys

class BinaryReadStream:
	"""
	A binary file stream supporting only needed operations
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

def formathex(n):
	"""
	Format 32-bit integer as hexidecimal
	"""
	n = n if (n >= 0) else (-n) + (1 << 31)
	return "0x" + '{:08X}'.format(n)

# Load the opcodes from opcodes.py
f = open('opcodes.py', 'r')
OP_TABLE = eval(f.read())
f.close()

def print_nnl(x): print(x, end='')

def dissassemble(path, output):
	"""
	Disassemble a strat
	"""
	
	strat = BinaryReadStream(path)
	output = open(output, "w")
	
	size = strat.readInt32LE()
	secondint = strat.readInt32BE()
	
	output.write(f"; Strat was {size} bytes long.\n")
	output.write(f"; Second bytes were {formathex(secondint)}\n")
	
	while (True):
		start = strat.getPos()
		opcode = strat.readInt32BE()
		
		# Break on EOF or incomplete opcode
		if (opcode == None):
			break
		
		# Write opcode based on arguments in table
		elif (opcode in OP_TABLE):
			# Write opcode name
			output.write(OP_TABLE[opcode][0])
			
			# Parse opcode arguments
			arg = 1
			while (arg < len(OP_TABLE[opcode])):
				# Get the type of argument
				type = OP_TABLE[opcode][arg]
				
				output.write(' ')
				
				# Based on the type, format the value appropraitely
				if (type == 'string'):
					output.write('"' + strat.readString() + '"')
				elif (type == 'int32'):
					output.write(str(strat.readInt32LE()))
				
				arg += 1
			
			# Write location comment
			output.write(f"     ; at {formathex(start)}")
			output.write("\n")
		
		# Unknown opcode comment
		else:
			output.write(f"; Unknown opcode: {formathex(opcode)}\n")
			pass

def main(path):
	dissassemble(path, path + ".DIS")

if (__name__ == "__main__"):
	main(sys.argv[1])
