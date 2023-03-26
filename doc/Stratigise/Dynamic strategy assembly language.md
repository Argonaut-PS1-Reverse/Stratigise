# Dynamic strategy assembly language

The documents the grammar of the **DSAL** (**D**ynamic **S**trategy **A**ssembly **L**anguage) that the disassembler produces.

## Notation

* `(A)*`: Match zero or more of `A`
* `(A)?`: Match zero or one of `A`
* `A | B`: Match `A` or match `B`
* `A ! B`: Match things in `A` if they are not in `B`
* `A B`: Match `A` followed by `B`
* `A[const: explain]`: Match a specific number of things based on an external specification

This is not a 100% working grammar but should give you an idea of what is happening.

## Lexical grammar

```c
CHAR      -> [anything]
DIGIT     -> [0-9]
ALPHA     -> [a-z] | [A-Z]
IDENTCHR  -> DIGIT | ALPHA | '_'
SPACE     -> ' ' | '\n' | '\r' | '\t'
USED      -> '@' | ':' | '{' | '}'

Symbol    -> ALPHA (IDENTCHR)*
String    -> '"' (CHAR)* '"'
Number    -> DIGIT (DIGIT)*
```

## Grammar 

```c
program   -> (line)*
line      -> (instr | attr | label)
instr     -> Symbol (params)[const: number of params to instruction]
             // The number and what things to match is based on the spec loaded and the specific symbol at instr
params    -> Symbol | Number | String | eval
eval      -> '{' evalinstr (evalinstr)* '}'
evalinstr -> Symbol (evalprm)[const: number of params to eval instruction]
evalprm   -> Number | String | Symbol
attr      -> '@' Symbol (Number | String)
label     -> Symbol ':'
```
