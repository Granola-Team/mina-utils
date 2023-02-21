#!/usr/bin/env sh

# Unzip today's Berkeley archive dump

dumps=""

for item in *; do
  if [[ -d $item ]]; then
    if [[ $item == dumps ]]; then
      dumps+=0;
      break;
    fi
  fi
done

if [[ $dumps == "" ]]; then
  mkdir dumps;
fi

cd dumps

_date=$(date -I)
pattern="berkeley-archive-dump-${_date}_*.sql.tar.gz"

found=""

for item in *; do
  if [[ $item == $pattern ]]; then
    gzip -d $item;
    found=$item;
    break;
  fi
done

if [[ $found == "" ]]; then
  echo "Have you gotten today's Berkeley dump?";
  echo "Maybe try: sh get_todays_berkeley_dump.sh";
else
  echo "Success!";
  echo "Unzipped ${found}";
fi

cd ..
