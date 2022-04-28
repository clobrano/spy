.PHONY: tests build upload

tests:
	echo "TDD Running [`date +%H:%M:%S`]" > ~/.tdd-result
	python3 -m pytest && echo "TDD OK [`date +%H:%M:%S`]" > ~/.tdd-result || echo "TDD FAIL [`date +%H:%M:%S`]" > ~/.tdd-result 

virtualenv-create: .venv
	python3 -m venv .venv

install:
	python3 -m pip install -r requirements.txt
	python3 -m pip install pytest
	python3 -m pip install black

build:
	python3 -m pip install --upgrade build; \
	python3 -m build

upload-test: build
	python3 -m pip install --upgrade twine; \
	python3 -m twine upload --repository testpypi dist/* --verbose;

upload: build
	python3 -m pip install --upgrade twine; \
	python3 -m twine upload dist/* --verbose;
