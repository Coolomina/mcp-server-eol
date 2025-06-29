# MCP Server EOL - Makefile
# Convenient commands for development, building, and releasing

# Variables
DOCKER_REPO := ghcr.io/$(shell git config --get remote.origin.url | sed 's/.*[:/]\([^/]*\)\/\([^/]*\)\.git/\1\/\2/')
VERSION := $(shell git describe --tags --exact-match 2>/dev/null || echo "dev")
COMMIT := $(shell git rev-parse --short HEAD)
BUILD_DATE := $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m # No Color

.PHONY: help build test run clean version tag-patch tag-minor tag-major release local-build push

# Default target
help: ## Show this help message
	@echo "MCP Server EOL - Development Tools"
	@echo "=================================="
	@echo ""
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Development commands
install: ## Install dependencies using PDM
	@echo "$(YELLOW)Installing dependencies...$(NC)"
	pdm install

test: ## Run all tests
	@echo "$(YELLOW)Running test suite...$(NC)"
	pdm run python run_tests.py

test-quick: ## Run quick smoke test only
	@echo "$(YELLOW)Running quick test...$(NC)"
	pdm run python tests/test_quick.py

test-comprehensive: ## Run comprehensive test only
	@echo "$(YELLOW)Running comprehensive test...$(NC)"
	pdm run python tests/test_comprehensive.py

clean: ## Clean up cache and build artifacts
	@echo "$(YELLOW)Cleaning up...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pdm-build/ dist/ *.egg-info/ .pytest_cache/
	@echo "$(GREEN)Cleanup complete$(NC)"

# Docker commands
local-build: ## Build Docker image locally
	@echo "$(YELLOW)Building Docker image locally...$(NC)"
	docker build -t mcp-server-eol:latest -t mcp-server-eol:$(COMMIT) .
	@echo "$(GREEN)Local build complete: mcp-server-eol:latest$(NC)"

run: ## Run the Docker container locally
	@echo "$(YELLOW)Running Docker container...$(NC)"
	docker run -it --rm mcp-server-eol:latest

run-bash: ## Run Docker container with bash shell
	@echo "$(YELLOW)Starting bash in Docker container...$(NC)"
	docker run -it --rm --entrypoint bash mcp-server-eol:latest

# Version management
version: ## Show current version information
	@echo "Current version info:"
	@echo "  Git tag:     $(VERSION)"
	@echo "  Commit:      $(COMMIT)"
	@echo "  Build date:  $(BUILD_DATE)"
	@echo "  Docker repo: $(DOCKER_REPO)"

current-version: ## Show the current version tag
	@git describe --tags --abbrev=0 2>/dev/null || echo "No tags found"

next-patch: ## Show what the next patch version would be
	@echo "$(YELLOW)Next patch version:$(NC)"
	@./scripts/next-version.sh patch

next-minor: ## Show what the next minor version would be
	@echo "$(YELLOW)Next minor version:$(NC)"
	@./scripts/next-version.sh minor

next-major: ## Show what the next major version would be
	@echo "$(YELLOW)Next major version:$(NC)"
	@./scripts/next-version.sh major

# Release commands (these create and push tags)
tag-patch: ## Create and push a patch version tag (x.y.Z)
	@echo "$(YELLOW)Creating patch release...$(NC)"
	@./scripts/create-tag.sh patch

tag-minor: ## Create and push a minor version tag (x.Y.0)
	@echo "$(YELLOW)Creating minor release...$(NC)"
	@./scripts/create-tag.sh minor

tag-major: ## Create and push a major version tag (X.0.0)
	@echo "$(YELLOW)Creating major release...$(NC)"
	@./scripts/create-tag.sh major

release: test ## Run tests and create a patch release
	@echo "$(GREEN)All tests passed!$(NC)"
	@make tag-patch

# GitHub workflow status
workflow-status: ## Check GitHub Actions workflow status
	@echo "$(YELLOW)Checking GitHub Actions status...$(NC)"
	@gh run list --limit 5 --workflow=docker-publish.yml 2>/dev/null || echo "GitHub CLI not installed or not authenticated"

# Development workflow
dev-build: clean test local-build ## Clean, test, and build locally
	@echo "$(GREEN)Development build complete!$(NC)"

# CI/CD helpers
ci-info: ## Show information about CI environment
	@echo "CI Environment Info:"
	@echo "  GITHUB_REF: $(GITHUB_REF)"
	@echo "  GITHUB_SHA: $(GITHUB_SHA)"
	@echo "  GITHUB_ACTOR: $(GITHUB_ACTOR)"

# Quick development cycle
dev: clean test ## Quick development cycle: clean and test
	@echo "$(GREEN)Development cycle complete!$(NC)"

# Show Docker images
images: ## List local Docker images for this project
	@echo "$(YELLOW)Local Docker images:$(NC)"
	@docker images | grep -E "(mcp-server-eol|$(DOCKER_REPO))" || echo "No local images found"
