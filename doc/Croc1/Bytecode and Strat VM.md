# Bytecode and the strategy VM

This document attempts to document the bytecode and virtual machine/interpreter used to run it. Currently, it only contains information that seems to be accurate.

## The bytecode format

The format as the bytecode is (seemingly) simple. There is a strat header, then each opcode is stored in four byte integers followed by its arguments, which are usually either `NUL`-terminated strings or 32-bit integers. Nothing needs to be properly aligned.

The strat header is:

| Offset   | Size     | Purpose    | Description |
| -------- | -------- | ---------- | ----------- |
| `0x00`   | `0x04`   | `size`     | The size of the strat stream, minus the header size. |
| `0x04`   | `0x04`   | Unknown    | ??? |
| =        | `0x08`   | | |

**TODO**:

 * Find out how exactly script variables are allocated. [See here](https://discord.com/channels/313375426112389123/416998863467970583/801521013547597885) for some info.
 * There might be a footer, but I have not found it yet.

## The virtual machine and running scripts

The virtual machine (what runs the scripts) is stacked based, so values are pushed onto a stack, an operation is called and then the operation pops the operands off of the stack and pushes the result.

For example:

```asm
push 4      ; push 4 onto stack - the stack is [ 4 ]
push 10     ; push 10 onto stack - the stack is [ 4, 10 ]
push 2      ; push 2 onto stack - the stack is [ 4, 10, 2 ]
mul         ; pop last two and multiply, then push result - the stack is [ 4, 20 ]
add         ; pop last two and add, then push result - the stack is [ 24 ]
```
