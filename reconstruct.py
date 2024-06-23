#!/usr/bin/env python
"""
reconstruction of secript from an assembly
"""

import sys, re

import c1script.tokenizer as tokenizer
from c1script.asm_parser import *
from c1script.reconstructor import *
from c1script.formatter import *

def reconstruct(input, output):
    try:
        input_file = open(input)
        text = input_file.read()
        lines = text.split("\n")
        tokens = tokenizer.tokens(text)

        asm_parser = AsmParser(tokens, lines)
        insns, strat_attrs, preloads = asm_parser.parse()

        reconstructor = Reconstructor(insns, strat_attrs, preloads)
        strat_trees = reconstructor.reconstruct()

        print("\nWritting output...")
        for strat, tree in strat_trees.items():
            formatter = Formatter(tree, f"Reconstructed code for {strat} from {input}")
            code = formatter.format()
            #print("\nTree:\n")
            #print(tree.format_tree())

            with open(f"{output}.{strat}.c1s", "w") as f:
                f.write(code)
                print(f"  --> {output}.{strat}.c1s")

    except OSError as e:
        print(f"Error opening file: {e}", file=sys.stderr)
        exit(1)

if (__name__ == "__main__"):
    if (len(sys.argv) == 3):
        reconstruct(sys.argv[1], sys.argv[2])
    else:
        print(f"Usage: {sys.argv[0]} <DIS file> <strat files prefix>")
