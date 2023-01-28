#!/bin/bash
cd /bak
source /bak/env/bin/activate

if [[ $# -eq 1 ]]; then
  p=$1
elif [[ $# -eq 2 ]]; then
  p=$1
  t=$2
fi

if [[ $p ]] && [[ $t ]]; then
  echo "Running with ${t} thread | proxy ${p}"
  python3.9 bot.py -p ${p} -t ${t}
else
  echo "Running with 1 thread | proxy L"
  python3.9 bot.py -p L -t 1
fi
