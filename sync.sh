#!/usr/bin/env bash
# Better sync script for Zola-based FMHY site
set -e

echo "Ensuring upstream remote..."
git remote add upstream https://github.com/fmhy/FMHY.git || true

echo "Fetching updates from upstream..."
git fetch upstream main

# Create a temporary docs folder to store upstream files for processing
echo "Processing docs from upstream..."
rm -rf docs/
git checkout upstream/main -- docs/

# Run the Zola conversion script
if [ -f convert_content_zola.py ]; then
    echo "Converting content..."
    python3 convert_content_zola.py
else
    echo "Error: convert_content_zola.py not found!"
    exit 1
fi

# Clean up
echo "Cleaning up..."
rm -rf docs/

echo "Sync complete."
