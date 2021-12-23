# Stored bytecode format

This document attempts to note the format of the compiled bytecode files in Croc 1.

The format as the bytecode is (seemingly) simple. There is a strat header, then each opcode is stored in a single byte followed by its arguments.

## Header

The strat header is:

| Offset       | Size     | Purpose                  | Description and Notes |
| ------------ | -------- | ------------------------ | --------------------- |
| (1) `0x00`   | `0x04`   | `size`                   | The size of the strat stream, minus the header size. |
| (2) `0x04`   | `0x01`   | `audio_base_pointer`     | Pointer to start of audio data. |
| (3) `0x05`   | `0x01`   | Unknown                  | Always seems to be zero. |
| (4) `0x06`   | `0x02`   | Unknown                  | Offset into the file of a different type of data, though not clear what it is; usually to these are the last few bytes of the file. |
| =            | `0x08`   | | |

## Instructions

Bytecodes for the instructions are stored as one would expect. Each opcode is a single byte, followed by arguments for that instruction. For example:

```
15 04 01 00 00 00 12 04 00
```

Is interpreted as `if (1) { goto (ip + 4); }`. The `If` is `15`; the opcode for `stIf`. Then, the arguments follow. `If` has a two arguments: one uses `stEvaluate` to read an arbitrary value which will be tested against, and a 16-bit little endian integer that will be used as an offset.

| Byte(s)       | Meaning                                              |
| ------------- | ---------------------------------------------------- |


To see a list of opcodes throughout various versions of *Croc: Legend of the Gobbos*, see [Opcodes.md](Opcodes.md).

## Loading

Strats are loaded in `SolveAllStrats` and `PreLoadStrats` in the PSX EU demo.

Once you have function names, search for `FCRead(void *buffer, size_t size)` on PSX and for `BrFileRead(void *buffer, size_t size, int count, void *file)` on PC, then see the incoming function calls. Some will be for strat loading. (Tip: This is also a good way to see how exactly any file format loads into the game.)

## Further reading

 * [stEvaluate documentation](stEvaluate.md) - For evaluate bytecode

## Todo

 * Find out how exactly script variables are allocated. [See here](https://discord.com/channels/313375426112389123/416998863467970583/801521013547597885) for some info.
