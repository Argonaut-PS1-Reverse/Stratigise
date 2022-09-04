"""
Break a Croc 2 style wad into files for each section
"""

import os
import sys
from stratigise.common import BinaryReadStream

def writeBinaryFile(path, content):
	with open(path, "wb") as f:
		f.write(content)

def breakWad(input):
	wad = BinaryReadStream(input + ".wad")
	
	# Create dir
	os.makedirs(input, exist_ok = True)
	
	# Read wad
	wad_length = wad.readInt32LE()
	
	sect_num = 0
	
	while (True):
		# Read section header
		sect_nam = wad.readBytes(4)
		
		# Check for end of file
		if (sect_nam == None):
			break
		
		# Get name and length
		sect_nam = sect_nam.decode('latin_1')[::-1]
		sect_len = wad.readInt32LE()
		
		print(f"Writing section {sect_nam} of length {hex(sect_len)} ...")
		
		# Write file
		data = wad.readBytes(sect_len)
		
		if (data == None):
			data = b""
		
		writeBinaryFile(input + "/" + str(sect_num) + "_" + sect_nam + ".BIN", data)
		
		# Increment section number
		sect_num += 1

def main():
	if (len(sys.argv) < 2):
		print(f"Usage: {sys.argv[0]} [path to wad]\n\nA folder is made next to the wad containing the extacted contents.")
	
	if (sys.argv[1].endswith(".wad")):
		h = sys.argv[1].split(".")
		h.pop()
		sys.argv[1] = ".".join(h)
	
	breakWad(sys.argv[1])

if (__name__ == "__main__"):
	main()
