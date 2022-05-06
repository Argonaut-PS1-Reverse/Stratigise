**Update 2022-05-06**

The source code for Croc: Legend of the Gobbos *could* (not *will*) be released soon, coming after BRender's open-sourcing on 3 May 2022, which contains the full strat interpreter (and presumably build toolchain) for Croc 1! If so, the disassembler will stop development (since it would be pointless) and I will look more at documenting the strat code, if it's not already been done well.

For more info and probably an annoucement if or when it is available, check [Croc discord](https://discord.gg/JtrPB3F).

Probable links to source code for [Definitive Edition](https://croc.epiclper.com) once available: [BRender (DE)](https://github.com/crocguy0688/CrocDE-BRender) | [Game code (DE)](https://github.com/crocguy0688/Croc) | [Data (DE)](https://github.com/crocguy0688/CrocData)

[Screenshot of first lines of stEvaluate](https://cdn.discordapp.com/attachments/347524018334859265/971494443968503878/unknown.png)

# ASL Strategy Dissassembler

**Important**: This project *does not* produce vaild disassemblies at time of writing.

This is a proof of concept/WIP dissassembler meant to aid in understanding what strats are doing. It cannot reassemble strats at the moment and isn't meant for serious use.

This is mainly meant for *Croc: Legend of the Gobbos* and *Croc 2*, but it may be helpful with strats from other games, too.

## Usage

To disassemble a single strat, put it as `decompile.py`'s first argument:

```zsh
$ ./decompile.py /path/to/the/STRAT.BIN
```

It will output a file with the original name plus the `.DIS` extension.

Advnaced usage:

```
decompile.py --spec gamename1 file1 file2 ... --spec gamename2 file1 file2 ...
```

## Todo

### Documentation

 * Reverse engineer opcode arguments and fill in the rest of the opcode list
 * Also, stEvaluate
 * Documenting other strat functions/the C API would be a good idea too

### Disassembler

 * Cleaner parsing and an actual intermediate representation
 * Labels 
 * Re-assembling dissassembled files
 * Reimplement in C, once the bytecode format is mostly known

## More Info

Make sure to read things in the `doc` folder if you want to know more.

You can also read more info about strats on [my modding notes](https://gist.github.com/knot126/bb80efbc838972e8e477ed7eaabdb221#stratigies-script-information), which also links to other resources.
