# Adding opcodes

You can add opcodes in the `specs/<game name>.py` file, which is a dictionary of opcodes with a few special, game-specific decompilation functions.

The format of opcode entries is simple:

```py
	opcode: [opname, argtypes ...],
```

Where the valid argument types are `string`, `eval`, `int32`, `int16` and `int8` at time of writing.

In the future, an `addr` type may be used to indicate that a type is an address in the strat.
