#!/usr/bin/python

import sys
import os
import shutil
import json

def load_build_config(profile = "default"):
	"""
	Load a build config file (controls linking, includes and may include
	compiler location information)
	"""
	
	with open("build.json", "r") as f:
		return json.load(f).get(profile, None)

def list_files_in_folder(d, ending = ".c"):
	"""
	List files in a folder
	"""
	
	lst = []
	outline = []
	
	for root, dirs, files in os.walk(d):
		root = str(root)
		
		for f in files:
			f = str(f)
			
			if (not f.endswith(ending)):
				continue
			
			lst.append(root + "/" + f)
		
		for d in dirs:
			outline.append(root + "/" + str(d))
	
	return (lst, outline)

def create_folder(d, mode = 0o755):
	"""
	Create a directory
	"""
	
	try:
		os.makedirs(d, mode = mode)
	except FileExistsError:
		print(f"\033[33mWarning: Tried to created file \"{d}\" when it already exsists.\033[0m")

def align_string(base, count = 8):
	"""
	Create an aligned string
	
	"7/12", count = 10 -> "7/12      " 
	"""
	
	string = [" "] * count
	
	for i in range(len(base)):
		string[i] = base[i]
	
	return "".join(string)

def main():
	if (os.name == "nt"):
		os.system("cls")
	
	# Set up the profile
	profile = sys.argv[1] if len(sys.argv) > 1 else "default"
	config = load_build_config(profile)
	
	if (config == None):
		print(f"\033[31m[No such build profile: {profile}]\033[0m")
		return 1
	
	print(f"\033[35m[Using build profile {profile}]\033[0m")
	
	# Run prebuild commands
	for cmd in config.get("prebuild", []):
		print(f"\033[35m[Run command: {cmd}]\033[m")
		os.system(cmd)
	
	# Create some dirs
	shutil.rmtree("temp", ignore_errors = True)
	create_folder("temp", mode = 0o755)
	
	# Enumerate files to build
	files, outline = [], []
	
	for folder in config.get("folders", ["src"]):
		create_folder("temp/" + folder)
		files_a, outline_a = list_files_in_folder(folder)
		files += files_a
		outline += outline_a
	
	for folder in outline:
		create_folder("temp/" + folder, mode = 0o755)
	
	# Set up include dirs
	include = ""
	
	for incl in config["includes"]:
		include += f"-I\"{incl}\" "
	
	print(f"\033[35m[Include dirs: {include}]\033[0m")
	
	# Set up defines
	defines = ""
	
	for incl in config.get("defines", []):
		defines += f"-D{incl} "
	
	print(f"\033[35m[Defines: {defines}]\033[0m")
	
	# Build files
	compiler = config.get("compiler", "cc")
	item = 1
	
	for f in files:
		progress = align_string(f"{item}/{len(files)}", count = 2 * len(str(len(files))) + 1)
		print(f"\033[36m[{progress} Building item: \"{f}\"]\033[0m")
		status = os.system(f"{compiler} -c {defines} -o temp/{f}.output -Wall -Wextra -Wno-missing-braces -Wno-unused-parameter {f} {include}")
		
		if (status):
			print(f"\033[31m[Failed to build \"{f}\"]\033[0m")
			sys.exit(status)
		
		item += 1
	
	# Set up linker
	include = ""
	
	for incl in config["links"]:
		print(f"\033[36m[Adding linked library {incl}]\033[0m")
		include += f"-l{incl} "
	
	# output files
	output_files = ""
	
	for f in files:
		output_files += f"temp/{f}.output "
	
	# Link!
	print(f"\033[32m[Linking binary]\033[0m")
	
	output = config.get("output", "application")
	status = os.system(f"{compiler} -o {output} -std=c2x {output_files} {include}")
	
	if (status):
		print(f"\033[31m[Failed to link binary]\033[0m")
	
	return status

if (__name__ == "__main__"):
	main()
