#!/usr/bin/env python
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
	end, attr, labels = assembler.assemble(f, tokeniser.tokenise(input + ".DIS"))
	
	# Collect info about strats
	strat_info = {}
	
	# Parse the info
	for a in attr:
		if (a.startswith("strat")):
			parts = a.split("_")
			strat_number = int(parts[0][5:])
			strat_key = parts[1]
			strat_value = attr[a]
			
			if (strat_number not in strat_info):
				strat_info[strat_number] = {}
			
			strat_info[strat_number][strat_key] = strat_value
	
	# Print out label physical locations
	print()
	print("*" * 80)
	print("STRUN.BIN/croc.db might need to be updated, if you have modified the strat in such a way that the entry point addresses have changed.")
	print("To update croc.db (for Definitive Edition) you need to open croc.db at table StratIndex in database browsing software and run the following:")
	print()
	
	for s in strat_info:
		print(f"UPDATE StratIndex SET pc = {labels[strat_info[s]['pc']] - 4} WHERE name = '{strat_info[s]['name']}';")
	
	print()
	print("Right now there is no way to edit STRUN.BIN unless you have a hexeditor and know the format.")
	print("*" * 80)
	print()
	
	# Write audio data
	filesize = f.getLength()
	f.setPos(filesize)
	
	f.writeBytes(Path(input + ".AXX").read_bytes())
	
	filesize = f.getPos()
	
	# Write real header
	f.setPos(0)
	f.writeInt32LE(filesize - 8)
	f.writeInt16LE(attr["entry"])
	f.writeInt16LE(end - 4)

if (__name__ == "__main__"):
	if (len(sys.argv) == 3):
		main(sys.argv[1], sys.argv[2])
	else:
		print(f"Usage: {sys.argv[0]} [base file name, DIS and AXX pair] [output strat name]")
