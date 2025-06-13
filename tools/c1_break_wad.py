#!/usr/bin/env python3
"""
Break a Croc 1 wad into (possibly still compressed) files
"""

from pathlib import Path
import os
import argparse

def readChunk(wad, offset, length):
	wad.seek(offset, 0)
	return wad.read(length)

def splitWad(wad, idx, dirname):
	for line in idx.readlines():
		line = line[:-1].split(",")
		filename = line[0]
		position = int(line[1])
		length = int(line[2])
		ulength = int(line[3])
		compression = line[4]
		
		if compression != "u":
			filename += f".{compression.upper()}"
		
		data = readChunk(wad, position, length)
		
		Path(os.path.join(dirname, filename)).write_bytes(data)

def main():
	args = argparse.ArgumentParser(prog="splitwad", description="Split a Croc 1 wad into seprate parts, possibly still compressed")
	args.add_argument("input", help="Input file path")
	args.add_argument("output", help="Output directory (created if it doesn't exist)")
	args = args.parse_args()
	
	os.makedirs(args.output, exist_ok=True)
	
	with open(args.input, "rb") as wad:
		with open(args.input.removesuffix(".wad") + ".idx", "r") as idx:
			splitWad(wad, idx, args.output)

if __name__ == "__main__":
	main()
