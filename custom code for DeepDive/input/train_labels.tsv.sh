#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

deepdive load train_labels /home/hill103/nips_2017/input/train_labels.tsv

