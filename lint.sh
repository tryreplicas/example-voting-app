#!/bin/sh
if grep -q "import os" vote/format.py; then
  echo "vote/format.py:1 os imported but unused"
  exit 1
fi
