import os
import sys
import json
import pathlib
import requests
import mina_voting_constants as mvc

def pp(resp):
	  return json.dumps(resp, indent=4)

def get_next_staking_ledger_granola_github_auth(ep: int, ledger_hash: str, repo: str):
    '''
    ### Requires github auth token

    Request the next staking ledger via hash from Granola's `mina-ledger` GitHub repo

    Write to local file {mvc.local_data_dir(ep) / ledger_hash}.json
    '''
    if not mvc.GITHUB_AUTH_TOKEN.exists():
        print(f"You must copy a github auth token to file {mvc.GITHUB_AUTH_TOKEN}")
        sys.exit(1)

    with mvc.GITHUB_AUTH_TOKEN.open("r", encoding="utf-8") as f:
        auth_token = f.read().strip()
        f.close()

    print(f"Fetching: Granola-Team/mina-ledger/main/mainnet/{ledger_hash}.json")
    os.system(f'curl -H "Accept: application/vnd.github.v4.raw" \
        -H "Authorization: bearer {auth_token}" \
        "{mvc.LEDGER_SOURCES["granola"]}/{ledger_hash}.json" > {mvc.ledger_loc(ep, ledger_hash)}')

def get_all_sources(ep, ledger_hash):
    for src in mvc.LEDGER_SOURCES:
        get_next_staking_ledger(ep, ledger_hash, src, True)

def diff(fpath1: pathlib.Path, fpath2: pathlib.Path):
    output = os.system(f'diff {fpath1} {fpath2}')
    if output:
        print(output)
        sys.exit(1)

def get_next_staking_ledger(ep: int, ledger_hash: str, src: str, extra = False):
    '''
    Get the next staking ledger via `wget`
    '''
    assert src in mvc.LEDGER_SOURCES
    target = mvc.ledger_loc(ep, ledger_hash)

    if extra:
        src_dir = mvc.LEDGERS_DIR / src
        if not src_dir.exists():
            if not mvc.LEDGERS_DIR.exists():
                os.mkdir(mvc.LEDGERS_DIR)
            os.mkdir(src_dir)
        target = src_dir / f"{ledger_hash}.json"

    if src == "granola":
        os.system(f'wget "{mvc.LEDGER_SOURCES["granola"]}/{ledger_hash}.json" -O {target}')

    if src == "zkvalidator":
        os.system(f'wget "{mvc.LEDGER_SOURCES["zkvalidator"]}/{ledger_hash}.json" -O {target}')

def template_request_gql(query: str, variables: dict = {}, endpoint: str = mvc.MINA_EXPLORER) -> dict:
    '''
    Template GraphQL request
    '''
    query = " ".join(query.split())
    payload = {"query": query}

    if variables:
        payload = {**payload, "variables": variables}

    headers = {"Accept": "application/json"}
    response = requests.post(endpoint, json=payload, headers=headers)
    resp_json = response.json()

    if response.status_code == 200 and "errors" not in resp_json:
        return resp_json

    else:
        print(response.text)
        raise Exception(f"Query failed -- returned code {response.status_code} with response {response.text}")

def get_next_ledger_hash_gql(epoch: int, endpoint: str = mvc.MINA_EXPLORER) -> dict:
    '''
    Returns ledger hash for supplied epoch

    Variables: `epoch`
    '''
    query = """query($epoch: Int) {
  blocks(query: {canonical: true, protocolState: {consensusState: {epoch: $epoch}}}, limit: 1) {
    protocolState {
      consensusState {
        nextEpochData {
          ledger {
            hash
          }
        }
        epoch
      }
    }
  }
}"""
    return template_request_gql(query, {"epoch": epoch}, endpoint)

def get_next_staking_ledger_gql(ledger_hash: str, endpoint: str = mvc.MINA_EXPLORER) -> dict:
    '''
    Return the staking ledger

    Variables: `limit`, `ledgerHash`
    '''
    query = """query ($ledgerHash: String!, $limit: Int = 1000000) {
  nextstakes(query: {ledgerHash: $ledgerHash}, limit: $limit) {
    pk
    balance
    delegate
  }
}"""
    return template_request_gql(query, {"ledgerHash": ledger_hash}, endpoint)

def get_block_heights(variables, endpoint: str = mvc.MINA_EXPLORER):
    '''
    Returns the canonical block heights within specified parameters

	Variables: `min_date_time`, `max_date_time`
    '''
    query = """query($min_date_time: DateTime!, $max_date_time: DateTime!) {
  blocks(query: {canonical: true, dateTime_gte: $min_date_time, dateTime_lte: $max_date_time}, limit: 7140) {
    blockHeight
  }
}"""
    return template_request_gql(query, variables, endpoint)

def get_payments_in_block_height(variables, endpoint: str = mvc.MINA_EXPLORER):
    '''
    Returns the PAYMENT transactions in the specified block

	Variables: `block_height`, `limit`
    '''
    query = """query($block_height: Int!, $limit: Int = 1000) {
  transactions(query: {blockHeight: $block_height, canonical: true, kind: "PAYMENT"}, sortBy: DATETIME_DESC, limit: $limit) {
    blockHeight
    memo
    nonce
    receiver {
      publicKey
    }
    source {
      publicKey
    }
  }
}"""
    return template_request_gql(query, variables, endpoint)

def get_transactions(variables, endpoint: str = mvc.MINA_EXPLORER) -> dict:
    '''
    Returns transactions within specified parameters

    Variables: `source`, `receiver`, `kind`, `min_block_height`, `max_block_height`, `min_date_time`, `max_date_time`, `limit`, `block_height`
    '''
    query = """query($source: String, $receiver: String, $kind: String, $block_height: Int, $min_block_height: Int, $max_block_height: Int, $min_date_time: DateTime, $max_date_time: DateTime, $limit: Int = 1000) {
  transactions(query: {source: {publicKey: $source}, receiver: {publicKey: $receiver}, kind: $kind, memo_exists: $memo_exists, canonical: true, blockHeight_gte: $min_block_height, blockHeight_lte: $max_block_height, dateTime_gte: $min_date_time, dateTime_lte: $max_date_time}, sortBy: DATETIME_DESC, limit: $limit) {
    memo
    source {
      publicKey
    }
    receiver {
      publicKey
    }
    nonce
    kind
    dateTime
    blockHeight
    hash
    amount
  }
}"""
    return template_request_gql(query, variables, endpoint)

def get_blocks(variables, endpoint: str = mvc.MINA_EXPLORER) -> dict:
    '''
    Returns blocks within specified parameters

    Variables: `creator`, `epoch`, `min_block_height`, `max_block_height`, `min_date_time`, `max_date_time`, `limit`
    '''
    query = """query($creator: String, $epoch: Int, $min_block_height: Int, $max_block_height: Int, $min_date_time: DateTime, $max_date_time: DateTime, $limit: Int = 10) {
  blocks(query: {creator: $creator, protocolState: {consensusState: {epoch: $epoch}}, canonical: true, blockHeight_gte: $min_block_height, blockHeight_lte: $max_block_height, dateTime_gte: $min_date_time, dateTime_lte: $max_date_time}, sortBy: DATETIME_DESC, limit: $limit) {
    blockHeight
    canonical
    creator
    dateTime
    txFees
    snarkFees
    receivedTime
    stateHash
    stateHashField
    protocolState {
      consensusState {
        blockHeight
        epoch
        slotSinceGenesis
      }
    }
    transactions {
      coinbase
      coinbaseReceiverAccount {
        publicKey
      }
      feeTransfer {
        fee
        recipient
        type
      }
    }
  }
}"""
    return template_request_gql(query, variables, endpoint)
