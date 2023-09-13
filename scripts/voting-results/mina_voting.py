import os
import sys
import json
import base58
import argparse
import mina_voting_query as mvq
import mina_voting_constants as mvc

#####################
# stake distribution
#####################

def get_next_staking_ledger_hash(epoch: int, endpoint: str) -> str:
    return mvq.get_next_ledger_hash_gql(
        epoch + 1,
        endpoint
    )["data"]["blocks"][0]["protocolState"]["consensusState"]["nextEpochData"]["ledger"]["hash"]

def download_ledger(ep: int, ledger_hash: str, src: str, verbose = False) -> list:
    '''
    Downloads next staking ledger from https://github.com/Granola-Team/mina-ledger/tree/main/mainnet/

    Write local json
    '''
    ledger_srcs = mvc.LEDGER_SOURCES.keys()
    if src not in ledger_srcs:
        print(f"Please provide a valid ledger source: {ledger_srcs}")
        sys.exit(1)

    # prep local dir
    ldir = mvc.ledger_loc(ep, ledger_hash)
    if not ldir.exists():
        os.mkdir(ldir)

    # write the ledger
    if verbose:
        print(f"Downloading ledger with hash {ledger_hash} from {mvc.LEDGER_SOURCES[src]}...")
    mvq.get_next_staking_ledger(ep, ledger_hash, src)

    # load the ledger
    if verbose:
        print(f"Loading ledger with hash {ledger_hash}...")
    with mvc.ledger_loc(ep, ledger_hash).open('r', encoding='utf8') as f:
        raw_ledger_list = json.load(f)
        f.close()

    return raw_ledger_list

def filter_dict_keys(keys, dict: dict) -> dict:
    res = {}
    for k in keys:
        res[k] = dict[k]
    return res

def parse_ledger(raw_ledger: list) -> list:
    '''
    Returns the list of (balance, delegate)-dicts
    '''
    essential = ['balance', 'delegate']
    ledger = filter(lambda d: filter_dict_keys(essential, d), raw_ledger)
    return list(ledger)

def aggregate_stake(ledger: list, ep: int, verbose = False) -> dict:
    '''
    Returns aggregated stake
    '''
    if verbose:
        print("Aggregating stake...")

    agg_stake = {}
    delegations: dict[str, list] = {}
    self_delegations = set()
    non_self_delegations = set()

    # - aggregate delegated stake
    # - separate self-delegators, non-self-delegators
    for account in ledger:
        pk = account['pk']
        dg = account['delegate']
        bal = float(account['balance'])

        try:
            delegations[pk].add(dg)
        except:
            delegations[pk] = [dg]

        # distinguish
        try:
            if delegations[pk] == [pk]:
                self_delegations.add(pk)
        except:
            non_self_delegations.add(pk)

        # sum delegated balances
        try:
            agg_stake[dg] += bal
        except:
            agg_stake[dg] = bal

    # filter out non-self-delegators from agg stake
    for nsd in non_self_delegations:
        try:
            del agg_stake[nsd]
        except:
            pass

    # write agg stake to local file
    with mvc.agg_stake_loc(ep).open("w", encoding="utf-8") as f:
        f.write(mvq.pp(agg_stake))
        f.close()

    return agg_stake

########
# votes
########

def get_block_heights_for_period(variables: dict, endpoint: str) -> list[int]:
    '''
    Returns block heights for the given voting period
    '''
    assert variables["min_date_time"] and variables["max_date_time"]

    raw_block_heights = mvq.get_block_heights(variables, endpoint)
    raw_block_heights = raw_block_heights["data"]["blocks"]

    return list(map(
        lambda d: d["blockHeight"],
        raw_block_heights
    ))

def get_transactions_in_block(block_height: int, endpoint: str) -> list[dict]:
    '''
    Returns the list of payment transactions in the given block
    '''
    variables = {
        "block_height": block_height
    }
    return mvq.get_payments_in_block_height(
        variables,
        endpoint
    )["data"]["transactions"]

