#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m unittest discover -s tests -v
python3 scripts/check_links.py
python3 scripts/build_lesson_visuals.py --check
git diff --check
