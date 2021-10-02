# Stored bytecode format

This document attempts to note the format of the compiled bytecode files in Croc 1.

## The stored bytecode format

The format as the bytecode is (seemingly) simple. There is a strat header, then each opcode is stored in {four byte integers}(Croc DE) {single-byte integers}(EU PSX Demo) followed by its arguments.

The strat header is:

| Offset   | Size     | Purpose    | Description |
| -------- | -------- | ---------- | ----------- |
| `0x00`   | `0x04`   | `size`     | The size of the strat stream, minus the header size. |
| `0x04`   | `0x04`   | Unknown    | ??? |
| =        | `0x08`   | | |

**TODO**:

 * Find out how exactly script variables are allocated. [See here](https://discord.com/channels/313375426112389123/416998863467970583/801521013547597885) for some info.
 * There might be a footer, but I have not found it yet.
