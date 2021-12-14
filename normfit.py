# try to fit runners to a gaussian/normal curve based on times, and assign scores based on percentiles
from scipy import asarray as ar
from scipy.stats import skewnorm
import datetime
import time
import util
import copy

def time_to_seconds(timestring):
    t = time.strptime(timestring, '%H:%M:%S')
    return datetime.timedelta(hours=t.tm_hour, minutes=t.tm_min, seconds=t.tm_sec).total_seconds()

def score(n, time):
    return 1000 - (1000 * n.cdf(time))

def actuals(race, forfeit=0, pltlabel=None):
    time_secs = [time_to_seconds(t) for t in race['times']]
    ts_arr = ar(time_secs)
    n = skewnorm(*skewnorm.fit(ts_arr))
    if pltlabel is not None:
        import matplotlib.pyplot as plt
        import matplotlib.ticker as tick
        fig, ax = plt.subplots(1,1)
        ax.xaxis.set_major_formatter(tick.FuncFormatter(lambda x, pos: (datetime.datetime.min + datetime.timedelta(seconds=x)).strftime("%H:%M:%S")))
        ax.plot(ts_arr, n.pdf(ts_arr), 'r-', lw=5, alpha=0.6, label='norm pdf')
        ax.hist(ts_arr, density=True, alpha=0.2)
        ax.legend(loc='best', frameon=False)
        plt.title(pltlabel)
        plt.show()
    scores = {}

    if isinstance(race["finishers"], list):
        for p in range(len(race["finishers"])):
            scores[race["finishers"][p]] = score(n, ts_arr[p])
    elif isinstance(race["finishers"], dict):
        for k in race["finishers"].keys():
            player_score = score(n, ts_arr[k-1])
            if isinstance(race["finishers"][k], list):
                for p in race["finishers"][k]:
                    scores[p] = player_score
            else:
                scores[race["finishers"][k]] = player_score
    for player in race["forfeits"]:
        scores[player] = forfeit
    return scores

def rankdiff(nplay, expected, actual):
    return nplay * (actual - expected)

def expected(rank, otherranks):
    if all(other == rank for other in otherranks):
        return 50
    allranks = otherranks + [rank]
    ar_arr = ar(allranks)
    (loc, scale) = norm.fit(ar_arr)
    n = norm(loc=loc, scale=scale)
    #print([(r, score(n, r)) for r in sorted(allranks)])
    return 100 * n.cdf(rank)
    #score(n, rank)

def raceranks(races, startval=500, forfeit=0, alpha=0.1):
    ranks = [dict([(p, startval) for p in util.all_participating_players(races)])] + [None for r in range(len(races))]

    for r in range(len(races)):
        print("Race " + str(r+1))
        ranks[r+1] = copy.deepcopy(ranks[r])
        race = races[r]
        race_players = util.finishers(race) | set(race["forfeits"])
        ac = actuals(race, forfeit=forfeit, pltlabel=None)
        for player in race_players:
            #if ranks[r].get(player, startval) == startval:
            #    ranks[r+1][player] = ac[player]
            #else:
            diff = alpha * (ac[player] - ranks[r].get(player, startval))
            ranks[r+1][player] = ranks[r].get(player, startval) + diff
            print(player, ranks[r][player], diff, ranks[r+1][player])
            #otherranks = [ranks[r].get(p, startval) for p in race_players if p != player]
            #ex = expected(ranks[r].get(player, startval), otherranks)
            #print("rankdiff", player, ex, ac.get(player, startval), rankdiff(len(race_players), ex, ac.get(player, startval)))
            #ranks[r+1][player] = int(round(ranks[r+1].get(player, startval) + rankdiff(len(race_players), expected(ranks[r+1].get(player, startval), otherranks), ac.get(player, startval))))

    return ranks

if __name__ == "__main__":
    import races
    import pprint
    pprint.pprint(raceranks(races.races, startval=500))
