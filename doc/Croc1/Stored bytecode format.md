# Stored bytecode format

This document attempts to note the format of the compiled bytecode files in Croc 1.

The format as the bytecode is (seemingly) simple. There is a strat header, then each opcode is stored in a single byte followed by its arguments.

## Header

The strat header is:

| Offset       | Size     | Purpose    | Description and Notes |
| ------------ | -------- | ---------- | --------------------- |
| (1) `0x00`   | `0x04`   | `size`     | The size of the strat stream, minus the header size. |
| (2) `0x04`   | `0x04`   | Unknown    | The Blue Page says its a `uint8_t *` but it also seems like it could be two `uint16_t`s? |
| =            | `0x08`   | | |

### Speculation on (2)

For (2) to be an in-file `uint8_t *` (offset) like the blue page says, it would have to be within the range of the first value. However, looking at the start for Croc shows that this is not the case:

```
A6 3C 00 00   04 00 C4 3A
```

The second number has to be larger than the first, regardless of endianess, so it cannot be an offset into the file. It also seems like strats always start execution from the first instruction, so it wouldn't really have an intuitive purpose even if it were. It seems that this is more likely flags for the strat.

## Bytecodes

The bytecodes are stored as one would expect. Each opcode is a single byte, followed by arguments and data for that opcode. For example:

```
3A 13 01 00 00 00 00
```

Is interpreted as `SetModel lookupStratId(0)`. The `SetModel` is `3A`; the opcode for `stSetModel`. Then, the argument follow. `SetModel` has a signle argument that uses `stEvaluate` to read a long integer (`int32_t`) and get another integer based on that, which is the way that the bytecode loads arbitrary values.

You can find this example right at the start of `CROC.BIN`.

To see a list of opcodes throughout various versions of *Croc: Legend of the Gobbos*, see [Opcodes.md](Opcodes.md).

## Todo

 * Find out how exactly script variables are allocated. [See here](https://discord.com/channels/313375426112389123/416998863467970583/801521013547597885) for some info.
 * `lookupStratId` is just an assumption based on what I saw. Do more research!
