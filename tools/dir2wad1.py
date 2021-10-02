#!/usr/bin/python
"""
Script to convert a folder of files into an uncompressed Croc 1 wad and idx pair
"""

from os import listdir
from os.path import isfile, join, split
import sys

def getFiles(dir):
	"""
	Get the relitive paths of only files in the given directory
	"""
	
	return [f for f in listdir(dir) if isfile(join(dir, f))]

def makeWad(input, output):
	"""
	Make a croc 1 wad/idx pair given the input and output filenames.
	"""
	
	files = getFiles(input)
	
	index = open(output + ".idx", "w")
	wad = open(output + ".wad", "wb")
	
	for f in files:
		print(f"Write file: {f}")
		
		# read file content
		candidate_file = open(join(input, f), "rb")
		content = candidate_file.read()
		candidate_file.close()
		
		# get attribs
		length = str(len(content))
		
		# write index
		# filename,position,length,uncompressedlength,compression
		index.write(f + "," + str(wad.tell()) + "," + length + "," + length + ",u\n")
		
		# write wad
		wad.write(content)
	
	wad.close()
	index.close()

def main():
	if (len(sys.argv) == 3):
		makeWad(sys.argv[1], sys.argv[2])
	else:
		print(sys.argv[0], "[input directory] [output wad file]")

if (__name__ == "__main__"):
	main()
