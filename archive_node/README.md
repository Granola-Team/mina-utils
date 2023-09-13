# mina-utils archive node blocks

This project contains helpful scripts and information related to running a Mina archive node.

However, there exists a much more robust utility for syncing your local Mina precomputed block collection nowadays, see [iggy](https://github.com/Granola-Team/iggy).

Scripts for archive node related activities

- downloading and unzipping today's archive dumps
- building archive tools
  - Berkeley & Mainnet
  - `mina`
  - `archive`
  - `archive-blocks`
  - `extract-blocks`
  - `missing-blocks-auditor`
  - `replayer`

## O1 Google Cloud Resources

- [Mina network block data](https://console.cloud.google.com/storage/browser/mina_network_block_data)
- [Mina archive dumps](https://console.cloud.google.com/storage/browser/mina-archive-dumps)
- [Mina seed lists](https://console.cloud.google.com/storage/browser/seed-lists)
- [Mina nix cache](https://console.cloud.google.com/storage/browser/mina-nix-cache)
- [O(1) Labs container registry](https://console.cloud.google.com/gcr/images/o1labs-192920/global)

### run

You must have a PostgreSQL db `archive` and a server listening on port `5432`

Start a mina archive node instance with `postgres` user and connect to the `archive` db with `--server-port 3086`

```sh
cd archive_node/scripts/
chmod +x mina_archive_run.sh
./mina_archive_run.sh
```

### archive daemon

Start a mina daemon with `--server-port 3086`

```sh
cd archive_node/scripts/
chmod +x mina_archive_daemon.sh
./mina_archive_daemon.sh
```

### [postgres user scripts](./postgres_scripts/)

Sets up the `postgres` user for an archive node
