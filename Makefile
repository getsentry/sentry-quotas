develop:
	pip install -e .
	pip install pytest unittest2 exam mock pytest-django

test: develop
	python runtests.py
