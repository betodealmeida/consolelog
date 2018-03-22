init:
	pip install -r requirements.txt

test:
	py.test tests

README.rst: README.md
	pandoc --from=markdown --to=rst --output=README.rst README.md

requirements.txt: console_log.py
	pipreqs --force .

upload: README.rst
	python setup.py upload

.PHONY: init test
