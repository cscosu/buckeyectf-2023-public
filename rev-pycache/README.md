# `rev-pycache`

So the idea is that when python imports a module,
it creates the __pycache__ folder with a compiled
(to python bytecode) version of the imported module.
The challenges revolves around deleteing some source
code and accidentily distributing the pycache folder.

Python versions < 3.11 and below can be compiled very well using [pydc](https://github.com/zrax/pycdc).
So we use python 3.13-dev so they have to disassemble
and read python bytecode, pretty fun.