#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

deepdive load valid_labels /home/hill103/nips_2017/input/valid_labels.tsv

