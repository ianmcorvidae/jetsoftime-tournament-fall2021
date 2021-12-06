import sys
import races
import util

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Need to pass a logic type to use")
        sys.exit(1)
    lt = sys.argv[1]
    noincomplete = "--no-incomplete" in sys.argv
    plot = "--plot" in sys.argv
    filter_too_few = "--filter" in sys.argv
    rs = races.races
    raceranks = None
    startval = 0
    exclude = []
    if noincomplete:
        rs = [r for r in races.races if not r.get("incomplete", False)]
    if filter_too_few:
        for player in util.all_players(rs):
            player_races = sum([1 for r in rs if (player in util.finishers(r) or player in r["forfeits"])])
            if len(rs) - player_races > 3:
                exclude.append(player)
    if lt == "elo":
        import elologic
        raceranks = elologic.raceranks
        startval = 1500
    elif lt == "elohighknum":
        import elohighknum
        raceranks = elohighknum.raceranks
        startval = 1500
    elif lt == "eloten":
        import elotenlogic
        raceranks = elotenlogic.raceranks
        startval = 1500
    elif lt == "ff6wc":
        import ff6wclogic
        raceranks = ff6wclogic.raceranks
        startval = 1500
    elif lt == "mariokart":
        import mariokart
        raceranks = mariokart.raceranks
    elif lt == "mariokartavg":
        import mariokartavg
        raceranks = mariokartavg.raceranks
    elif lt == "simpleavg":
        import simpleavg
        raceranks = simpleavg.raceranks
    elif lt == "raster":
        import rasterlogic
        raceranks = rasterlogic.raceranks
    elif lt == "rasteradjusted":
        import rasteradjusted
        raceranks = rasteradjusted.raceranks
    elif lt == "raster1500":
        import raster1500
        raceranks = raster1500.raceranks
    elif lt == "rasterfantasy":
        import rasterfantasy
        raceranks = rasterfantasy.raceranks
    else:
        print("unrecognized logic type")
        sys.exit(1)
    if plot:
        import graph
        graph.graph(rs, raceranks(rs, startval=startval), startval=startval, title=lt, exclude=exclude)
    print(util.table(rs, raceranks(rs, startval=startval), startval=startval, exclude=exclude))

