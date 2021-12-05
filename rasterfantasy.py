import util
import copy
import decimal
import rasterlogic

def expected(player, past_races, maxscore=100, minscore=10, step=-10, forfeitscore=0):
    ex = 50
    past_participants = util.all_participating_players(past_races)
    if player in past_participants:
        actuals = [rasterlogic.actuals(r, maxscore, minscore, step, forfeitscore) for r in past_races]
        player_actuals = [ac[player] for ac in actuals if player in ac]
        ex = sum(player_actuals)/len(player_actuals) - 20
    return ex

def all_expected(race, past_races, maxscore=100, minscore=10, step=-10, forfeitscore=0):
    players = util.finishers(race) | set(race["forfeits"])
    return dict([(player, expected(player, past_races, maxscore, minscore, step, forfeitscore)) for player in players])

def rankdiffs(race, past_races, ranks, denom, maxscore=100, minscore=10, step=-10, forfeitscore=0, startval=1500):
    ex = all_expected(race, past_races, maxscore, minscore, step, forfeitscore)
    ac = rasterlogic.actuals(race, maxscore, minscore, step, forfeitscore)
    r = dict()
    nplay = len(ac.keys())
    for player in ac.keys():
        r[player] = rasterlogic.rankdiff(nplay, ex[player], ac[player])
    return r

def raceranks(races, startval=1500, maxscore=100, minscore=10, step=-10, forfeitscore=0):
    denom = rasterlogic.first_race_denom(races[0])
    ranks = [dict([(p, startval) for p in util.all_players(races)])] + [None for r in range(len(races))]
    #ranks[1] = rankdiffs(races[0], [], ranks[0], denom, maxscore, minscore, step, forfeitscore, startval=startval)
    for r in range(len(races)):
        race = races[r]
        ranks[r+1] = copy.deepcopy(ranks[r])
        finishers = util.finishers(race)
        forfeits = set(race["forfeits"])
        diffs = rankdiffs(races[r], races[:r], ranks[r], denom, maxscore, minscore, step, forfeitscore, startval=startval)
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