def download_transactions(variables: dict, ep: int, endpoint: str) -> dict:
    '''
    Downloads transactions in voting period from the graphql `endpoint`
    '''
    raw_tx_data = {}
    block_heights = get_block_heights_for_period(variables, endpoint)

    print(block_heights)
    print(f"Fetching blocks {block_heights[0]} - {block_heights[-1]}")
    print("This may take several minutes...")

    for height in block_heights:
        raw_tx_data[height] = get_transactions_in_block(height, endpoint)
        print(f"Got block {height}")

    with mvc.txns_loc(ep).open("w", encoding="utf-8") as f:
        f.write(mvq.pp(raw_tx_data))
        f.close()
    return raw_tx_data

def is_vote(raw_tx: dict, keyword: str) -> bool:
    return all([
        in_favor(raw_tx["memo"], keyword) or against(raw_tx["memo"], keyword),
        raw_tx["source"]["publicKey"] == raw_tx["receiver"]["publicKey"]
    ])

def parse_transactions(per_block_tx_data: dict, keyword: str) -> tuple[dict, int]:
    '''
    Parses raw transaction data

    Returns raw votes (`memo` base58 encoded) and number of votes
    '''
    txns = []
    num_txs = 0
    raw_votes = {}

    for block_height in per_block_tx_data.keys():
        txns += per_block_tx_data[block_height]

    for tx in txns:
        num_txs += 1
        pk = tx["source"]["publicKey"]

        if is_vote(tx, keyword):
            memo = tx["memo"]
            nonce = tx["nonce"]
            height = tx["blockHeight"]
            data = [memo, height, nonce]

            try:
                v = raw_votes[pk]
                if v[1] < height or v[1] == height and v[2] < nonce:
                    raw_votes[pk] = data
                else:
                    pass
            except:
                raw_votes[pk] = data

    return raw_votes, num_txs

##########
# results
##########

def get_account(ledger: list, pubkey: str) -> dict:
    '''
    Returns account associated with `pubkey`
    '''
    res = {}
    for account in ledger:
        pk = account['pk']
        if pk == pubkey:
            res = account
            break
    return res

def mk_csv(num_txns: int, yes_votes: int, no_votes: int, vote_stake: dict, yes_stake: float, no_stake: float, yes_weight: float, no_weight: float) -> str:
    return """Num_epoch_txns,Num_yes_votes,Num_no_votes,Total_vote_stake,Yes_vote_stake,No_vote_stake,Yes_vote_weight,No_vote_weight
%s,%s,%s,%s,%s,%s,%s,%s
""" % (num_txns, yes_votes, no_votes, vote_stake, yes_stake, no_stake, yes_weight, no_weight)

def display(res: dict, test = False):
    '''
    Print results to stdout
    '''
    ep = res['epoch']
    rep = res['rep']
    key = res['key']
    num_txns = res['num']
    ledger = res['ledger']
    ledger_hash = res['hash']
    votes, yes_votes, no_votes = res['votes']
    vote_weight, yes_weight, no_weight = res['weight']
    agg_stake, total_vote_stake, yes_stake, no_stake = res['stake']
    pp = lambda pk: (pk, {
            "vote": memo_of_vote(votes[pk][0]),
            "stake": weight_or_delegation(ledger, agg_stake, pk, True),
            "weight": weight_or_delegation(ledger, vote_weight, pk, False)
        })
    votes = dict(map(pp, votes))
    total_stake = total(ep, ledger_hash)
    report = """\
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~ Voting Results Report ~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Keyword: %s
Outcome: %s

Yes vote stake:  %s
No vote stake:   %s

Yes vote weight: %s
No vote weight:  %s

Vote stake:      %s
Total stake:     %s
Turnout:         %s

Num epoch txns:  %s
Num "vote" txns: %s
Num delegated:   %s
Num yes votes:   %s
Num no votes:    %s

Vote data:
%s""" % (key, "YES" if yes_weight > no_weight else "NO",
         f"{yes_stake:.14g}", f"{no_stake:.14g}",
         f"{yes_weight:.14g}", f"{no_weight:.14g}",
         f"{total_vote_stake:.14g}", f"{total_stake:.14g}", f"{total_vote_stake / total_stake:.2%}",
         num_txns, len(votes), len(votes) - yes_votes - no_votes, yes_votes, no_votes,
         mvq.pp(votes))

    if not test and args.v:
        print(report)

    if rep:
        keydir = mvc.RESULTS_DIR / str(key)
        report_csv = keydir / "report.csv"
        votes_json = keydir / "votes.json"

        if not keydir.exists():
            os.mkdir(keydir)

        r = open(report_csv, "w", encoding="utf-8")
        v = open(votes_json, "w", encoding="utf-8")
        r.write(mk_csv(num_txns, yes_votes, no_votes, total_vote_stake, yes_stake, no_stake, yes_weight, no_weight))
        v.write(mvq.pp(votes))
        r.close()
        v.close()

