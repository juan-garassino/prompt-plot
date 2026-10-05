#!/bin/bash
# usage: crops.sh N  -> true-width full page + detail crops of faithful_vN into the scratch dir
G=~/Downloads/pp_millennium_poincare_faithful_v$1.gcode
SP=${2:-/tmp}
R="$(dirname "$0")/render_truewidth.py"
PY=.venv/bin/python
$PY $R $G $SP/v$1_full.png 0 0 297 420 5
$PY $R $G $SP/v$1_neck.png 135 170 205 240 14
$PY $R $G $SP/v$1_foot.png 180 15 282 140 8
$PY $R $G $SP/v$1_top.png 15 320 150 405 8
$PY $R $G $SP/v$1_pole.png 25 60 125 160 10
