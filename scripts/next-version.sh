#!/bin/bash
# Calculate the next version based on semver

set -e

BUMP_TYPE=${1:-patch}

# Get the latest tag
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")

# Remove 'v' prefix if present
VERSION=${LATEST_TAG#v}

# Split version into parts
IFS='.' read -ra VERSION_PARTS <<< "$VERSION"
MAJOR=${VERSION_PARTS[0]:-0}
MINOR=${VERSION_PARTS[1]:-0}
PATCH=${VERSION_PARTS[2]:-0}

# Calculate next version based on bump type
case $BUMP_TYPE in
  major)
    MAJOR=$((MAJOR + 1))
    MINOR=0
    PATCH=0
    ;;
  minor)
    MINOR=$((MINOR + 1))
    PATCH=0
    ;;
  patch)
    PATCH=$((PATCH + 1))
    ;;
  *)
    echo "Error: Invalid bump type. Use: major, minor, or patch"
    exit 1
    ;;
esac

NEXT_VERSION="v${MAJOR}.${MINOR}.${PATCH}"
echo "$NEXT_VERSION"
