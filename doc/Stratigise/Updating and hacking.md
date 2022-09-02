# Updating and hacking on Stratigise

Most of the core of Stratigise lives in [`/stratigise`](../../stratigise), and the disassembler core is in [`/stratigise/disassembler.py`](../../stratigise/disassembler.py). These are probably what need to be modified if there are non-bytecode related changes that need to be made, like feature additions.

Bytecode and game-specific related changes are made for that game's bytecode format, which is specified in its file in [`/specs`](../../specs).

Stratigise is designed to seperate the process of specifying the bytecode to decompile and developing the decompiler as much as possible. For example, actual bytecode numbers are split into a seprate file and treated as data. Keep this in mind when adding a feature.

## Style

* Please use `camelCase` for consistency.
