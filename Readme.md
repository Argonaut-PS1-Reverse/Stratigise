# Stratigise: Argonaut Strategy Language Reverse Engineering and Tools

This is a work-in-progress assembler and dissassembler meant to aid in understanding what strats are doing in games created by Argonaut Games. There is a general bias towards the first *Croc: Legend of the Gobbos*, but we welcome contributions that benefit any game.

It is not currently meant for serious use.

Argonaut PSX reversing Discord: [![Discord](https://img.shields.io/discord/1013732315186335764?label=Join%20our%20Discord%20%21&logo=discord)](https://discord.gg/feMkSQeFms)

## Disclaimer(s)

> **Warning**: This project does not always produce vaild disassemblies at time of writing. If you see `CommandError`, `__unknown_operation_0x`[...] or anything suspicous, that means something went wrong and you can't trust anything written after or slightly before that instruction.

> **Note**: Our reassembler is currently only designed to handle Croc 1 and is in general quite messy code. In fact, the entire project is quite messy.

## Usage

To disassemble a single strat, put it as `decompile.py`'s first argument:

```zsh
$ ./disassemble.py path/to/the/STRAT.BIN
```

It will output two files with the original name plus the `.DIS` and `.AXX` extensions.

To reassemble a strat, use assemble with the first argument as the original strat name (witohut `.BIN`) and the second as the output bin file name:

```zsh
$ ./assemble.py path/to/the/INPUT.BIN path/to/the/OUTPUT.BIN
```

### Example

There are some examples strats from Croc DE in the `strats` folder:

```
$ ./disassemble.py strats/croc-de130/CROC.BIN
Processing "strats/croc-de130/CROC.BIN" with spec "croc1" ⋅⋅⋅
```

Part of the example output:

```c
Label_b55:
	TurnRight { PushExternGlobal 10 ReturnTop }
	If { GetAVar 12 PushInt32 8 BitAnd ReturnTop } Label_ba9
	If { PushExternGlobal 10 PushInt32 747110 CmpTopGreater ReturnTop } Label_b80
	LetXGVar 10 { PushInt32 747110 ReturnTop }
	Else Label_ba6

Label_b80:
	If { PushExternGlobal 10 PushInt32 2621440 CmpTopGreater ReturnTop } Label_b9d
	LetXGVar 10 { PushExternGlobal 10 PushInt32 85196 Divide ReturnTop }
	Else Label_ba6

Label_b9d:
	LetXGVar 10 { PushInt32 2621440 ReturnTop }

Label_ba6:
	Else Label_bca

Label_ba9:
	If { PushExternGlobal 10 PushInt32 229376 CmpTopLess ReturnTop } Label_bc6
	LetXGVar 10 { PushExternGlobal 10 PushInt32 6553 Divide ReturnTop }
	Else Label_bca

Label_bc6:
	LetXGVar 10 { ReturnZero }

Label_bca:
	EndProc
	
```

### Advanced usage

You can pass in multipule files and use `--spec` to set the disassembler:

```
disassemble.py --spec gamename1 file1 file2 ... --spec gamename2 file1 file2 ...
```

## Todo

### Documentation

 * Reverse engineer opcode arguments and fill in the rest of the opcode list (close to done)
 * Also, `stEvaluate` (good progress)
 * Documenting other strat functions/the C API would be a good idea too

### Disassembler

 * Cleaner parsing and an actual intermediate representation
 * Re-assembling dissassembled files
 * Clean implementation, possibly in C

### Assembler

 * Make it more generic, currently only doing Croc 1 properly

## More Info

Make sure to read things in the `doc` folder if you want to know more.

You can also read more info about strats on [my modding notes](https://gist.github.com/knot126/bb80efbc838972e8e477ed7eaabdb221#stratigies-script-information), which also links to other resources.
