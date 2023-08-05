def test_core():
    market = Market()
    print '\ncoin()'
    print market.coin('bitcoin', limit=1)
    print '\nstats()'
    print market.stats()
