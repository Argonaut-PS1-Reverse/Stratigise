#!/usr/bin/env python
"""
Run disasembler, reconstructor and compiler for all strats
"""

import sys, os, shutil, subprocess, re, csv

KNOWN_BROKEN = [
    "BIRDSHLD.BIN", # Broken header
    "BLKNT_A3.BIN", # Empty
    "BMANTEST.BIN", # Empty
    "BUBBGEN.BIN", # Broken header
    "CORC.BIN", # Empty
    "FADETEST.BIN", # Empty
    "FLIBBY1.BIN", # Empty
    "MVSNPLAT.BIN", # Empty
    "MVSNWPLT.BIN", # Empty
    "MVSNWQT3.BIN", # Empty
    "PLATPETE.BIN", # Empty
    "SEED2.BIN", # Empty
    "SNAPPY.BIN", # Empty
    "SPIN.BIN", # Empty
    "ROLBOL0.BIN", # Broken header
    "TARPLAT.BIN", # Broken header
    "TIMESWCH.BIN", # Broken header

    # "BRAT1.BIN", # There are some zeros after valid `CreateTrigger 1 Label`
    # "FIRSTAT.BIN", # Weird PlayerIsWithinRadius2D call on empty stack
    # "FRST.BIN", # Weird PlayerIsWithinRadius2D call on empty stack
    # "RDFL.BIN", # There are some zeros after valid `CreateTrigger 1 Label`
    # "RKMO1.BIN", # Incompatible 32-bit placeholders instead of 64-bit
    # "TWST1.BIN", # Weird PlayerIsWithinRadius2D call on empty stack
    # "TWST2.BIN", # Weird PlayerIsWithinRadius2D call on empty stack
    # "SHFN.BIN", # Incompatible 32-bit placeholders instead of 64-bit
    # "SMASHBLK.BIN", # Incompatible 32-bit placeholders instead of 64-bit
    # "SMOKIE.BIN", # There are some zeros after valid `CreateTrigger 1 Label`
    # "UPEXIT.BIN" # Some weird 0xfd after valid `UnpausePlayer`
]

KNOWN_SIZES = {
    "DesertExplosion": 1, # Bigger than in the table!
    "Grinder": 1, # Bigger than in the table!
    "LavaSpout": 1, # Bigger than in the table!
    "MrLavaBlub": 0,
    "FrkSpkle": 0,
    "MalletMan2": 1,
    "TeleportingTemp": 0
}

def full_run(strats_dir, csv_path, output_dir):
    if not os.path.isdir(strats_dir):
        raise Exception(f"{strats_dir} is not a directory")
    if not os.path.isdir(output_dir):
        raise Exception(f"{output_dir} is not a directory")
    if not os.path.isfile(csv_path):
        raise Exception(f"{csv_path} doesn't exist")
    
    items = os.listdir(strats_dir)
    strats = []
    for item in items:
        if item[-4:] == ".BIN" and os.path.isfile(os.path.join(strats_dir, item)):
            strats.append(item)

    strat_sizes = load_strat_sizes(csv_path)

    print_fixed("STRAT", 15)
    print_fixed("DISASM", 12)
    print_fixed("ASM", 12)
    print_fixed("DIFF", 12)
    print_fixed("DECOMP", 12)
    print("COMP")

    counts = {
        "disassembler": {"success": 0, "warning": 0, "failed": 0},
        "assembler": {"success": 0, "warning": 0, "failed": 0},
        "diff": {"success": 0, "warning": 0, "failed": 0},
        "reconstructor": {"success": 0, "warning": 0, "failed": 0},
        "compiler": {"success": 0, "warning": 0, "failed": 0},
        "ignored": 0
    }

    for strat in strats:
        run_strat(strat, os.path.join(strats_dir, strat), csv_path,
                  os.path.join(output_dir, strat[:-4]), counts, strat_sizes)

    print("")
    print_fixed("STAGE", 20)
    print_fixed("OK", 10)
    print_fixed("WARNING", 10)
    print_fixed("FAILED", 10)
    print_fixed("SKIPPED", 10)
    print("SCORE")

    total = len(strats) - counts["ignored"]

    for stage in ["disassembler", "assembler", "diff", "reconstructor", "compiler"]:
        print_fixed(stage, 20)
        print_fixed(counts[stage]["success"], 10)
        print_fixed(counts[stage]["warning"], 10)
        print_fixed(counts[stage]["failed"], 10)
        print_fixed(total - counts[stage]["success"] - counts[stage]["warning"] - counts[stage]["failed"], 10)

        success = counts[stage]["success"] + counts[stage]["warning"] / 2.0
        percentage = success / float(total) * 100.0
        print(f"{percentage:.1f}%")
    
    print(f"\nIgnored {counts['ignored']} strat files")

