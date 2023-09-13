#!/usr/bin/env sh

systemctl --user daemon-reload
systemctl --user start mina
systemctl --user enable mina
sudo loginctl enable-linger
mina daemon --peer-list-url https://api.ipfsbrowser.com/ipfs/get.php?hash=QmVpGhL5qr56KFfSZPyivH9Zsx5ppNUREWH4RAuq3HeoSL
