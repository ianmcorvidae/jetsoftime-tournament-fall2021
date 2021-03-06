import sys
import races
import util
import preprocess
import re

logics = ["elo", "elohighknum", "elodesc", "eloasc", "eloten", "ff6wc", "f1", "mariokart", "mariokartavg", "simpleavg", "raster", "rasteradjusted", "raster1500", "rasterfantasy", "newfantasy", "newfantasy2", "normfit", "elocurve"]

def get_settings(logic):
    raceranks = None
    startval = 0
    hasIntegratedDrop = False
    if lt == "elo":
        import elologic
        raceranks = elologic.raceranks
        startval = 1500
    elif lt == "elocurve":
        import elocurvelogic
        raceranks = elocurvelogic.raceranks
        startval = 1500
        hasIntegratedDrop = True
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
        hasIntegratedDrop = True
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
    return (raceranks, startval, hasIntegratedDrop)

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
        print("--filter-count <n>: change --filter to filter those with <n> missed races instead of 3")
        print("--filter-count-ratio <n>: change --filter to filter those with round(<n>*number of races) missed races instead of 3")
        print("--plot: generate a plot and either show it or output it depending on --output-file")
        print("--output-file <file>: set plot output file to <file>. Will do weird things if you don't provide a filename, so be good")
        print("--drop <n>: drop the worst <n> results. Some logic types do this directly within themselves, the rest do it by preprocessing the races to remove the worst <n>")
        print("--drop-ratio <n>: like --drop, but <n> should be a ratio between 0 and 1, which will be multiplied by the number of races and then rounded to get the actual number of dropped races.")
    if len(sys.argv) < 2:
        print("Need to pass a logic type to use")
        sys.exit(1)
    rs = races.races
    lt = re.sub(r"(\.py)?$", "",sys.argv[1])
    (raceranks, startval, hasIntegratedDrop) = get_settings(lt)
    noincomplete = "--no-incomplete" in sys.argv
    plot = "--plot" in sys.argv
    filter_too_few = "--filter" in sys.argv
    if "--filter-count" in sys.argv:
        filter_count = int(sys.argv[sys.argv.index("--filter-count") + 1])
    elif "--filter-count-ratio" in sys.argv:
        filter_count = round(float(sys.argv[sys.argv.index("--filter-count-ratio") + 1]) * len(rs))
    else:
        filter_count = 3
    drop = "--drop" in sys.argv or "--drop-ratio" in sys.argv
    if "--drop" in sys.argv:
        drop_n = int(sys.argv[sys.argv.index("--drop") + 1])
    elif "--drop-ratio" in sys.argv:
        drop_n = round(float(sys.argv[sys.argv.index("--drop-ratio") + 1]) * len(rs))
    if drop and drop_n > len(rs) - 1:
        drop_n = len(rs) - 1
    miss_forfeit = "--miss-is-forfeit" in sys.argv
    of = None
    if '--output-file' in sys.argv:
        of = sys.argv[sys.argv.index('--output-file') + 1]
    exclude = []
    if noincomplete:
        rs = [r for r in races.races if not r.get("incomplete", False)]
    if filter_too_few:
        for player in util.all_players(rs):
            player_races = sum([1 for r in rs if (player in util.finishers(r) or player in r["forfeits"])])
            complete_races = sum([1 for r in rs if not r.get("incomplete", False)])
            if complete_races - player_races > filter_count:
                exclude.append(player)
    if miss_forfeit:
        rs = preprocess.miss_is_forfeit(rs)
    kwargs = {'startval': startval}
    if drop and not hasIntegratedDrop:
        rs = preprocess.drop_worst_n(rs, drop_n)
    elif drop:
        kwargs["drop_count"] = drop_n
    if plot:
        import graph
        title = lt
        if filter_too_few:
            title = title + " (excluding " + str(filter_count) + "+ missed)"
        if miss_forfeit:
            title = title + " (misses are forfeits)"
        if drop:
            title = title + " (drop " + str(drop_n) + " worst placings)"
        graph.graph(rs, raceranks(rs, **kwargs), startval=startval, title=title, exclude=exclude, output_file=of)
    print(util.table(rs, raceranks(rs, **kwargs), startval=startval, exclude=exclude))

