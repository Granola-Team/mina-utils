#!/usr/bin/env sh

# Download today's Berkeley archive dump

_date=$(date -I)

echo "Downloading today's Berkeley dump (${_date})"

dumps=""

for item in *; do
  if [[ -d $item ]]; then
    if [[ $item == "berkeley_dumps" ]]; then
      dumps+=0;
      break;
    fi
  fi
done

if [[ $dumps == "" ]]; then
  mkdir berkeley_dumps;
fi

cd berkeley_dumps

gsutil cp -n "gs://mina-archive-dumps/berkeley-archive-dump-${_date}*.sql.tar.gz" .

sh unzip_todays_berkeley_dumps.sh

cd ..
