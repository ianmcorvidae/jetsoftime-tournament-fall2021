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
