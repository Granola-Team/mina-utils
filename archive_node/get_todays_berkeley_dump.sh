# mina-archive-dumps/berkeley-archive-dump-2023-02-21_0000.sql.tar.gz
_date=$(date -I)
gsutil cp -n "gs://mina-archive-dumps/berkeley-archive-dump-${_date}*.sql.tar.gz" .
