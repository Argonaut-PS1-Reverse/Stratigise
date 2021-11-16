# ASL Strategy Dissassembler

This is a proof of concept/WIP dissassembler meant to aid in understanding what strats are doing. It cannot reassemble strats at the moment and isn't meant for serious use.

This is mainly meant for the Croc games' strats, but maybe it will be helpful with strats from other games, too. The only game it is known for sure not to work with is the PSX demo of Croc 1 since the instruction sizes are different between versions.

## Usage

To disassemble a single strat, put it as `decompile.py`'s first argument:

```zsh
$ ./decompile.py /path/to/the/STRAT.BIN
```

It will output a file with the original name plus the `.DIS` extension.

Advnaced usage:

```
decompile.py optable=OPTABLE1 file1 file2 ... optable=OPTABLE2 file3 file4 ...
```

## Adding Opcodes

You can add opcodes in the `opcodes.py` file, which is just a dictionary of opcodes. The opcodes are in big endian for convinence purposes, so they look the same as they do in the file. This could change in the future, but for now it works.

The format of opcode entries is simple:

```py
	opcode: [opname, argtypes ...],
```

Where the valid argument types are `string`, `eval`, `int32` and `int16` at time of writing.

## To-do

Aside from figuring out all of the opcodes and the file format of the strat files:

 * Reverse engineer opcode arguments and fill in the rest of the opcode list.
 * Cleaner parsing and an actual intermediate representation (useful for adding labels and processing things in general).
 * Re-assembling dissassembled files
 * Reimplement in C, once the bytecode format is mostly known.

## More Info

Make sure to read things in the `doc` folder if you want to know more. You can also read more info about strats on [my modding notes](https://gist.github.com/knot126/bb80efbc838972e8e477ed7eaabdb221#stratigies-script-information), which also links to other helpful resources when possible.
