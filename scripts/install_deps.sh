#!/usr/bin/env sh

# set up stable package repos
echo "deb [trusted=yes] http://packages.o1test.net $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/mina.list
sudo apt-get update
sudo apt-get install --yes apt-transport-https

# install mina-mainnet
sudo apt-get install -y curl unzip mina-mainnet

# install mina-generate-keypair
sudo apt-get install mina-generate-keypair
