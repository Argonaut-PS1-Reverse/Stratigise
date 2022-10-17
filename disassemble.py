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
		# Set current strat spec
		if (params[i] == "--spec"):
			if (len(params) > (i + 1)):
				spec = params[i + 1]
				i += 1
			else:
				print("Warning: Strat Spec was specified without a game name.")
		
		# Process file
		else:
			path = params[i]
			print(f"Processing \"{path}\" with spec \"{spec}\" ⋅⋅⋅")
			dis.loadSpec(spec)
			dis.process(path)
		
		i += 1

if (__name__ == "__main__"):
	main(sys.argv[1:])
