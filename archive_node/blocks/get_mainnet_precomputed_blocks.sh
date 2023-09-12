#!/usr/bin/env sh

echo "Downloading Mainnet precomputed blocks"

blocks=""

for item in *; do
  if [[ -d $item ]]; then
    if [[ $item == "mainnet" ]]; then
      blocks+=0;
      break;
    fi
  fi
done

if [[ $blocks == "" ]]; then
  mkdir mainnet;
fi

cd mainnet

gsutil -m cp -n "gs://mina_network_block_data/mainnet-*.json" .

sh load_mainnet_precomputed_blocks.sh

cd ..
