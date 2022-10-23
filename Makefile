POETRY	:= poetry
PYTHON	:= $(POETRY) run python

default: start

.PHONY: start prepare

start:
	$(PYTHON) ./alien_invasion.py

prepare:
	$(POETRY) install