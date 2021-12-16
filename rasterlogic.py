import copy
import util
import decimal

def rankdiff(nplay, expected, actual):
    #print("\t", nplay, actual-expected)
    return nplay * (actual - expected)

def expected(nplay, rank, otherranks, denom):
    #print("\t", ((nplay * rank - sum(otherranks))/nplay)/denom, nplay * rank, sum(otherranks))
    return ((nplay * rank - sum(otherranks))/nplay)/denom

def all_expected(race, ranks, denom, startval=0):
    players = util.finishers(race) | set(race["forfeits"])
    return dict([(player, expected(len(players), ranks.get(player, startval), [ranks.get(p,startval) for p in players if p != player], denom)) for player in players])

def actuals(race, maxscore=100, minscore=10, step=-10, forfeitscore=0):
    topscores = list(range(maxscore, minscore+1, step)) # +1 so minscore isn't included
    if len(util.finishers(race)) < len(topscores):
        print("not enough finishers, probably an error about to happen")
    scores = {}
    if isinstance(race["finishers"], list):
        scores = dict(zip([race["finishers"][i] for i in range(min(len(race["finishers"]), len(topscores)))], topscores))
    elif isinstance(race["finishers"], dict):
        for k in sorted(race["finishers"].keys()):
            if k > len(topscores):
                break
            if isinstance(race["finishers"][k], list):
                for p in race["finishers"][k]:
                    scores[p] = topscores[k-1]
            else:
                scores[race["finishers"][k]] = topscores[k-1]
    finishers = util.finishers(race)
    forfeits = set(race["forfeits"])
    for player in (finishers | forfeits) - set(scores.keys()):
        if player in finishers:
            scores[player] = minscore
        elif player in forfeits:
            scores[player] = forfeitscore
        else:
            print("player shouldn't have appeared", player, race)
    return scores

def rankdiffs(race, ranks, denom, denom_as_nplay=False, maxscore=100, minscore=10, step=-10, forfeitscore=0, startval=0):
    ex = all_expected(race, ranks, denom, startval=startval)
    ac = actuals(race, maxscore, minscore, step, forfeitscore)
    r = dict()
    nplay = len(ac.keys())
    if denom_as_nplay:
        nplay = denom
    for (k, v) in util.byscore(ex):
        print("{0}{1}ex:{2}\tac:{3}\tdiff:{4}".format(v, "\t" if len(v) > 7 else "\t\t", round(k,7), ac.get(v, None), round(rankdiff(nplay, k, ac.get(v,0)),7)))
    for player in ac.keys():
        r[player] = rankdiff(nplay, ex[player], ac[player])
    return r

def first_race_denom(race):
    return len(util.finishers(race) | set(race["forfeits"]) | set(race["nonparticipants"]))

def raceranks(races, startval=0, maxscore=100, minscore=10, step=-10, forfeitscore=0):
    denom = first_race_denom(races[0])
    ranks = [dict([(p, startval) for p in util.all_players(races)])] + [None for r in range(len(races))]
    print("Race 1")
    ranks[1] = rankdiffs(races[0], ranks[0], denom, True, maxscore, minscore, step, forfeitscore, startval=startval)
    for r in range(1,len(races)):
        race = races[r]
        print("Race " + str(r + 1))
        ranks[r+1] = copy.deepcopy(ranks[r])    
        finishers = util.finishers(race)
        forfeits = set(race["forfeits"])
        diffs = rankdiffs(races[r], ranks[r], denom, False, maxscore, minscore, step, forfeitscore, startval=startval)
        for player in diffs.keys():
            ranks[r+1][player] = int(decimal.Decimal(ranks[r+1].get(player, startval) + diffs[player]).quantize(decimal.Decimal('1'), rounding=decimal.ROUND_HALF_UP))
    return ranks

if __name__ == "__main__":
    import races
    import sys
    rs = races.races
    if len(sys.argv) > 1 and sys.argv[1] == "--no-incomplete":
        rs = [r for r in races.races if not r.get("incomplete", False)]
    if len(sys.argv) > 1 and sys.argv[1] == "--plot":
        import graph
        graph.graph(rs, raceranks(rs))
    print(util.table(rs, raceranks(rs)))
