#!/usr/bin/env sh

# Download today's Berkeley archive dump

dumps=""

for item in *; do
  if [[ -d $item ]]; then
    if [[ $item == "berkeley_dumps" ]]; then
      dumps+=$item;
      break;
    fi
  fi
done

if [[ $dumps == "" ]]; then
  mkdir berkeley_dumps;
fi

cd berkeley_dumps

_date=$(date -I)
gsutil cp -n "gs://mina-archive-dumps/berkeley-archive-dump-${_date}*.sql.tar.gz" .

cd ..
