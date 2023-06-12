POETRY	:= poetry
PYTHON	:= $(POETRY) run python
ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

default: help

.PHONY: start install help

# taken from https://github.com/lapce/lapce/blob/0d4f6fd30a4e463a2d617fe188a24a55e73b62a3/Makefile#L24
help: ## Print this help message
	@grep -E '^[a-zA-Z._-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-30s\033[0m %s\n", $$1, $$2}'

run: ## Start alien invasion from source
	$(PYTHON) ./run.py

install: ## Create environment and install dependencies
	$(POETRY) config virtualenvs.in-project true --local
	$(POETRY) install
	$(POETRY) run pre-commit install

# see https://stackoverflow.com/questions/18136918/how-to-get-current-relative-directory-of-your-makefile
build: ## Compile using nuitka to ./run.dist/run.bin
	$(PYTHON) -m nuitka \
	--follow-imports ./run.py \
	--standalone \
	--include-data-dir=$(ROOT_DIR)/alien_invasion/resources=internal_resources \
	--include-data-dir=$(ROOT_DIR)/data=data \
	--include-package=uuid
