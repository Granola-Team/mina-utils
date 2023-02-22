#!/usr/bin/env bash

# Run from the Mina project root

# 1. install nix
# 2. set up mina in nix registry

# start nix dev shell for mina
nix develop mina

# build
echo "Building Mina daemon..."
dune build src/app/cli/src/mina.exe

echo "Building archive process..."
dune build src/app/archive/archive.exe

DIR_NAME=$( dirname -- "${BASH_SOURCE[0]}")
SCRIPT_DIR=$( cd -- $DIR_NAME &> /dev/null && pwd )

# suggest
echo "Success!";
echo "  To give friendlier names to the executables, do"
echo "  $ source ${SCRIPT_DIR}/.env";