def prep_args(args, test = False) -> dict[str, list]:
    '''
    Prepare args for `results(ledger_list, agg_stake, votes, keyword, num_txns)`
    '''
    ep = args.ep[0]
    diff = args.diff
    keyword = args.kw[0]
    endpoint = args.gql[0] if args.gql else mvc.MINA_EXPLORER
    ledger_hash = args.lh[0] if args.lh else None
    variables = {
        "min_date_time": args.start[0],
        "max_date_time": args.end[0]
    }

    # download next staking ledger hash
    try:
        ledger_hash = get_next_staking_ledger_hash(ep, endpoint)

    except:
        print("FAILED: next staking ledger hash")
        sys.exit(1)

    # check if provided ledger hash matches downloaded
    if args.lh:
        if ledger_hash != args.lh[0]:
            print("⚠️ Mismatched ⚠️")
            print(f"- provided hash: {args.lh[0]}")
            print(f"- download hash: {ledger_hash}")
            sys.exit(1)
        else:
            print(f"Correct next staking ledger hash for epoch {ep}")

    # only download the ledger if we don't already have it
    lloc = mvc.ledger_loc(ep, ledger_hash)

    if not lloc.exists():
        raw_ledger_list = download_ledger(ep, ledger_hash, endpoint)

    else:
        # otherwise load
        with lloc.open("r", encoding="utf-8") as f:
            raw_ledger_list = json.load(f)
            f.close()

    ledger_list = parse_ledger(raw_ledger_list)

    # only aggregate stake if we haven't done so already
    if not mvc.agg_stake_loc(ep).exists():
        agg_stake = aggregate_stake(ledger_list, ep)

    else:
        # otherwise load
        with mvc.agg_stake_loc(ep).open("r", encoding="utf-8") as f:
            agg_stake = json.load(f)
            f.close()

    # only download transactions if we don't already have them
    if not mvc.txns_loc(ep).exists():
        raw_tx_data = download_transactions(variables, ep, endpoint)

    else:
        # otherwise load
        with mvc.txns_loc(ep).open("r", encoding="utf-8") as f:
            raw_tx_data = json.load(f)
            f.close()

    if diff:
        mvq.diff(
            mvc.source_loc("granola", ledger_hash),
            mvc.source_loc("zkvalidator", ledger_hash)
        )

    # parse transactions and display results
    votes, num_txns = parse_transactions(raw_tx_data, keyword)
    return results(ledger_list, agg_stake, votes, keyword, num_txns, ep, ledger_hash)

def results(ledger_list, agg_stake, votes, keyword, num_txns, ep, ledger_hash, report = False) -> dict[str, list]:
    '''
    Returns all results `num`, `keys`, `ledger`, `stake`, `votes`, `weight`
    '''
    no_votes = 0
    no_stake = 0
    yes_votes = 0
    yes_stake = 0
    vote_weight = {}
    total_vote_stake = 0

    # calculate total voting stake
    for pk in votes:
        vote = votes[pk]
        try:
            total_vote_stake += agg_stake[pk]
        except:
            pass

    # calculate vote weights
    for pk in votes:
        try:
            vote = votes[pk]
            vote_weight[pk] = agg_stake[pk] / total_vote_stake
        except:
            pass

    # aggregate voting stake
    for pk in votes:
        vote = votes[pk]
        memo = vote[0]

        if pk in agg_stake.keys():
            # sum yes stake
            if in_favor(memo, keyword):
                yes_votes += 1
                try:
                    yes_stake += agg_stake[pk]
                except:
                    pass

            # sum no stake
            elif against(memo, keyword):
                no_votes += 1
                try:
                    no_stake += agg_stake[pk]
                except:
                    pass

    # calculate voting weight
    yes_weight = yes_stake / total_vote_stake
    no_weight = no_stake / total_vote_stake

    return {
        'num'   : num_txns,
        'epoch' : ep,
        'hash'  : ledger_hash,
        'key'   : keyword,
        'rep'   : [report],
        'stake' : [agg_stake, total_vote_stake, yes_stake, no_stake],
        'votes' : [votes, yes_votes, no_votes],
        'weight': [vote_weight, yes_weight, no_weight],
        'ledger': ledger_list,
    }

