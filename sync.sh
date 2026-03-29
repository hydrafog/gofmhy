#!/usr/bin/env bash

# Exit on error
set -e

echo "Fetching updates from upstream..."
git fetch upstream main

# Create a temporary branch to merge upstream changes
git checkout -b temp-upstream upstream/main

# The upstream repo has content in docs/
# We want to sync docs/ to our content/ while keeping our Zola structure
# A simple way is to use our conversion script on the new/updated files

# Switch back to main (or whatever your current branch is)
# We'll assume 'main' for the Zola site
git checkout main

echo "Merging upstream changes into a temporary directory for processing..."
# We don't want to merge directly because it will conflict with our Zola structure
# Instead, we'll just check out the docs directory from upstream
git checkout upstream/main -- docs/

# Run the conversion script
echo "Converting new/updated content..."
python3 convert_content_zola.py

# Clean up docs/
rm -rf docs/

echo "Sync complete. Review changes and commit."
