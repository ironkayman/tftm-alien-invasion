POETRY	:= poetry
PYTHON	:= $(POETRY) run python

default: start

.PHONY: start install

start:
	$(PYTHON) ./run.py

install:
	$(POETRY) install
