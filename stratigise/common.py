"""
Common utilities for the stratigise project.
"""

import struct
import sys
import importlib.util as imut

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
	
	def setPos(self, pos):
		"""
		Set the current file position
		"""
		
		self.file.seek(pos)
	
	def getLength():
		"""
		Get the length of the file
		"""
		
		# Save old pos
		old = self.getPos()
		
		# Get ending pos
		self.file.seek(0, 2)
		length = self.file.getPos()
		
		# Return old pos
		self.setPos(old)
		
		return length
	
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
	
	def readInt24LE(self):
		"""
		Read and return a 24-bit little-endian integer.
		"""
		
		b = self.file.read(3)
		
		if (len(b) != 3):
			return None
		
		return struct.unpack("<i", b + b"\x00")[0]
	
	def readInt24BE(self):
		"""
		Read and return a 24-bit big-endian integer.
		"""
		
		b = self.file.read(3)
		
		if (len(b) != 3):
			return None
		
		return struct.unpack(">i", b"\x00" + b)[0]
	
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
		Read an n byte integer (four or less bytes only).
		"""
		
		if (size == 1):
			return self.readInt8()
		elif (size == 2):
			return self.readInt16LE()
		elif (size == 3):
			return self.readInt24LE()
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

class SectionInfo:
	"""
	Information about a section of a strat file.
	"""
	
	def __init__(self, type, start, length, extension, *, params = None):
		self.type = type
		self.start = start
		self.length = length
		self.extension = extension
		self.params = params

class Symbol:
	"""
	Eval symbol: the job of this class is only to contain a string that will be 
	added without quotes to the output.
	"""
	
	def __init__(self, value):
		self.value = value

def formatHex(n):
	"""
	Format 32-bit integer as hexidecimal
	"""
	n = n if (n >= 0) else (-n) + (1 << 31)
	return "0x" + '{:08X}'.format(n)

def formatHexOfSize(size, number):
	"""
	Format any size integer as any length hexidecimal. The hexidecimal should be
	representitive of the bits that make up the number and not nessicarially the
	number itself.
	"""
	
	# Account for twos compliment and format behaviour
	number = number if (number >= 0) else (-number) + (1 << ((size * 8) - 1))
	return ("0x{:" + str(size) + "X}").format(number)

def loadModule(path):
	"""
	Load a module from a file path
	"""
	
	spec = imut.spec_from_file_location("opcodes", path)
	module = imut.module_from_spec(spec)
	spec.loader.exec_module(module)
	
	return module

def getLabelString(addr):
	"""
	Get the string for a label
	"""
	
	if (addr == None):
		return "ERRLABEL"
	
	return "Label_" + hex(addr)[2:]
