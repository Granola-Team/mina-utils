import argparse
import unittest
import mina_voting

class Test(unittest.TestCase):
    def test_res(self):
        '''
        Voting results:

        `https://mina.vote/mainnet/cftest-2/results?start=1671202800000&end=1672487999000&hash=jxWMPncjMY9VhwehhVKHhobvJuAhZcdx5kfUtX4V3dy9Rw9aMZA`
        '''
        res = mina_voting.calculate(argparse.Namespace(
            kw=['cftest-2'],
            lh=None,
            ep=[43],
            start=['2022-12-16T10:00:00Z'],
            end=['2022-12-31T06:59:59Z'],
            gql=None,
            v=False),
            test=True
        )
        if not res:
            assert False
        else:
            ledger = res['ledger']
            votes = res['votes'][0]
            yes_votes = res['votes'][1]
            no_votes  = res['votes'][2]
            yes_weight = res['weight'][1]
            no_weight  = res['weight'][2]
            total_vote_stake = res['stake'][1]

            assert yes_votes == 0
            assert yes_weight == 0
            assert no_votes == 1
            assert no_weight == 1
            assert total_vote_stake == 0.4451
            assert len(votes) == 6
            assert len(ledger) == 137737

if __name__ == "__main__":
    unittest.main()
