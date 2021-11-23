import copy
import elo
import util

def raceranks(races, startval=1500):
    ranks = [dict([(p, startval) for p in util.all_participating_players(races)])] + [None for r in range(len(races))]
    for r in range(len(races)):
        match = elo.ELOMatch()
        match.setPreround(False)
        match.setChangeMultiplier(3)
        race = races[r]
        for i in range(len(race["finishers"])):
            player = race["finishers"][i]
            match.addPlayer(player, i+1, ranks[r].get(player, startval))
        for player in race["forfeits"]:
            match.addPlayer(player, len(race["finishers"])+1, ranks[r].get(player, startval))
        match.calculateELOs()
        ranks[r+1] = copy.deepcopy(ranks[r])
        for player in race["finishers"] + race["forfeits"]:
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
