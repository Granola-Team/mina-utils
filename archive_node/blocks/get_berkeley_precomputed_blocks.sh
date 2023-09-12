#!/usr/bin/env sh

echo "Downloading Berkeley precomputed blocks"

blocks=""

for item in *; do
  if [[ -d $item ]]; then
    if [[ $item == "berkeley" ]]; then
      blocks+=0;
      break;
    fi
  fi
done

if [[ $blocks == "" ]]; then
  mkdir berkeley;
fi

cd berkeley

gsutil -m cp -n "gs://mina_network_block_data/berkeley-*.json" .

sh load_berkeley_precomputed_blocks.sh

cd ..
