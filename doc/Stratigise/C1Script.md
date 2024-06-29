# C1Script language

> Warning! The language design is still WIP, do not rely too much on its current syntax!

This document contains the description of C1S language for writing Croc 1 strats

## Values

The following values are supported:

```python
16 # integer
16.000046 # decimal value
0xf2b # hex integer
raw(26) # raw integer value (will not be multiplied by 0x10000 internally)
"aaaaa" # string
```

When values are combined into expressions, the result value will be calculated
at the compile time.

## Constants

Constants are the identifiers with values calculated at the compile time. They
have to be declared globally the following way:

```javascript
const MY_CONST = 4
const MY_CONST2 = 4 + 8 / MY_CONST
const MY_STRING = "aaaa"
const MY_STRING2 = "bbbbbb" + MY_STRING
```

These constants can be then passed to any command where a static int/string value is expected.

## Variables

In Croc 1 the variables are located in several arrays for different purposes. All
these variables are 32-bit values interpreted as 16x16 floats or integers depending
on the context. In C1S the integer values are treated as floats (multiplied by 2^16)
by default unless you wrap them in `raw()`.

There are multiple ways of declaring variable.

### Explicit allocations

You can declare variable explicitly specifying its location:

```javascript
use vars[3] as my_g_var
use pg_vars[2] as my_pg_var
use alien_vars[1] as alien_var
use params[2] as my_param
use xg_vars[5] as my_xg_var
use x_params[3] as my_x_param
```

This is useful when you need to refer to this variable from another strat or
specifying a parameter passed from the map file.

The C1S decompiler always preserves the locations of the variables by specifying
explicit allocations

### Global variables

```javascript
global my_var
```

When declared globally the variable will be allocated at the first available
slot in `params` array or `g_vars` if there are no available params.

### Local variables

```javascript
my_local_var = 25
```

When there is an assignment to an unknown identifier it is treated as a local
variable declaration. Redefinition of identifiers in nested blocks isn't supported.

The variable is allocated at the first available `params`/`g_vars` slot once
per declaration. Be aware of this behavior! There is no stack for local variables
so there can be problems with recursion.

## Sections

### Procedures

You can turn a reusable chunk of code into a procedure:

```javascript
proc myProc {
    hide()
    collisionOff(1)
    playSound(2, param3, 40)
}
```

Then you can call it from anywhere:

```javascript
myProc()
```

The procedures don't support parameters and don't return values.

### Triggers

You can define a trigger handler:

```javascript
trigger onTrigger {
    if (!xg_var1) {
        stopAnim()
        g_var9 = 0
    }
}
```

And then use it:

```javascript
createTrigger(2, 1, onTrigger)
```

### Strats

The entry point of a strat:

```javascript
strat DantiniWalk {
    setModel(loadObject("DT01.MOD"))
    anim1 = loadAnim("DT01-01.ANI")
    anim2 = loadAnim("DT01-02.ANI")
    ...
}
```

The strat execution begins there. When the block finishes, the strat is removed.
You can interrupt the execution by calling `remove()` from anywhere.

## Statements

### Commands

The commands are called in a proc-like way:

```javascript
turnTowardWaypointY(64)
spawn(5, "FootPrint", -0.02, 0.5, 0, 40)
playSound(4, param7, 25, -2, 1)
setModel(loadObject("DT01.MOD"))
```

The arguments can be expressions or constant expressions depending on the command.
There is a command for basically every opcode in Croc 1 except jumps, loops, var getter/setters and `End*` ops.

### Conditions

The following conditional statements are supported:

```javascript
if (condition) {
    ...
}

if (condition) {
    ...
}
else {
    ...
}

if (condition) {
    ...
}
else if (another_condition) {
    ...
}
else {
    ...
}
```

### Switch

```javascript
switch (expr) {
    case (value1) {
        ...
    }
    case (value2) {

    }
    default {
        ...
    }
}
```

### Loops

There are three loop statements and they are executed concurrently (one iteration per
cycle) unless the `immediately` keyword is specified.

```javascript
while (condition) immediately {
    ...
}

repeat immediately {
    ...
} until (condition)

for x from 1 to 10 immediately {
    ...
}
```

## Expressions

Youc can write math expressions with the following operators and some of `stEvaluate`
functions:

```javascript
g_var2 * sin(27 + a_bar2)
!((a_var0 > g_var12 + 0.006 or a_var0 < g_var12 - 0.006) and g_var8 == 1)
bitAnd(g_var2 >> 2, 1)
"aaa" + "bbb" + CONST_STRING
checkAnimFlag32(loadAsset2("CROC_CLD.ANI"), raw(8))
```

### Operators precedence

| Operators            |
| -------------------- |
| +, -, ! (unary)      |
| *, /                 |
| +, -                 |
| >>, <<               |
| ==, !=, >, <, >=, <= |
| &                    |
| |                    |
| and                  |
| or                   |

### Assignments

The following assignment operators are supported:

```javascript
g_var2 = g_var6
a_var2 += 1
pg_var2 -= 2
xg_var *= 2
param1 /= 2
```
