import util
import copy

def points(place, default=1):
    placeranks = [150,120,100,90,80,70,60,50,40,30,20,10]
    if place < len(placeranks):
        return placeranks[place]
    else:
        return default

def racepoints(player, race):
    if isinstance(race["finishers"], list):
        for i in range(len(race["finishers"])):
            if player == race["finishers"][i]:
                return points(i)
    elif isinstance(race["finishers"], dict):
        for k in sorted(race["finishers"].keys()):
            if isinstance(race["finishers"][k], list):
                for p in race["finishers"][k]:
                    if p == player:
                        return points(k-1)
            else:
                return points(k-1)
    elif player in race["forfeits"]:
        return 0
    else:
        return None

def raceranks(races, startval=0):
    ranks = [dict([(p, startval) for p in util.all_players(races)])] + [None for r in range(len(races))]
    ranks[1] = dict([(p, racepoints(p, races[0]) or startval) for p in util.all_players(races[:1])])
    for r in range(1,len(races)):
        race = races[r]
        ranks[r+1] = copy.deepcopy(ranks[r])
        for player in util.all_players([race]):
            points = [racepoints(player, race) for race in races[:r] if racepoints(player, race) is not None]
            if racepoints(player, race) is not None:
                points = points + [racepoints(player, race)]
            if len(points) > 0:
                ranks[r+1][player] = sum(points) / len(points)
            else:
                ranks[r+1][player] = startval
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

