import copy
import elocurve
import util
import preprocess

def _raceranks(races, startval=1500, drop=None):
    ranks = [dict([(p, startval) for p in util.all_participating_players(races)])] + [None for r in range(len(races))]
    for r in range(len(races)):
        match = elocurve.ELOMatch()
        match.setPreround(False)
        match.setChangeMultiplier(3)
        race = races[r]
        if isinstance(race["finishers"], list):
            for i in range(len(race["finishers"])):
                player = race["finishers"][i]
                match.addPlayer(player, race["times"][i], ranks[r].get(player, startval))
        elif isinstance(race["finishers"], dict):
            for k in sorted(race["finishers"].keys()):
                # k is place, but we need 0-indexed
                if isinstance(race["finishers"][k], list):
                    for player in race["finishers"][k]:
                        match.addPlayer(player, race["times"][k-1], ranks[r].get(player, startval))
                else:
                    player = race["finishers"][k]
                    match.addPlayer(player, race["times"][k-1], ranks[r].get(player, startval))
        for player in race["forfeits"]:
            match.addPlayer(player, 0, ranks[r].get(player, startval))
        match.calculateELOs()
        ranks[r+1] = copy.deepcopy(ranks[r])
        for player in util.finishers(race) | set(race["forfeits"]):
            if (drop is not None) and (r in drop.get(player, [])):
                ranks[r+1][player] = ranks[r][player]
            else:
                ranks[r+1][player] = match.getELO(player)
    return ranks

def raceranks(races, startval=1500, drop_count=None):
    if drop_count is None:
        return _raceranks(races, startval=startval)
    else:
        drops = preprocess.get_worst_n(races, drop_count)
        return _raceranks(races, startval=1500, drop=drops)

if __name__ == "__main__":
    import races
    import util 
    import sys
    rs = races.races
    if len(sys.argv) > 1 and sys.argv[1] == "--no-incomplete":
        rs = [r for r in races.races if not r.get("incomplete", False)]
    if len(sys.argv) > 1 and sys.argv[1] == "--plot":
        import graph
        graph.graph(rs, raceranks(rs), startval=1500)
    print(util.table(rs, raceranks(rs), startval=1500))
