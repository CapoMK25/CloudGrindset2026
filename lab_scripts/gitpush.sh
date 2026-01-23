#!/usr/bin/env bash
set -e

git add .

read -rp "Enter commit message: " commitMessage

if [ -z "$commitMessage" ]; then
  echo "Commit message cannot be empty"
  exit 1
fi

git commit -m "$commitMessage"

read -rp "Enter branch name (default: current): " branch

if [ -z "$branch" ]; then
  branch=$(git branch --show-current)
fi

echo "Pushing to origin/$branch"
git push origin "$branch"

echo "Done"
