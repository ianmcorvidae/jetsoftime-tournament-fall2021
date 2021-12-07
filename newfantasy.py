# Old rank + (Actual score/expected) * (Participant count - Position(Ranking in the match))  * 10 + ((expected - Actual score)/expected) * (1 - Position(same meaning as earlier)) * 10

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
        #print("actuals", player, player_actuals)
        ex = max(sum(player_actuals)/len(player_actuals),10)
    #print("expected", player, ex)
    return ex

def all_expected(race, past_races, maxscore=100, minscore=10, step=-10, forfeitscore=0):
    players = util.finishers(race) | set(race["forfeits"])
    return dict([(player, expected(player, past_races, maxscore, minscore, step, forfeitscore)) for player in players])

def rankdiff(actual, expected, nplay, place):
    # 1-indexed place needed, but we'll pass in 0-indexed
    p = place + 1
    #print(actual, expected, p, (actual/expected) * (nplay - p) * 10, ((expected-actual)/expected) * (1-p) * 10)
    #return (actual/expected) * (nplay - p) * 10 + ((expected - actual)/expected) * (1-p)*10
    return (actual/expected) * ((nplay - p) * 10 + (0 - p) * 10)

def rankdiffs(race, past_races, ranks, denom, maxscore=100, minscore=10, step=-10, forfeitscore=0, startval=1500):
    ex = all_expected(race, past_races, maxscore, minscore, step, forfeitscore)
    ac = rasterlogic.actuals(race, maxscore, minscore, step, forfeitscore)
    r = dict()
    nplay = len(ac.keys())
    for player in ac.keys():
        #print("rankdiff:", player)
        place = None
        if isinstance(race["finishers"], list) and player in util.finishers(race):
            place = race["finishers"].index(player)
        elif isinstance(race["finishers"], dict) and player in util.finishers(race):
            for p in race["finishers"].keys():
                if isinstance(race["finishers"][p], list):
                    if player in race["finishers"][p]:
                        place = p - 1
                elif player == race["finishers"][p]:
                    place = p - 1
        elif player in race["forfeits"]:
            place = len(util.finishers(race))+1
        r[player] = rankdiff(ac[player], ex[player], nplay, place)
        #print(r[player])
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
