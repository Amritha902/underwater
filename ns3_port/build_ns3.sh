#!/usr/bin/env bash
# Fetch and build ns-3 (release) with the modules the QLFR/LAQR port needs, and link our program
# (ns3_port/scratch/laqr-sim) into the ns-3 scratch directory.
# Usage: bash ns3_port/build_ns3.sh [NS3_DIR]   (default: ../../ns-3 relative to this script, i.e. next to the repo)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
NS3_DIR="${1:-$HERE/../../ns-3}"
TAG="ns-3.44"
if [ ! -d "$NS3_DIR/.git" ]; then
  git clone --depth 1 --branch "$TAG" https://github.com/nsnam/ns-3-dev-git "$NS3_DIR"
fi
ln -sfn "$HERE/scratch/laqr-sim" "$NS3_DIR/scratch/laqr-sim"
cd "$NS3_DIR"
./ns3 configure -d release --disable-examples --disable-tests \
  --enable-modules="core;network;mobility;energy;uan;propagation" -G Ninja
./ns3 build scratch/laqr-sim/laqr-sim
