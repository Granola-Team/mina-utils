# General Linux Commands

## Firewall

Current firewall status

```sh
sudo ufw status
```

Allow/limit traffic on a port (make a `rule`)

```sh
# by name
sudo ufw allow https
sudo ufw limit https

# by port number
sudo ufw allow 8302/tcp
sudo ufw limit 8302/tcp
```

Delete a rule

```sh
# by name
sudo ufw delete allow https
sudo ufw delete limit https

# by port number
sudo ufw delete allow 8302/tcp
sudo ufw delete limit 8302/tcp
```

Mina node uses

```
8302/tcp
3085/tcp
```

## Services

Show status of all services

```sh
# less detail
service --status-all

# more detail
systemctl --user status
```

[Start](../scripts/mina_start.sh) a `mina` node instance

```sh
systemctl --user daemon-reload
systemctl --user start mina
systemctl --user enable mina
sudo loginctl enable-linger
mina daemon --peer-list-url https://storage.googleapis.com/mina-seed-lists/mainnet_seeds.txt
```

Read the logs

```sh
sudo journalctl --user -u mina -n 1000 -f
journalctl --user-unit mina -n 1000 -f
```

## PostgreSQL

TODO
