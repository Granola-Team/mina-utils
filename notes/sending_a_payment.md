# [Sending a payment](https://docs.minaprotocol.com/node-operators/sending-a-payment#using-a-connected-node)

Import a local account

```sh
chmod 700 ~/.mina-keys
mina accounts --privkey-path ~/.mina-keys/<YOUR_WALLET_NAME>
chmod 600 ~/.mina-keys
# should get something like the following:
# 😄 Imported account!
# Public key: B62qpP7yjM4F6XFk9vgq87r8W8s8BER7RYShMnKgadWrb4Gmr58FWNL
```

Alternatively, you can supply the python script with `--import-account`

Create local account

```sh
mina accounts create
```

Check your balance(s)

```sh
mina accounts list
```

Unlock your account and make a payment

```sh
mina accounts unlock --public-key $MINA_PUBLIC_KEY
mina client send-payment \
  --amount 1.5 \
  --receiver $MINA_PUBLIC_KEY \
  --fee 0.1 \
  --sender $MINA_PUBLIC_KEY
```

## [Advanced transactions](https://docs.minaprotocol.com/node-operators/sending-a-payment#advanced)

TODO
