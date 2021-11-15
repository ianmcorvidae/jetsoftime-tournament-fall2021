import copy
import util

def rankdiff(nplay, expected, actual):
    return nplay * (actual - expected)

def expected(nplay, rank, otherranks, denom):
    return ((nplay * rank - sum(otherranks))/nplay)/denom

def all_expected(race, ranks, denom, startval=0):
    players = set(race["finishers"]) | set(race["forfeits"])
    return dict([(player, expected(len(players), ranks.get(player, startval), [ranks.get(p,startval) for p in players if p != player], denom)) for player in players])

def actuals(race, maxscore=100, minscore=10, step=-10, forfeitscore=0):
    topscores = list(range(maxscore, minscore+1, step)) # +1 so minscore isn't included
    if len(race["finishers"]) < len(topscores):
        print("not enough finishers, probably an error about to happen")
    scores = dict(zip([race["finishers"][i] for i in range(min(len(race["finishers"]), len(topscores)))], topscores))
    finishers = set(race["finishers"])
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
    #print(ex,ac)
    r = dict()
    nplay = len(ac.keys())
    if denom_as_nplay:
        nplay = denom
    for player in ac.keys():
        r[player] = rankdiff(nplay, ex[player], ac[player])
    return r

def first_race_denom(race):
    return len(set(race["finishers"]) | set(race["forfeits"]) | set(race["nonparticipants"]))

def raceranks(races, startval=0, maxscore=100, minscore=10, step=-10, forfeitscore=0):
    denom = first_race_denom(races[0])
    ranks = [dict([(p, startval) for p in util.all_players(races)])] + [None for r in range(len(races))]
    ranks[1] = rankdiffs(races[0], ranks[0], denom, True, maxscore, minscore, step, forfeitscore, startval=startval)
    for r in range(1,len(races)):
        race = races[r]
        ranks[r+1] = copy.deepcopy(ranks[r])    
        finishers = set(race["finishers"])
        forfeits = set(race["forfeits"])
        diffs = rankdiffs(races[r], ranks[r], denom, False, maxscore, minscore, step, forfeitscore, startval=startval)
        for player in diffs.keys():
            print(r, player, diffs[player])
            ranks[r+1][player] = int(round(ranks[r+1].get(player, startval) + diffs[player]))
    return ranks

if __name__ == "__main__":
    import races
    import sys
    rs = races.races
    if len(sys.argv) > 1 and sys.argv[1] == "--no-incomplete":
        rs = [r for r in races.races if not r.get("incomplete", False)]
    print(util.table(rs, raceranks(rs)))
