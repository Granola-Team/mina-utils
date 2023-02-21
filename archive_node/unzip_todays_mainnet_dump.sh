#!/usr/bin/env sh

# Unzip today's Mainnet archive dump

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

_date=$(date -I)
pattern="mainnet-archive-dump-${_date}_*.sql.tar.gz"

found=""

for item in *; do
  if [[ $item == $pattern ]]; then
    gzip -d $item;
    echo "Unzipped ${item}";
    found+=0;
  fi
done

if [[ $found == "" ]]; then
  echo "Have you gotten today's Mainnet dump?";
  echo "Maybe try: sh get_todays_mainnet_dump.sh";
else
  echo "Success!";
fi

cd ..
