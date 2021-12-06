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

def make_ordinal(n):
    '''
    Convert an integer into its ordinal representation::

        make_ordinal(0)   => '0th'
        make_ordinal(3)   => '3rd'
        make_ordinal(122) => '122nd'
        make_ordinal(213) => '213th'
    '''
    n = int(n)
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix

def table(races, ranks, startval=0, exclude=[]):
    from tabulate import tabulate
    cols = ['Place', 'Player', 'Start']
    for i in range(1, len(ranks)):
        cols.extend(['W' + str(i), '+/-'])
    tab = [[] for x in (all_players(races) - set(exclude))]
    ranks_by_score = [rk for rk in byscore(ranks[-1]) if rk[1] not in exclude]
    lastplaces = dict(zip([x[1] for x in byscore(ranks[0])], range(len(ranks[0]))))
    for i in range(len(ranks_by_score)):
        player = ranks_by_score[i][1]
        tab[i] = [make_ordinal(i+1), player, ranks[0].get(player, startval)]
        for j in range(1, len(ranks)):
            thisrank = int(ranks[j].get(player, startval))
            thisplaces = dict(zip([x[1] for x in byscore(ranks[j])], range(len(ranks[j]))))
            thisplace = thisplaces.get(player, max(thisplaces.values())+1)
            lastplace = lastplaces.get(player, max(lastplaces.values())+1)
            this_status0 = this_status1 = diffstr = ''
            placediff = 0
            if player in races[j-1]["forfeits"]:
                this_status1 = '^'
            elif player not in finishers(races[j-1]):
                this_status0 = '('
                this_status1 = ')'
            if j > 1 and lastplace != thisplace:
                #print("Race {0}, player {1}, place {2} to {3}".format(j, player, lastplace, thisplace))
                placediff = lastplace - thisplace
                diffstr = '{0}({1:+}) {2}{3:+}{4}'.format(make_ordinal(thisplace+1), placediff, this_status0, int(thisrank - ranks[j-1].get(player, startval)), this_status1)
            else:
                diffstr = '{0} {1}{2:+}{3}'.format(make_ordinal(thisplace+1), this_status0, int(thisrank - ranks[j-1].get(player, startval)), this_status1)
            lastplaces = thisplaces
            tab[i].extend([thisrank, diffstr])
    return tabulate(tab, headers=cols, disable_numparse=True)
