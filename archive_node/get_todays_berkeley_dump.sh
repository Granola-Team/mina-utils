# Download today's Berkeley archive dump

dumps=""

for item in *; do
  if [[ -d $item ]]; then
    if [[ $item == "dumps" ]]; then
      dumps+=0;
      break;
    fi
  fi
done

if [[ $dumps == "" ]]; then
  mkdir ./dumps;
fi

cd dumps

_date=$(date -I)
gsutil cp -n "gs://mina-archive-dumps/berkeley-archive-dump-${_date}*.sql.tar.gz" .

cd ..
