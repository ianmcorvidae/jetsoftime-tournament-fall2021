#!/bin/sh
for ltype in $(python3 cmdline.py --lt);
do python3 cmdline.py $ltype --plot --no-incomplete --output-file img/${ltype}.png;
   python3 cmdline.py $ltype --plot --miss-is-forfeit --drop-ratio 0.3 --no-incomplete --output-file img/${ltype}-missf-drop0.3.png;
done;
