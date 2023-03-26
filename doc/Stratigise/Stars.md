# STARS programming language

> Stars is just in the planning stage!

The idea of the **STARS** (**ST**rat **A**nalygous **R**ememberable **S**ystem &mdash; a horrid backronym) programming language is to give a general language for argonaut strategy languages that more closely resembles modern languages. Specifically, a Lua-like language would be very nice.

## Example

```lua
-- Note that there are only globals.
x = 1
y = 3
z = 2

function main()
  model = LoadModel("CROC.MOD")
  
  while (x <= 7) do
    Move(x, y, z)
    x = x + 2;
  end
  
  cowhile (true) { -- executes one loop every frame
    if (PAD_LEFT) then
      Turn(-1)
    elseif (PAD_RIGHT) then
      Turn(1)
    elseif (PAD_UP) then
      break
    end
  end
  
  EndLevel()
end

function bad_examples()
   h = Move(1, 1, -1) -- note that functions may complain when used as expressions
end

@raw(0x3b) -- EndFile
```
