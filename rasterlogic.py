import copy

def rankdiff(nplay, expected, actual):
    return nplay * (actual - expected)

def expected(nplay, rank, otherranks, denom):
    return ((nplay * rank - sum(otherranks))/nplay)/denom

def all_expected(race, ranks, denom):
    players = set(race["finishers"]) | set(race["forfeits"])
    return dict([(player, expected(len(players), ranks.get(player, 0), [ranks.get(p,0) for p in players if p != player], denom)) for player in players])

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

def rankdiffs(race, ranks, denom, denom_as_nplay=False, maxscore=100, minscore=10, step=-10, forfeitscore=0):
    ex = all_expected(race, ranks, denom)
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

def all_participating_players(races):
    all_players = set()
    for race in races:
        all_players = all_players | set(race['finishers']) | set(race['forfeits'])
    return all_players

def all_players(races):
     all_players = set()
     for race in races:
             all_players = all_players | set(race['finishers']) | set(race['forfeits']) | set(race['nonparticipants'])
     return all_players

def raceranks(races, startval=0, maxscore=100, minscore=10, step=-10, forfeitscore=0):
    denom = first_race_denom(races[0])
    ranks = [dict([(p, startval) for p in all_players(races)])] + [None for r in range(len(races))]
    ranks[1] = rankdiffs(races[0], ranks[0], denom, True, maxscore, minscore, step, forfeitscore)
    for r in range(1,len(races)):
        race = races[r]
        ranks[r+1] = copy.deepcopy(ranks[r])    
        finishers = set(race["finishers"])
        forfeits = set(race["forfeits"])
        diffs = rankdiffs(races[r], ranks[r], denom, False, maxscore, minscore, step, forfeitscore)
        for player in diffs.keys():
            ranks[r+1][player] = int(round(ranks[r+1].get(player, 0) + diffs[player]))
    return ranks

def byscore(ranks):
    return sorted([(v, k) for k,v in ranks.items()], reverse=True)

def numbered_byscore(ranks):
    bs = byscore(ranks)
    return [(i+1, bs[i][0], bs[i][1]) for i in range(len(bs))]

def table(races, ranks):
    from tabulate import tabulate
    cols = ['Player', 'Start']
    for i in range(1, len(ranks)):
        cols.extend(['W' + str(i), '+/-'])
    tab = [[] for x in all_players(races)]
    ranks_by_score = byscore(ranks[-1])
    for i in range(len(ranks_by_score)):
        player = ranks_by_score[i][1]
        tab[i] = [player, ranks[0].get(player, 0)]
        for j in range(1, len(ranks)):
            thisrank = int(ranks[j].get(player, 0))
            this_status0 = this_status1 = ''
            if player in races[j-1]["forfeits"]:
                this_status1 = '^'
            elif player not in races[j-1]["finishers"]:
                this_status0 = '('
                this_status1 = ')'
            tab[i].extend([thisrank, '{0}{1:+}{2}'.format(this_status0, int(thisrank - ranks[j-1].get(player, 0)), this_status1)])
    return tabulate(tab, headers=cols, disable_numparse=True)

if __name__ == "__main__":
    import races
    #import pprint
    #pprint.pprint([numbered_byscore(r) for r in raceranks(races.races)])
    import sys
    rs = races.races
    if len(sys.argv) > 1 and sys.argv[1] == "--no-incomplete":
        rs = [r for r in races.races if not r.get("incomplete", False)]
    print(table(rs, raceranks(rs)))
