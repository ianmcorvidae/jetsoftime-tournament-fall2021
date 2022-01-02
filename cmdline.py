import sys
import races
import util
import preprocess
import re

logics = ["elo", "elohighknum", "elodesc", "eloasc", "eloten", "ff6wc", "f1", "mariokart", "mariokartavg", "simpleavg", "raster", "rasteradjusted", "raster1500", "rasterfantasy", "newfantasy", "newfantasy2", "normfit"]

def get_settings(logic):
    raceranks = None
    startval = 0
    if lt == "elo":
        import elologic
        raceranks = elologic.raceranks
        startval = 1500
    elif lt == "elohighknum":
        import elohighknum
        raceranks = elohighknum.raceranks
        startval = 1500
    elif lt == "elodesc":
        import elodesc
        raceranks = elodesc.raceranks
        startval = 1500
    elif lt == "eloasc":
        import eloasc
        raceranks = eloasc.raceranks
        startval = 1500
    elif lt == "eloten":
        import elotenlogic
        raceranks = elotenlogic.raceranks
        startval = 1500
    elif lt == "ff6wc":
        import ff6wclogic
        raceranks = ff6wclogic.raceranks
        startval = 1500
    elif lt == "f1":
        import f1
        raceranks = f1.raceranks
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
        startval = 1500
    elif lt == "rasterfantasy":
        import rasterfantasy
        raceranks = rasterfantasy.raceranks
    elif lt == "newfantasy":
        import newfantasy
        raceranks = newfantasy.raceranks
        startval = 1500
    elif lt == "newfantasy2":
        import newfantasy2
        raceranks = newfantasy2.raceranks
        startval = 1500
    elif lt == "normfit":
        import normfit
        raceranks = normfit.raceranks
        startval = 500
    else:
        print("unrecognized logic type")
        sys.exit(1)
    return (raceranks, startval)

if __name__ == "__main__":
    if "--lt" in sys.argv:
        print(" ".join(logics))
        sys.exit(0)
    if "--help" in sys.argv:
        print("Usage: python3 cmdline.py <logic type> <args>")
        print("available logic types: " + ", ".join(logics))
        print("args:")
        print("--no-incomplete: exclude races marked incomplete in races.py")
        print("--filter: filter out players with more than 3 missed races")
        print("--plot: generate a plot and either show it or output it depending on --output-file")
        print("--output-file <file>: set plot output file to <file>. Will do weird things if you don't provide a filename, so be good")
    if len(sys.argv) < 2:
        print("Need to pass a logic type to use")
        sys.exit(1)
    lt = re.sub(r"(\.py)?$", "",sys.argv[1])
    (raceranks, startval) = get_settings(lt)
    noincomplete = "--no-incomplete" in sys.argv
    plot = "--plot" in sys.argv
    filter_too_few = "--filter" in sys.argv
    drop_3 = "--drop-three" in sys.argv
    miss_forfeit = "--miss-is-forfeit" in sys.argv
    of = None
    if '--output-file' in sys.argv:
        of = sys.argv[sys.argv.index('--output-file') + 1]
    rs = races.races
    exclude = []
    if noincomplete:
        rs = [r for r in races.races if not r.get("incomplete", False)]
    if filter_too_few:
        for player in util.all_players(rs):
            player_races = sum([1 for r in rs if (player in util.finishers(r) or player in r["forfeits"])])
            complete_races = sum([1 for r in rs if not r.get("incomplete", False)])
            if complete_races - player_races > 3:
                exclude.append(player)
    if miss_forfeit:
        rs = preprocess.miss_is_forfeit(rs)
    if drop_3:
        rs = preprocess.drop_worst_n(rs, 3)
    if plot:
        import graph
        title = lt
        if filter_too_few:
            title = title + " (excluding ineligible)"
        if miss_forfeit:
            title = title + " (misses are forfeits)"
        if drop_3:
            title = title + " (drop three worst placings)"
        graph.graph(rs, raceranks(rs, startval=startval), startval=startval, title=title, exclude=exclude, output_file=of)
    print(util.table(rs, raceranks(rs, startval=startval), startval=startval, exclude=exclude))

