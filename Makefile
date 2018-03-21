init:
	pip install -r requirements.txt

test:
	py.test tests

README.rst: README.md
	pandoc --from=markdown --to=rst --output=README.rst README.md

requirements.txt:
	pipreqs --force druiddb --savepath requirements.txt

.PHONY: init test
