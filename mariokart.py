import util
import copy

def points(place, default=1):
    placeranks = [15,12,10,9,8,7,6,5,4,3,2,1]
    if place < len(placeranks):
        return placeranks[place]
    else:
        return default

def raceranks(races, startval=0):
    ranks = [dict([(p, startval) for p in util.all_players(races[:1])])] + [None for r in range(len(races))]
    for r in range(len(races)):
        race = races[r]
        ranks[r+1] = copy.deepcopy(ranks[r])
        if isinstance(race["finishers"], list):
            for i in range(len(race["finishers"])):
                player = race["finishers"][i]
                ranks[r+1][player] = ranks[r+1].get(player, startval) + points(i)
        elif isinstance(race["finishers"], dict):
            for k in sorted(race["finishers"].keys()):
                if isinstance(race["finishers"][k], list):
                    for player in race["finishers"][k]:
                        ranks[r+1][player] = ranks[r+1].get(player, startval) + points(k - 1)
                else:
                    player = race["finishers"][k]
                    ranks[r+1][player] = ranks[r+1].get(player, startval) + points(k - 1)

        for player in race["forfeits"]:
            ranks[r+1][player] = ranks[r+1].get(player, startval) - 1

    return ranks

if __name__ == "__main__":
    import races
    import sys
    rs = races.races
    if len(sys.argv) > 1 and sys.argv[1] == "--no-incomplete":
        rs = [r for r in races.races if not r.get("incomplete", False)]
    if len(sys.argv) > 1 and sys.argv[1] == "--plot":
        import graph
        graph.graph(rs, raceranks(rs), startval=0)
    print(util.table(rs, raceranks(rs), startval=0))

