test:
	python setup.py test

flake8:
	flake8 --max-line-length 120 --max-complexity 12 hipsaint

install:
	python setup.py install

develop:
	python setup.py develop

coverage:
	coverage run --include=hipsaint/* setup.py test

clean:
	rm -rf .tox/ dist/ *.egg *.egg-info .coverage reports/
