#!/bin/bash
cd /bak
source /bak/env/bin/activate
wait_time=20

if [[ $# -eq 1 ]]; then
  browser_count=$1
elif [[ $# -eq 2 ]]; then
  browser_count=$1
  wait_time=$2
fi

while true; do
  if [[ $browser_count -gt 1 ]]; then
    echo "Running with ${browser_count} browsers..."
    python3.9 run_ad_clicker.py -qf q.txt -pf p.txt --headless -bc ${browser_count}
  else
    python3.9 run_ad_clicker.py -qf q.txt -pf p.txt --headless -bc 1
  fi

  echo "Sleeping ${wait_time} seconds..."

  filename='adclicker.log'
  touch $filename
  if [ -f $filename ]; then
    rm adclicker.log
    echo "$filename is removed"
  fi

  sleep $wait_time
done
