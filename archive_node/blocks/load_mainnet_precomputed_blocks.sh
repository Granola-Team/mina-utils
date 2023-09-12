#!/usr/bin/env sh

# Load db with precomputed blocks from ./mainnet
# 
# This requires a running archive process, postgres process
# This must be run from the root of the mina repo after
# building src/app/archive_blocks/archive_blocks.exe, see ./build.sh

ARCHIVE_BLOCKS=_build/default/src/app/archive_blocks/archive_blocks.exe
POSTGRES_URI=postgres://postgres:password@localhost:5432/archive

echo "Loading precomputed blocks with --archive-uri"
echo ${POSTGRES_URI}

find ./mainnet -name "*.json" | xargs -I \
  % ${ARCHIVE_BLOCKS} \
    --precomputed \
  % --archive-uri ${POSTGRES_URI} \
    --log-successful false \
    --successful-files success.txt \
    --failed-files failed.txt
