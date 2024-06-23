#!/usr/bin/env python
"""
CLS compiler
"""

import sys, re

import c1script.tokenizer as tokenizer
from c1script.parser import *
from c1script.generator import *
from c1script.formatter import *
import assemble

def compile(inputs, output):
    try:
        full_asm = ""
        strat_index = 0

        for i in range(len(inputs)):
            input = inputs[i]
            input_file = open(input)
            
            text = input_file.read()
            lines = text.split("\n")

            tokens = tokenizer.tokens(text)
            parser = Parser(tokens)
            tree = parser.parse()
            #print("\nTree:\n")
            #print(tree.format_tree())

            #formatter = Formatter(tree)
            #formatted = formatter.format()
            #with open(input + ".formatted.c1s", "w") as f:
            #    f.write(formatted)
            #print("\nIdentifiers:\n")
            #for id in parser.identifiers.keys():
            #    print(f"    {id}: {parser.identifiers[id]}")

            generator = Generator(tree, strat_index, i > 0, i < len(inputs) - 1)
            asm, strat_index = generator.generate()
            #print("\nAssembly output:\n")
            #print(asm)

            full_asm += asm

        output_asm = output + ".intermediate.DIS"

        with open(output_asm, "w") as f:
            f.write(full_asm)

        assemble.main(output_asm, output)

    except tokenizer.TokenizerException as e:
        report_error(str(e), e.line, e.pos, lines)
        exit(1)
    except ParserException as e:
        report_error(str(e), e.loc.line, e.loc.pos, lines)
        exit(1)
    except NodeException as e:
        report_error(str(e), e.loc.line, e.loc.pos, lines)
        exit(1)
    except OSError as e:
        print(f"Error opening input file: {e}", file=sys.stderr)
        exit(1)

def report_error(message, line, pos, lines):
    print("", file=sys.stderr)
    print(lines[line - 1], file=sys.stderr)
    indent = re.sub("[^\t]", " ", lines[line - 1][0:pos])
    print(indent + "^", file=sys.stderr)
    print(f"Error: {message}", file=sys.stderr)
    print("", file=sys.stderr)

if (__name__ == "__main__"):
    if (len(sys.argv) >= 3):
        compile(sys.argv[1:-1], sys.argv[-1])
    else:
        print(f"Usage: {sys.argv[0]} <c1s file> [<c1s file> [<c1s file> [...]]]  <output strat file>]", file=sys.stderr)
