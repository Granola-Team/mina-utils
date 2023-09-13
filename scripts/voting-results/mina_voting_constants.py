import pathlib

PARENT_DIR = pathlib.Path(__file__).parent
RESULTS_DIR = PARENT_DIR / "results"
LEDGERS_DIR = PARENT_DIR / "ledgers"

LEDGER_SOURCES = {
    "granola": "https://raw.githubusercontent.com/Granola-Team/mina-ledger/main/mainnet",
    "zkvalidator" : "https://raw.githubusercontent.com/zkvalidator/mina-graphql-rs/main/data/epochs/"
}

GITHUB_AUTH_TOKEN = PARENT_DIR / "voting_github_auth_token"

MINA_EXPLORER = "https://graphql.minaexplorer.com"
'''
Mina Explorer GraphQL endpoint
'''

def on_chain_data_loc(ep: int, fname: str) -> pathlib.Path:
    '''
    ./voting_data/epoch_{ep}/{fname}.json
    '''
    return PARENT_DIR / f"voting-data/epoch_{ep}/{fname}.json"

def agg_stake_loc(ep: int) -> pathlib.Path:
    return on_chain_data_loc(ep, "aggregated_stake")

def txns_loc(ep: int) -> pathlib.Path:
    return on_chain_data_loc(ep, "transactions")

def ledger_loc(ep: int, ledger_hash: str) -> pathlib.Path:
    return on_chain_data_loc(ep, ledger_hash)

def source_loc(src: str, ledger_hash: str) -> pathlib.Path:
    return LEDGERS_DIR / src / f"{ledger_hash}.json"
