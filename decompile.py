#!/usr/bin/python

"""
Stratigise: Prototyping argounaut bytecode disassembler
"""

import sys
import stratigise.disassembler as dis

def printUsageAndExit():
	print(f"Usage: {sys.argv[0]} [opcodes=OPCODEFILE] file1 file2 ...")
	print("\topcodes: Set the opcodes for all of the files after the file is set. Set to 'croc1' by default. Possible values:")
	print("\t\tcroc1, croc2")
	print("\tfiles: Any number of files to process.")
	
	sys.exit(127) # TODO: Is this an appropraite exit code?

def main(params):
	"""
	Load default opcodes, then preform all commands
	"""
	
	if (len(params) == 0 or params[0] == "--help" or params[0] == "-h"):
		printUsageAndExit()
	
	params.insert(0, "opcodes=croc1")
	
	for cmd in params:
		cmd = cmd.split('=')
		
		if (cmd[0] == 'opcodes'):
			print(f"Loading opcodes for {cmd[1]} ⋅⋅⋅")
			dis.loadSpec(cmd[1])
		else:
			print(f"Processing \"{cmd[0]}\" ⋅⋅⋅")
			dis.disassemble(cmd[0], cmd[0] + ".DIS")

if (__name__ == "__main__"):
	main(sys.argv[1:])
