#!/bin/bash
cd /bak
source /bak/env/bin/activate

if [[ $# -eq 1 ]]; then
  t=$1
elif [[ $# -eq 2 ]]; then
  t=$1
  t1=$2
elif [[ $# -eq 3 ]]; then
  t=$1
  t1=$2
  t2=$3
fi

if [[ $t ]] && [[ $t1 ]] && [[ $t2 ]]; then
  echo "Running with ${t} thread"
  python3.9 bot.py -t ${t} -t1 ${t1} -t2 ${t2}
else
  echo "Running with default config"
  python3.9 bot.py
fi
