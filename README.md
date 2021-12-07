Usage:

`python3 cmdline.py --help` should tell you what you need to know hopefully

Current race scoring logic:
![current logic](./img/raster.png)

Graphs using different logics:

elo: simple Multiplayer-ELO, starting at 1500
![elo](./img/elo.png)

elohighknum: like elo, but instead of K = 32/number of players, use 128/number of players
![elohighknum](./img/elohighknum.png)

eloten: like elo, but count 10th-and-greater places as all tied for 10th
![eloten](./img/eloten.png)

ff6wc: like elo, but multiply elo changes by 3 and round all elo change values together, rather than individually
![ff6wc](./img/ff6wc.png)

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
