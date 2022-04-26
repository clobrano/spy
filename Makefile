.PHONY: tests

tests:
	echo "TDD Running [`date +%H:%M:%S`]" > ~/.tdd-result
	python3 -m pytest && echo "TDD OK [`date +%H:%M:%S`]" > ~/.tdd-result || echo "TDD FAIL [`date +%H:%M:%S`]" > ~/.tdd-result 

virtualenv-create: .venv
	python3 -m venv .venv

install:
	python3 -m pip install -r requirements.txt
	python3 -m pip install pytest
	python3 -m pip install black
