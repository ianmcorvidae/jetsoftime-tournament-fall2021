def finishers(race):
    if isinstance(race['finishers'], list):
        return set(race['finishers'])
    elif isinstance(race['finishers'], dict):
        fin = set()
        for k in race['finishers'].keys():
            if isinstance(race['finishers'][k], list):
                fin = fin | set(race['finishers'][k])
            else:
                fin.add(race['finishers'][k])
        return fin

def all_participating_players(races):
    all_players = set()
    for race in races:
        all_players = all_players | finishers(race) | set(race['forfeits'])
    return all_players

def all_players(races):
     all_players = all_participating_players(races)
     for race in races:
         all_players = all_players | set(race['nonparticipants'])
     return all_players

def byscore(ranks):
    return sorted([(v, k) for k,v in ranks.items()], reverse=True)

def numbered_byscore(ranks):
    bs = byscore(ranks)
    return [(i+1, bs[i][0], bs[i][1]) for i in range(len(bs))]

def table(races, ranks, startval=0):
    from tabulate import tabulate
    cols = ['Place', 'Player', 'Start']
    for i in range(1, len(ranks)):
        cols.extend(['W' + str(i), '+/-'])
    tab = [[] for x in all_players(races)]
    ranks_by_score = byscore(ranks[-1])
    for i in range(len(ranks_by_score)):
        player = ranks_by_score[i][1]
        tab[i] = [i+1, player, ranks[0].get(player, startval)]
        for j in range(1, len(ranks)):
            thisrank = int(ranks[j].get(player, startval))
            this_status0 = this_status1 = ''
            if player in races[j-1]["forfeits"]:
                this_status1 = '^'
            elif player not in finishers(races[j-1]):
                this_status0 = '('
                this_status1 = ')'
            tab[i].extend([thisrank, '{0}{1:+}{2}'.format(this_status0, int(thisrank - ranks[j-1].get(player, startval)), this_status1)])
    return tabulate(tab, headers=cols, disable_numparse=True)
