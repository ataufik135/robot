#!/bin/bash
cd /bak
source /bak/env/bin/activate

if [[ $# -eq 1 ]]; then
  th=$1
elif [[ $# -eq 2 ]]; then
  th=$1
  i=$2
elif [[ $# -eq 3 ]]; then
  th=$1
  i=$2
  t=$3
fi

if [[ $th ]] && [[ $i ]] && [[ $t ]]; then
  echo "Running with ${th} thread"
  python3.9 bot.py -th ${th} -i ${i} -t ${t}
else
  echo "Running with default config"
  python3.9 bot.py
fi