def run_strat(strat, strat_path, csv_path, output_dir, counts, strat_sizes):
    print_fixed(strat, 15)

    if strat in KNOWN_BROKEN:
        print("Known broken -- ignored")
        counts["ignored"] += 1
        return

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    strat_bin = os.path.join(output_dir, strat)
    shutil.copy(strat_path, output_dir)
    shutil.copy(csv_path, output_dir)

    bin_dir = os.path.dirname(sys.argv[0])

    # Disasm

    cmd = ["python", os.path.join(bin_dir, '..', '..', 'disassemble.py'), strat_bin]

    try:
        result = subprocess.run(cmd, capture_output = True, encoding = "utf-8", env={'PYTHONIOENCODING': 'utf-8'}, timeout=1)
    except subprocess.TimeoutExpired:
        print("Timeout!")
        counts["disassembler"]["failed"] += 1
        return

    os.remove(os.path.join(output_dir, os.path.basename(csv_path)))

    with open(os.path.join(output_dir, f"{strat}.disassembler.out"), "w", encoding = "utf-8") as f:
        f.write(result.stdout)
    with open(os.path.join(output_dir, f"{strat}.disassembler.err"), "w", encoding = "utf-8") as f:
        f.write(result.stderr)

    if result.returncode != 0:
        print("Failed!")
        counts["disassembler"]["failed"] += 1
        return
    
    mo = re.search("Found (\\d+) strat\\(s\\) in", result.stdout)
    if not mo:
        print("Invalid output!")
        counts["reconstructor"]["failed"] += 1
        return
    #if int(mo.group(1)) == 0:
    #    print("No strats -- ignored")
    #    counts["ignored"] += 1
    #    return
    
    strat_disasm = strat_bin + ".DIS"
    
    errors = 0
    with open(strat_disasm) as f:
        text = f.read()
        errors += text.count("CommandError")
        errors += text.count("__unknown_operation_0x")

    if errors > 0:
        print_fixed(f"{errors} errors", 12)
        counts["disassembler"]["warning"] += 1
    else:
        print_fixed("OK", 12)
        counts["disassembler"]["success"] += 1

    # Assembler

    strat_reasm = strat_bin[:-4] + ".reassembled.BIN"
    
    cmd = ["python", os.path.join(bin_dir, '..', '..', 'assemble.py'), strat_disasm, strat_reasm]

    try:
        result = subprocess.run(cmd, capture_output = True, encoding = "utf-8", env={'PYTHONIOENCODING': 'utf-8'}, timeout=1)
    except subprocess.TimeoutExpired:
        print("Timeout!")
        counts["assembler"]["failed"] += 1
        return

    with open(os.path.join(output_dir, f"{strat}.assembler.out"), "w", encoding = "utf-8") as f:
        f.write(result.stdout)
    with open(os.path.join(output_dir, f"{strat}.assembler.err"), "w", encoding = "utf-8") as f:
        f.write(result.stderr)

    if result.returncode != 0:
        print("Failed!")
        counts["assembler"]["failed"] += 1
        return
    
    print_fixed("OK", 12)
    counts["assembler"]["success"] += 1
    
    # Difference check
    
    cmd = ["python", os.path.join(bin_dir, '..', '..', 'check_diff.py'), strat_bin, strat_reasm]

    try:
        result = subprocess.run(cmd, capture_output = True, encoding = "utf-8", env={'PYTHONIOENCODING': 'utf-8'}, timeout=1)

        with open(os.path.join(output_dir, f"{strat}.check_diff.out"), "w", encoding = "utf-8") as f:
            f.write(result.stdout)
        with open(os.path.join(output_dir, f"{strat}.check_diff.err"), "w", encoding = "utf-8") as f:
            f.write(result.stderr)

        if result.returncode != 0:
            print_fixed("Failed!", 12)
            counts["diff"]["failed"] += 1
        else:
            if result.stdout != "":
                print_fixed("Mismatch!", 12)
                counts["diff"]["failed"] += 1
            else:
                counts["diff"]["success"] += 1
                print_fixed("OK", 12)

    except subprocess.TimeoutExpired:
        print_fixed("Timeout!", 12)
        counts["diff"]["failed"] += 1

    # Reconstruction

    cmd = ["python", os.path.join(bin_dir, '..', '..', 'reconstruct.py'), strat_disasm, strat_bin]

    try:
        result = subprocess.run(cmd, capture_output = True, encoding = "utf-8", env={'PYTHONIOENCODING': 'utf-8'}, timeout=1)
    except subprocess.TimeoutExpired:
        print("Timeout!")
        counts["reconstructor"]["failed"] += 1
        return

    with open(os.path.join(output_dir, f"{strat}.reconstructor.out"), "w", encoding = "utf-8") as f:
        f.write(result.stdout)
    with open(os.path.join(output_dir, f"{strat}.reconstructor.err"), "w", encoding = "utf-8") as f:
        f.write(result.stderr)

    if result.returncode != 0:
        print("Failed!")
        counts["reconstructor"]["failed"] += 1
        return
    
    mo = re.search("([\d\.]+%) of lines have been processed", result.stdout)
    if not mo:
        print("Invalid output!")
        counts["reconstructor"]["failed"] += 1
        return
    
    if mo.group(1) == "100.0%":
        counts["reconstructor"]["success"] += 1
    else:
        counts["reconstructor"]["warning"] += 1
        print(mo.group(1))
        return
    
    print_fixed("OK", 12)

    # Recompiling

    strats_decomp = []
    strats_names = []
    for item in os.listdir(output_dir):
        path = os.path.join(output_dir, item)
        if os.path.isfile(path) and item[-4:] == ".c1s":
            strats_decomp.append(path)
            name = item.split(".")[-2]
            if name != "__unused":
                strats_names.append(name)

    strat_recompiled = strat_bin[:-4] + ".recompiled.BIN"

    if os.path.exists(strat_recompiled):
        os.remove(strat_recompiled)

    cmd = ["python", os.path.join(bin_dir, '..', '..', 'compile.py')] + strats_decomp + [strat_recompiled]

    try:
        result = subprocess.run(cmd, capture_output = True, encoding = "utf-8", env={'PYTHONIOENCODING': 'utf-8'}, timeout=10)
    except subprocess.TimeoutExpired:
        print("Timeout!")
        counts["compiler"]["failed"] += 1
        return

    with open(os.path.join(output_dir, f"{strat}.compiler.out"), "w", encoding = "utf-8") as f:
        f.write(result.stdout)
    with open(os.path.join(output_dir, f"{strat}.compiler.err"), "w", encoding = "utf-8") as f:
        f.write(result.stderr)

    if result.returncode != 0 or not os.path.isfile(strat_recompiled):
        print("Failed!")
        counts["compiler"]["failed"] += 1
        return
    
    new_sizes = {}
    for line in result.stdout.split("\n"):
        mo = re.search(
            "UPDATE StratIndex SET pc = \\d+, var_size = (\\d+) WHERE name = '(\\S+)';",
            line
        )
        if mo:
            new_sizes[mo.group(2)] = int(mo.group(1))

    for name in strats_names:
        if name not in new_sizes:
            print("Missing strat!")
            counts["compiler"]["failed"] += 1
            return
        
        if new_sizes[name] != strat_sizes[name]:
            if name not in KNOWN_SIZES or new_sizes[name] != KNOWN_SIZES[name]:
                print("Size mismatch!")
                counts["compiler"]["failed"] += 1
                return
    
    counts["compiler"]["success"] += 1
    print("OK")

def load_strat_sizes(csv_path):
    sizes = {}
    with open(csv_path, newline = "") as f:
        data = csv.DictReader(f)
        for entry in data:
            sizes[entry['name']] = int(entry['var_size'])

    return sizes

def print_fixed(string, width):
    s = str(string)
    print(s + " " * (width - len(s)), end = "")

if (__name__ == "__main__"):
    if (len(sys.argv) == 4):
        full_run(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print(f"Usage: {sys.argv[0]} <strats dir> <csv path> <output dir>")
