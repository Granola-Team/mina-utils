#!/usr/bin/env sh

# download ipfs kubo
DOWNLOADS=${HOME}/Downloads
TAR_GZ=$DOWNLOADS/kubo_v0.17.0_linux-amd64.tar.gz

wget https://github.com/ipfs/kubo/releases/download/v0.17.0/kubo_v0.17.0_linux-amd64.tar.gz -O $TAR_GZ
wget https://github.com/ipfs/kubo/releases/download/v0.17.0/kubo_v0.17.0_linux-amd64.tar.gz.sha512 -O "${TAR_GZ}.sha512"

# check hashes and install on match
actual_hash=$(sha512sum "${TAR_GZ}")
expect_hash=$(cat "${TAR_GZ}.sha512")

read -a actual <<< $actual_hash
read -a expect <<< $expect_hash

if [ "${actual[0]}" != "${expect[0]}" ]; then
  echo "Error: mismatching hashes!!!";
  echo "Actual: ${actual[0]}";
  echo "Expect: ${expect[0]}";
  exit 1
else
  echo "Hashes match! Installing ipfs...";
  tar -xvf $TAR_GZ -C $DOWNLOADS;
  chmod +x "${HOME}/Downloads/kubo/install.sh"
  sudo sh "${HOME}/Downloads/kubo/install.sh"
fi
