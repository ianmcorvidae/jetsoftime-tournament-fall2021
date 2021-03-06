import copy
import rasterlogic
import util
import decimal

def adjusted_expected_meandiff(expected, actuals, maxscore=100, minscore=10):
    mean_actual = sum(actuals.values())/len(actuals.values())
    mean_expected = sum(expected.values())/len(expected.values())
    meandiff = mean_actual - mean_expected

    new_expected = copy.deepcopy(expected)
    for k in new_expected:
        new_expected[k] = new_expected[k] + meandiff

    return new_expected

def adjusted_expected_mindiff_mult(expected, maxscore=100, minscore=10):
    minex = min(expected.values())
    maxex = max(expected.values())

    initialdiff = 0 - minex
    if (maxex + initialdiff) != 0:
        mult = (maxscore - minscore) / (maxex + initialdiff)
    else:
        mult = 1

    new_expected = copy.deepcopy(expected)
    for k in new_expected:
        new_expected[k] = (new_expected[k] + initialdiff) * mult + minscore

    return new_expected

def rankdiffs(race, ranks, denom, denom_as_nplay=False, maxscore=100, minscore=10, step=-10, forfeitscore=0):
    ex = rasterlogic.all_expected(race, ranks, denom)
    ac = rasterlogic.actuals(race, maxscore, minscore, step, forfeitscore)
    ex = adjusted_expected_mindiff_mult(ex, maxscore, minscore)
    r = dict()
    nplay = len(ac.keys())
    if denom_as_nplay:
        nplay = denom
    for player in ac.keys():
        r[player] = rasterlogic.rankdiff(nplay, ex[player], ac[player])
    return r

def raceranks(races, startval=0, maxscore=100, minscore=10, step=-10, forfeitscore=0):
    denom = rasterlogic.first_race_denom(races[0])
    ranks = [dict([(p, startval) for p in util.all_players(races)])] + [None for r in range(len(races))]
    ranks[1] = rankdiffs(races[0], ranks[0], denom, True, maxscore, minscore, step, forfeitscore)
    for r in range(1,len(races)):
        race = races[r]
        ranks[r+1] = copy.deepcopy(ranks[r])    
        finishers = util.finishers(race)
        forfeits = set(race["forfeits"])
        diffs = rankdiffs(races[r], ranks[r], denom, False, maxscore, minscore, step, forfeitscore)
        for player in diffs.keys():
            ranks[r+1][player] = int(decimal.Decimal(ranks[r+1].get(player, startval) + diffs[player]).quantize(decimal.Decimal('1'), rounding=decimal.ROUND_HALF_UP))
    return ranks

if __name__ == "__main__":
    import races
    import sys
    rs = races.races
    if len(sys.argv) > 1 and sys.argv[1] == "--no-incomplete":
        rs = [r for r in races.races if not r.get("incomplete", False)]
    print(util.table(rs, raceranks(rs)))
