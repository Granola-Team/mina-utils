#!/usr/bin/env python

import os
import pathlib
import argparse
import mina_gen_keypair

SECRETS_DIR = pathlib.Path(__file__).parent.parent / "secrets"

def run(args: argparse.Namespace):
    print(f"Changing {SECRETS_DIR} permissions to 700")
    os.system(f"chmod 700 {SECRETS_DIR}")
    try:
        pk = mina_gen_keypair.get_pubkey(args.pubkey[0])
    except:
        pk = mina_gen_keypair.get_pubkey()
    print(f"Using public key {pk}")
    print(f"Changing {SECRETS_DIR} permissions to 600")
    os.system(f"chmod 600 {SECRETS_DIR}")
    try:
        fee = args.fee[0]
    except:
        fee = 0.1
    os.system(f"mina client set-snark-work-fee {fee}")
    os.system(f"mina client set-snark-worker --address {pk}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mina snark worker util")
    parser.add_argument("--pubkey", action="store", nargs=1, type=str, help="set the snark worker public key")
    parser.add_argument("--fee", action="store", nargs=1, type=float, help="set the snark worker fee")
    args = parser.parse_args()
    run(args)
