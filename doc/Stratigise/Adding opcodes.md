# Adding opcodes

You can add opcodes in the `specs/<game name>.py` file, which is a dictionary of opcodes with a few special, game-specific decompilation functions.

The format of opcode entries is simple:

```py
	opcode: [opname, argtypes ...],
```

## Argument types

Where the valid argument types are:

| Type | Size | Purpose |
| ---- | ---- | ------- |
| `string`| Until `NUL` byte | `NUL`-terminated string |
| `eval` | Variable | Used to decode stEvaluate immediate values (Croc 1 only) |
| `varargs` | Variable | Used to decode a variable number of args (Croc 1 only) |
| `offset16` | `0x2` | Relative address |
| `address16` | `0x2` | Literal/absolute address (adds `0x4` to value) |
| `int32` | `0x4` | Little-endian 32-bit integer |
| `int16` | `0x2` | Little-endian 16-bit integer |
| `int8` | `0x1` | 8-bit integer |
