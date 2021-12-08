import util
import copy

def remove_from_finishers(finishers, player):
    if isinstance(finishers, list):
        f = copy.copy(finishers)
        f.remove(player)
        return f
    elif isinstance(finishers, dict):
        # find player
        place = None
        istie = False
        for k in finishers.keys():
            if isinstance(finishers[k], list) and player in finishers[k]:
                place = k
                istie = True
            elif finishers[k] == player:
                place = k
        f = dict()
        for k in finishers.keys():
            if k < place:
                f[k] = finishers[k]
            elif k > place:
                f[k-1] = finishers[k]
            elif istie and len(finishers[k]) == 2:
                thisidx = finishers[k].index(player)
                f[k] = finishers[k][0 if thisidx == 1 else 1]
            elif istie and len(finishers[k]) > 2:
                new = copy.copy(finishers[k])
                new.remove(player)
                f[k] = new
            else:
                # not tied, and we're changing every other key, so just pass
                pass
        return f

def remove_from_race(race, player):
    r = copy.deepcopy(race)
    if player in util.finishers(race):
        r["finishers"] = remove_from_finishers(race["finishers"], player)
    elif player in race["forfeits"]:
        f = copy.copy(race["forfeits"])
        f.remove(player)
        r["forfeits"] = f
    return r

def drop_worst_n(races, n):
    new_r = [None for r in races]
    player_placings = dict()
    player_min_n = dict()
    for player in util.all_players(races):
        placings = [None for r in races]
        min_n = []
        for r in range(len(races)):
            race = races[r]
            if player in util.finishers(race):
                if isinstance(race["finishers"], list):
                    placings[r] = race["finishers"].index(player)
                elif isinstance(race["finishers"], dict):
                    for k in race["finishers"].keys():
                        if (isinstance(race["finishers"][k], list) and player in race["finishers"][k]) or race["finishers"][k] == player:
                            placings[r] = k-1
            elif player in race["forfeits"]:
                placings[r] = 1000
            else:
                placings[r] = 1000000
            if len(min_n) < n:
                min_n.append(r)
            elif placings[r] > max([placings[x] for x in min_n]):
                # this is strictly worse, add it
                toremove = min([placings[x] for x in min_n])
                toremove_idx = [placings[x] for x in min_n].index(toremove)
                min_n[toremove_idx] = r
            elif placings[r] == max([placings[x] for x in min_n]):
                # equal to existing min, so only replace if the max is higher
                toremove = min([placings[x] for x in min_n])
                if toremove < placings[r]:
                    toremove_idx = [placings[x] for x in min_n].index(toremove)
                    min_n[toremove_idx] = r
        player_placings[player] = placings
        player_min_n[player] = min_n

    for r in range(len(races)):
        new = copy.deepcopy(races[r])
        for player in player_min_n.keys():
            if r in player_min_n[player]:
                new = remove_from_race(new, player)

        new_r[r] = new
    return new_r

