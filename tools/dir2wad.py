#!/usr/bin/python
"""
Script to convert a folder of files into a Croc: Legend of the Gobbos .WAD and
.IDX pair
"""

from os import listdir
from os.path import isfile, join, split
import argparse

def countRun(data, width=1):
	for i in range(width, len(data)):
		if data[i] != data[i % width]:
			return i
	
	return len(data)

toSignedByte = lambda i: int.from_bytes(i.to_bytes(1, 'little', signed=True), 'little')

def _compress(data, chunkSize=1, minRun=3):
	"""
	Compress data using Croc's RLE format.
	
	chunkSize - 1 for byte compression or 2 for word compression
	minRun - minium run, 3 for byte compression or 2 for word compression
	"""
	
	# Append data with zeros if it's size is not a multiple of the chunk size.
	# It's a HACK but CrocUtils seems to round up the output size if needed
	# and I can assume that's what the game does as well.
	if (len(data) % chunkSize != 0):
		data += b"\x00" * (chunkSize - (len(data) % chunkSize))
	
	maxRun = minRun + 127
	output = bytearray(len(data))
	outIndex = 0
	literals = 0
	i = 0
	
	def runLength(data, index, chunkSize, maxRun):
		"""
		Determine the optimal run length for the chunk at index
		"""
		
		assert(index < len(data))
		
		chunk = data[chunkSize*index:chunkSize*(index+1)]
		
		assert(chunk != b'')
		
		for i in range(1, maxRun):
			if data[(index+i)*chunkSize:(index+i+1)*chunkSize] != chunk:
				return i
		else:
			return maxRun
	
	def putLiterals(data, output, fromIndex, toIndex, count, chunkSize):
		"""
		Output literals from the input data to an output buffer
		"""
		
		if count > 0:
			output[toIndex] = toSignedByte(-count)
			
			for i in range(chunkSize * count):
				output[toIndex + i + 1] = data[chunkSize * fromIndex + i]
			
			return 1 + chunkSize * count
		else:
			return 0
	
	def putRun(data, output, fromIndex, toIndex, minRun, chunkSize, runLength):
		"""
		Encode a run marker
		"""
		
		output[toIndex] = toSignedByte(runLength - minRun)
		
		for i in range(chunkSize):
			output[toIndex + i + 1] = data[chunkSize * fromIndex + i]
		
		return 1 + chunkSize
	
	while i < (len(data) // chunkSize):
		runlen = runLength(data, i, chunkSize, maxRun)
		
		if runlen < minRun:
			literals += 1
			i += 1
		else:
			outIndex += putLiterals(data, output, i - literals, outIndex, literals, chunkSize)
			literals = 0
			
			outIndex += putRun(data, output, i, outIndex, minRun, chunkSize, runlen)
			i += runlen
		
		if literals >= 128:
			outIndex += putLiterals(data, output, i - literals, outIndex, literals, chunkSize)
			literals = 0
	
	# Output any remaining literals
	outIndex += putLiterals(data, output, i - literals, outIndex, literals, chunkSize)
	
	return output[:outIndex]

def compress(data, chunkSize=1, minRun=3):
	try:
		return _compress(data, chunkSize, minRun)
	except:
		return None

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
			# Byte RLE
			cb_content = compress(content)
			
			# Word RLE
			cw_content = compress(content, 2, 2)
			
			# Determine best compression
			if cw_content and len(cw_content) < len(content):
				content = cw_content
				length = str(len(cw_content))
				compression = "w"
			
			if cb_content and len(cb_content) < len(content):
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
	args.add_argument("-c", "--compress", action='store_true', help="Try to compress files; this may take longer but produces a smaller WAD")
	args.add_argument("-q", "--quiet", action='store_true', help="Do not print contents of the index file while building wad")
	args.add_argument("input", help="The directory to turn into a WAD file")
	args.add_argument("output", help="The base name of the WAD (e.g. without .WAD/.IDX)")
	args = args.parse_args()
	
	makeWad(args.input, args.output, use_compression = args.compress, print_index = not args.quiet)

if (__name__ == "__main__"):
	main()
