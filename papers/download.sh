#!/usr/bin/env bash
# Downloads the free papers into ./papers and zips them. Run on your own computer:
#   bash download.sh
# Paywalled papers (marked "needs library access" in DOWNLOAD_LIST.md) must be saved by hand into ./papers first.
set -e
mkdir -p papers
get() { echo "-> $1"; curl -fL --retry 3 -A "Mozilla/5.0" -o "papers/$1" "$2" || echo "   FAILED: $2 (download it manually)"; }
get QLFR_arxiv_2002.09623.pdf        https://arxiv.org/pdf/2002.09623
get AquaSimFG_arxiv_2410.20698.pdf   https://arxiv.org/pdf/2410.20698
get CARMA_JSAC2019.pdf               https://www.ece.neu.edu/fac-ece/basagni/papers/DiValerioLPPSB19.pdf
get DoubleQ_vanHasselt2010.pdf       https://papers.nips.cc/paper_files/paper/2010/file/091d584fced301b442654dd8c23b3fc9-Paper.pdf
ls -lh papers
zip -r papers.zip papers
echo "Done: upload papers.zip in the chat (or the PDFs to GitHub folder papers/)."
