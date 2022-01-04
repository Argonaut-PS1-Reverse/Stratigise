#!/usr/bin/python

"""
Stratigise: Prototyping argounaut bytecode disassembler
"""

import sys
import stratigise.disassembler as dis

DEFAULT_STRAT_SPEC = "croc1"

def printUsageAndExit():
	print(f"Usage: {sys.argv[0]} [options] files ...")
	print()
	print("\toptions: See below.")
	print("\tfiles: Any number of strat BIN files to process.")
	print()
	print("Options:")
	print("\t--spec gamename: Set the strat spec to the one for the game gamename. Default: " + DEFAULT_STRAT_SPEC)
	print("\t--help, -h, /?: Print this help message.")
	print()
	
	sys.exit(127) # TODO: Is this an appropraite exit code?

def main(params):
	"""
	Load default opcodes, then preform all commands
	"""
	
	if (len(params) == 0 or params[0] == "--help" or params[0] == "-h" or params[0] == "/?"):
		printUsageAndExit()
	
	spec = DEFAULT_STRAT_SPEC
	
	i = 0
	while (i < len(params)):
		if (params[i] == "--spec"):
			spec = params[i + 1]
			i += 1
		else:
			dis.loadSpec(spec)
			dis.disassemble(params[i], params[i] + ".DIS")
		
		i += 1
	
	
	
	#for cmd in params:
		#cmd = cmd.split('=')
		
		#if (cmd[0] == 'opcodes'):
			#print(f"Loading opcodes for {cmd[1]} ⋅⋅⋅")
			#dis.loadSpec(cmd[1])
		#else:
			#print(f"Processing \"{cmd[0]}\" ⋅⋅⋅")
			#dis.disassemble(cmd[0], cmd[0] + ".DIS")

if (__name__ == "__main__"):
	main(sys.argv[1:])