##########
# helpers
##########

# memo

def decode_memo(b58_encoded: str) -> str:
    '''
    Returns the base58 decoded input
    '''
    decoded = base58.b58decode(b58_encoded)
    if decoded[1] == b'x01':
        res = ""
    else:
        end_idx = decoded[2] + 3
        memo = decoded[3:end_idx]
        res = memo.decode('utf-8')
    return res

def memo_of_vote(encoded_memo: str) -> str:
    '''
    Returns the lowercase base58 decoded memo field
    '''
    memo = decode_memo(encoded_memo)
    return memo.lower()

# vote

def in_favor(encoded_memo, keyword) -> bool:
    '''
    Is this a vote in favor of the proposal?
    '''
    memo = memo_of_vote(encoded_memo)
    if not memo:
        return False
    else:
        return memo == keyword

def against(encoded_memo, keyword) -> bool:
    '''
    Is this a vote against the proposal?
    '''
    memo = memo_of_vote(encoded_memo)
    if not memo:
        return False
    else:
        return memo == f'no {keyword}'

# weight or delegation

def weight_or_delegation(ledger: list, dist: dict, pk: str, is_delegation: bool):
    '''
    Returns `pk`'s stake weight or the public key `pk` delegated to
    '''
    try:
        return dist[pk]
    except:
        if is_delegation:
            return get_account(ledger, pk)['delegate']
        else:
            return "N/A"

def total(ep: int, ledger_hash: str) -> float:
    with mvc.ledger_loc(ep, ledger_hash).open("r", encoding="utf-8") as f:
        raw_ledger = json.load(f)
        ledger = parse_ledger(raw_ledger)
        f.close()

    res = 0
    for account in ledger:
        res += float(account['balance'])

    return res

######
# cli
######

def check(args: argparse.Namespace):
    '''
    Validate the args

    Exit on failure
    '''
    if not args.ep:
        print("must provide an epoch number via -ep")
        sys.exit(1)
    if not args.kw:
        print("must provide a voting keyword via -kw")
        sys.exit(1)
    if not args.start:
        print("must provide a start time for the voting period via -start")
        sys.exit(1)
    if not args.end:
        print("must provide an end time for the voting period via -end")
        sys.exit(1)
    if args.lh and len(args.lh) > 1:
        print("can provide at most one ledger hash via -lh")
        sys.exit(1)

# main

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Mina on-chain voting results calculator and report generator")
    parser.add_argument("-kw", type=str, nargs=1, help="MIP keyword")
    parser.add_argument("-ep", type=int, nargs=1, help="Voting epoch number")
    parser.add_argument("-lh", type=str, nargs="*", help="Staking ledger hash")
    parser.add_argument("-start", type=str, nargs=1, help="Voting period start time (in your local timezone) - ISO-8601 YY-mm-ddTHH:MM:SS")
    parser.add_argument("-end", type=str, nargs=1, help="Voting period end time (in your local timezone) - ISO-8601 YY-mm-ddTHH:MM:SSZ")
    parser.add_argument("-v",  action="store_true", help="Verbose - shows all votes with memos decoded")
    parser.add_argument("-gql", type=str, nargs="*", help=f"GraphQL endpoint (default: {mvc.MINA_EXPLORER})")
    parser.add_argument("-report", action="store_true", help="Write report to file")
    parser.add_argument("-votes", action="store_true", help="Write votes to file")
    parser.add_argument("-diff", action="store_true", help="Get the staking ledger from various sources and diff")

    # validate args
    args = parser.parse_args()
    check(args)

    # prep result args
    res = prep_args(args)
    num = res['num']
    key = res['key']
    ep = res['epoch']
    stake = res['stake']
    votes = res['votes']
    ledger = res['ledger']
    ledger_hash = res['hash']

    # display results
    display(results(list(ledger), stake[0], votes[0], key, num, ep, ledger_hash, report=args.report))
