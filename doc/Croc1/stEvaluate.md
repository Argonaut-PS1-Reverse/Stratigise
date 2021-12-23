# stEvaluate

## What is it?

`stEvaluate` is a way for an instruction to evaluate a value without being fixed to using a specific variable, constant or type. It dynamically *evaluates* a value, returning the value that results in the end.

It functions like its own bytecode interpreter. When an instruction calls `stEvaluate`, it will read *evaluate instructions* from the instruction stream, telling `stEvaluate` where to find the value that is wanted. This value could be stored as a constant, in local variable for the script, a global for the game or even something else.

Essentially, it is a bytecode interpeter in a bytecode interpreter that loads an arbitrary value. If you know how python pickle works, think of it like that but for a game.

## Further reading

 * [`stratigise.uneval` Module](../stratigise/uneval.py) with inline documentation about some opcodes
 * [Croc & Stuff discord](https://discord.gg/JtrPB3F) - Some Croc 2 strat info that also applies to Croc 1 is here

## Todo

 * Basically everything
