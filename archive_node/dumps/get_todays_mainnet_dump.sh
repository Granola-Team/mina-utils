#!/usr/bin/env sh

# Download today's Mainnet archive dump

_date=$(date -I)

echo "Downloading today's Mainnet dump (${_date})"

dumps=""

for item in *; do
  if [[ -d $item ]]; then
    if [[ $item == "mainnet_dumps" ]]; then
      dumps+=0;
      break;
    fi
  fi
done

if [[ $dumps == "" ]]; then
  mkdir mainnet_dumps;
fi

cd mainnet_dumps

gsutil cp -n "gs://mina-archive-dumps/mainnet-archive-dump-${_date}*.sql.tar.gz" .

sh unzip_todays_mainnet_dump.sh

cd ..
