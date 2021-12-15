#!/bin/sh
for ltype in $(python3 cmdline.py --lt);
do python3 cmdline.py $ltype --plot --no-incomplete --output-file img/${ltype}.png;
done;
