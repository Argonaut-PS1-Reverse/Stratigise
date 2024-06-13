#!/usr/bin/env python
"""
Strat ASM assembler
"""

import c1asm.tokeniser as tokeniser
import c1asm.assembler as assembler
import c1asm.common as common
from pathlib import Path
import sys
import os
import sqlite3

def run_sql_script(db_path, content):
	"""
	Run an SQL script on the Croc DE database.
	"""
	
	con = sqlite3.connect(db_path)
	cur = con.cursor()
	cur.executescript(content)
	con.commit() # Might not be needed?
	con.close()

def main(input, output):
	assembler.loadSpec("croc1")
	
	# Open file write stream
	f = common.BinaryWriteStream(output)
	
	# Write temp header
	f.writeInt32LE(0)
	f.writeInt32LE(0)
	
	# Tokenise and assemble
	end, attr, labels = assembler.assemble(f, tokeniser.tokenise(input))
	
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
	
	# Generate label physical locations
	sql_script = ""
	
	failed_strats = []
	for s in strat_info:
		if strat_info[s]['pc'] in labels:
			sql_script += f"UPDATE StratIndex SET pc = {labels[strat_info[s]['pc']] - 4}, var_size = {strat_info[s]['vars']} WHERE name = '{strat_info[s]['name']}';\n"
		else:
			failed_strats.append(strat_info[s]['name'])

	if len(failed_strats) > 0:
		print()
		print("WARNING!!!: No matching labels for strats: " + ", ".join(failed_strats))
	
	# Update DB automatically or print out info on how to do that
	if (os.getenv("CROC_DB")):
		print("Updating croc.db... ", end='')
		run_sql_script(os.getenv("CROC_DB"), sql_script)
		print("Done!")
	else:
		print()
		print("*" * 80)
		print("STRUN.BIN or croc.db might need to be updated, if you have modified the strat in such a way that the entry point addresses or numbers of used global variables have changed.")
		print("To update croc.db (for Definitive Edition) you need to open croc.db at table StratIndex in database browsing software and run the following SQL script:")
		print()
		print(sql_script)
		print("Tip: You can set the CROC_DB environment variable to the path of croc.db and it will be automatically updated.")
		print("Right now there is no way to edit STRUN.BIN unless you have a hexeditor and know the format.")
		print("*" * 80)
		print()
	
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
		print("Usage:")
		print(f"    {sys.argv[0]} [DIS file name] [output strat name]")
