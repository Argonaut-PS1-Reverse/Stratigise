# ASL Strategy Dissassembler

This is a proof of concept/WIP dissassembler meant to aid in understanding what strats are doing. It cannot reassemble strats at the moment and isn't meant for serious use.

This is mainly meant for Croc 1 strats, but maybe it will be helpful with other formats, too.

## Adding Opcodes

You can add opcodes in the `opcodes.py` file, which is just a dicionary of opcodes. The opcodes are in big endian for convinence purposes, so they look the same as they do in the file. This could change in the future, but for now it works.

The format of opcode entries is simple:

```py
	opcode: [opname, argtypes ...],
```

Where the valid argument types are `string` and `int32` at time of writing.

## To-do

Aside from figuring out all of the opcodes and the file format of the strat files:

 * Cleaner parsing and an actual intermediate representation (useful for adding labels and processing things in general)
