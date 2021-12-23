# Adding opcodes

You can add opcodes in the `opcodes/<game name>.py` file, which is just a dictionary of opcodes.

The format of opcode entries is simple:

```py
	opcode: [opname, argtypes ...],
```

Where the valid argument types are `string`, `eval`, `int32`, `int16` and `int8` at time of writing.
