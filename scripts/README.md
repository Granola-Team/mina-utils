# Mina scripts

Required `python >= 3.9`

## Keys

Python script for generating cryptographically secure passwords, keypairs, and env file for mina

```sh
# from mina-utils/scripts
python -m mina_gen_keypair --help
```

## Daemon

### start

Start the daemon

```sh
# from ./scripts
./mina_start.sh
```

### snark

Set the snark worker and fee for a mina node

```sh
# from ./scripts
python -m mina_snark --help
```
