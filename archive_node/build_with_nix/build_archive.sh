#!/usr/bin/env sh

# Run from the Mina project root after
# installing nix and setting up mina in the registry

# start nix dev shell for mina
nix develop mina

# build mina.exe
dune build src/app/cli/src/mina.exe

# build archive.exe
dune build src/app/archive/archive.exe
