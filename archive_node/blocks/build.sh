#!/usr/bin/env sh

# Build all the necessary apps for running an archive node

# set your dune profile
DUNE_PROFILE=mainnet

dune build --profile=${DUNE_PROFILE} \
  src/app/cli/src/mina.exe \
  src/app/archive/archive.exe \
  src/app/archive_blocks/archive_blocks.exe \
  src/app/missing_blocks_auditor/missing_blocks_auditor.exe \
  src/app/extract_blocks/extract_blocks.exe \
  src/app/replayer/replayer.exe
