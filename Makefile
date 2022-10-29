POETRY	:= poetry
PYTHON	:= $(POETRY) run python

default: start

.PHONY: start prepare

start:
	$(PYTHON) ./run.py

prepare:
	$(POETRY) install