import copy
import elo
import util

def raceranks(races, startval=1500):
    ranks = [dict([(p, startval) for p in util.all_participating_players(races)])] + [None for r in range(len(races))]
    for r in range(len(races)):
        match = elo.ELOMatch()
        race = races[r]
        if isinstance(race["finishers"], list):
            for i in range(len(race["finishers"])):
                player = race["finishers"][i]
                match.addPlayer(player, min(i+1,10), ranks[r].get(player, startval))
        elif isinstance(race["finishers"], dict):
            skip = 0
            for k in sorted(race["finishers"].keys()):
                # k is place, but if there's skips we have to offset
                if isinstance(race["finishers"][k], list):
                    for player in race["finishers"][k]:
                        match.addPlayer(player, min(k,10)-skip, ranks[r].get(player, startval))
                    skip = skip + len(race["finishers"][k]) - 1 # offset by tied players, minus 1, for next loops
                else:
                    player = race["finishers"][k]
                    match.addPlayer(player, min(k,10)-skip, ranks[r].get(player, startval))
        for player in race["forfeits"]:
            match.addPlayer(player, min(11, len(util.finishers(race))+1), ranks[r].get(player, startval))
        match.calculateELOs()
        ranks[r+1] = copy.deepcopy(ranks[r])
        for player in util.finishers(race) | set(race["forfeits"]):
            ranks[r+1][player] = match.getELO(player)
    return ranks

if __name__ == "__main__":
    import races
    import util 
    import sys
    rs = races.races
    if len(sys.argv) > 1 and sys.argv[1] == "--no-incomplete":
        rs = [r for r in races.races if not r.get("incomplete", False)]
    print(util.table(rs, raceranks(rs)))
