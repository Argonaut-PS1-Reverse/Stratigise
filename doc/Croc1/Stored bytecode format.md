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
| (4) `0x06`   | `0x02`   | Unknown                  | Offset into the file of a different type of data, though not clear what it is. |
| =            | `0x08`   | | |

## Bytecodes

The bytecodes are stored as one would expect. Each opcode is a single byte, followed by arguments and data for that opcode. For example:

```
3A 13 01 00 00 00 00
```

Is interpreted as `SetModel lookupStratId(0)`. The `SetModel` is `3A`; the opcode for `stSetModel`. Then, the argument follow. `SetModel` has a signle argument that uses `stEvaluate` to read a long integer (`int32_t`) and get another integer based on that, which is the way that the bytecode loads arbitrary values.

You can find this example right at the start of `CROC.BIN`.

To see a list of opcodes throughout various versions of *Croc: Legend of the Gobbos*, see [Opcodes.md](Opcodes.md).

## Loading

Strats are loaded in `SolveAllStrats` and `PreLoadStrats` in the PSX EU demo.

Once you have function names, search for `FCRead(void *buffer, size_t size)` on PSX and for `BrFileRead(void *buffer, size_t size, int count, void *file)` on PC, then see the incoming function calls. Some will be for strat loading. (Tip: This is also a good way to see how exactly any file format loads into the game.)

## Todo

 * Find out how exactly script variables are allocated. [See here](https://discord.com/channels/313375426112389123/416998863467970583/801521013547597885) for some info.
 * `lookupStratId` is just an assumption based on what I saw. Do more research!
