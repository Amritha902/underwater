#!/usr/bin/env bash
# Multi-seed QLFR vs LAQR evaluation in ns-3 (evaluation seeds 0-9; settings fixed beforehand on seeds 100-101).
# Usage: ./run_eval.sh [ns3_dir] [jobs] [tag] [extra simulator args...]
#   e.g. ./run_eval.sh /home/user/ns-3 4 cw --mac=cw --maxAttempts=400
set -euo pipefail
NS3=${1:-/home/user/ns-3}; JOBS=${2:-4}; TAG=${3:-}; shift $(( $# < 3 ? $# : 3 )); EXTRA="$*"
OUT=$(cd "$(dirname "$0")" && pwd)/results/ns3_eval${TAG:+_$TAG}.csv
export LD_LIBRARY_PATH=$NS3/build/lib
BIN=$NS3/build/scratch/laqr-sim/ns3.44-laqr-sim
COMMON="--rounds=50 --rateBps=20000 --fcHz=40000 --bwHz=20000 --txPowerDb=114 --helloEvery=1 --freshRounds=1 --k=0.15 $EXTRA"
echo "scenario,protocol,nodes,seed,speed,pdr,delay,energy_used,lifetime,tx_per_pkt,helloTx,sendFails" > "$OUT"
for sc in "desync 3.5" "sync 0.5"; do
  set -- $sc
  for n in 100 200 300 400 500; do for seed in $(seq 0 9); do
    for p in "qlfr --pdrTh=0.90" "qlfr97 --protocol=qlfr --pdrTh=0.97" "laqr"; do
      name=${p%% *}; args=${p#* }; [ "$name" = "$p" ] && args=""
      proto=$name; [ "$name" = "qlfr97" ] && proto=qlfr
      echo "$1 $name --protocol=$proto $args --nodes=$n --seed=$seed --dataJitter=$2"
    done
  done; done
done | xargs -P "$JOBS" -L 1 bash -c 'sc=$0; name=$1; shift 1; r=$('"$BIN"' '"$COMMON"' "$@" 2>/dev/null); echo "$sc,$name,${r#*,}"' >> "$OUT"
echo "wrote $OUT"
