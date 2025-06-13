#!/usr/bin/env python3
"""
Inspect word RLE compression for Croc 1
"""
from pathlib import Path
import os
import argparse

toInteger = lambda x: int.from_bytes(x, 'big', signed=True)

def analyse(f, chunkSize):
	minRun = 3 if chunkSize == 1 else 2
	
	while True:
		p = f.tell()
		cmd = f.read(1)
		
		if not cmd:
			print("<end of data>")
			break
		else:
			cmd = toInteger(cmd)
		
		if cmd < 0:
			b = f.read(-cmd * chunkSize)
			
			print(f"{p:05x} <copy {-cmd}> {b.hex()}")
			
			if (len(b) != -cmd * chunkSize):
				print("<incomplete>")
				break
		else:
			b = f.read(chunkSize)
			
			print(f"{p:05x} <run {minRun + cmd}> {b.hex()}")
			
			if len(b) != chunkSize:
				print("<incomplete>")
				break

def main():
	args = argparse.ArgumentParser(prog="inspect_compression", description="Inspect Croc 1 RLE compression")
	args.add_argument("input", help="Input file path")
	args.add_argument("-w", "--word", action='store_true', help="Word RLE")
	args = args.parse_args()
	
	with open(args.input, "rb") as f:
		analyse(f, 2 if args.word else 1)

if __name__ == "__main__":
	main()
