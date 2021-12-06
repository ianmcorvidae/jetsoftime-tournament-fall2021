import rasterlogic
import util

def raceranks(races, startval=1500, maxscore=100, minscore=10, step=-10, forfeitscore=0):
    return rasterlogic.raceranks(races,startval=startval,maxscore=maxscore,minscore=minscore,step=step,forfeitscore=forfeitscore)
if __name__ == "__main__":
    import races
    import sys
    rs = races.races
    if len(sys.argv) > 1 and sys.argv[1] == "--no-incomplete":
        rs = [r for r in races.races if not r.get("incomplete", False)]
    print(util.table(rs, rasterlogic.raceranks(rs, startval=1500), startval=1500))
