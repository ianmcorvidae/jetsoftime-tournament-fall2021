#!/bin/sh
for ltype in elo elohighknum eloten ff6wc mariokart mariokartavg simpleavg raster rasteradjusted raster1500 rasterfantasy;
do python3 cmdline.py $ltype --plot --output-file img/${ltype}.png;
done;