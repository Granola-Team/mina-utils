#!/usr/bin/env sh

mina-archive run \
  --postgres-uri postgres://localhost:5432/archive \
  --server-port 3086
