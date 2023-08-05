from coinwrap.core import Market


def test_core():
    market = Market()  # change to Local
    print '\ncoin()'
    print market.coin('bitcoin', limit=1)
    print '\nstats()'
    print market.stats()
