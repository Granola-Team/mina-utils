## [Staking, delegating, and snarking](https://docs.minaprotocol.com/node-operators/staking-and-snarking)

## [Staking](https://docs.minaprotocol.com/node-operators/staking-and-snarking#staking-mina)

TODO no `set-staking` client subcommand

## [Delegating](https://docs.minaprotocol.com/node-operators/staking-and-snarking#delegating-mina)

To delegate stake to `<DELEGATE-PUBLIC-KEY>` do

```sh
mina account unlock --public-key $MINA_PUBLIC_KEY
mina client delegate-stake \
    --receiver <DELEGATE-PUBLIC-KEY> \
    --sender $MINA_PUBLIC_KEY \
    --fee 0.1
```

*Note*: there is a latency period of 2-4 weeks before new stake delegations go into effect

## [Snark](https://docs.minaprotocol.com/node-operators/staking-and-snarking#compressing-data-in-the-mina-network)

To set snark worker do

```sh
mina client set-snark-work-fee <FEE>
mina client set-snark-worker --address $MINA_PUBLIC_KEY
```

Alternatively, you can use [`mina_snark`](../scripts/mina_snark.sh)

Confirm it worked

```sh
mina client status
# the SNARK worker field should now be <MINA_PUBLIC_KEY>
```

### Using `daemon.json` to configure mina daemon

Create the file

```sh
$ nano ~/.mina-config/daemon.config
# Example `daemon.json` file
{
  "daemon": {
    "client-port": 1000,
    "external-port": 1001,
    "rest-port": 1002,
    "block-producer-key": "/path/to/privkey-file",
    "block-producer-password": "mypassword",
    "block-producer-pubkey": "<MY PUBLICKEY>",
    "coinbase-receiver": "<MY PUBLICKEY>",
    "log-block-creation": false,
    "log-received-blocks": false,
    "log-snark-work-gossip": false,
    "log-txn-pool-gossip": false,
    "peers": ["seed-one.o1test.net", "seed-two.o1test.net"],
    "run-snark-worker": "<MY PUBLICKEY>",
    "snark-worker-fee": 10,
    "snark-worker-parallelism": 1,
    "work-reassignment-wait": 420000,
    "work-selection": "seq"
  }
}
```
