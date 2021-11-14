# stEvaluate

You may notice a lot of speak about `eval`, `stEval` or `stEvaluate`. This is because it is used very often, and is probably the most complex and as-yet undocumented part of understanding strat bytecode.

## What is it?

`stEvaluate` is a way for an instruction to evaluate a value without being fixed to using a specific variable, constant or type. It dynamically *evaluates* a value, returning the value that results in the end.

It functions like its own bytecode interpreter. When an instruction calls `stEvaluate`, it will read *evaluate instructions* from the instruction stream, telling `stEvaluate` where to find the value that is wanted. This value could be stored as a constant, in local variable for the script, a global for the game or even something else.

Essentially, it is a bytecode interpeter in a bytecode interpreter that loads an arbitrary value. If you know how python pickle works, think of it like that but for a game.

## An example

Going back to the example from the [Stored bytecode format](Stored bytecode format.md) documentation:

```
3A 13 01 00 00 00 00
```

`3A` (`SetModel`) is just an opcode for the strat interpreter, and is not really relevant to this. When `SetModel` is run, it calls `stEvaluate` to get an integer that identifies that model (or something to that effect, I have not looked into it). `stEvaluate` will read the stream and return that.

The `13` is an evaluate instruction, which reads yet another byte. For `13`, that byte will determine the exact behavour of is returned, though it usually involves returning a `int32_t`. In this case, the byte is `01`, so it reads the next `int32_t` from the stream (`00 00 00 00`) and sends that to `SearchForEntry`, which does some magic and returns a value. That values is then given back to `stSetModel`, where it is able to use that value to set the model.

## Todo

 * Basically everything, since we have only started to RE `stEvaluate`.
