# rev-tape

`ass.py` is the assembler, give it an input file and output file name and it will assemble into belt machinecode.

The `belt` directory holds the Rust VM. Just give it the file containing the belt machine code.

`./run.sh` is a script to assemble and run a `.blt` belt assembly file.

For example

```sh
./run.sh chal.blt
```

`make_flag_check.py` is a script to make `chal.blt`.

The actual challenge flag checker reads in N bytes from the input (equal to the flag length) and xors them with a 9 byte key found in `make_flag_checker.py`.
