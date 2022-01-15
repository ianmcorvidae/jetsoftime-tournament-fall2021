Usage:

`python3 cmdline.py --help` should tell you what you need to know hopefully

Current race scoring logic:
![current logic](./img/raster.png)

Graphs using different logics:

elo: simple Multiplayer-ELO, starting at 1500
![elo](./img/elo.png)

elohighknum: like elo, but instead of K = 32/number of players, use 128/number of players
![elohighknum](./img/elohighknum.png)

eloasc: like elo/elohighknum, but start at K=32/n then 64/n, etc. (K=32 * racenum / number of players)
![eloasc](./img/eloasc.png)

elodesc: like elodesc, but in reverse. use 32 * (10 - race num), or 32 * (number of races - race number) if more than 10
![elodesc](./img/elodesc.png)

eloten: like elo, but count 10th-and-greater places as all tied for 10th
![eloten](./img/eloten.png)

ff6wc: like elo, but multiply elo changes by 3 and round all elo change values together, rather than individually
![ff6wc](./img/ff6wc.png)

f1: like formula 1 scoring (as described by Tekenu)
![f1](./img/f1.png)

mariokart: places get a given score resembling Mario Kart; rank is the sum
![mariokart](./img/mariokart.png)

mariokartavg: like mariokart, but average the scores rather than summing them
![mariokartavg](./img/mariokartavg.png)

simpleavg: like mariokartavg, but max score is total # of players in tournament, 2nd is that minus 1, etc.
![simpleavg](./img/simpleavg.png)

rasteradjusted: like the current logic, but shift and multiply the range of 'expected' values to the range 10-100 (where the 'actual' values end up)
![rasteradjusted](./img/rasteradjusted.png)

raster1500: like the current logic, but start at 1500
![raster1500](./img/raster1500.png)

rasterfantasy: (obsolete for now) the "fantasy ladder rankings" as they were originally implemented
![rasterfantasy](./img/rasterfantasy.png)

newfantasy: new experimental "fantasy" rankings:
![newfantasy](./img/newfantasy.png)

newfantasy2: new experimental "fantasy" rankings, take 2:
![newfantasy2](./img/newfantasy2.png)

normfit: each week, fit finish times to a scipy.stats.skewnorm distribution; scores are multiplied percentiles. overall score is an exponentially weighted moving average with a starting value corresponding to 50th percentile and (for now) an alpha of 0.25
![normfit](./img/normfit.png)

elocurve: fit finish times like normfit, but use them to calculate a score to use for elo (ff6wc-style, with post-rounding and multiplier of 3). S is set to 0.5 plus half the difference between each pair's survival factor (which is 1-cdf), a number which is close to 1 for the best times and close to 0 for the worst. So, a close win will be a bit above 0.5, a close loss will be a bit below it, etc.
![elocurve](./img/elocurve.png)
