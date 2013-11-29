pep8:
	flake8 fairepart --ignore=E501,E127,E128,E124

test:
	coverage run --branch --source=fairepart manage.py test fairepart
	coverage report --omit=fairepart/test*

release:
	python setup.py sdist register upload -s

