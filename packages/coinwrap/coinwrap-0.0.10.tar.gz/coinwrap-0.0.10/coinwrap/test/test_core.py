from ..core import Market


def test_core():
    market = Market()
    print '\ncoin()'
    print market.coin('bitcoin', limit=1)
    print '\nstats()'
    print market.stats()


if __name__ == '__main__':
    test_core()
