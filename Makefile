.PHONY: tests

virtualenv-create: .venv
	python3 -m venv .venv

install:
	python3 -m pip install -r requirements.txt
	python3 -m pip install pytest
	python3 -m pip install black

tests:
	python3 -m pytest
