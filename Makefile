test:
	python setup.py test

flake8:
	flake8 --ignore=E501,E225,E128,W391,W404,W402 --max-complexity 12 hipsaint

install:
	python setup.py install

develop:
	python setup.py develop

coverage:
	coverage run --include=hipsaint/* setup.py test

clean:
	rm -rf .tox/ dist/ *.egg *.egg-info .coverage reports/
