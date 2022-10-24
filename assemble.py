"""
Strat ASM assembler
"""

import c1asm.tokeniser as tokeniser
import c1asm.assembler as assembler
import c1asm.common as common
from pathlib import Path
import sys

def main(input, output):
	assembler.loadSpec("croc1")
	
	# Open file write stream
	f = common.BinaryWriteStream(output)
	
	# Write temp header
	f.writeInt32LE(0)
	f.writeInt32LE(0)
	
	# Tokenise and assemble
	end, attr = assembler.assemble(f, tokeniser.tokenise(input + ".DIS"))
	
	# Write audio data
	filesize = f.getLength()
	f.setPos(filesize)
	
	f.writeBytes(Path(input + ".AXX").read_bytes())
	
	filesize = f.getPos()
	
	# Write real header
	f.setPos(0)
	f.writeInt32LE(filesize - 4)
	f.writeInt16LE(attr["audio_upper"])
	f.writeInt16LE(end)

if (__name__ == "__main__"):
	if (len(sys.argv) == 3):
		main(sys.argv[1], sys.argv[2])
	else:
		print(f"Usage: {sys.argv[0]} [base file name, DIS and AXX pair] [output strat name]")
