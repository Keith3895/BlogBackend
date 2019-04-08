#!/bin/bash
set -e

echo '$1 = ' $1
echo '$2 = ' $2
echo '$3 = ' $3

git add .
git commit -m "$1"
python3 setupEnv.py
git push $2 $3