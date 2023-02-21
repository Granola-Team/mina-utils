#!/usr/bin/env sh

# Download today's Mainnet archive dump

dumps=""

for item in *; do
  if [[ -d $item ]]; then
    if [[ $item == "mainnet_dumps" ]]; then
      dumps+=$item;
      break;
    fi
  fi
done

if [[ $dumps == "" ]]; then
  mkdir mainnet_dumps;
fi

cd mainnet_dumps

_date=$(date -I)
gsutil cp -n "gs://mina-archive-dumps/mainnet-archive-dump-${_date}*.sql.tar.gz" .

cd ..
