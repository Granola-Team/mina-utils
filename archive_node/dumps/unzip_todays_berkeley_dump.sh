#!/usr/bin/env sh

# Unzip today's Berkeley archive dump

echo "Unzipping..."

_date=$(date -I)
pattern="berkeley-archive-dump-${_date}_*.sql.tar.gz"

found=""

for item in *; do
  if [[ $item == $pattern ]]; then
    gzip -d $item;
    echo "Unzipped ${item}";
    found+=0;
  fi
done

if [[ $found == "" ]]; then
  echo "Have you gotten today's Berkeley dump?";
  echo "Maybe try: sh get_todays_berkeley_dump.sh";
else
  echo "Success!";
fi
