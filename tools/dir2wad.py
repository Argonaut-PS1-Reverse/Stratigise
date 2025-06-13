#!/usr/bin/python
"""
Script to convert a folder of files into a Croc: Legend of the Gobbos .WAD and
.IDX pair
"""

from os import listdir
from os.path import isfile, join, split
import argparse
import sys

def countRun(data, width=1):
	for i in range(width, len(data)):
		if data[i] != data[i % width]:
			return i
	
	return len(data)

tobyte = lambda i: i.to_bytes(1, 'little', signed=True)

def compressByte(input):
	"""
	Preform byte-wise run length encoding
	"""
	
	output = bytearray()
	buf = bytearray()
	
	def outputLiterals():
		nonlocal buf, output
		if len(buf) > 0:
			output += tobyte(-len(buf))
			output += buf
			buf = bytearray()
	
	i = 0
	
	while True:
		runlen = countRun(input[i:i+130])
		
		if len(buf) >= 127 or runlen >= 3:
			outputLiterals()
		
		if runlen >= 3:
			output += tobyte(runlen - 3)
			output.append(input[i])
			i += runlen
		else:
			buf.append(input[i])
			i += 1
		
		if i == len(input):
			outputLiterals()
			break
	
	return bytes(output)

def compressWord(input):
	"""
	Preform word-wise run length encoding (only works for inputs where
	len(input) % 2 == 0)
	"""
	
	output = bytearray()
	buf = bytearray()
	
	def outputLiterals():
		nonlocal buf, output
		if len(buf) > 0:
			output += tobyte(-(len(buf)//2))
			output += buf
			buf = bytearray()
	
	i = 0
	
	while True:
		runlen = countRun(input[2*i:2*(i+129)], 2)//2
		
		if len(buf) >= 254 or runlen >= 2:
			outputLiterals()
		
		if runlen >= 2:
			output += tobyte(runlen - 2)
			output += input[2*i:2*i+2]
			i += runlen
		else:
			buf += input[2*i:2*i+2]
			i += 1
		
		if i == len(input)//2:
			outputLiterals()
			break
	
	return bytes(output)

def getFiles(dir):
	"""
	Get the relitive paths of only files in the given directory
	"""
	
	return [f for f in listdir(dir) if isfile(join(dir, f))]

def makeWad(input, output, *, use_compression=True, print_index=True):
	"""
	Make a Croc WAD/IDX pair given the input and output filenames.
	"""
	
	files = sorted(getFiles(input))
	
	index = open(output + ".idx", "w")
	wad = open(output + ".wad", "wb")
	
	for f in files:
		# print(f"Write file: {f}")
		
		# read file content
		candidate_file = open(join(input, f), "rb")
		content = candidate_file.read()
		candidate_file.close()
		
		# get attribs
		uncompressed_length = str(len(content))
		
		# try compression if allowed
		length = uncompressed_length
		compression = "u"
		
		if use_compression:
			# Byte RLE (have to do this before word so we don't accidently
			# compress twice - let's not ask how I know)
			cb_content = compressByte(content)
			
			# Word RLE (only when input length is even)
			if len(content) % 2 == 0:
				cw_content = compressWord(content)
				if len(cw_content) < len(content):
					content = cw_content
					length = str(len(cw_content))
					compression = "w"
			
			if len(cb_content) < len(content):
				content = cb_content
				length = str(len(cb_content))
				compression = "b"
		
		# write index
		# filename,position,length,uncompressedlength,compression
		index_entry = f + "," + str(wad.tell()) + "," + length + "," + uncompressed_length + "," + compression + "\n"
		index.write(index_entry)
		if print_index: print(index_entry, end="")
		
		# write wad
		wad.write(content)
	
	wad.close()
	index.close()

def main():
	args = argparse.ArgumentParser(prog="dir2wad", description="Convert a folder to a Croc: Legend of the Gobbos WAD/IDX pair")
	args.add_argument("-C", "--no-compress", action='store_true', help="Do not compress files")
	args.add_argument("-q", "--quiet", action='store_true', help="Do not print contents of the index file while building wad")
	args.add_argument("input", help="The directory to turn into a WAD file")
	args.add_argument("output", help="The base name of the WAD (e.g. without .WAD/.IDX)")
	args = args.parse_args()
	
	makeWad(args.input, args.output, use_compression = not args.no_compress, print_index = not args.quiet)

def test_compression():
	TEST_DATA = b"\xed\xef\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x0d\x77\x21\x21\x22\x21\x21\x00\x00\x00\x00\x00\x00\x00\x00\x3a"
	
	import binascii
	
	byte = compressByte(TEST_DATA)
	word = compressWord(TEST_DATA)
	
	print("orig: len =", len(TEST_DATA))
	print("#1  :", binascii.hexlify(byte), len(byte)/len(TEST_DATA))
	print("#2  :", binascii.hexlify(word), len(word)/len(TEST_DATA))

if (__name__ == "__main__"):
	main()
