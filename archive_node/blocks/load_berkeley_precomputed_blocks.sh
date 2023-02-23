#!/usr/bin/env sh

# Load db with precomputed blocks from ./berkeley

echo "Loading precomputed block with --archive-uri"
echo "postgres://postgres:password@localhost:5432/archive"

find ./berkeley -name "*.json" | xargs -I \
  % _build/default/src/app/archive_blocks/archive_blocks.exe \
    --precomputed \
  % --archive-uri postgres://postgres:password@localhost:5432/archive \
    --log-successful false \
    --successful-files success.txt \
    --failed-files failed.txt
