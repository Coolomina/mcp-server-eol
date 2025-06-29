#!/bin/bash
# Create and push a new version tag

set -e

BUMP_TYPE=${1:-patch}

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're on main branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo -e "${RED}Error: You must be on the main branch to create a release${NC}"
    echo "Current branch: $CURRENT_BRANCH"
    exit 1
fi

# Check if working directory is clean
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${RED}Error: Working directory is not clean${NC}"
    echo "Please commit or stash your changes first"
    git status --short
    exit 1
fi

# Get the next version
NEXT_VERSION=$(./scripts/next-version.sh $BUMP_TYPE)

echo -e "${YELLOW}Creating $BUMP_TYPE release: $NEXT_VERSION${NC}"

# Confirm with user
read -p "Continue with creating tag $NEXT_VERSION? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled"
    exit 1
fi

# Create the tag
echo -e "${YELLOW}Creating tag $NEXT_VERSION...${NC}"
git tag -a "$NEXT_VERSION" -m "Release $NEXT_VERSION"

# Push the tag
echo -e "${YELLOW}Pushing tag to origin...${NC}"
git push origin "$NEXT_VERSION"

echo -e "${GREEN}Successfully created and pushed tag: $NEXT_VERSION${NC}"
echo -e "${GREEN}GitHub Actions will now build and publish the Docker image${NC}"
echo ""
echo "You can track the build at:"
echo "https://github.com/$(git config --get remote.origin.url | sed 's/.*[:/]\([^/]*\)\/\([^/]*\)\.git/\1\/\2/')/actions"
