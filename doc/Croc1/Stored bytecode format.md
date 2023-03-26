# Stored bytecode format

This document attempts to note the format of the compiled bytecode files in Croc 1.

The format as the bytecode is (seemingly) simple. There is a strat header, then each opcode is stored in a single byte followed by its arguments.

## Header

The strat header is:

| #   | Offset       | Size     | Purpose                   | Description and Notes |
| --- | ------------ | -------- | ------------------------- | --------------------- |
| 1   | `0x00`   | `0x04`   | `size` (`= FileSize - 8`) | The size of the strat stream, minus the header size. |
| 2   | `0x04`   | `0x02`   | `entry_point`             | The entry point, relative to 0x4 offset in the binary.<sup>1</sup> |
| 3   | `0x06`   | `0x02`   | `audio_base_pointer`      | Absolute position in the file to the start of the audio data, minus four; alternately, relative position to audio data plus two |
|     | =            | `0x08`   | | |

1. This only applies in some cases. If `stAddStrategy::base_memory /* param_2 */ == NULL`, then it is loaded from somewhere around `WADS/EXCLUDES.WAD`<sub>(PSX)</sub> or (not currently known)<sub>(PC/Croc DE)</sub>.

## Instructions

Bytecodes for the instructions are stored as one would expect. Each opcode is a single byte, followed by arguments for that instruction. For example:

```
15 04 01 00 00 00 12 04 00
```

Is interpreted as `if (1) { goto (ip + 4); }`. The `If` is `15`; the opcode for `stIf`. Then, the arguments follow. `If` has a two arguments: one uses `stEvaluate` to read an arbitrary value which will be tested against, and a 16-bit little endian integer that will be used as an offset.

| Part    | Byte(s)       | Meaning                                              |
| ------- | ------------- | ---------------------------------------------------- |
| Opcode  | `15`          | `stIf` opcode                                        |
|         |               | Expect: &lt;eval statement&gt; &lt;offset&gt;        |
| Eval    | `04`          | Push number to the top of the eval stack             |
| Eval    | `01 00 00 00` | Number to push                                       |
| Eval    | `12`          | Return the value on the top of the stack             |
| Offset  | `04 00`       | Offset to jump to                                    |

To see a list of opcodes throughout various versions of *Croc: Legend of the Gobbos*, see [Opcodes.md](Opcodes.md).

## Loading

Strats are loaded in `SolveAllStrats` and `PreLoadStrats` in the PSX EU demo.

Once you have function names, search for `FCRead(void *buffer, size_t size)` on PSX and for `BrFileRead(void *buffer, size_t size, int count, void *file)` on PC, then see the incoming function calls. Some will be for strat loading. (Tip: This is also a good way to see how exactly any file format loads into the game.)

## Further reading

 * [stEvaluate documentation](stEvaluate.md) - For evaluate bytecode

## Todo

 * Find out how exactly script variables are allocated. [See here](https://discord.com/channels/313375426112389123/416998863467970583/801521013547597885) for some info.
