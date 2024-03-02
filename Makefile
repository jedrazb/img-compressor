VENV := venv
PYTHON := $(VENV)/bin/python

$(PYTHON):
	python3 -m venv $(VENV)

venv: $(PYTHON) requirements.txt
	$(PYTHON) -m pip install -r requirements.txt


run: venv
	$(PYTHON) run.py