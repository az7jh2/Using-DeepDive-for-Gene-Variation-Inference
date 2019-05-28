#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

deepdive load articles /home/hill103/nips_2017/input/articles.tsv

